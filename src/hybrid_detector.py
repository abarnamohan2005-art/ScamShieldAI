
import joblib
import re
import pandas as pd
import tldextract

from urllib.parse import urlparse

# Load the trained models
text_model = joblib.load("models/text_model.pkl")
url_model = joblib.load("models/url_model.pkl")

# Classification thresholds
TEXT_THRESHOLD = 0.40
URL_THRESHOLD = 0.50

# Offline Public Suffix List
extractor = tldextract.TLDExtract(suffix_list_urls=())

# Trusted brand domains
TRUSTED_BRANDS = {
    "amazon": ["amazon.com", "amazon.in", "amazon.co.uk"],
    "google": ["google.com", "google.co.in"],
    "microsoft": ["microsoft.com"],
    "paypal": ["paypal.com"],
    "sbi": ["sbi.co.in"],
    "apple": ["apple.com"],
    "facebook": ["facebook.com"],
    "instagram": ["instagram.com"],
    "netflix": ["netflix.com"]
}


# Explain suspicious messages
def explain_message(message):

    reasons = []
    message_lower = message.lower()

    suspicious_keywords = [
        "urgent", "immediately", "blocked",
        "verify", "password", "account",
        "winner", "prize", "claim",
        "free", "bank"
    ]

    for word in suspicious_keywords:
        if word in message_lower:
            reasons.append(
                f"Suspicious keyword detected: '{word}'"
            )

    if not reasons:
        reasons.append(
            "No predefined suspicious keywords detected."
        )

    return reasons


# Extract URL features
def extract_url_features(url):

    url = str(url).strip()

    parsed = urlparse(
        url if "://" in url else "http://" + url
    )

    domain = parsed.netloc
    path = parsed.path

    features = {}

    # Original 11 features
    features["url_length"] = len(url)
    features["domain_length"] = len(domain)
    features["dot_count"] = url.count(".")
    features["hyphen_count"] = url.count("-")
    features["at_count"] = url.count("@")
    features["digit_count"] = sum(
        c.isdigit() for c in url
    )

    features["subdomain_count"] = max(
        0, len(domain.split(".")) - 2
    )

    features["https"] = int(
        parsed.scheme == "https"
    )

    features["ip_address"] = int(
        bool(re.match(
            r"^\d{1,3}(\.\d{1,3}){3}$",
            domain.split(":")[0]
        ))
    )

    suspicious_words = [
        "login", "verify", "update", "secure",
        "account", "banking", "password", "confirm"
    ]

    features["suspicious_word_count"] = sum(
        word in url.lower()
        for word in suspicious_words
    )

    features["path_length"] = len(path)

    # New 12th feature: Brand impersonation
    extracted = extractor(domain)

    registered_domain = (
        extracted.top_domain_under_public_suffix
    )

    brand_impersonation = 0

    for brand, trusted_domains in TRUSTED_BRANDS.items():

        if brand in domain.lower():

            if registered_domain not in trusted_domains:
                brand_impersonation = 1
                break

    features["brand_impersonation"] = brand_impersonation

    return features


# Explain suspicious URL characteristics
def explain_url(url):

    features = extract_url_features(url)
    reasons = []

    if features["https"] == 0:
        reasons.append("URL does not use HTTPS.")

    if features["ip_address"] == 1:
        reasons.append(
            "URL uses an IP address instead of a domain name."
        )

    if features["url_length"] > 75:
        reasons.append(
            "URL has an unusually long address."
        )

    if features["subdomain_count"] >= 3:
        reasons.append(
            "URL contains multiple subdomains."
        )

    if features["hyphen_count"] >= 3:
        reasons.append(
            "URL contains several hyphens."
        )

    if features["at_count"] > 0:
        reasons.append(
            "URL contains an '@' symbol."
        )

    if features["suspicious_word_count"] > 0:
        reasons.append(
            "URL contains suspicious keywords."
        )

    if features["brand_impersonation"] == 1:
        reasons.append(
            "A known brand name appears in a domain "
            "that does not match its configured trusted domains."
        )

    if not reasons:
        reasons.append(
            "No predefined suspicious URL characteristics detected."
        )

    return reasons


# Detect scam in a message
def detect_message(message):

    probabilities = text_model.predict_proba([message])[0]

    spam_index = list(text_model.classes_).index("spam")
    spam_probability = probabilities[spam_index]

    if spam_probability >= TEXT_THRESHOLD:
        result = "Suspicious Message"
    else:
        result = "Likely Legitimate Message"

    return spam_probability, result


# Detect phishing in a URL
def detect_url(url):

    features = extract_url_features(url)

    feature_data = pd.DataFrame([features])

    probabilities = url_model.predict_proba(
        feature_data
    )[0]

    phishing_index = list(
        url_model.classes_
    ).index("phishing")

    phishing_probability = probabilities[phishing_index]

    if phishing_probability >= URL_THRESHOLD:
        result = "Phishing URL"
    else:
        result = "Likely Legitimate URL"

    return phishing_probability, result


# Hybrid detection
def hybrid_detection(message="", url=""):

    print("\n========== SCAMSHIELD AI ==========")

    risk_scores = []

    if message.strip():

        message_score, message_result = detect_message(message)

        print("\nMessage Result:", message_result)
        print(
            "Message Risk:",
            round(message_score * 100, 2), "%"
        )

        print("\nWhy this message was flagged:")

        for reason in explain_message(message):
            print("-", reason)

        risk_scores.append(message_score)

    if url.strip():

        url_score, url_result = detect_url(url)

        print("\nURL Result:", url_result)
        print(
            "URL Risk:",
            round(url_score * 100, 2), "%"
        )

        print("\nWhy this URL was flagged:")

        for reason in explain_url(url):
            print("-", reason)

        risk_scores.append(url_score)

    if not risk_scores:
        print("\nPlease enter a message or URL.")
        return

    overall_risk = max(risk_scores)

    print(
        "\nOverall Risk:",
        round(overall_risk * 100, 2), "%"
    )

    if overall_risk >= 0.70:
        print("FINAL RESULT: HIGH RISK")

    elif overall_risk >= 0.40:
        print("FINAL RESULT: UNCERTAIN - REVIEW REQUIRED")

    else:
        print("FINAL RESULT: LOW RISK")


# Run the detector
if __name__ == "__main__":

    message = input(
        "Enter a message (or press Enter to skip): "
    )

    url = input(
        "Enter a URL (or press Enter to skip): "
    )

    hybrid_detection(message, url)
