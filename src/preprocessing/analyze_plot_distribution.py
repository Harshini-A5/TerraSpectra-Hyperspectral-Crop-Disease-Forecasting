
import csv
from collections import defaultdict
from pathlib import Path


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

plot_samples = defaultdict(dict)

print("Analyzing disease distribution across grapevine plots...")

with DATA_FILE.open("r", encoding="cp1252", newline="") as file:
    reader = csv.DictReader(file)

    for row in reader:
        sample_id = row["Var2"]
        plot = row["parcelle"]
        label = row["flavescenceDor"]

        # Count each sample only once.
        plot_samples[plot][sample_id] = label


print("\n========== PLOT DISTRIBUTION REPORT ==========")

all_labels = sorted({
    label
    for samples in plot_samples.values()
    for label in samples.values()
})

print(f"\nTotal plots: {len(plot_samples)}")

header = f"{'Plot':<15}" + "".join(
    f"{label:>12}" for label in all_labels
) + f"{'Total':>10}"

print(header)
print("-" * len(header))

for plot in sorted(plot_samples):
    counts = defaultdict(int)

    for label in plot_samples[plot].values():
        counts[label] += 1

    total = sum(counts.values())

    line = f"{plot:<15}"
    for label in all_labels:
        line += f"{counts[label]:>12}"

    line += f"{total:>10}"
    print(line)


print("\nDisease class coverage by plot:")

for label in all_labels:
    covered_plots = [
        plot
        for plot, samples in plot_samples.items()
        if label in samples.values()
    ]

    print(
        f"{label}: present in "
        f"{len(covered_plots)} of {len(plot_samples)} plots"
    )

total_samples = sum(
    len(samples) for samples in plot_samples.values()
)

print(f"\nTotal unique samples: {total_samples}")
print("\nPlot distribution analysis completed.")
