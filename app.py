
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import ast


from src.database import (
    register_user,
    authenticate_user,
    save_scan,
    get_all_scans,
    save_feedback,
    get_all_feedback,
    review_feedback
)


from src.hybrid_detector import (
    detect_message,
    detect_url,
    explain_message,
    explain_url
)


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="ScamShield AI",
    page_icon="🛡️",
    layout="wide"
)

# LOGIN PAGE THEME AND ANIMATIONS
st.markdown("""
<style>

/* Animated background */
.stApp {
    background: linear-gradient(
        -45deg,
        #171027,
        #211538,
        #2A1942,
        #171027
    );
    background-size: 400% 400%;
    animation: gradientMove 14s ease infinite;
}

@keyframes gradientMove {
    0%   { background-position: 0% 50%; }
    50%  { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}

/* Login and signup form */
div[data-testid="stForm"] {
    background: rgba(42, 29, 66, 0.88);
    border: 1px solid #493564;
    border-radius: 18px;
    padding: 25px;
    box-shadow: 0 8px 30px rgba(139, 92, 246, 0.16);
    transition: all 0.3s ease;
}

div[data-testid="stForm"]:hover {
    border-color: #A78BFA;
    box-shadow: 0 10px 35px rgba(139, 92, 246, 0.30);
    transform: translateY(-3px);
}

/* Input fields */
div[data-testid="stTextInput"] input {
    background-color: #171027;
    color: #F5F0FF;
    border: 1px solid #493564;
    border-radius: 10px;
    transition: all 0.25s ease;
}

div[data-testid="stTextInput"] input:focus {
    border-color: #A78BFA;
    box-shadow: 0 0 10px rgba(167, 139, 250, 0.35);
}

/* Buttons */
.stButton > button,
.stFormSubmitButton > button {
    background: linear-gradient(90deg, #8B5CF6, #A78BFA);
    color: white;
    border: none;
    border-radius: 10px;
    font-weight: 600;
    transition: all 0.3s ease;
}

.stButton > button:hover,
.stFormSubmitButton > button:hover {
    background: linear-gradient(90deg, #A78BFA, #F0A4C8);
    color: white;
    transform: translateY(-2px);
    box-shadow: 0 5px 18px rgba(139, 92, 246, 0.35);
}

/* Login headings */
h1, h2, h3 {
    color: #F5F0FF;
}

/* Labels and text */
.stApp p,
.stApp label {
    color: #E6DDF5;
}

/* Smooth appearance */
div[data-testid="stVerticalBlock"] {
    transition: all 0.3s ease;
}

</style>
""", unsafe_allow_html=True)




# =========================================================
# SESSION STATE
# =========================================================

if "history" not in st.session_state:
    st.session_state.history = []

if "feedback" not in st.session_state:
    st.session_state.feedback = []

if "user" not in st.session_state:
    st.session_state.user = None

if "auth_page" not in st.session_state:
    st.session_state.auth_page = "Login"


# =========================================================
# LOGIN AND SIGN UP
# =========================================================

if st.session_state.user is None:

    st.markdown(
        "<h1 style='text-align:center;'>🛡️ ScamShield AI</h1>",
        unsafe_allow_html=True
    )

    st.markdown(
        "<p style='text-align:center;'>"
        "Intelligent Scam and Phishing Detection"
        "</p>",
        unsafe_allow_html=True
    )

    _, center, _ = st.columns([1, 1.4, 1])

    with center:

        auth_choice = st.radio(
            "Account",
            ["Login", "Sign Up"],
            horizontal=True,
            key="auth_choice"
        )

        if auth_choice == "Sign Up":

            st.subheader("Create Your Account")

            with st.form("signup_form"):

                name = st.text_input("Full Name")
                email = st.text_input("Email Address")
                password = st.text_input(
                    "Password (minimum 8 characters)",
                    type="password"
                )
                confirm_password = st.text_input(
                    "Confirm Password",
                    type="password"
                )

                signup_clicked = st.form_submit_button(
                    "Create Account",
                    use_container_width=True
                )

                if signup_clicked:

                    if password != confirm_password:
                        st.error("Passwords do not match.")

                    else:
                        success, message = register_user(
                            name,
                            email,
                            password
                        )

                        if success:
                            st.success(message)
                            st.info(
                                "Select Login above to access your account."
                            )
                        else:
                            st.error(message)

        else:

            st.subheader("Welcome Back")

            with st.form("login_form"):

                email = st.text_input("Email Address")
                password = st.text_input(
                    "Password",
                    type="password"
                )

                login_clicked = st.form_submit_button(
                    "Login",
                    use_container_width=True
                )

                if login_clicked:

                    user = authenticate_user(
                        email,
                        password
                    )

                    if user:
                        st.session_state.user = user
                        st.session_state.history = []
                        st.session_state.feedback = []
                        st.rerun()

                    else:
                        st.error(
                            "Invalid email or password."
                        )

    st.stop()


