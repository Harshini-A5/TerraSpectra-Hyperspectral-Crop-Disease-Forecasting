
import csv
from collections import Counter
from pathlib import Path

from sklearn.model_selection import train_test_split


PROJECT_ROOT = Path(__file__).resolve().parents[2]

INPUT_FILE = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "grapevine_model_dataset.csv"
)

OUTPUT_DIR = PROJECT_ROOT / "data" / "processed"

TRAIN_FILE = OUTPUT_DIR / "train_dataset.csv"
TEST_FILE = OUTPUT_DIR / "test_dataset.csv"

RANDOM_STATE = 42
TEST_SIZE = 0.20


print("Loading processed grapevine dataset...")

with INPUT_FILE.open("r", encoding="utf-8", newline="") as file:
    reader = csv.DictReader(file)
    columns = reader.fieldnames
    rows = list(reader)

labels = [row["disease_label"] for row in rows]

print(f"Total samples loaded: {len(rows)}")

print("\nSplitting dataset into training and testing sets...")

train_rows, test_rows = train_test_split(
    rows,
    test_size=TEST_SIZE,
    random_state=RANDOM_STATE,
    stratify=labels
)

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

for output_file, dataset in [
    (TRAIN_FILE, train_rows),
    (TEST_FILE, test_rows),
]:
    with output_file.open(
        "w", encoding="utf-8", newline=""
    ) as file:
        writer = csv.DictWriter(file, fieldnames=columns)
        writer.writeheader()
        writer.writerows(dataset)


train_ids = {row["sample_id"] for row in train_rows}
test_ids = {row["sample_id"] for row in test_rows}

train_counts = Counter(row["disease_label"] for row in train_rows)
test_counts = Counter(row["disease_label"] for row in test_rows)

print("\n========== DATA SPLIT REPORT ==========")

print(f"Total samples: {len(rows)}")
print(f"Training samples: {len(train_rows)}")
print(f"Testing samples: {len(test_rows)}")

print("\nTraining class distribution:")
for label, count in sorted(train_counts.items()):
    print(f"{label}: {count}")

print("\nTesting class distribution:")
for label, count in sorted(test_counts.items()):
    print(f"{label}: {count}")

print("\nData leakage check:")
print(f"Overlapping sample IDs: {len(train_ids & test_ids)}")

print(f"\nTraining file: {TRAIN_FILE}")
print(f"Testing file: {TEST_FILE}")

if (
    len(train_rows) + len(test_rows) == len(rows)
    and len(train_ids & test_ids) == 0
    and len(train_rows) == 163
    and len(test_rows) == 41
):
    print("\nRESULT: Train-test split completed successfully.")
else:
    print("\nRESULT: Split verification failed. Review the results.")
