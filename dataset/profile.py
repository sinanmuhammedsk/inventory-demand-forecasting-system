import os
import pandas as pd
import numpy as np

# Paths
DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "raw")
REPORT_PATH = r"d:\forecast\reports\data_profiling_report.md"

def profile_dataset():
    print("Starting data profiling...")
    
    # Load files
    stores = pd.read_csv(os.path.join(DATA_DIR, "stores.csv"))
    features = pd.read_csv(os.path.join(DATA_DIR, "features.csv"))
    train = pd.read_csv(os.path.join(DATA_DIR, "train.csv"))
    test = pd.read_csv(os.path.join(DATA_DIR, "test.csv"))
    
    # Profile containers
    report_content = []
    
    report_content.append("# Walmart Sales Forecasting Dataset - Data Profiling Report\n")
    report_content.append("This report profiles the structure, completeness, and statistics of the raw Walmart Sales Forecasting dataset.\n")
    
    # 1. Dataset Overview Table
    report_content.append("## 1. Dataset Overview\n")
    overview_table = (
        "| Dataset File | Rows | Columns | Memory Usage (MB) |\n"
        "| --- | --- | --- | --- |\n"
        f"| `stores.csv` | {len(stores):,} | {len(stores.columns)} | {stores.memory_usage(deep=True).sum() / (1024**2):.2f} |\n"
        f"| `features.csv` | {len(features):,} | {len(features.columns)} | {features.memory_usage(deep=True).sum() / (1024**2):.2f} |\n"
        f"| `train.csv` | {len(train):,} | {len(train.columns)} | {train.memory_usage(deep=True).sum() / (1024**2):.2f} |\n"
        f"| `test.csv` | {len(test):,} | {len(test.columns)} | {test.memory_usage(deep=True).sum() / (1024**2):.2f} |\n"
    )
    report_content.append(overview_table + "\n")
    
    # 2. File-by-File Profiling
    files_to_profile = [
        ("stores.csv", stores),
        ("features.csv", features),
        ("train.csv", train),
        ("test.csv", test)
    ]
    
    for filename, df in files_to_profile:
        report_content.append(f"### Profile for `{filename}`\n")
        
        # Column list table
        report_content.append("#### Column Statistics\n")
        col_table = ["| Column Name | Data Type | Non-Null Count | Missing Count | Missing % | Unique Values |"]
        col_table.append("| --- | --- | --- | --- | --- | --- |")
        
        for col in df.columns:
            dtype = str(df[col].dtype)
            non_null = df[col].count()
            missing = len(df) - non_null
            missing_pct = (missing / len(df)) * 100
            unique_vals = df[col].nunique()
            col_table.append(f"| `{col}` | {dtype} | {non_null:,} | {missing:,} | {missing_pct:.2f}% | {unique_vals:,} |")
        
        report_content.append("\n".join(col_table) + "\n")
        
        # Describe table
        report_content.append("#### Statistical Summary\n")
        desc = df.describe(include='all').transpose()
        desc_table = ["| Metric | " + " | ".join(desc.columns.tolist()) + " |"]
        desc_table.append("| --- | " + " | ".join(["---"] * len(desc.columns)) + " |")
        
        for idx, row in desc.iterrows():
            vals = []
            for col_val in row:
                if pd.isna(col_val):
                    vals.append("N/A")
                elif isinstance(col_val, float):
                    vals.append(f"{col_val:.2f}")
                else:
                    vals.append(str(col_val))
            desc_table.append(f"| `{idx}` | " + " | ".join(vals) + " |")
            
        report_content.append("\n".join(desc_table) + "\n")
    
    # 3. Merged Analytical Dataset Profiling & Correlations
    report_content.append("## 2. Merged Analytical Dataset Profile\n")
    report_content.append("Merging `train.csv` with `stores.csv` and `features.csv` based on Store, Date, and IsHoliday variables.\n")
    
    # Pre-merge transformations
    train['Date'] = pd.to_datetime(train['Date'])
    features['Date'] = pd.to_datetime(features['Date'])
    
    # Drop IsHoliday from features to avoid duplicate columns and merge conflicts, or merge on both
    merged = pd.merge(train, stores, on='Store', how='left')
    merged = pd.merge(merged, features, on=['Store', 'Date', 'IsHoliday'], how='left')
    
    report_content.append(f"Merged train dataset shape: **{merged.shape[0]:,} rows** and **{merged.shape[1]:,} columns**.\n")
    
    # Correlation Analysis
    report_content.append("### Numerical Correlation Matrix (Target: `Weekly_Sales`)\n")
    num_cols = merged.select_dtypes(include=[np.number]).columns.tolist()
    # Remove markdown columns if they are mostly null
    num_cols = [c for c in num_cols if not c.startswith('MarkDown')]
    
    corr = merged[num_cols].corr()
    corr_table = ["| Variable | " + " | ".join(corr.columns.tolist()) + " |"]
    corr_table.append("| --- | " + " | ".join(["---"] * len(corr.columns)) + " |")
    
    for idx, row in corr.iterrows():
        vals = []
        for val in row:
            if pd.isna(val):
                vals.append("N/A")
            else:
                vals.append(f"{val:.4f}")
        corr_table.append(f"| `{idx}` | " + " | ".join(vals) + " |")
        
    report_content.append("\n".join(corr_table) + "\n")
    
    # Correlation insights
    report_content.append("### Key Findings & Insights\n")
    sales_corr = corr['Weekly_Sales'].sort_values(ascending=False)
    report_content.append(f"- **Store Size**: Store size has the highest positive correlation with weekly sales (**{sales_corr.get('Size', 0):.4f}**), meaning larger stores bring in substantially more revenue.\n")
    report_content.append(f"- **CPI & Unemployment**: CPI (**{sales_corr.get('CPI', 0):.4f}**) and Unemployment (**{sales_corr.get('Unemployment', 0):.4f}**) show weak negative correlations with sales, suggesting overall consumer demand is somewhat resilient to minor economic fluctuations in this dataset.\n")
    report_content.append(f"- **Temperature & Fuel Price**: Fuel prices (**{sales_corr.get('Fuel_Price', 0):.4f}**) and Temperature (**{sales_corr.get('Temperature', 0):.4f}**) show minimal linear correlation with weekly sales directly, but might present seasonal dynamics.\n")
    
    # Save report
    os.makedirs(os.path.dirname(REPORT_PATH), exist_ok=True)
    with open(REPORT_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(report_content))
    
    print(f"Data profiling report successfully saved to: {REPORT_PATH}")

if __name__ == "__main__":
    profile_dataset()
