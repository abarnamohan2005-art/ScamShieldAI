
import sqlite3
from pathlib import Path
from datetime import datetime

# Database location: ScamShieldAI/data/scamshield.db
BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "data" / "scamshield.db"


def get_connection():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def initialize_database():
    conn = get_connection()
    cursor = conn.cursor()

    # Store every message or URL scan
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS scans (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            scan_type TEXT NOT NULL,
            input_text TEXT NOT NULL,
            prediction TEXT NOT NULL,
            risk_score REAL NOT NULL,
            risk_level TEXT NOT NULL,
            reasons TEXT,
            created_at TEXT NOT NULL
        )
    """)

    # Store user feedback separately for review
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

    conn.commit()
    conn.close()


def save_scan(scan_type, input_text, prediction,
              risk_score, risk_level, reasons):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO scans (
            scan_type, input_text, prediction, risk_score,
            risk_level, reasons, created_at
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
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
    conn.close()

    return scan_id


def get_all_scans():
    conn = get_connection()
    rows = conn.execute(
        "SELECT * FROM scans ORDER BY id DESC"
    ).fetchall()
    conn.close()

    return [dict(row) for row in rows]


def save_feedback(scan_id, user_feedback, comments=""):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
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
    conn.close()


def get_all_feedback():
    conn = get_connection()

    rows = conn.execute("""
        SELECT feedback.*, scans.scan_type,
               scans.input_text, scans.prediction,
               scans.risk_score, scans.risk_level
        FROM feedback
        JOIN scans ON feedback.scan_id = scans.id
        ORDER BY feedback.id DESC
    """).fetchall()

    conn.close()
    return [dict(row) for row in rows]


def review_feedback(feedback_id, status, reviewer_notes=""):
    if status not in ("Verified", "Rejected"):
        raise ValueError("Invalid review status")

    conn = get_connection()

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
    conn.close()


# Create database tables when this module is imported
initialize_database()