# =========================================================
# THEME COLORS
# =========================================================

BG = "#171027"
SIDEBAR = "#120C20"
CARD = "#2A1D42"
BORDER = "#493564"

LAVENDER = "#A78BFA"
PURPLE = "#8B5CF6"
PINK = "#F0A4C8"
MINT = "#6EE7C0"
WHITE = "#F5F0FF"
MUTED = "#C6B5E8"

RISK_COLORS = {
    "High Risk": "#F28BA8",
    "Uncertain": "#F6CB79",
    "Low Risk": "#6EE7C0"
}


# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown("""
<style>

.stApp {
    background: linear-gradient(
        135deg,
        #171027 0%,
        #211538 50%,
        #171027 100%
    );
    color: #F5F0FF;
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
}

/* Headings */

h1, h2, h3, h4 {
    color: #F5F0FF !important;
    font-weight: 700 !important;
}

/* Text */

p, label, li, .stMarkdown {
    color: #DED5F2;
}

/* Sidebar */

[data-testid="stSidebar"] {
    background: #120C20;
    border-right: 1px solid #493564;
}

[data-testid="stSidebar"] * {
    color: #E9DFFF;
}

/* Metric cards */

[data-testid="stMetric"] {
    background: #2A1D42;
    padding: 20px;
    border-radius: 14px;
    border: 1px solid #493564;
    box-shadow: 0 4px 15px rgba(0,0,0,0.20);
}

[data-testid="stMetricLabel"] {
    color: #C6B5E8 !important;
}

[data-testid="stMetricValue"] {
    color: #FFFFFF !important;
}

/* Input fields */

.stTextInput input,
.stTextArea textarea {
    background-color: #2A1D42 !important;
    color: #FFFFFF !important;
    border: 1px solid #665087 !important;
    border-radius: 10px !important;
}

.stTextInput input::placeholder,
.stTextArea textarea::placeholder {
    color: #B7A8CF !important;
}

/* Select boxes */

.stSelectbox [data-baseweb="select"] > div {
    background-color: #2A1D42;
    color: #FFFFFF;
    border-color: #665087;
}

/* Buttons */

.stButton > button,
.stDownloadButton > button,
.stFormSubmitButton > button {
    background: #8B5CF6;
    color: white;
    border: none;
    border-radius: 10px;
    font-weight: 600;
    padding: 0.55rem 1rem;
    transition: 0.2s ease;
}

.stButton > button:hover,
.stDownloadButton > button:hover,
.stFormSubmitButton > button:hover {
    background: #A78BFA;
    color: #171027;
}

/* Expanders */

[data-testid="stExpander"] {
    background: #261A3B;
    border: 1px solid #493564;
    border-radius: 12px;
}

/* Dataframes */

[data-testid="stDataFrame"] {
    border: 1px solid #493564;
    border-radius: 10px;
}

/* Dividers */

hr {
    border-color: #493564;
}

/* Alerts */

[data-testid="stAlert"] {
    border-radius: 10px;
}

/* Links */

a {
    color: #C4A7FF !important;
}

