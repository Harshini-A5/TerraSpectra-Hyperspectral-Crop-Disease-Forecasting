
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]

REPORT_DIR = PROJECT_ROOT / "reports"
REPORT_FILE = REPORT_DIR / "pca_analysis.txt"

fold_results = [
    ("Couffouleux", 4, 0.9532),
    ("DEVT", 4, 0.9598),
    ("LISLE SUR TARN", 5, 0.9737),
    ("Rabastens", 4, 0.9519),
    ("Terral", 4, 0.9503),
]

original_features = 204

average_components = (
    sum(result[1] for result in fold_results)
    / len(fold_results)
)

average_variance = (
    sum(result[2] for result in fold_results)
    / len(fold_results)
)

lines = [
    "TERRASPECTRA - PCA ANALYSIS REPORT",
    "=" * 45,
    "",
    f"Original spectral features: {original_features}",
    "PCA variance retention target: 95%",
    "",
    "FOLD-WISE PCA RESULTS",
    "-" * 45,
]

for plot, components, variance in fold_results:
    reduction = (
        (1 - components / original_features) * 100
    )

    lines.append(
        f"{plot}: {components} components, "
        f"{variance * 100:.2f}% variance explained, "
        f"{reduction:.2f}% feature reduction"
    )

lines.extend([
    "",
    f"Average components retained: {average_components:.2f}",
    f"Average variance explained: {average_variance * 100:.2f}%",
    "",
    "CONCLUSION",
    "-" * 45,
    "PCA reduced 204 spectral features to 4 or 5 components.",
    "At least 95% of training-data variance was retained",
    "in every validation fold.",
    "PCA Logistic Regression achieved an overall macro F1",
    "of 0.6981 and accuracy of 69.12%.",
    "",
    "These results are preliminary because the dataset",
    "contains only 204 samples from five vineyard plots.",
])

REPORT_DIR.mkdir(parents=True, exist_ok=True)

with REPORT_FILE.open("w", encoding="utf-8") as file:
    file.write("\n".join(lines))

print("\n".join(lines))
print(f"\nReport saved to: {REPORT_FILE}")
