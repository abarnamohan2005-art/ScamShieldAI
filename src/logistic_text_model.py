
import pandas as pd

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix
)

# Load datasets
train_data = pd.read_csv("data/train.csv")
val_data = pd.read_csv("data/validation.csv")

X_train = train_data["message"]
y_train = train_data["label"]

X_val = val_data["message"]
y_val = val_data["label"]

# Create Logistic Regression model
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

# Train model
model.fit(X_train, y_train)

print("LOGISTIC REGRESSION TRAINED!")


# Get spam probabilities
spam_probabilities = model.predict_proba(X_val)[:, 1]

# Test different thresholds
for threshold in [0.30, 0.40, 0.50, 0.60, 0.70]:

    predictions = [
        "spam" if probability >= threshold else "ham"
        for probability in spam_probabilities
    ]

    print("\nTHRESHOLD:", threshold)

    print(classification_report(
        y_val,
        predictions,
        labels=["ham", "spam"],
        zero_division=0
    ))

    print("CONFUSION MATRIX:")
    print(confusion_matrix(
        y_val,
        predictions,
        labels=["ham", "spam"]
    ))

