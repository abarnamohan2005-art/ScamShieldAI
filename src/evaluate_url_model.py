
import pandas as pd
import joblib

from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix
)

# Load the saved Random Forest model
model = joblib.load("models/url_model.pkl")

# Load the untouched test dataset
test_data = pd.read_csv("data/url_test_features.csv")

# Separate features and actual labels
X_test = test_data.drop("type", axis=1)
y_test = test_data["type"]

# Make predictions
predictions = model.predict(X_test)

# Calculate accuracy
accuracy = accuracy_score(y_test, predictions)

print("========== FINAL URL MODEL EVALUATION ==========")

print("\nTest Accuracy:", round(accuracy * 100, 2), "%")

print("\nClassification Report:")
print(classification_report(y_test, predictions))

print("Confusion Matrix:")
print(confusion_matrix(
    y_test,
    predictions,
    labels=["legitimate", "phishing"]
))

# Calculate false predictions
cm = confusion_matrix(
    y_test,
    predictions,
    labels=["legitimate", "phishing"]
)

tn, fp, fn, tp = cm.ravel()

print("\n========== FALSE PREDICTIONS ==========")
print("False Positives:", fp)
print("False Negatives:", fn)
print("Correct Legitimate Predictions:", tn)
print("Correct Phishing Predictions:", tp)
