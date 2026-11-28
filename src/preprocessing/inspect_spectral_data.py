
import csv
import math
from collections import Counter
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATASET_PATH = (
    PROJECT_ROOT
    / "data"
    / "raw"
    / "Grapevibe"
    / "extracted"
    / "b33r2dzng8-1"
    / "tab_all_expended_element.csv"
)


def inspect_spectral_data(file_path):

    missing_counts = Counter()
    invalid_counts = Counter()

    minimum_values = {}
    maximum_values = {}
    spectral_value_counts = Counter()

    total_records = 0
    total_spectral_values = 0
    finite_values = 0
    infinite_values = 0

    print("Starting spectral data quality inspection...")
    print("Dataset:", file_path)

    with open(file_path, encoding="cp1252", newline="") as file:
        reader = csv.DictReader(file)

        if not reader.fieldnames:
            raise ValueError("Dataset has no column headers.")

        spectral_columns = reader.fieldnames[8:]

        if len(spectral_columns) != 204:
            raise ValueError(
                f"Expected 204 spectral columns, found {len(spectral_columns)}."
            )

        for column in spectral_columns:
            minimum_values[column] = math.inf
            maximum_values[column] = -math.inf

        for row in reader:
            total_records += 1

            for column in spectral_columns:
                value = row[column].strip()
                total_spectral_values += 1

                if value == "":
                    missing_counts[column] += 1
                    continue

                try:
                    numeric_value = float(value)
                except ValueError:
                    invalid_counts[column] += 1
                    continue

                if not math.isfinite(numeric_value):
                    infinite_values += 1
                    invalid_counts[column] += 1
                    continue

                finite_values += 1
                spectral_value_counts[column] += 1

                minimum_values[column] = min(
                    minimum_values[column], numeric_value
                )
                maximum_values[column] = max(
                    maximum_values[column], numeric_value
                )

    total_missing = sum(missing_counts.values())
    total_invalid = sum(invalid_counts.values())

    valid_ranges = [
        column for column in spectral_columns
        if spectral_value_counts[column] > 0
    ]

    print("\n========== SPECTRAL DATA QUALITY REPORT ==========")

    print("\nDataset overview:")
    print("Total records:", total_records)
    print("Spectral measurement columns:", len(spectral_columns))
    print("Total spectral values:", total_spectral_values)

    print("\nValue quality:")
    print("Finite numeric values:", finite_values)
    print("Missing values:", total_missing)
    print("Invalid values:", total_invalid)
    print("Infinite values:", infinite_values)

    print("\nOverall spectral range:")

    if valid_ranges:
        overall_min = min(
            minimum_values[column] for column in valid_ranges
        )
        overall_max = max(
            maximum_values[column] for column in valid_ranges
        )

        print("Minimum:", overall_min)
        print("Maximum:", overall_max)
    else:
        print("No valid numeric spectral values found.")

    print("\nColumns containing missing values:", len(missing_counts))
    print("Columns containing invalid values:", len(invalid_counts))

    print("\nFirst 10 spectral columns:")

    for column in spectral_columns[:10]:
        print(
            f"{column}: "
            f"min={minimum_values[column]}, "
            f"max={maximum_values[column]}, "
            f"missing={missing_counts[column]}, "
            f"invalid={invalid_counts[column]}"
        )

    print("\n==================================================")


if __name__ == "__main__":

    if not DATASET_PATH.exists():
        raise FileNotFoundError(
            f"Dataset not found: {DATASET_PATH}"
        )

    inspect_spectral_data(DATASET_PATH)
