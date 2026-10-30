
import joblib
import os
import pandas as pd

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix
)

# Load training and testing data
train_data = pd.read_csv("data/train.csv")
test_data = pd.read_csv("data/test.csv")

X_train = train_data["message"]
y_train = train_data["label"]

X_test = test_data["message"]
y_test = test_data["label"]

# Build the model
model = Pipeline([
    ("tfidf", TfidfVectorizer(
        lowercase=True,
        ngram_range=(1, 2),
        stop_words="english"
    )),
    ("classifier", LogisticRegression(
        class_weight="balanced",
        max_iter=1000,
        random_state=42
    ))
])

# Train using training data only
model.fit(X_train, y_train)

# Predict spam probabilities
spam_probabilities = model.predict_proba(X_test)[:, 1]

# Apply selected threshold
threshold = 0.40

predictions = [
    "spam" if probability >= threshold else "ham"
    for probability in spam_probabilities
]

# Evaluate final test performance
print("FINAL TEST RESULTS")
print("Threshold:", threshold)

print("\nACCURACY:")
print(accuracy_score(y_test, predictions))

print("\nCLASSIFICATION REPORT:")
print(classification_report(y_test, predictions))

print("\nCONFUSION MATRIX:")
print(confusion_matrix(
    y_test,
    predictions,
    labels=["ham", "spam"]
))
# Save trained model
os.makedirs("models", exist_ok=True)

joblib.dump(model, "models/text_model.pkl")

print("\nTEXT MODEL SAVED SUCCESSFULLY!")