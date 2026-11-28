
import csv
from pathlib import Path

import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    f1_score,
)
from sklearn.model_selection import StratifiedKFold, cross_val_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC


PROJECT_ROOT = Path(__file__).resolve().parents[2]

PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"
TRAIN_FILE = PROCESSED_DIR / "train_dataset.csv"
TEST_FILE = PROCESSED_DIR / "test_dataset.csv"

MODEL_DIR = PROJECT_ROOT / "models"
REPORT_DIR = PROJECT_ROOT / "reports"

RANDOM_STATE = 42
TARGET_COLUMN = "disease_label"
FEATURE_COLUMNS = [f"Var{i}" for i in range(9, 213)]


def load_dataset(file_path):
    with file_path.open("r", encoding="utf-8", newline="") as file:
        reader = csv.DictReader(file)
        rows = list(reader)

    features = [
        [float(row[column]) for column in FEATURE_COLUMNS]
        for row in rows
    ]
    labels = [row[TARGET_COLUMN] for row in rows]

    return features, labels


print("Loading training and testing datasets...")

X_train, y_train = load_dataset(TRAIN_FILE)
X_test, y_test = load_dataset(TEST_FILE)

print(f"Training samples: {len(X_train)}")
print(f"Testing samples: {len(X_test)}")
print(f"Spectral features: {len(FEATURE_COLUMNS)}")


models = {
    "Logistic Regression": Pipeline([
        ("scaler", StandardScaler()),
        ("classifier", LogisticRegression(
            max_iter=5000,
            class_weight="balanced",
            random_state=RANDOM_STATE
        ))
    ]),

    "Support Vector Machine": Pipeline([
        ("scaler", StandardScaler()),
        ("classifier", SVC(
            kernel="rbf",
            class_weight="balanced"
        ))
    ]),

    "Random Forest": RandomForestClassifier(
        n_estimators=300,
        class_weight="balanced",
        random_state=RANDOM_STATE,
        n_jobs=-1
    )
}


cross_validation = StratifiedKFold(
    n_splits=5,
    shuffle=True,
    random_state=RANDOM_STATE
)

results = {}

print("\n========== MODEL COMPARISON ==========")

for model_name, model in models.items():
    print(f"\nEvaluating {model_name}...")

    scores = cross_val_score(
        model,
        X_train,
        y_train,
        cv=cross_validation,
        scoring="f1_macro",
        n_jobs=-1
    )

    mean_score = scores.mean()
    std_score = scores.std()

    results[model_name] = {
        "model": model,
        "mean_f1": mean_score,
        "std_f1": std_score
    }

    print(f"Fold F1 scores: {scores.round(4)}")
    print(f"Mean macro F1: {mean_score:.4f}")
    print(f"Standard deviation: {std_score:.4f}")


best_model_name = max(
    results,
    key=lambda name: results[name]["mean_f1"]
)

best_model = results[best_model_name]["model"]

print("\n========== BEST MODEL ==========")
print(f"Selected model: {best_model_name}")
print(
    f"Cross-validation macro F1: "
    f"{results[best_model_name]['mean_f1']:.4f}"
)


print("\nTraining selected model on complete training data...")

best_model.fit(X_train, y_train)

print("\nEvaluating on untouched test data...")

predictions = best_model.predict(X_test)

accuracy = accuracy_score(y_test, predictions)
macro_f1 = f1_score(y_test, predictions, average="macro")

print("\n========== TEST RESULTS ==========")
print(f"Accuracy: {accuracy:.4f}")
print(f"Macro F1-score: {macro_f1:.4f}")

print("\nClassification Report:")
report = classification_report(
    y_test,
    predictions,
    zero_division=0
)
print(report)

print("Confusion Matrix:")
print(confusion_matrix(
    y_test,
    predictions,
    labels=sorted(set(y_train))
))


MODEL_DIR.mkdir(parents=True, exist_ok=True)
REPORT_DIR.mkdir(parents=True, exist_ok=True)

model_path = MODEL_DIR / "best_grapevine_classifier.joblib"
report_path = REPORT_DIR / "model_evaluation.txt"

joblib.dump(best_model, model_path)

with report_path.open("w", encoding="utf-8") as file:
    file.write("TERRASPECTRA MODEL EVALUATION\n\n")

    file.write("Cross-validation results:\n")
    for name, result in results.items():
        file.write(
            f"{name}: mean macro F1 = "
            f"{result['mean_f1']:.4f}, "
            f"std = {result['std_f1']:.4f}\n"
        )

    file.write(f"\nSelected model: {best_model_name}\n")
    file.write(f"Test accuracy: {accuracy:.4f}\n")
    file.write(f"Test macro F1: {macro_f1:.4f}\n\n")
    file.write("Classification report:\n")
    file.write(report)

print(f"\nSaved model: {model_path}")
print(f"Saved evaluation report: {report_path}")
print("\nBaseline model training completed successfully.")
