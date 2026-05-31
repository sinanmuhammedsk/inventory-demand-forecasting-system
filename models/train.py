import os
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import xgboost as xgb
import joblib

# Paths
PROCESSED_DATA_PATH = r"d:\forecast\dataset\processed\analytical_dataset.csv"
MODEL_SAVE_PATH = r"d:\forecast\models\best_model.joblib"
METRICS_SAVE_PATH = r"d:\forecast\reports\model_comparison.csv"

def train_and_evaluate():
    print("Loading analytical dataset...")
    if not os.path.exists(PROCESSED_DATA_PATH):
        raise FileNotFoundError(f"Processed dataset not found at {PROCESSED_DATA_PATH}. Please run preprocessor first.")
        
    df = pd.read_csv(PROCESSED_DATA_PATH)
    df['Date'] = pd.to_datetime(df['Date'])
    
    # Sort chronologically
    df = df.sort_values('Date').reset_index(drop=True)
    
    # Define features and target
    feature_cols = [
        'Store', 'Dept', 'IsHoliday', 'Type_Encoded', 'Size', 
        'Temperature', 'Fuel_Price', 'CPI', 'Unemployment', 
        'Day', 'Week', 'Month', 'Quarter', 'Year', 
        'Is_SuperBowl', 'Is_LaborDay', 'Is_Thanksgiving', 'Is_Christmas', 
        'Season_Encoded', 'Size_Unemployment_Ratio', 'Size_CPI_Ratio'
    ]
    
    # Use outlier-treated sales for training target
    target_col = 'Weekly_Sales_Cleaned'
    
    print(f"Total rows: {len(df):,}")
    print(f"Features used: {feature_cols}")
    
    # Chronological Split (Train: < 2012-05-01, Val: >= 2012-05-01)
    split_date = pd.to_datetime('2012-05-01')
    
    train_mask = df['Date'] < split_date
    val_mask = df['Date'] >= split_date
    
    train_df = df[train_mask]
    val_df = df[val_mask]
    
    X_train, y_train = train_df[feature_cols], train_df[target_col]
    X_val, y_val = val_df[feature_cols], val_df[target_col]  # Evaluate on cleaned sales
    
    print(f"Train set size: {len(X_train):,} rows (from {train_df['Date'].min().strftime('%Y-%m-%d')} to {train_df['Date'].max().strftime('%Y-%m-%d')})")
    print(f"Validation set size: {len(X_val):,} rows (from {val_df['Date'].min().strftime('%Y-%m-%d')} to {val_df['Date'].max().strftime('%Y-%m-%d')})")
    
    # Initialize models
    models = {
        "Linear Regression": LinearRegression(),
        "Random Forest": RandomForestRegressor(n_estimators=30, max_depth=12, random_state=42, n_jobs=-1),
        "XGBoost": xgb.XGBRegressor(n_estimators=60, max_depth=6, learning_rate=0.15, random_state=42, n_jobs=-1)
    }
    
    results = []
    trained_models = {}
    
    # Train and evaluate each model
    for name, model in models.items():
        print(f"\nTraining {name}...")
        model.fit(X_train, y_train)
        trained_models[name] = model
        
        # Predict on train and validation
        train_preds = model.predict(X_train)
        val_preds = model.predict(X_val)
        
        # Metrics
        train_rmse = np.sqrt(mean_squared_error(y_train, train_preds))
        val_rmse = np.sqrt(mean_squared_error(y_val, val_preds))
        
        train_mae = mean_absolute_error(y_train, train_preds)
        val_mae = mean_absolute_error(y_val, val_preds)
        
        train_r2 = r2_score(y_train, train_preds)
        val_r2 = r2_score(y_val, val_preds)
        
        print(f"{name} Results:")
        print(f"  Train - RMSE: {train_rmse:.2f}, MAE: {train_mae:.2f}, R²: {train_r2:.4f}")
        print(f"  Val   - RMSE: {val_rmse:.2f}, MAE: {val_mae:.2f}, R²: {val_r2:.4f}")
        
        results.append({
            "Model": name,
            "Train_RMSE": train_rmse,
            "Val_RMSE": val_rmse,
            "Train_MAE": train_mae,
            "Val_MAE": val_mae,
            "Train_R2": train_r2,
            "Val_R2": val_r2
        })
        
    # Save comparison table
    comparison_df = pd.DataFrame(results)
    os.makedirs(os.path.dirname(METRICS_SAVE_PATH), exist_ok=True)
    comparison_df.to_csv(METRICS_SAVE_PATH, index=False)
    print(f"\nModel comparison metrics saved to: {METRICS_SAVE_PATH}")
    
    # Select best model based on validation RMSE
    best_model_name = comparison_df.loc[comparison_df['Val_RMSE'].idxmin(), 'Model']
    print(f"\nBest Model Selected: {best_model_name}")
    
    # Retrain best model on full training dataset
    print(f"Retraining the best model ({best_model_name}) on full historical dataset...")
    X_full, y_full = df[feature_cols], df[target_col]
    
    best_model = models[best_model_name]
    best_model.fit(X_full, y_full)
    
    # Save model artifact package
    model_package = {
        "model_name": best_model_name,
        "model": best_model,
        "features": feature_cols,
        "metrics": comparison_df.to_dict(orient='records')
    }
    
    os.makedirs(os.path.dirname(MODEL_SAVE_PATH), exist_ok=True)
    joblib.dump(model_package, MODEL_SAVE_PATH)
    print(f"Successfully serialized best model package to: {MODEL_SAVE_PATH}")
    
if __name__ == "__main__":
    train_and_evaluate()
