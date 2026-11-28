
import csv
import math
from collections import Counter
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATA_FILE = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "grapevine_model_dataset.csv"
)

SPECTRAL_COLUMNS = [f"Var{i}" for i in range(9, 213)]

expected_columns = [
    "sample_id",
    "disease_label",
    "variety",
    "plot",
] + SPECTRAL_COLUMNS

sample_ids = set()
class_counts = Counter()
missing_values = 0
invalid_values = 0
duplicate_samples = 0
spectral_min = float("inf")
spectral_max = float("-inf")
total_spectral_values = 0


print("Starting processed dataset validation...")

with DATA_FILE.open("r", encoding="utf-8", newline="") as file:
    reader = csv.DictReader(file)

    actual_columns = reader.fieldnames

    if actual_columns != expected_columns:
        raise ValueError("Dataset column structure is incorrect.")

    for row in reader:
        sample_id = row["sample_id"]

        if sample_id in sample_ids:
            duplicate_samples += 1
        else:
            sample_ids.add(sample_id)

        if not row["disease_label"] or not row["variety"] or not row["plot"]:
            missing_values += 1

        class_counts[row["disease_label"]] += 1

        for column in SPECTRAL_COLUMNS:
            value = row[column]

            if value == "":
                missing_values += 1
                continue

            try:
                number = float(value)
            except ValueError:
                invalid_values += 1
                continue

            if not math.isfinite(number):
                invalid_values += 1
                continue

            spectral_min = min(spectral_min, number)
            spectral_max = max(spectral_max, number)
            total_spectral_values += 1


print("\n========== VALIDATION REPORT ==========")
print(f"Total samples: {len(sample_ids)}")
print(f"Total columns: {len(actual_columns)}")
print(f"Total spectral values checked: {total_spectral_values}")
print(f"Duplicate samples: {duplicate_samples}")
print(f"Missing values: {missing_values}")
print(f"Invalid or non-finite values: {invalid_values}")

print("\nDisease class distribution:")
for label, count in sorted(class_counts.items()):
    print(f"{label}: {count}")

print("\nSpectral value range:")
print(f"Minimum: {spectral_min:.8f}")
print(f"Maximum: {spectral_max:.8f}")

if (
    duplicate_samples == 0
    and missing_values == 0
    and invalid_values == 0
    and len(sample_ids) == 204
    and total_spectral_values == 204 * 204
):
    print("\nRESULT: Dataset validation PASSED.")
else:
    print("\nRESULT: Dataset validation FAILED. Review the issues above.")
