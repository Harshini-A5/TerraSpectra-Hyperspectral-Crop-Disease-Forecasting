
import csv
from collections import defaultdict
from pathlib import Path

import matplotlib.pyplot as plt


PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATA_FILE = (
    PROJECT_ROOT
    / "data"
    / "raw"
    / "Grapevibe"
    / "extracted"
    / "b33r2dzng8-1"
    / "tab_all_expended_element.csv"
)

OUTPUT_DIR = PROJECT_ROOT / "reports" / "figures"
OUTPUT_FILE = OUTPUT_DIR / "mean_spectral_signatures.png"

SPECTRAL_COLUMNS = [f"Var{i}" for i in range(9, 213)]

# Accumulate spectral values separately for each sample.
sample_sums = {}
sample_counts = {}
sample_labels = {}


print("Reading grapevine hyperspectral dataset...")

with DATA_FILE.open("r", encoding="cp1252", newline="") as file:
    reader = csv.DictReader(file)

    for row in reader:
        sample_id = row["Var2"]
        label = row["flavescenceDor"]

        if sample_id not in sample_sums:
            sample_sums[sample_id] = [0.0] * len(SPECTRAL_COLUMNS)
            sample_counts[sample_id] = 0
            sample_labels[sample_id] = label

        sample_counts[sample_id] += 1

        for index, column in enumerate(SPECTRAL_COLUMNS):
            sample_sums[sample_id][index] += float(row[column])


print("Calculating sample-level mean spectra...")

class_sums = defaultdict(lambda: [0.0] * len(SPECTRAL_COLUMNS))
class_sample_counts = defaultdict(int)

for sample_id, sums in sample_sums.items():
    label = sample_labels[sample_id]
    count = sample_counts[sample_id]

    for index, total in enumerate(sums):
        class_sums[label][index] += total / count

    class_sample_counts[label] += 1


class_means = {}

for label, sums in class_sums.items():
    number_of_samples = class_sample_counts[label]
    class_means[label] = [
        total / number_of_samples for total in sums
    ]


print("Generating spectral signature plot...")

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

plt.figure(figsize=(13, 7))

for label in sorted(class_means):
    plt.plot(
        range(1, len(SPECTRAL_COLUMNS) + 1),
        class_means[label],
        label=f"Class: {label} ({class_sample_counts[label]} samples)",
        linewidth=2
    )

plt.title("Mean Hyperspectral Signatures by Disease Class")
plt.xlabel("Spectral Band Index (Var9–Var212)")
plt.ylabel("Mean Reflectance")
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()

plt.savefig(OUTPUT_FILE, dpi=300)
plt.close()

print("\n========== SPECTRAL SIGNATURE REPORT ==========")

for label in sorted(class_sample_counts):
    print(
        f"Class {label}: "
        f"{class_sample_counts[label]} samples"
    )

print(f"\nTotal samples analysed: {len(sample_sums)}")
print(f"Plot saved to: {OUTPUT_FILE}")
print("\nSpectral signature analysis completed successfully.")