</style>
""", unsafe_allow_html=True)


# =========================================================
# CHART STYLE FUNCTION
# =========================================================

def style_chart(fig, ax, title):

    fig.patch.set_facecolor(CARD)
    ax.set_facecolor(CARD)

    ax.set_title(
        title,
        color=WHITE,
        fontsize=13,
        fontweight="bold",
        pad=15
    )

    ax.tick_params(colors=MUTED)

    ax.xaxis.label.set_color(MUTED)
    ax.yaxis.label.set_color(MUTED)

    for spine in ax.spines.values():
        spine.set_color(BORDER)

    ax.grid(
        axis="y",
        color=BORDER,
        linestyle="--",
        alpha=0.5
    )


# =========================================================
# RISK CLASSIFICATION
# =========================================================

def get_risk_level(score):

    if score >= 0.70:
        return "High Risk"

    elif score >= 0.40:
        return "Uncertain"

    return "Low Risk"


# =========================================================
# DATA
# =========================================================

# =========================================================
# DATA — LOAD PERSISTENT RECORDS FROM SQLITE
# =========================================================
# DATA — LOAD PERSISTENT RECORDS FROM SQLITE

saved_scans = get_all_scans(
    user_id=st.session_state.user["id"]
)

saved_feedback = get_all_feedback(
    user_id=st.session_state.user["id"]
)

history_records = []

for scan in saved_scans:

    try:
        reasons = ast.literal_eval(scan["reasons"]) if scan["reasons"] else []
    except (ValueError, SyntaxError):
        reasons = []

    history_records.append({
        "ID": scan["id"],
        "Date": datetime.fromisoformat(
            scan["created_at"]
        ).strftime("%d-%m-%Y %H:%M:%S"),
        "Type": scan["scan_type"],
        "Input": scan["input_text"],
        "Result": scan["prediction"],
        "Score": round(scan["risk_score"] * 100, 2),
        "Level": scan["risk_level"],
        "Reasons": reasons
    })

history_df = pd.DataFrame(history_records)

if not history_df.empty:

    history_df["Score"] = pd.to_numeric(
        history_df["Score"],
        errors="coerce"
    )

    history_df["DateTime"] = pd.to_datetime(
        history_df["Date"],
        format="%d-%m-%Y %H:%M:%S",
        errors="coerce"
    )


# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.markdown(
    """
    <h1 style="color:#C4A7FF;">
        🛡️ ScamShield AI
    </h1>
    <p style="color:#BBAAD9;">
        Intelligent Threat Detection
    </p>
    """,
    unsafe_allow_html=True
)

st.sidebar.divider()

page = st.sidebar.radio(
    "NAVIGATION",
    [
        "Overview",
        "Threat Scanner",
        "Scan History",
        "Analytics",
        "Feedback"
    ]
)

st.sidebar.divider()

st.sidebar.metric(
    "Total Scans",
    len(history_df)
)

st.sidebar.caption(
    "AI-powered SMS and phishing URL detection"
)


# =========================================================
# OVERVIEW
# =========================================================

if page == "Overview":

    st.title("Security Overview")

    st.write(
        "Monitor suspicious messages and phishing URLs "
        "using machine learning."
    )

    total = len(history_df)

    if total:

        high = int(
            (history_df["Level"] == "High Risk").sum()
        )

        uncertain = int(
            (history_df["Level"] == "Uncertain").sum()
        )

        low = int(
            (history_df["Level"] == "Low Risk").sum()
        )

    else:

        high = 0
        uncertain = 0
        low = 0

    # METRIC CARDS

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("Total Scans", total)
    c2.metric("High Risk", high)
    c3.metric("Uncertain", uncertain)
    c4.metric("Low Risk", low)

    st.divider()

    if total:

        # ---------------------------------------------
        # PIE CHART
        # ---------------------------------------------

        left, right = st.columns(2)

        with left:

            st.subheader("Threat Distribution")

            risk_labels = [
                "High Risk",
                "Uncertain",
                "Low Risk"
            ]

            risk_values = [
                high,
                uncertain,
                low
            ]

            nonzero = [
                (label, value)
                for label, value in zip(
                    risk_labels,
                    risk_values
                )
                if value > 0
            ]

            labels, values = zip(*nonzero)

            fig, ax = plt.subplots(figsize=(6, 4))

            fig.patch.set_facecolor(CARD)
            ax.set_facecolor(CARD)

            ax.pie(
                values,
                labels=labels,
                autopct="%1.1f%%",
                startangle=90,
                colors=[
                    RISK_COLORS[label]
                    for label in labels
                ],
                textprops={
                    "color": WHITE,
                    "fontsize": 10
                },
                wedgeprops={
                    "edgecolor": CARD,
                    "linewidth": 3
                }
            )

            ax.axis("equal")

            st.pyplot(fig, use_container_width=True)
            plt.close(fig)

        # ---------------------------------------------
        # BAR CHART: SCAN TYPES
        # ---------------------------------------------

        with right:

            st.subheader("Detection Categories")

            type_counts = (
                history_df["Type"]
                .value_counts()
                .reindex(
                    ["Message", "URL"],
                    fill_value=0
                )
            )

            fig, ax = plt.subplots(figsize=(6, 4))

            ax.bar(
                type_counts.index,
                type_counts.values,
                color=[PURPLE, LAVENDER],
                width=0.55
            )

            ax.set_ylabel("Number of Scans")

            style_chart(
                fig,
                ax,
                "Message vs URL Scans"
            )

            st.pyplot(fig, use_container_width=True)
            plt.close(fig)

        st.divider()

        # ---------------------------------------------
        # PREDICTION RESULTS
        # ---------------------------------------------

        st.subheader("Prediction Results")

        prediction_counts = history_df[
            "Result"
        ].value_counts()

        fig, ax = plt.subplots(figsize=(10, 4))

        bars = ax.bar(
            prediction_counts.index.astype(str),
            prediction_counts.values,
            color=[
                PINK if "spam" in str(label).lower()
                or "phishing" in str(label).lower()
                else MINT
                for label in prediction_counts.index
            ]
        )

        ax.set_ylabel("Number of Predictions")

        style_chart(
            fig,
            ax,
            "Legitimate vs Suspicious Predictions"
        )

        ax.tick_params(
            axis="x",
            rotation=15
        )

        st.pyplot(fig, use_container_width=True)
        plt.close(fig)

        st.divider()

        # ---------------------------------------------
        # DAILY ACTIVITY LINE GRAPH
        # ---------------------------------------------

        st.subheader("Daily Scan Activity")

        activity = history_df.dropna(
            subset=["DateTime"]
        ).copy()

        if not activity.empty:

            activity["Day"] = (
                activity["DateTime"].dt.date
            )

            daily_scans = (
                activity.groupby("Day")
                .size()
                .reset_index(name="Scans")
            )

            fig, ax = plt.subplots(figsize=(10, 4))

            ax.plot(
                daily_scans["Day"].astype(str),
                daily_scans["Scans"],
                marker="o",
                linewidth=2.5,
                color=LAVENDER
            )

            ax.fill_between(
                range(len(daily_scans)),
                daily_scans["Scans"],
                color=PURPLE,
                alpha=0.15
            )

            ax.set_ylabel("Number of Scans")
            ax.set_xlabel("Date")

            style_chart(
                fig,
                ax,
                "Daily Scanning Activity"
            )

            ax.tick_params(
                axis="x",
                rotation=25
            )

            st.pyplot(fig, use_container_width=True)
            plt.close(fig)

        st.divider()

        # ---------------------------------------------
        # RISK SCORE TREND
        # ---------------------------------------------

        st.subheader("Risk Score Trend")

        score_data = history_df.dropna(
            subset=["Score"]
        ).reset_index(drop=True)

        if not score_data.empty:

            fig, ax = plt.subplots(figsize=(10, 4))

            ax.plot(
                score_data.index + 1,
                score_data["Score"],
                marker="o",
                color=PINK,
                linewidth=2
            )

            ax.axhline(
                70,
                color="#F28BA8",
                linestyle="--",
                label="High Risk Threshold"
            )

            ax.axhline(
                40,
                color="#F6CB79",
                linestyle="--",
                label="Review Threshold"
            )

            ax.set_xlabel("Scan Number")
            ax.set_ylabel("Risk Score (%)")
            ax.set_ylim(0, 100)

            style_chart(
                fig,
                ax,
                "Risk Score Across Scans"
            )

            ax.legend(
                facecolor=CARD,
                labelcolor=WHITE
            )

            st.pyplot(fig, use_container_width=True)
            plt.close(fig)

        st.divider()

        # ---------------------------------------------
        # COMMON WARNING INDICATORS
        # ---------------------------------------------

        st.subheader("Common Warning Indicators")

        all_reasons = []

        for reasons in history_df["Reasons"].dropna():

            if isinstance(reasons, list):
                all_reasons.extend(reasons)

        if all_reasons:

            reason_counts = (
                pd.Series(all_reasons)
                .value_counts()
                .head(8)
                .sort_values()
            )

            fig, ax = plt.subplots(figsize=(10, 5))

            ax.barh(
                reason_counts.index,
                reason_counts.values,
                color=LAVENDER
            )

            ax.set_xlabel("Number of Occurrences")

            style_chart(
                fig,
                ax,
                "Frequently Detected Warning Indicators"
            )

            st.pyplot(fig, use_container_width=True)
            plt.close(fig)

        else:

            st.info(
                "Warning indicator analytics will appear "
                "after new scans."
            )

        st.divider()

        # ---------------------------------------------
        # RECENT ACTIVITY
        # ---------------------------------------------

        st.subheader("Recent Activity")

        st.dataframe(
            history_df.tail(5).iloc[::-1].drop(
                columns=["DateTime", "Reasons"],
                errors="ignore"
            ),
            use_container_width=True,
            hide_index=True
        )

    else:

        st.info(
            "No scan data available yet. Open Threat Scanner "
            "and analyze some messages or URLs to generate analytics."
        )


# =========================================================
# THREAT SCANNER
# =========================================================

elif page == "Threat Scanner":

    st.title("Threat Scanner")

    st.write(
        "Analyze messages and website URLs for suspicious characteristics."
    )

    scan_mode = st.selectbox(
        "Choose scanning mode",
        [
            "Message Scan",
            "URL Scan",
            "Combined Scan"
        ]
    )

    message = ""
    url = ""

    if scan_mode in [
        "Message Scan",
        "Combined Scan"
    ]:

        message = st.text_area(
            "Enter your message",
            placeholder="Paste an SMS, email or suspicious message...",
            height=150
        )

    if scan_mode in [
        "URL Scan",
        "Combined Scan"
    ]:

        url = st.text_input(
            "Enter website URL",
            placeholder="https://example.com"
        )

    if st.button(
        "🔍 Analyze Now",
        type="primary",
        use_container_width=True
    ):

        if not message.strip() and not url.strip():

            st.warning(
                "Enter a message or URL to scan."
            )

        else:

            risk_scores = []
            scan_details = []

            scan_time = datetime.now().strftime(
                "%d-%m-%Y %H:%M:%S"
            )

            # MESSAGE ANALYSIS

            if message.strip():

                score, result = detect_message(message)

                reasons = explain_message(message)

                risk_scores.append(score)

                scan_details.append({
                    "Type": "Message",
                    "Input": message,
                    "Result": result,
                    "Score": score,
                    "Reasons": reasons
                })

                with st.expander(
                    "Message Analysis",
                    expanded=True
                ):

                    st.write(
                        "Prediction:",
                        result
                    )

                    st.metric(
                        "Message Risk Score",
                        f"{score * 100:.2f}%"
                    )

                    st.progress(
                        float(max(0, min(score, 1)))
                    )

                    st.write("Warning Indicators")

                    if reasons:

                        for reason in reasons:
                            st.write("•", reason)

                    else:

                        st.write(
                            "No warning indicators returned."
                        )

            # URL ANALYSIS

            if url.strip():

                score, result = detect_url(url)

                reasons = explain_url(url)

                risk_scores.append(score)

                scan_details.append({
                    "Type": "URL",
                    "Input": url,
                    "Result": result,
                    "Score": score,
                    "Reasons": reasons
                })

                with st.expander(
                    "URL Analysis",
                    expanded=True
                ):

                    st.write(
                        "Prediction:",
                        result
                    )

                    st.metric(
                        "URL Risk Score",
                        f"{score * 100:.2f}%"
                    )

                    st.progress(
                        float(max(0, min(score, 1)))
                    )

                    st.write("Warning Indicators")

                    if reasons:

                        for reason in reasons:
                            st.write("•", reason)

                    else:

                        st.write(
                            "No warning indicators returned."
                        )

            # OVERALL RISK

            overall = max(risk_scores)

            overall_level = get_risk_level(overall)

            st.divider()

            st.subheader("Overall Risk Assessment")

            st.metric(
                "Overall Threat Score",
                f"{overall * 100:.2f}%"
            )

            if overall_level == "High Risk":

                st.error(
                    "HIGH RISK — Potential threat detected."
                )

            elif overall_level == "Uncertain":

                st.warning(
                    "UNCERTAIN — Further review recommended."
                )

            else:

                st.success(
                    "LOW RISK — No strong scam indicators detected."
                )

           

            # SAVE EACH INDIVIDUAL SCAN TO SQLITE

            for item in scan_details:

                item_level = get_risk_level(item["Score"])

                scan_id = save_scan(
    scan_type=item["Type"],
    input_text=item["Input"],
    prediction=item["Result"],
    risk_score=item["Score"],
    risk_level=item_level,
    reasons=item["Reasons"],
    user_id=st.session_state.user["id"]
)

                st.write(f"Scan #{scan_id} saved successfully.")

            st.caption(
                "Predictions are estimates, not guarantees of safety."
            )

            st.success(
                "Scan results added to your history."
            )


# =========================================================
# SCAN HISTORY
# =========================================================

elif page == "Scan History":

    st.title("Scan History")

    st.write(
        "Review your previous detection results."
    )

    if not history_df.empty:

        search = st.text_input(
            "Search messages or URLs"
        )

        filter_type = st.selectbox(
            "Filter by scan type",
            ["All", "Message", "URL"]
        )

        filter_level = st.selectbox(
            "Filter by risk level",
            [
                "All",
                "High Risk",
                "Uncertain",
                "Low Risk"
            ]
        )

        filtered = history_df.copy()

        if search:

            filtered = filtered[
                filtered["Input"].str.contains(
                    search,
                    case=False,
                    na=False
                )
            ]

        if filter_type != "All":

            filtered = filtered[
                filtered["Type"] == filter_type
            ]

        if filter_level != "All":

            filtered = filtered[
                filtered["Level"] == filter_level
            ]

        st.dataframe(
            filtered.drop(
                columns=["DateTime", "Reasons"],
                errors="ignore"
            ),
            use_container_width=True,
            hide_index=True
        )

        st.download_button(
            "📥 Export Scan History",
            data=filtered.drop(
                columns=["DateTime"],
                errors="ignore"
            ).to_csv(index=False),
            file_name="scamshield_history.csv",
            mime="text/csv"
        )

        if st.button("Clear All History"):

            st.session_state.history = []

            st.rerun()

    else:

        st.info(
            "No scan history available."
        )


# =========================================================
# ANALYTICS
# =========================================================

elif page == "Analytics":

    st.title("Detection Analytics")

    if not history_df.empty:

        total = len(history_df)

        high = int(
            (history_df["Level"] == "High Risk").sum()
        )

        uncertain = int(
            (history_df["Level"] == "Uncertain").sum()
        )

        low = int(
            (history_df["Level"] == "Low Risk").sum()
        )

        # SUMMARY

        c1, c2, c3 = st.columns(3)

        c1.metric("High Risk", high)
        c2.metric("Uncertain", uncertain)
        c3.metric("Low Risk", low)

        st.divider()

        # RISK DISTRIBUTION

        st.subheader("Risk Level Distribution")

        risk_data = pd.Series({
            "High Risk": high,
            "Uncertain": uncertain,
            "Low Risk": low
        })

        fig, ax = plt.subplots(figsize=(8, 4))

        ax.bar(
            risk_data.index,
            risk_data.values,
            color=[
                RISK_COLORS[label]
                for label in risk_data.index
            ]
        )

        ax.set_ylabel("Number of Scans")

        style_chart(
            fig,
            ax,
            "Risk Level Distribution"
        )

        st.pyplot(fig, use_container_width=True)
        plt.close(fig)

        st.divider()

        # TYPE DISTRIBUTION

        st.subheader("Message vs URL Scans")

        type_counts = (
            history_df["Type"]
            .value_counts()
            .reindex(
                ["Message", "URL"],
                fill_value=0
            )
        )

        fig, ax = plt.subplots(figsize=(8, 4))

        ax.bar(
            type_counts.index,
            type_counts.values,
            color=[PURPLE, LAVENDER]
        )

        ax.set_ylabel("Number of Scans")

        style_chart(
            fig,
            ax,
            "Scan Type Comparison"
        )

        st.pyplot(fig, use_container_width=True)
        plt.close(fig)

        st.divider()

        # SCORE DISTRIBUTION

        st.subheader("Risk Score Distribution")

        fig, ax = plt.subplots(figsize=(8, 4))

        ax.hist(
            history_df["Score"].dropna(),
            bins=10,
            color=LAVENDER,
            edgecolor=CARD
        )

        ax.set_xlabel("Risk Score (%)")
        ax.set_ylabel("Number of Scans")

        style_chart(
            fig,
            ax,
            "Distribution of Risk Scores"
        )

        st.pyplot(fig, use_container_width=True)
        plt.close(fig)

        st.divider()

        # WARNING INDICATORS

        st.subheader("Warning Indicator Analysis")

        all_reasons = []

        for reasons in history_df["Reasons"].dropna():

            if isinstance(reasons, list):
                all_reasons.extend(reasons)

        if all_reasons:

            reason_counts = (
                pd.Series(all_reasons)
                .value_counts()
                .head(10)
                .sort_values()
            )

            fig, ax = plt.subplots(figsize=(10, 5))

            ax.barh(
                reason_counts.index,
                reason_counts.values,
                color=PINK
            )

            ax.set_xlabel("Occurrences")

            style_chart(
                fig,
                ax,
                "Most Common Warning Indicators"
            )

            st.pyplot(fig, use_container_width=True)
            plt.close(fig)

        else:

            st.info(
                "No warning indicator data available yet."
            )

    else:

        st.info(
            "Analytics will appear after you perform some scans."
        )


# =========================================================
# FEEDBACK
# =========================================================

elif page == "Feedback":

    st.title("User Feedback")

    st.write(
        "Help us understand whether the detection result "
        "matches your assessment."
    )

    with st.form("feedback_form"):

        scan_type = st.selectbox(
            "Scan type",
            ["Message", "URL"]
        )

        feedback_text = st.text_area(
            "Enter the scanned message or URL"
        )

        prediction = st.selectbox(
            "Was the prediction correct?",
            [
                "Correct",
                "Incorrect",
                "Not sure"
            ]
        )

        comments = st.text_area(
            "Additional comments (optional)"
        )

        submitted = st.form_submit_button(
            "Submit Feedback"
        )

        if submitted:

            if not feedback_text.strip():

                st.warning(
                    "Please enter the scanned content."
                )

            else:

                st.session_state.feedback.append({

                    "Date": datetime.now().strftime(
                        "%d-%m-%Y %H:%M:%S"
                    ),

                    "Type": scan_type,

                    "Input": feedback_text,

                    "Feedback": prediction,

                    "Comments": comments

                })

                st.success(
                    "Feedback recorded successfully."
                )

    # DISPLAY FEEDBACK

    if st.session_state.feedback:

        st.divider()

        st.subheader("Submitted Feedback")

        feedback_df = pd.DataFrame(
            st.session_state.feedback
        )

        st.dataframe(
            feedback_df,
            use_container_width=True,
            hide_index=True
        )

        st.download_button(
            "Download Feedback",
            data=feedback_df.to_csv(index=False),
            file_name="scamshield_feedback.csv",
            mime="text/csv"
        )


# =========================================================
# FOOTER
# =========================================================

st.divider()

st.markdown(
    """
    <div style="
        text-align:center;
        color:#BBAAD9;
        padding:10px;
    ">
        🛡️ <b>ScamShield AI</b><br>
        Real-Time, Explainable and Adaptive
        Scam & Phishing Detection System
    </div>
    """,
    unsafe_allow_html=True
)

st.sidebar.divider()
st.sidebar.write(f"Logged in as **{st.session_state.user['name']}**")

if st.sidebar.button("Log Out", use_container_width=True):
    st.session_state.user = None
    st.session_state.history = []
    st.session_state.feedback = []
    st.rerun()
