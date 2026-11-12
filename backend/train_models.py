
# ==========================================
# INTERNSHIELD AI
# IMPROVED MODEL TRAINING
# ==========================================

import joblib
import pandas as pd
import matplotlib.pyplot as plt

from pathlib import Path

from sklearn.linear_model import LogisticRegression
from sklearn.svm import LinearSVC

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    average_precision_score,
    confusion_matrix,
    classification_report,
    ConfusionMatrixDisplay
)

BASE_DIR = Path(__file__).resolve().parent.parent

MODEL_DIR = BASE_DIR / "models"
REPORT_DIR = BASE_DIR / "reports"

MODEL_DIR.mkdir(exist_ok=True)
REPORT_DIR.mkdir(exist_ok=True)

# Load features

print("\nLoading features...")

data = joblib.load(
    MODEL_DIR / "tfidf_features.joblib"
)

X_train = data["X_train"]
X_test = data["X_test"]

y_train = data["y_train"]
y_test = data["y_test"]

print("Training:", X_train.shape)
print("Testing:", X_test.shape)

# Define models

models = {
    "Logistic Regression": LogisticRegression(
        max_iter=2000,
        class_weight="balanced",
        solver="liblinear",
        random_state=42
    ),

    "Linear SVM": LinearSVC(
        class_weight="balanced",
        random_state=42,
        max_iter=5000
    )
}

results = []
trained_models = {}

# Train and evaluate

for name, model in models.items():

    print("\nTraining:", name)

    model.fit(X_train, y_train)

    predictions = model.predict(X_test)

    scores = model.decision_function(X_test)

    metrics = {
        "Model": name,
        "Accuracy": accuracy_score(y_test, predictions),
        "Precision": precision_score(
            y_test, predictions, zero_division=0
        ),
        "Recall": recall_score(
            y_test, predictions, zero_division=0
        ),
        "F1 Score": f1_score(
            y_test, predictions, zero_division=0
        ),
        "ROC AUC": roc_auc_score(y_test, scores),
        "PR AUC": average_precision_score(y_test, scores)
    }

    results.append(metrics)
    trained_models[name] = model

    print("\nClassification Report:")
    print(
        classification_report(
            y_test,
            predictions,
            target_names=["Genuine", "Fake"],
            zero_division=0
        )
    )

    # Confusion matrix

    cm = confusion_matrix(y_test, predictions)

    disp = ConfusionMatrixDisplay(
        confusion_matrix=cm,
        display_labels=["Genuine", "Fake"]
    )

    fig, ax = plt.subplots(figsize=(6, 5))

    disp.plot(
        cmap="Blues",
        ax=ax,
        colorbar=False
    )

    plt.title(name + " Confusion Matrix")
    plt.tight_layout()

    filename = (
        name.lower().replace(" ", "_")
        + "_confusion_matrix.png"
    )

    plt.savefig(REPORT_DIR / filename)
    plt.close()

# Results comparison

results_df = pd.DataFrame(results)

results_df = results_df.sort_values(
    by="F1 Score",
    ascending=False
)

print("\nMODEL COMPARISON")
print(results_df.to_string(index=False))

results_df.to_csv(
    REPORT_DIR / "model_metrics.csv",
    index=False
)

# Save both models

joblib.dump(
    trained_models,
    MODEL_DIR / "all_models.joblib"
)

# Select model using F1 as primary metric
# and recall as a tie-breaker.

best_model_name = (
    results_df.sort_values(
        by=["F1 Score", "Recall"],
        ascending=False
    ).iloc[0]["Model"]
)

best_model = trained_models[best_model_name]

joblib.dump(
    best_model,
    MODEL_DIR / "best_model.joblib"
)

print("\nSelected model:", best_model_name)

print("\nMODEL TRAINING COMPLETED!")
