
import sqlite3
import hashlib
import hmac
import secrets
from pathlib import Path
from datetime import datetime


# Database location
BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "data" / "scamshield.db"


def get_connection():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")

    return conn


# ---------------- USER PASSWORD HELPERS ----------------

def hash_password(password, salt=None):
    if salt is None:
        salt = secrets.token_bytes(16)

    password_hash = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt,
        600000
    )

    return salt.hex(), password_hash.hex()


def verify_password(password, salt_hex, password_hash_hex):
    salt = bytes.fromhex(salt_hex)
    _, calculated_hash = hash_password(password, salt)

    return hmac.compare_digest(
        calculated_hash,
        password_hash_hex
    )


# ---------------- DATABASE INITIALIZATION ----------------

def initialize_database():
    conn = get_connection()
    cursor = conn.cursor()

    # Individual user accounts
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL COLLATE NOCASE UNIQUE,
            password_hash TEXT NOT NULL,
            password_salt TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
    """)

    # Store scans belonging to individual users
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS scans (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            scan_type TEXT NOT NULL,
            input_text TEXT NOT NULL,
            prediction TEXT NOT NULL,
            risk_score REAL NOT NULL,
            risk_level TEXT NOT NULL,
            reasons TEXT,
            created_at TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    """)

    # Store feedback for review
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS feedback (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            scan_id INTEGER NOT NULL,
            user_feedback TEXT NOT NULL,
            comments TEXT,
            review_status TEXT DEFAULT 'Pending',
            reviewer_notes TEXT,
            submitted_at TEXT NOT NULL,
            reviewed_at TEXT,
            FOREIGN KEY (scan_id) REFERENCES scans(id)
        )
    """)

    # Migrate an existing scans table without deleting old records
    scan_columns = {
        row["name"]
        for row in cursor.execute(
            "PRAGMA table_info(scans)"
        ).fetchall()
    }

    if "user_id" not in scan_columns:
        cursor.execute(
            "ALTER TABLE scans ADD COLUMN user_id INTEGER REFERENCES users(id)"
        )

    conn.commit()
    conn.close()


# ---------------- USER ACCOUNT FUNCTIONS ----------------

def register_user(name, email, password):
    name = name.strip()
    email = email.strip().lower()

    if not name or not email or not password:
        return False, "Please fill in every field."

    if "@" not in email or "." not in email.rsplit("@", 1)[-1]:
        return False, "Enter a valid email address."

    if len(password) < 8:
        return False, "Password must contain at least 8 characters."

    salt, password_hash = hash_password(password)

    conn = get_connection()

    try:
        conn.execute("""
            INSERT INTO users (
                name, email, password_hash, password_salt, created_at
            )
            VALUES (?, ?, ?, ?, ?)
        """, (
            name,
            email,
            password_hash,
            salt,
            datetime.now().isoformat(timespec="seconds")
        ))

        conn.commit()
        return True, "Account created successfully. You can now log in."

    except sqlite3.IntegrityError:
        return False, "An account with this email already exists."

    finally:
        conn.close()


def authenticate_user(email, password):
    email = email.strip().lower()

    conn = get_connection()

    try:
        user = conn.execute("""
            SELECT id, name, email, password_hash, password_salt
            FROM users
            WHERE email = ?
        """, (email,)).fetchone()

        if user and verify_password(
            password,
            user["password_salt"],
            user["password_hash"]
        ):
            return {
                "id": user["id"],
                "name": user["name"],
                "email": user["email"]
            }

        return None

    finally:
        conn.close()


# ---------------- SCAN FUNCTIONS ----------------

def save_scan(
    scan_type,
    input_text,
    prediction,
    risk_score,
    risk_level,
    reasons,
    user_id=None
):
    conn = get_connection()

    try:
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO scans (
                user_id, scan_type, input_text, prediction,
                risk_score, risk_level, reasons, created_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            user_id,
            scan_type,
            input_text,
            prediction,
            float(risk_score),
            risk_level,
            str(reasons),
            datetime.now().isoformat(timespec="seconds")
        ))

        scan_id = cursor.lastrowid
        conn.commit()

        return scan_id

    finally:
        conn.close()


def get_all_scans(user_id=None):
    conn = get_connection()

    try:
        if user_id is None:
            rows = conn.execute("""
                SELECT * FROM scans ORDER BY id DESC
            """).fetchall()
        else:
            rows = conn.execute("""
                SELECT * FROM scans
                WHERE user_id = ?
                ORDER BY id DESC
            """, (user_id,)).fetchall()

        return [dict(row) for row in rows]

    finally:
        conn.close()


# ---------------- FEEDBACK FUNCTIONS ----------------

def save_feedback(scan_id, user_feedback, comments=""):
    conn = get_connection()

    try:
        conn.execute("""
            INSERT INTO feedback (
                scan_id, user_feedback, comments,
                review_status, submitted_at
            )
            VALUES (?, ?, ?, 'Pending', ?)
        """, (
            scan_id,
            user_feedback,
            comments,
            datetime.now().isoformat(timespec="seconds")
        ))

        conn.commit()

    finally:
        conn.close()


def get_all_feedback(user_id=None):
    conn = get_connection()
    cursor = conn.cursor()

    if user_id is None:
        cursor.execute("""
            SELECT feedback.*, scans.user_id
            FROM feedback
            JOIN scans ON feedback.scan_id = scans.id
            ORDER BY feedback.submitted_at DESC
        """)
    else:
        cursor.execute("""
            SELECT feedback.*, scans.user_id
            FROM feedback
            JOIN scans ON feedback.scan_id = scans.id
            WHERE scans.user_id = ?
            ORDER BY feedback.submitted_at DESC
        """, (user_id,))

    rows = cursor.fetchall()
    conn.close()

    return [dict(row) for row in rows]


def review_feedback(feedback_id, status, reviewer_notes=""):
    if status not in ("Verified", "Rejected"):
        raise ValueError("Invalid review status")

    conn = get_connection()

    try:
        conn.execute("""
            UPDATE feedback
            SET review_status = ?,
                reviewer_notes = ?,
                reviewed_at = ?
            WHERE id = ?
        """, (
            status,
            reviewer_notes,
            datetime.now().isoformat(timespec="seconds"),
            feedback_id
        ))

        conn.commit()

    finally:
        conn.close()


# Initialize tables
initialize_database()
