
import pandas as pd

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn.metrics import (
    classification_report,
    confusion_matrix,
    accuracy_score
)

# Load training and validation datasets
train_data = pd.read_csv("data/train.csv")
val_data = pd.read_csv("data/validation.csv")

X_train = train_data["message"]
y_train = train_data["label"]

X_val = val_data["message"]
y_val = val_data["label"]

# Create the machine learning pipeline
model = Pipeline([
    ("tfidf", TfidfVectorizer(
        lowercase=True,
        ngram_range=(1, 2),
        stop_words="english"
    )),
    ("classifier", MultinomialNB())
])

# Train the model
model.fit(X_train, y_train)

print("MODEL TRAINED SUCCESSFULLY!")

# Predict validation messages
predictions = model.predict(X_val)

# Evaluate the model
print("\nACCURACY:")
print(accuracy_score(y_val, predictions))

print("\nCLASSIFICATION REPORT:")
print(classification_report(y_val, predictions))

print("\nCONFUSION MATRIX:")
print(confusion_matrix(
    y_val,
    predictions,
    labels=["ham", "spam"]
))
