
import csv
from collections import defaultdict
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]

INPUT_FILE = (
    PROJECT_ROOT
    / "data"
    / "raw"
    / "Grapevibe"
    / "extracted"
    / "b33r2dzng8-1"
    / "tab_all_expended_element.csv"
)

OUTPUT_DIR = PROJECT_ROOT / "data" / "processed"
OUTPUT_FILE = OUTPUT_DIR / "grapevine_model_dataset.csv"

SPECTRAL_COLUMNS = [f"Var{i}" for i in range(9, 213)]


print("Starting model dataset preparation...")

sample_sums = {}
sample_counts = defaultdict(int)
sample_metadata = {}

with INPUT_FILE.open("r", encoding="cp1252", newline="") as file:
    reader = csv.DictReader(file)

    for row in reader:
        sample_id = row["Var2"]

        if sample_id not in sample_sums:
            sample_sums[sample_id] = [0.0] * len(SPECTRAL_COLUMNS)

            sample_metadata[sample_id] = {
                "sample_id": sample_id,
                "disease_label": row["flavescenceDor"],
                "variety": row["cepage"],
                "plot": row["parcelle"],
            }

        sample_counts[sample_id] += 1

        for index, column in enumerate(SPECTRAL_COLUMNS):
            sample_sums[sample_id][index] += float(row[column])


print("Calculating sample-level mean reflectance...")

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

output_columns = [
    "sample_id",
    "disease_label",
    "variety",
    "plot",
] + SPECTRAL_COLUMNS

with OUTPUT_FILE.open(
    "w", encoding="utf-8", newline=""
) as file:
    writer = csv.DictWriter(file, fieldnames=output_columns)
    writer.writeheader()

    for sample_id, sums in sample_sums.items():
        pixel_count = sample_counts[sample_id]

        output_row = sample_metadata[sample_id].copy()

        for index, column in enumerate(SPECTRAL_COLUMNS):
            output_row[column] = sums[index] / pixel_count

        writer.writerow(output_row)


print("\n========== MODEL DATASET REPORT ==========")
print(f"Total samples: {len(sample_sums)}")
print(f"Spectral features per sample: {len(SPECTRAL_COLUMNS)}")
print(f"Total columns: {len(output_columns)}")
print(f"Output file: {OUTPUT_FILE}")
print("\nModel dataset preparation completed successfully.")

