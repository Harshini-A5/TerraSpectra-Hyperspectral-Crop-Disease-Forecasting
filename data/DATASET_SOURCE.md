# TerraSpectra – Dataset Source and Inspection

## 1. Dataset Information

- **Dataset Name:** Grapevine Hyperspectral Spectral Dataset
- **Contributor:** Maxime Ryckewaert
- **Published:** 31 March 2022
- **Version:** 1
- **DOI:** 10.17632/b33r2dzng8.1
- **Source:** Mendeley Data
- **Project:** VINIoT
- **Licence:** CC BY 4.0

## 2. Official Dataset Description

The dataset contains spectra obtained from hyperspectral images of grapevine leaves. It includes healthy leaves and leaves showing symptoms associated with diseases, dehydration, stress, and other conditions.

## 3. Local Dataset Details

- **File:** `tab_all_expended_element.csv`
- **File Size:** Approximately 1.5 GB
- **Total Columns:** 212
- **Metadata Columns:** 8
- **Measurement Columns:** 204
- **Total Records:** 425,847

## 4. Identified Columns

The first eight columns are:

- Var1
- Var2
- flavescenceDor
- parcelle
- cepage
- chL
- flav
- nbi

The remaining 204 columns contain numerical measurements that appear to represent spectral reflectance values.

## 5. Observed Label Distribution

| Label | Records |
|---|---:|
| oui | 152,938 |
| sain | 119,993 |
| non | 152,916 |
| **Total** | **425,847** |

The exact meaning of each label requires further confirmation from the dataset documentation.

## 6. Grape Varieties

Seven grape varieties were identified:

- Gamay
- Fer
- Duras
- Colombard
- Loin de l'œil
- Mauzac
- Chardonnay

## 7. Initial Inspection

- The CSV file was successfully extracted.
- The file was inspected using Python's built-in CSV library.
- The first records contained numeric measurement values.
- Disease-related labels and grape varieties were inspected.
- The full dataset has not yet been preprocessed or used for model training.

## 8. Dataset Usage Plan

The dataset will be evaluated for grapevine leaf condition classification using hyperspectral measurements. Further investigation is required to confirm label definitions, sample structure, and suitable validation strategies before model development.

**Dataset source:** https://data.mendeley.com/datasets/b33r2dzng8/1

**DOI:** https://doi.org/10.17632/b33r2dzng8.1