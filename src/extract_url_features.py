
import pandas as pd
import re
import tldextract
from urllib.parse import urlparse

# Use the bundled Public Suffix List without requiring a network request
extractor = tldextract.TLDExtract(suffix_list_urls=())

# Common brands and their legitimate registered domains
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


def extract_features(url):

    url = str(url).strip()

    parsed = urlparse(
        url if "://" in url else "http://" + url
    )

    domain = parsed.hostname or ""
    path = parsed.path

    features = {}

    # Original 11 features
    features["url_length"] = len(url)
    features["domain_length"] = len(domain)
    features["dot_count"] = url.count(".")
    features["hyphen_count"] = url.count("-")
    features["at_count"] = url.count("@")
    features["digit_count"] = sum(char.isdigit() for char in url)

    features["subdomain_count"] = max(
        0, len(domain.split(".")) - 2
    )

    features["https"] = int(parsed.scheme == "https")

    features["ip_address"] = int(
        bool(re.match(r"^\d{1,3}(\.\d{1,3}){3}$", domain))
    )

    suspicious_words = [
        "login", "verify", "update", "secure",
        "account", "banking", "password", "confirm"
    ]

    features["suspicious_word_count"] = sum(
        word in url.lower() for word in suspicious_words
    )

    features["path_length"] = len(path)

    # New feature: brand impersonation detection
    extracted = extractor(domain)

    registered_domain = extracted.top_domain_under_public_suffix

    brand_impersonation = 0

    for brand, trusted_domains in TRUSTED_BRANDS.items():

        if brand in domain.lower():

            if registered_domain not in trusted_domains:
                brand_impersonation = 1
                break

    features["brand_impersonation"] = brand_impersonation

    return features


# Process each dataset
datasets = {
    "train": "data/url_train.csv",
    "validation": "data/url_validation.csv",
    "test": "data/url_test.csv"
}

for name, file_path in datasets.items():

    print(f"\nProcessing {name} dataset...")

    data = pd.read_csv(file_path)

    feature_data = pd.DataFrame(
        data["url"].apply(extract_features).tolist()
    )

    # Add original target labels
    feature_data["type"] = data["type"].values

    # Save extracted features
    output_path = f"data/url_{name}_features.csv"

    feature_data.to_csv(output_path, index=False)

    print("Saved:", output_path)
    print("Shape:", feature_data.shape)

print("\nFeature extraction completed!")
