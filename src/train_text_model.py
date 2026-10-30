
import pandas as pd
from sklearn.model_selection import train_test_split

# Load the dataset
data = pd.read_csv(
    "data/SMSSpamCollection",
    sep="\t",
    header=None,
    names=["label", "message"]
)

# Remove duplicate messages
data = data.drop_duplicates(subset=["message"])

print("Dataset after removing duplicates:")
print(data["label"].value_counts())

# Separate messages and labels
X = data["message"]
y = data["label"]

# Split into training (70%) and temporary data (30%)
X_train, X_temp, y_train, y_temp = train_test_split(
    X, y,
    test_size=0.30,
    random_state=42,
    stratify=y
)

# Split temporary data into validation (15%) and testing (15%)
X_val, X_test, y_val, y_test = train_test_split(
    X_temp, y_temp,
    test_size=0.50,
    random_state=42,
    stratify=y_temp
)

# Save the three datasets
train_data = pd.DataFrame({
    "label": y_train,
    "message": X_train
})

val_data = pd.DataFrame({
    "label": y_val,
    "message": X_val
})

test_data = pd.DataFrame({
    "label": y_test,
    "message": X_test
})

train_data.to_csv("data/train.csv", index=False)
val_data.to_csv("data/validation.csv", index=False)
test_data.to_csv("data/test.csv", index=False)

# Display split sizes
print("\nDATASET SPLIT:")
print("Training:", len(train_data))
print("Validation:", len(val_data))
print("Testing:", len(test_data))

print("\nDATASETS SAVED SUCCESSFULLY!")
