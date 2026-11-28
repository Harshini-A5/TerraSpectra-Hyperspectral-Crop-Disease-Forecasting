
import csv
from collections import defaultdict
from pathlib import Path
from sklearn.decomposition import PCA
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    f1_score,
    confusion_matrix,
    classification_report,
)
from sklearn.model_selection import LeaveOneGroupOut
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC


PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATA_FILE = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "grapevine_model_dataset.csv"
)

REPORT_DIR = PROJECT_ROOT / "reports"
REPORT_FILE = REPORT_DIR / "plot_based_validation.txt"

FEATURE_COLUMNS = [f"Var{i}" for i in range(9, 213)]
TARGET_COLUMN = "disease_label"
GROUP_COLUMN = "plot"
RANDOM_STATE = 42

CLASS_LABELS = ["non", "oui", "sain"]


def load_dataset():
    with DATA_FILE.open("r", encoding="utf-8", newline="") as file:
        reader = csv.DictReader(file)
        rows = list(reader)

    X = [
        [float(row[column]) for column in FEATURE_COLUMNS]
        for row in rows
    ]

    y = [row[TARGET_COLUMN] for row in rows]
    groups = [row[GROUP_COLUMN] for row in rows]

    return X, y, groups


def create_models():
    return {
        "Logistic Regression": Pipeline([
            ("scaler", StandardScaler()),
            ("classifier", LogisticRegression(
                max_iter=5000,
                class_weight="balanced",
                random_state=RANDOM_STATE
            ))
        ]),

        "PCA Logistic Regression": Pipeline([
            ("scaler", StandardScaler()),
            ("pca", PCA(n_components=0.95)),
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

print("Loading processed grapevine dataset...")

X, y, groups = load_dataset()

print(f"Total samples: {len(X)}")
print(f"Spectral features: {len(FEATURE_COLUMNS)}")
print(f"Unique plots: {len(set(groups))}")

logo = LeaveOneGroupOut()

models = create_models()

results = defaultdict(lambda: {
    "actual": [],
    "predicted": [],
    "fold_scores": []
})

report_lines = []

print("\n========== LEAVE-ONE-PLOT-OUT VALIDATION ==========")

for fold_number, (train_indices, test_indices) in enumerate(
    logo.split(X, y, groups),
    start=1
):
    held_out_plot = groups[test_indices[0]]

    print(f"\nFold {fold_number}: Holding out {held_out_plot}")

    X_train = [X[i] for i in train_indices]
    y_train = [y[i] for i in train_indices]

    X_test = [X[i] for i in test_indices]
    y_test = [y[i] for i in test_indices]

    print(f"Training samples: {len(X_train)}")
    print(f"Testing samples: {len(X_test)}")

    for model_name, model in models.items():
        model.fit(X_train, y_train)
        predictions = model.predict(X_test)
        if model_name == "PCA Logistic Regression":
            pca = model.named_steps["pca"]

            print(f"PCA components retained: {pca.n_components_}")
            print(
                "Explained variance retained: "
                f"{sum(pca.explained_variance_ratio_):.4f}"
    )
        fold_f1 = f1_score(
            y_test,
            predictions,
            average="macro",
            zero_division=0
        )

        results[model_name]["actual"].extend(y_test)
        results[model_name]["predicted"].extend(predictions)
        results[model_name]["fold_scores"].append(fold_f1)

        print(f"{model_name} macro F1: {fold_f1:.4f}")


print("\n========== OVERALL VALIDATION RESULTS ==========")

for model_name, result in results.items():
    actual = result["actual"]
    predicted = result["predicted"]
    fold_scores = result["fold_scores"]

    overall_accuracy = accuracy_score(actual, predicted)

    overall_f1 = f1_score(
        actual,
        predicted,
        average="macro",
        zero_division=0
    )

    mean_fold_f1 = sum(fold_scores) / len(fold_scores)

    matrix = confusion_matrix(
        actual,
        predicted,
        labels=CLASS_LABELS
    )

    class_report = classification_report(
        actual,
        predicted,
        labels=CLASS_LABELS,
        target_names=[
            "Other disease (non)",
            "Flavescence doree (oui)",
            "Healthy (sain)"
        ],
        zero_division=0
    )

    print(f"\nModel: {model_name}")
    print(f"Mean fold macro F1: {mean_fold_f1:.4f}")
    print(f"Overall macro F1: {overall_f1:.4f}")
    print(f"Overall accuracy: {overall_accuracy:.4f}")

    print("\nConfusion matrix:")
    print(matrix)

    print("\nClass-wise performance:")
    print(class_report)

    report_lines.append(f"\nModel: {model_name}\n")
    report_lines.append(f"Fold F1 scores: {fold_scores}\n")
    report_lines.append(f"Mean fold macro F1: {mean_fold_f1:.4f}\n")
    report_lines.append(f"Overall macro F1: {overall_f1:.4f}\n")
    report_lines.append(f"Overall accuracy: {overall_accuracy:.4f}\n")
    report_lines.append(f"Confusion matrix:\n{matrix}\n")
    report_lines.append(f"Class-wise performance:\n{class_report}\n")


REPORT_DIR.mkdir(parents=True, exist_ok=True)

with REPORT_FILE.open("w", encoding="utf-8") as file:
    file.write("TERRASPECTRA - PLOT-BASED VALIDATION\n")
    file.write("Leave-One-Plot-Out Cross-Validation\n")
    file.writelines(report_lines)

print(f"\nReport saved to: {REPORT_FILE}")
print("\nPlot-based validation completed successfully.")
