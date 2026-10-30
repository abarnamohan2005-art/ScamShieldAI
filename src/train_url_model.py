
import pandas as pd
import joblib

from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier

from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix
)

# Load training and validation datasets
train_data = pd.read_csv("data/url_train_features.csv")
val_data = pd.read_csv("data/url_validation_features.csv")

# Separate input features and target labels
X_train = train_data.drop("type", axis=1)
y_train = train_data["type"]

X_val = val_data.drop("type", axis=1)
y_val = val_data["type"]

# Define the algorithms
models = {
    "Random Forest": RandomForestClassifier(
        n_estimators=100,
        class_weight="balanced",
        random_state=42,
        n_jobs=-1
    ),

    "Logistic Regression": LogisticRegression(
        class_weight="balanced",
        max_iter=1000
    ),

    "Decision Tree": DecisionTreeClassifier(
        class_weight="balanced",
        random_state=42
    )
}

# Train and evaluate each model
results = {}

for name, model in models.items():

    print("\nTraining:", name)

    model.fit(X_train, y_train)

    predictions = model.predict(X_val)

    accuracy = accuracy_score(y_val, predictions)

    print("\nAccuracy:", round(accuracy * 100, 2), "%")
    print("\nClassification Report:")
    print(classification_report(y_val, predictions))

    print("Confusion Matrix:")
    print(confusion_matrix(
        y_val,
        predictions,
        labels=["legitimate", "phishing"]
    ))

    results[name] = accuracy

# Compare model accuracy
print("\n========== MODEL COMPARISON ==========")

for name, accuracy in results.items():
    print(name, ":", round(accuracy * 100, 2), "%")

# Save the best model based on validation accuracy
best_model_name = max(results, key=results.get)
best_model = models[best_model_name]

joblib.dump(best_model, "models/url_model.pkl")

print("\nBest model:", best_model_name)
print("Saved as models/url_model.pkl")
