# Walmart Sales Forecasting Dataset - Data Profiling Report

This report profiles the structure, completeness, and statistics of the raw Walmart Sales Forecasting dataset.

## 1. Dataset Overview

| Dataset File | Rows | Columns | Memory Usage (MB) |
| --- | --- | --- | --- |
| `stores.csv` | 45 | 3 | 0.00 |
| `features.csv` | 8,190 | 12 | 0.77 |
| `train.csv` | 421,570 | 5 | 17.29 |
| `test.csv` | 115,064 | 4 | 3.84 |


### Profile for `stores.csv`

#### Column Statistics

| Column Name | Data Type | Non-Null Count | Missing Count | Missing % | Unique Values |
| --- | --- | --- | --- | --- | --- |
| `Store` | int64 | 45 | 0 | 0.00% | 45 |
| `Type` | str | 45 | 0 | 0.00% | 3 |
| `Size` | int64 | 45 | 0 | 0.00% | 40 |

#### Statistical Summary

| Metric | count | unique | top | freq | mean | std | min | 25% | 50% | 75% | max |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `Store` | 45.00 | N/A | N/A | N/A | 23.00 | 13.13 | 1.00 | 12.00 | 23.00 | 34.00 | 45.00 |
| `Type` | 45 | 3 | A | 22 | N/A | N/A | N/A | N/A | N/A | N/A | N/A |
| `Size` | 45.00 | N/A | N/A | N/A | 130287.60 | 63825.27 | 34875.00 | 70713.00 | 126512.00 | 202307.00 | 219622.00 |

### Profile for `features.csv`

#### Column Statistics

| Column Name | Data Type | Non-Null Count | Missing Count | Missing % | Unique Values |
| --- | --- | --- | --- | --- | --- |
| `Store` | int64 | 8,190 | 0 | 0.00% | 45 |
| `Date` | str | 8,190 | 0 | 0.00% | 182 |
| `Temperature` | float64 | 8,190 | 0 | 0.00% | 4,178 |
| `Fuel_Price` | float64 | 8,190 | 0 | 0.00% | 1,011 |
| `MarkDown1` | float64 | 4,032 | 4,158 | 50.77% | 4,023 |
| `MarkDown2` | float64 | 2,921 | 5,269 | 64.33% | 2,715 |
| `MarkDown3` | float64 | 3,613 | 4,577 | 55.89% | 2,885 |
| `MarkDown4` | float64 | 3,464 | 4,726 | 57.70% | 3,405 |
| `MarkDown5` | float64 | 4,050 | 4,140 | 50.55% | 4,045 |
| `CPI` | float64 | 7,605 | 585 | 7.14% | 2,505 |
| `Unemployment` | float64 | 7,605 | 585 | 7.14% | 404 |
| `IsHoliday` | bool | 8,190 | 0 | 0.00% | 2 |

#### Statistical Summary

| Metric | count | unique | top | freq | mean | std | min | 25% | 50% | 75% | max |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `Store` | 8190.00 | N/A | N/A | N/A | 23.00 | 12.99 | 1.00 | 12.00 | 23.00 | 34.00 | 45.00 |
| `Date` | 8190 | 182 | 2010-02-05 | 45 | N/A | N/A | N/A | N/A | N/A | N/A | N/A |
| `Temperature` | 8190.00 | N/A | N/A | N/A | 59.36 | 18.68 | -7.29 | 45.90 | 60.71 | 73.88 | 101.95 |
| `Fuel_Price` | 8190.00 | N/A | N/A | N/A | 3.41 | 0.43 | 2.47 | 3.04 | 3.51 | 3.74 | 4.47 |
| `MarkDown1` | 4032.00 | N/A | N/A | N/A | 7032.37 | 9262.75 | -2781.45 | 1577.53 | 4743.58 | 8923.31 | 103184.98 |
| `MarkDown2` | 2921.00 | N/A | N/A | N/A | 3384.18 | 8793.58 | -265.76 | 68.88 | 364.57 | 2153.35 | 104519.54 |
| `MarkDown3` | 3613.00 | N/A | N/A | N/A | 1760.10 | 11276.46 | -179.26 | 6.60 | 36.26 | 163.15 | 149483.31 |
| `MarkDown4` | 3464.00 | N/A | N/A | N/A | 3292.94 | 6792.33 | 0.22 | 304.69 | 1176.42 | 3310.01 | 67474.85 |
| `MarkDown5` | 4050.00 | N/A | N/A | N/A | 4132.22 | 13086.69 | -185.17 | 1440.83 | 2727.14 | 4832.56 | 771448.10 |
| `CPI` | 7605.00 | N/A | N/A | N/A | 172.46 | 39.74 | 126.06 | 132.36 | 182.76 | 213.93 | 228.98 |
| `Unemployment` | 7605.00 | N/A | N/A | N/A | 7.83 | 1.88 | 3.68 | 6.63 | 7.81 | 8.57 | 14.31 |
| `IsHoliday` | 8190 | 2 | False | 7605 | N/A | N/A | N/A | N/A | N/A | N/A | N/A |

### Profile for `train.csv`

