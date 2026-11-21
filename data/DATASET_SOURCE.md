
# TerraSpectra Dataset Selection

## Project
TerraSpectra: Hyperspectral Crop Disease Forecasting

## Selected Dataset
Grapevine Hyperspectral Dataset

## Dataset Source
Mendeley Data

https://data.mendeley.com/datasets/b33r2dzng8/1

Dataset ID: b33r2dzng8

## Dataset Details

- Crop: Grapevine
- Disease: Flavescence dorée and other diseases
- Total observations: 425,847
- Total columns: 212
- Spectral bands: 204
- Unique leaf samples: 204
- Grape varieties: 7
- Collection locations/plots: 5
- Disease categories: 3
- File format: CSV
- Original archive size: Approximately 672 MB
- Extracted CSV size: Approximately 1.5 GB

## Disease Categories

| Label | Meaning | Number of Leaves |
|---|---|---:|
| oui | Flavescence dorée | 80 |
| non | Other diseased leaves | 80 |
| sain | Healthy leaves | 44 |

## Data Quality Inspection

- Total observations inspected: 425,847
- Spectral columns: 204
- Total spectral values checked: 86,872,788
- Missing or invalid spectral values: 0
- Minimum spectral value: -0.005596
- Maximum spectral value: 1.358567
- Unique leaf IDs: 204
- Leaves with consistent labels: 204
- Minimum observations per leaf: 48
- Maximum observations per leaf: 5,183

## Reason for Selection

This dataset contains genuine grapevine hyperspectral observations with multiple disease categories, seven grape varieties, and different collection locations.

It provides a suitable foundation for developing and evaluating a machine learning model for grape disease classification using spectral measurements.

## Dataset Status

- Dataset researched: Yes
- Dataset selected: Yes
- Dataset downloaded: Yes
- Dataset extracted: Yes
- Dataset structure inspected: Yes
- Disease labels inspected: Yes
- Data quality checked: Yes
- Preprocessing: Pending
- Exploratory data analysis: Pending
- Model development: Pending

## Important Modelling Considerations

- Split the dataset by leaf ID to prevent data leakage.
- Preserve the original spectral measurements during initial preprocessing.
- Investigate the meaning of all metadata columns.
- Evaluate the three disease categories separately.
- Consider both pixel-level and leaf-level model evaluation.

## Next Actions

1. Investigate spectral and metadata columns.
2. Perform exploratory data analysis.
3. Develop a preprocessing pipeline.
4. Prepare training and testing datasets using leaf-level splitting.
5. Train and evaluate suitable machine learning models.
