import pandas as pd
from sklearn.model_selection import train_test_split

# Load dataset
data = pd.read_csv("data/phishing_urls.csv")

# Remove any duplicate URLs, if present
data = data.drop_duplicates(subset=["url"])

# Remove rows with missing values
data = data.dropna(subset=["url", "type"])

# First split: 80% training, 20% temporary
train_data, temp_data = train_test_split(
    data,
    test_size=0.20,
    random_state=42,
    stratify=data["type"]
)

# Second split: 10% validation, 10% testing
validation_data, test_data = train_test_split(
    temp_data,
    test_size=0.50,
    random_state=42,
    stratify=temp_data["type"]
)

# Save datasets
train_data.to_csv("data/url_train.csv", index=False)
validation_data.to_csv("data/url_validation.csv", index=False)
test_data.to_csv("data/url_test.csv", index=False)

# Display dataset sizes
print("Training dataset:", len(train_data))
print("Validation dataset:", len(validation_data))
print("Testing dataset:", len(test_data))

print("\nTraining class distribution:")
print(train_data["type"].value_counts())

print("\nValidation class distribution:")
print(validation_data["type"].value_counts())

print("\nTesting class distribution:")
print(test_data["type"].value_counts())