#### Column Statistics

| Column Name | Data Type | Non-Null Count | Missing Count | Missing % | Unique Values |
| --- | --- | --- | --- | --- | --- |
| `Store` | int64 | 421,570 | 0 | 0.00% | 45 |
| `Dept` | int64 | 421,570 | 0 | 0.00% | 81 |
| `Date` | str | 421,570 | 0 | 0.00% | 143 |
| `Weekly_Sales` | float64 | 421,570 | 0 | 0.00% | 359,464 |
| `IsHoliday` | bool | 421,570 | 0 | 0.00% | 2 |

#### Statistical Summary

| Metric | count | unique | top | freq | mean | std | min | 25% | 50% | 75% | max |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `Store` | 421570.00 | N/A | N/A | N/A | 22.20 | 12.79 | 1.00 | 11.00 | 22.00 | 33.00 | 45.00 |
| `Dept` | 421570.00 | N/A | N/A | N/A | 44.26 | 30.49 | 1.00 | 18.00 | 37.00 | 74.00 | 99.00 |
| `Date` | 421570 | 143 | 2011-12-23 | 3027 | N/A | N/A | N/A | N/A | N/A | N/A | N/A |
| `Weekly_Sales` | 421570.00 | N/A | N/A | N/A | 15981.26 | 22711.18 | -4988.94 | 2079.65 | 7612.03 | 20205.85 | 693099.36 |
| `IsHoliday` | 421570 | 2 | False | 391909 | N/A | N/A | N/A | N/A | N/A | N/A | N/A |

### Profile for `test.csv`

#### Column Statistics

| Column Name | Data Type | Non-Null Count | Missing Count | Missing % | Unique Values |
| --- | --- | --- | --- | --- | --- |
| `Store` | int64 | 115,064 | 0 | 0.00% | 45 |
| `Dept` | int64 | 115,064 | 0 | 0.00% | 81 |
| `Date` | str | 115,064 | 0 | 0.00% | 39 |
| `IsHoliday` | bool | 115,064 | 0 | 0.00% | 2 |

#### Statistical Summary

| Metric | count | unique | top | freq | mean | std | min | 25% | 50% | 75% | max |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `Store` | 115064.00 | N/A | N/A | N/A | 22.24 | 12.81 | 1.00 | 11.00 | 22.00 | 33.00 | 45.00 |
| `Dept` | 115064.00 | N/A | N/A | N/A | 44.34 | 30.66 | 1.00 | 18.00 | 37.00 | 74.00 | 99.00 |
| `Date` | 115064 | 39 | 2012-12-21 | 3002 | N/A | N/A | N/A | N/A | N/A | N/A | N/A |
| `IsHoliday` | 115064 | 2 | False | 106136 | N/A | N/A | N/A | N/A | N/A | N/A | N/A |

## 2. Merged Analytical Dataset Profile

Merging `train.csv` with `stores.csv` and `features.csv` based on Store, Date, and IsHoliday variables.

Merged train dataset shape: **421,570 rows** and **16 columns**.

### Numerical Correlation Matrix (Target: `Weekly_Sales`)

| Variable | Store | Dept | Weekly_Sales | Size | Temperature | Fuel_Price | CPI | Unemployment |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `Store` | 1.0000 | 0.0240 | -0.0852 | -0.1829 | -0.0501 | 0.0653 | -0.2111 | 0.2086 |
| `Dept` | 0.0240 | 1.0000 | 0.1480 | -0.0030 | 0.0044 | 0.0036 | -0.0075 | 0.0078 |
| `Weekly_Sales` | -0.0852 | 0.1480 | 1.0000 | 0.2438 | -0.0023 | -0.0001 | -0.0209 | -0.0259 |
| `Size` | -0.1829 | -0.0030 | 0.2438 | 1.0000 | -0.0583 | 0.0034 | -0.0033 | -0.0682 |
| `Temperature` | -0.0501 | 0.0044 | -0.0023 | -0.0583 | 1.0000 | 0.1439 | 0.1821 | 0.0967 |
| `Fuel_Price` | 0.0653 | 0.0036 | -0.0001 | 0.0034 | 0.1439 | 1.0000 | -0.1642 | -0.0339 |
| `CPI` | -0.2111 | -0.0075 | -0.0209 | -0.0033 | 0.1821 | -0.1642 | 1.0000 | -0.3000 |
| `Unemployment` | 0.2086 | 0.0078 | -0.0259 | -0.0682 | 0.0967 | -0.0339 | -0.3000 | 1.0000 |

### Key Findings & Insights

- **Store Size**: Store size has the highest positive correlation with weekly sales (**0.2438**), meaning larger stores bring in substantially more revenue.

- **CPI & Unemployment**: CPI (**-0.0209**) and Unemployment (**-0.0259**) show weak negative correlations with sales, suggesting overall consumer demand is somewhat resilient to minor economic fluctuations in this dataset.

- **Temperature & Fuel Price**: Fuel prices (**-0.0001**) and Temperature (**-0.0023**) show minimal linear correlation with weekly sales directly, but might present seasonal dynamics.
