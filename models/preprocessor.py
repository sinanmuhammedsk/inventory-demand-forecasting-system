import os
import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder

class WalmartPreprocessor:
    def __init__(self, raw_dir=r"d:\forecast\dataset\raw", processed_dir=r"d:\forecast\dataset\processed"):
        self.raw_dir = raw_dir
        self.processed_dir = processed_dir
        self.label_encoders = {}
        
    def load_raw_data(self):
        """Loads train, stores, and features raw csv files."""
        print("Loading raw CSV files...")
        stores = pd.read_csv(os.path.join(self.raw_dir, "stores.csv"))
        features = pd.read_csv(os.path.join(self.raw_dir, "features.csv"))
        train = pd.read_csv(os.path.join(self.raw_dir, "train.csv"))
        test = pd.read_csv(os.path.join(self.raw_dir, "test.csv"))
        return train, stores, features, test

    def merge_datasets(self, main_df, stores_df, features_df):
        """Merges main sales dataframe with stores and features."""
        print("Merging datasets...")
        # Ensure correct types for merging
        main_df['Date'] = pd.to_datetime(main_df['Date'])
        features_df['Date'] = pd.to_datetime(features_df['Date'])
        
        # Merge store details
        df = pd.merge(main_df, stores_df, on='Store', how='left')
        # Merge features (on Store, Date, and IsHoliday if exists in main_df, else on Store, Date)
        if 'IsHoliday' in df.columns:
            df = pd.merge(df, features_df, on=['Store', 'Date', 'IsHoliday'], how='left')
        else:
            df = pd.merge(df, features_df, on=['Store', 'Date'], how='left')
            
        return df

    def handle_missing_values(self, df):
        """Implements missing value handling strategy."""
        print("Handling missing values...")
        df = df.copy()
        
        # MarkDown columns: NaNs indicate no markdown was active, fill with 0
        markdown_cols = [f'MarkDown{i}' for i in range(1, 6)]
        for col in markdown_cols:
            if col in df.columns:
                df[col] = df[col].fillna(0.0)
                
        # CPI and Unemployment: Forward fill within each Store, then fill remaining with median
        if 'CPI' in df.columns:
            df['CPI'] = df.groupby('Store')['CPI'].transform(lambda x: x.ffill().bfill())
            df['CPI'] = df['CPI'].fillna(df['CPI'].median())
            
        if 'Unemployment' in df.columns:
            df['Unemployment'] = df.groupby('Store')['Unemployment'].transform(lambda x: x.ffill().bfill())
            df['Unemployment'] = df['Unemployment'].fillna(df['Unemployment'].median())
            
        return df

    def treat_outliers(self, df):
        """Detects and handles extreme outliers using IQR method for Weekly_Sales."""
        print("Treating outliers...")
        df = df.copy()
        if 'Weekly_Sales' in df.columns:
            # We clip negative sales to 0 (returns or errors should be non-negative for forecasting demand)
            df['Weekly_Sales'] = df['Weekly_Sales'].clip(lower=0)
            
            # For machine learning, we clip extremely high sales (e.g. above 99.9th percentile per Department)
            # but keep the original sales column for historical reports
            df['Weekly_Sales_Cleaned'] = df.groupby('Dept')['Weekly_Sales'].transform(
                lambda x: x.clip(upper=x.quantile(0.999))
            )
        return df

    def engineer_features(self, df):
        """Generates temporal, seasonal, and business-relevant features."""
        print("Engineering features...")
        df = df.copy()
        
        # Ensure Date is datetime type
        df['Date'] = pd.to_datetime(df['Date'])
        
        # 1. Temporal features
        df['Day'] = df['Date'].dt.day
        df['Week'] = df['Date'].dt.isocalendar().week.astype(int)
        df['Month'] = df['Date'].dt.month
        df['Quarter'] = df['Date'].dt.quarter
        df['Year'] = df['Date'].dt.year
        
        # 2. Specific Holiday Indicators (Walmart Sales dataset holiday dates)
        # Super Bowl: 12-Feb-10, 11-Feb-11, 10-Feb-12, 8-Feb-13
        # Labor Day: 10-Sep-10, 9-Sep-11, 7-Sep-12, 6-Sep-13
        # Thanksgiving: 26-Nov-10, 25-Nov-11, 23-Nov-12, 29-Nov-13
        # Christmas: 31-Dec-10, 30-Dec-11, 28-Dec-12, 27-Dec-13
        
        df['Is_SuperBowl'] = df['Date'].isin(['2010-02-12', '2011-02-11', '2012-02-10', '2013-02-08']).astype(int)
        df['Is_LaborDay'] = df['Date'].isin(['2010-09-10', '2011-09-09', '2012-09-07', '2013-09-06']).astype(int)
        df['Is_Thanksgiving'] = df['Date'].isin(['2010-11-26', '2011-11-25', '2012-11-23', '2013-11-29']).astype(int)
        df['Is_Christmas'] = df['Date'].isin(['2010-12-31', '2011-12-30', '2012-12-28', '2013-12-27']).astype(int)
        
        # General IsHoliday
        if 'IsHoliday' in df.columns:
            df['IsHoliday'] = df['IsHoliday'].astype(int)
            
        # 3. Seasonal indicator
        # Define seasons based on months
        # Winter: 12, 1, 2; Spring: 3, 4, 5; Summer: 6, 7, 8; Fall: 9, 10, 11
        df['Season'] = df['Month'].map({
            12: 'Winter', 1: 'Winter', 2: 'Winter',
            3: 'Spring', 4: 'Spring', 5: 'Spring',
            6: 'Summer', 7: 'Summer', 8: 'Summer',
            9: 'Fall', 10: 'Fall', 11: 'Fall'
        })
        
        # 4. Encoding categorical columns
        # Store Type (A, B, C)
        le_type = LabelEncoder()
        df['Type_Encoded'] = le_type.fit_transform(df['Type'].astype(str))
        self.label_encoders['Type'] = le_type
        
        # Season Type
        le_season = LabelEncoder()
        df['Season_Encoded'] = le_season.fit_transform(df['Season'].astype(str))
        self.label_encoders['Season'] = le_season
        
        # 5. Economic & size interaction terms
        df['Size_Unemployment_Ratio'] = df['Size'] / (df['Unemployment'] + 0.1)
        df['Size_CPI_Ratio'] = df['Size'] / (df['CPI'] + 0.1)
        
        return df

    def run_pipeline(self):
        """Executes full loading, cleaning, engineering, and saving pipeline."""
        print("Starting preprocessing and feature engineering pipeline...")
        train, stores, features, test = self.load_raw_data()
        
        # Process training data
        train_processed = self.merge_datasets(train, stores, features)
        train_processed = self.handle_missing_values(train_processed)
        train_processed = self.treat_outliers(train_processed)
        train_processed = self.engineer_features(train_processed)
        
        # Process test data (for forecasting evaluation if needed, though models are trained on train)
        test_processed = self.merge_datasets(test, stores, features)
        test_processed = self.handle_missing_values(test_processed)
        # Test doesn't have Weekly_Sales, so we just engineer features
        test_processed = self.engineer_features(test_processed)
        
        # Remove duplicate rows if any
        train_processed = train_processed.drop_duplicates()
        test_processed = test_processed.drop_duplicates()
        
        # Save processed datasets
        os.makedirs(self.processed_dir, exist_ok=True)
        
        train_path = os.path.join(self.processed_dir, "analytical_dataset.csv")
        test_path = os.path.join(self.processed_dir, "test_dataset_processed.csv")
        
        train_processed.to_csv(train_path, index=False)
        test_processed.to_csv(test_path, index=False)
        
        print(f"Analytical training dataset saved to: {train_path} (Shape: {train_processed.shape})")
        print(f"Analytical test dataset saved to: {test_path} (Shape: {test_processed.shape})")
        
        return train_processed, test_processed

if __name__ == "__main__":
    preprocessor = WalmartPreprocessor()
    preprocessor.run_pipeline()
