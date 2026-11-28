
import csv
from collections import Counter, defaultdict
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]

DATASET_PATH = (
    PROJECT_ROOT
    / "data"
    / "raw"
    / "Grapevibe"
    / "extracted"
    / "b33r2dzng8-1"
    / "tab_all_expended_element.csv"
)

METADATA_COLUMNS = [
    "parcelle",
    "cepage",
    "chL",
    "flav",
    "nbi",
]


def analyze_labels(file_path):

    metadata_values = defaultdict(set)
    sample_info = defaultdict(
        lambda: {
            "labels": set(),
            "varieties": set(),
            "records": 0,
        }
    )

    rows_per_sample = Counter()
    pixel_label_counts = Counter()

    print("Starting disease label and variety analysis...")

    with open(file_path, encoding="cp1252", newline="") as file:
        reader = csv.DictReader(file)

        for row in reader:
            sample = row["Var2"].strip()
            label = row["flavescenceDor"].strip()
            variety = row["cepage"].strip()

            pixel_label_counts[label] += 1

            sample_info[sample]["labels"].add(label)
            sample_info[sample]["varieties"].add(variety)
            sample_info[sample]["records"] += 1

            rows_per_sample[sample] += 1

            for column in METADATA_COLUMNS:
                metadata_values[column].add(row[column].strip())

    # Count each sample only once
    sample_label_counts = Counter()
    variety_label_counts = Counter()

    inconsistent_samples = []

    for sample, info in sample_info.items():

        if (
            len(info["labels"]) != 1
            or len(info["varieties"]) != 1
        ):
            inconsistent_samples.append(sample)
            continue

        label = next(iter(info["labels"]))
        variety = next(iter(info["varieties"]))

        sample_label_counts[label] += 1
        variety_label_counts[(variety, label)] += 1

    labels = sorted(sample_label_counts.keys())
    varieties = sorted(metadata_values["cepage"])

    print("\n========== LABEL ANALYSIS REPORT ==========")

    print("\nSample-level disease distribution:")

    for label in labels:
        print(f"{label}: {sample_label_counts[label]}")

    print("\nDisease distribution across grape varieties:")
    print("Variety".ljust(20), end="")

    for label in labels:
        print(label.rjust(12), end="")

    print()

    for variety in varieties:
        print(variety.ljust(20), end="")

        for label in labels:
            count = variety_label_counts[(variety, label)]
            print(str(count).rjust(12), end="")

        print()

    print("\nMetadata diversity:")

    for column, values in metadata_values.items():
        print(f"{column}: {len(values)} unique values")

    print("\nSample record statistics:")
    print("Total samples:", len(sample_info))
    print("Minimum records:", min(rows_per_sample.values()))
    print("Maximum records:", max(rows_per_sample.values()))
    print(
        "Average records:",
        round(
            sum(rows_per_sample.values()) / len(rows_per_sample),
            2
        )
    )

    print("\nData consistency:")
    print("Inconsistent samples:", len(inconsistent_samples))

    if inconsistent_samples:
        print("Sample IDs:", inconsistent_samples)

    print("\n===========================================")


if __name__ == "__main__":

    if not DATASET_PATH.exists():
        raise FileNotFoundError(
            f"Dataset not found: {DATASET_PATH}"
        )

    analyze_labels(DATASET_PATH)
