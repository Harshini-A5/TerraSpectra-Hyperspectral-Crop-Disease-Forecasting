
import csv
from collections import Counter, defaultdict

file_path = (
    "data/raw/Grapevibe/extracted/"
    "b33r2dzng8-1/tab_all_expended_element.csv"
)

metadata_values = defaultdict(set)
sample_labels = defaultdict(set)
rows_per_sample = Counter()
class_counts = Counter()

metadata_columns = [
    "parcelle",
    "cepage",
    "chL",
    "flav",
    "nbi"
]

with open(file_path, "r", encoding="cp1252", newline="") as file:
    reader = csv.DictReader(file)

    for row in reader:
        label = row["flavescenceDor"].strip()
        sample = row["Var2"].strip()

        class_counts[label] += 1
        sample_labels[label].add(sample)
        rows_per_sample[sample] += 1

        for column in metadata_columns:
            metadata_values[column].add(row[column].strip())

print("Unique Var2 samples per disease class:")
for label, samples in sample_labels.items():
    print(label, ":", len(samples))

print("\nMetadata category counts:")
for column, values in metadata_values.items():
    print(column, ":", len(values))

print("\nRows per Var2 sample:")
print("Minimum:", min(rows_per_sample.values()))
print("Maximum:", max(rows_per_sample.values()))
