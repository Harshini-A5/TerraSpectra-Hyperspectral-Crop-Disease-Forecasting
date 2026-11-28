
import csv
from collections import Counter, defaultdict
from pathlib import Path


# Project root directory
PROJECT_ROOT = Path(__file__).resolve().parents[2]

# Dataset location
DATASET_PATH = (
    PROJECT_ROOT
    / "data"
    / "raw"
    / "Grapevibe"
    / "extracted"
    / "b33r2dzng8-1"
    / "tab_all_expended_element.csv"
)

# Required metadata columns
REQUIRED_COLUMNS = [
    "Var1",
    "Var2",
    "flavescenceDor",
    "parcelle",
    "cepage",
]


def validate_dataset(file_path):

    sample_info = defaultdict(
        lambda: {
            "labels": set(),
            "varieties": set(),
            "plots": set(),
            "images": set(),
            "records": 0,
        }
    )

    image_samples = defaultdict(set)
    label_records = Counter()
    total_records = 0

    print("Starting dataset validation...")
    print("Dataset:", file_path)

    with open(file_path, encoding="cp1252", newline="") as file:
        reader = csv.DictReader(file)

        columns = reader.fieldnames

        if not columns:
            raise ValueError("CSV file has no header.")

        missing = [
            column for column in REQUIRED_COLUMNS
            if column not in columns
        ]

        if missing:
            raise ValueError(f"Missing required columns: {missing}")

        measurement_columns = columns[8:]

        for row in reader:
            total_records += 1

            sample = row["Var2"]
            image = row["Var1"]
            label = row["flavescenceDor"]
            variety = row["cepage"]
            plot = row["parcelle"]

            info = sample_info[sample]

            info["labels"].add(label)
            info["varieties"].add(variety)
            info["plots"].add(plot)
            info["images"].add(image)
            info["records"] += 1

            image_samples[image].add(sample)
            label_records[label] += 1

    samples = list(sample_info.values())

    sample_labels = Counter(
        next(iter(info["labels"]))
        for info in samples
        if len(info["labels"]) == 1
    )

    inconsistent_samples = [
        sample
        for sample, info in sample_info.items()
        if (
            len(info["labels"]) > 1
            or len(info["varieties"]) > 1
            or len(info["plots"]) > 1
        )
    ]

    multiple_image_samples = {
        sample: sorted(info["images"])
        for sample, info in sample_info.items()
        if len(info["images"]) > 1
    }

    multiple_sample_images = {
        image: sorted(sample_ids)
        for image, sample_ids in image_samples.items()
        if len(sample_ids) > 1
    }

    record_counts = [
        info["records"] for info in samples
    ]

    print("\n========== DATASET VALIDATION REPORT ==========")

    print("\nDataset overview:")
    print("Total records:", total_records)
    print("Total columns:", len(columns))
    print("Measurement columns:", len(measurement_columns))
    print("Unique samples:", len(sample_info))
    print("Unique image IDs:", len(image_samples))

    print("\nPixel-level label distribution:")
    for label, count in sorted(label_records.items()):
        print(f"{label}: {count}")

    print("\nSample-level label distribution:")
    for label, count in sorted(sample_labels.items()):
        print(f"{label}: {count}")

    print("\nRecords per sample:")
    print("Minimum:", min(record_counts))
    print("Maximum:", max(record_counts))
    print(
        "Average:",
        round(sum(record_counts) / len(record_counts), 2)
    )

    print("\nMetadata validation:")
    print("Inconsistent samples:", len(inconsistent_samples))
    print("Samples with multiple images:", len(multiple_image_samples))
    print("Images linked to multiple samples:", len(multiple_sample_images))

    if multiple_image_samples:
        print("\nSamples with multiple images:")
        for sample, images in sorted(multiple_image_samples.items()):
            print(sample, "->", images)

    if inconsistent_samples:
        print("\nInconsistent sample IDs:")
        print(inconsistent_samples)

    print("\n===============================================")


if __name__ == "__main__":

    if not DATASET_PATH.exists():
        raise FileNotFoundError(
            f"Dataset not found: {DATASET_PATH}"
        )

    validate_dataset(DATASET_PATH)
