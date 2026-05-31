import os
import joblib
import pandas as pd
import numpy as np

# Paths
MODEL_PATH = r"d:\forecast\models\best_model.joblib"
TEST_DATA_PATH = r"d:\forecast\dataset\processed\test_dataset_processed.csv"
HISTORICAL_DATA_PATH = r"d:\forecast\dataset\processed\analytical_dataset.csv"

class DemandPredictor:
    def __init__(self):
        self.model_package = None
        self.model = None
        self.feature_cols = []
        self.val_rmse = 5447.12  # Fallback standard deviation for confidence intervals
        self.load_model()
        
    def load_model(self):
        """Loads the serialized model package."""
        if os.path.exists(MODEL_PATH):
            try:
                self.model_package = joblib.load(MODEL_PATH)
                self.model = self.model_package["model"]
                self.feature_cols = self.model_package["features"]
                # Extract validation RMSE for the selected model
                metrics = self.model_package["metrics"]
                model_name = self.model_package["model_name"]
                for metric in metrics:
                    if metric["Model"] == model_name:
                        self.val_rmse = metric["Val_RMSE"]
                print(f"Loaded best model: {model_name} (Val RMSE: {self.val_rmse:.2f})")
            except Exception as e:
                print(f"Error loading model: {e}")
        else:
            print("Warning: Model file not found. Forecasting will use random forest fallback if file is created later.")

    def forecast_demand(self, store, dept, horizon_days=30):
        """Generates demand forecasts for a given store, department, and horizon (7, 30, 90 days)."""
        if self.model is None:
            self.load_model()
            if self.model is None:
                raise FileNotFoundError("Forecasting model is not trained/loaded.")
                
        # Map horizon_days to weekly steps
        if horizon_days <= 7:
            steps = 1
        elif horizon_days <= 30:
            steps = 4
        else:
            steps = 13  # 90 days is approx 13 weeks
            
        print(f"Generating forecast for Store {store}, Dept {dept} for the next {steps} weeks ({horizon_days} days)...")
        
        # Load future features (from processed test set)
        if not os.path.exists(TEST_DATA_PATH):
            raise FileNotFoundError(f"Processed test set not found at {TEST_DATA_PATH}. Run preprocessor first.")
            
        test_df = pd.read_csv(TEST_DATA_PATH)
        test_df['Date'] = pd.to_datetime(test_df['Date'])
        
        # Filter for the requested store and department
        sub_df = test_df[(test_df['Store'] == store) & (test_df['Dept'] == dept)]
        sub_df = sub_df.sort_values('Date').reset_index(drop=True)
        
        if len(sub_df) == 0:
            # Fallback: if store-dept is not in test set, create generic future dates from last historical sales
            print(f"Warning: Store {store}, Dept {dept} not found in future test set. Creating synthetic timeline.")
            # Let's read from historical data to get some base parameters
            hist_df = pd.read_csv(HISTORICAL_DATA_PATH)
            hist_sub = hist_df[(hist_df['Store'] == store) & (hist_df['Dept'] == dept)]
            
            if len(hist_sub) == 0:
                # Store-Dept doesn't exist at all, return dummy dataframe
                dates = pd.date_range(start='2012-11-02', periods=steps, freq='W-FRI')
                forecast_df = pd.DataFrame({
                    'Date': dates,
                    'Forecast': [15000.0] * steps,
                    'Lower_CI': [15000.0 - 1.96 * self.val_rmse] * steps,
                    'Upper_CI': [15000.0 + 1.96 * self.val_rmse] * steps
                })
                forecast_df['Lower_CI'] = forecast_df['Lower_CI'].clip(lower=0)
                return forecast_df
            
            # Use last available row as base and project dates
            last_row = hist_sub.sort_values('Date').iloc[-1]
            dates = pd.date_range(start=pd.to_datetime(last_row['Date']) + pd.Timedelta(weeks=1), periods=steps, freq='W-FRI')
            
            # Build feature rows
            future_rows = []
            for i, dt in enumerate(dates):
                row = last_row.copy()
                row['Date'] = dt
                row['Day'] = dt.day
                row['Week'] = dt.isocalendar()[1]
                row['Month'] = dt.month
                row['Quarter'] = (dt.month - 1) // 3 + 1
                row['Year'] = dt.year
                future_rows.append(row)
                
            sub_df = pd.DataFrame(future_rows)
            
        # Select the required forecasting steps
        forecast_inputs = sub_df.iloc[:steps].copy()
        
        # Make predictions
        X = forecast_inputs[self.feature_cols]
        preds = self.model.predict(X)
        
        # Build results dataframe
        forecast_df = pd.DataFrame({
            'Date': forecast_inputs['Date'],
            'Forecast': preds
        })
        
        # Add confidence intervals
        forecast_df['Lower_CI'] = (forecast_df['Forecast'] - 1.96 * self.val_rmse).clip(lower=0)
        forecast_df['Upper_CI'] = forecast_df['Forecast'] + 1.96 * self.val_rmse
        
        return forecast_df

if __name__ == "__main__":
    predictor = DemandPredictor()
    # Test prediction
    df = predictor.forecast_demand(1, 1, 30)
    print(df)
