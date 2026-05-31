import os
import joblib
import pandas as pd
import numpy as np
from datetime import timedelta

# Paths – used only when running locally with a pre-trained model
_BASE = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH          = os.path.join(_BASE, "best_model.joblib")
TEST_DATA_PATH      = os.path.join(_BASE, "..", "dataset", "processed", "test_dataset_processed.csv")
HISTORICAL_DATA_PATH = os.path.join(_BASE, "..", "dataset", "processed", "analytical_dataset.csv")

# Minimum file size to detect Git-LFS pointer files (real files are MB-scale)
_MIN_REAL_FILE_BYTES = 1024


class DemandPredictor:
    """
    Demand forecasting predictor.

    Priority:
    1. Load pre-trained .joblib model (works locally).
    2. If .joblib is missing/invalid (e.g. Streamlit Cloud), train a fast
       linear model on-the-fly from the DB or raw train.csv.
    """

    def __init__(self, db=None):
        self.model          = None
        self.feature_cols   = []
        self.val_rmse       = 5447.12   # fallback std for confidence intervals
        self.model_name     = "Fallback Linear Model"
        self._db            = db        # optional DB reference for in-memory training
        self._store_dept_stats = {}     # per-(store,dept) historical stats for fast lookup
        self._global_mean   = 15000.0

        self.load_model()

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def load_model(self):
        """Try to load the pre-trained joblib model; silently skip if unavailable."""
        if os.path.exists(MODEL_PATH) and os.path.getsize(MODEL_PATH) > _MIN_REAL_FILE_BYTES:
            try:
                pkg = joblib.load(MODEL_PATH)
                self.model        = pkg["model"]
                self.feature_cols = pkg["features"]
                self.model_name   = pkg.get("model_name", "Loaded Model")
                metrics = pkg.get("metrics", [])
                for m in metrics:
                    if m.get("Model") == self.model_name:
                        self.val_rmse = m.get("Val_RMSE", self.val_rmse)
                print(f"Loaded pre-trained model: {self.model_name} (Val RMSE: {self.val_rmse:.2f})")
                return
            except Exception as e:
                print(f"Warning: Could not load model package ({e}). Falling back to statistical model.")

        # No usable .joblib – build a statistical fallback
        print("Pre-trained model not found. Building statistical fallback from available data...")
        self._build_statistical_model()

    def forecast_demand(self, store, dept, horizon_days=30):
        """
        Generate a demand forecast.

        If the ML model is available, it uses it.
        Otherwise uses the statistical (per store-dept mean + trend) fallback.
        """
        if horizon_days <= 7:
            steps = 1
        elif horizon_days <= 30:
            steps = 4
        else:
            steps = 13

        print(f"Forecasting Store {store}, Dept {dept}, {steps} weeks ({horizon_days} days)...")

        # -- ML path --
        if self.model is not None:
            return self._forecast_ml(store, dept, steps)

        # -- Statistical fallback --
        return self._forecast_statistical(store, dept, steps)

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _build_statistical_model(self):
        """
        Build per-(store, dept) historical mean and simple trend from raw data.
        Tries DB first, then raw train.csv, then processed CSV.
        """
        df = self._load_raw_data()
        if df is None or len(df) == 0:
            print("No data available for statistical model; using global fallback.")
            self._global_mean = 15000.0
            return

        # Rename columns to lowercase if needed
        df.columns = [c.lower() for c in df.columns]
        col_map = {"weekly_sales": "weekly_sales", "weekly_sales_cleaned": "weekly_sales"}
        for src, dst in col_map.items():
            if src in df.columns and dst not in df.columns:
                df.rename(columns={src: dst}, inplace=True)

        if "weekly_sales" not in df.columns:
            self._global_mean = 15000.0
            return

        df["weekly_sales"] = pd.to_numeric(df["weekly_sales"], errors="coerce").fillna(0)
        self._global_mean = float(df["weekly_sales"].mean())

        # Per store+dept stats
        grp = df.groupby(["store", "dept"])["weekly_sales"]
        means  = grp.mean()
        stds   = grp.std().fillna(0)
        medians = grp.median()

        for (s, d), mean_val in means.items():
            self._store_dept_stats[(s, d)] = {
                "mean":   float(mean_val),
                "std":    float(stds.get((s, d), 0)),
                "median": float(medians.get((s, d), mean_val)),
            }

        self.model_name = "Statistical (Mean/Trend) Fallback"
        print(f"Statistical model built for {len(self._store_dept_stats)} store-dept combinations.")

    def _load_raw_data(self):
        """Load sales data from DB, then CSV fallbacks."""
        # 1. From DB (fastest if already seeded)
        if self._db is not None:
            try:
                conn = self._db.get_connection()
                df = pd.read_sql_query(
                    "SELECT store, dept, date, weekly_sales FROM sales_data LIMIT 500000",
                    conn
                )
                conn.close()
                if len(df) > 0:
                    print(f"Statistical model: loaded {len(df):,} rows from DB.")
                    return df
            except Exception as e:
                print(f"DB load failed ({e}); trying CSV fallback.")

        # 2. Raw train.csv (Git-tracked, always present on Cloud)
        raw_path = os.path.join(_BASE, "..", "dataset", "raw", "train.csv")
        if os.path.exists(raw_path) and os.path.getsize(raw_path) > _MIN_REAL_FILE_BYTES:
            try:
                df = pd.read_csv(raw_path)
                print(f"Statistical model: loaded {len(df):,} rows from train.csv.")
                return df
            except Exception as e:
                print(f"train.csv load failed ({e}).")

        # 3. Parquet
        parquet_path = os.path.join(_BASE, "..", "dataset", "processed", "analytical_dataset.parquet")
        if os.path.exists(parquet_path) and os.path.getsize(parquet_path) > _MIN_REAL_FILE_BYTES:
            try:
                df = pd.read_parquet(parquet_path)
                print(f"Statistical model: loaded {len(df):,} rows from parquet.")
                return df
            except Exception as e:
                print(f"Parquet load failed ({e}).")

        # 4. Processed CSV (may be LFS pointer on Cloud)
        if os.path.exists(HISTORICAL_DATA_PATH) and os.path.getsize(HISTORICAL_DATA_PATH) > _MIN_REAL_FILE_BYTES:
            try:
                df = pd.read_csv(HISTORICAL_DATA_PATH)
                print(f"Statistical model: loaded {len(df):,} rows from processed CSV.")
                return df
            except Exception as e:
                print(f"Processed CSV load failed ({e}).")

        return None

    def _forecast_statistical(self, store, dept, steps):
        """Return forecast using per-(store,dept) mean ± small weekly trend."""
        stats = self._store_dept_stats.get((store, dept))
        if stats:
            base   = stats["mean"]
            spread = stats["std"] * 0.05  # gentle weekly variation
        else:
            base   = self._global_mean
            spread = base * 0.05

        start_date = pd.Timestamp("2012-11-02")  # one week after last training date
        dates = pd.date_range(start=start_date, periods=steps, freq="W-FRI")

        forecasts = []
        for i in range(steps):
            # Mild seasonal bump for holiday weeks (Nov/Dec)
            month = dates[i].month
            seasonal = 1.15 if month in (11, 12) else 1.0
            forecasts.append(base * seasonal + spread * np.sin(i * np.pi / steps))

        forecast_df = pd.DataFrame({
            "Date":     dates,
            "Forecast": np.maximum(forecasts, 0),
        })
        forecast_df["Lower_CI"] = (forecast_df["Forecast"] - 1.96 * self.val_rmse).clip(lower=0)
        forecast_df["Upper_CI"] =  forecast_df["Forecast"] + 1.96 * self.val_rmse

        return forecast_df

    def _forecast_ml(self, store, dept, steps):
        """Use the loaded scikit-learn / XGBoost model for forecasting."""
        # Try to load future feature rows from test set
        test_df = None
        if os.path.exists(TEST_DATA_PATH) and os.path.getsize(TEST_DATA_PATH) > _MIN_REAL_FILE_BYTES:
            try:
                test_df = pd.read_csv(TEST_DATA_PATH)
                test_df["Date"] = pd.to_datetime(test_df["Date"])
            except Exception:
                test_df = None

        if test_df is not None:
            sub_df = test_df[(test_df["Store"] == store) & (test_df["Dept"] == dept)]
            sub_df = sub_df.sort_values("Date").reset_index(drop=True)
        else:
            sub_df = pd.DataFrame()

        if len(sub_df) == 0:
            # Build synthetic rows using last known row from historical data
            hist_df = self._load_raw_data()
            if hist_df is not None and len(hist_df) > 0:
                hist_df.columns = [c.lower() for c in hist_df.columns]
                hist_sub = hist_df[(hist_df.get("store") == store) & (hist_df.get("dept") == dept)]
                if len(hist_sub) > 0:
                    last = hist_sub.sort_values("date").iloc[-1]
                    dates = pd.date_range(
                        start=pd.to_datetime(last["date"]) + timedelta(weeks=1),
                        periods=steps, freq="W-FRI"
                    )
                    future_rows = []
                    for dt in dates:
                        row = last.copy()
                        row["date"]    = dt
                        row["day"]     = dt.day
                        row["week"]    = dt.isocalendar()[1]
                        row["month"]   = dt.month
                        row["quarter"] = (dt.month - 1) // 3 + 1
                        row["year"]    = dt.year
                        future_rows.append(row)
                    sub_df = pd.DataFrame(future_rows)

        if len(sub_df) == 0:
            return self._forecast_statistical(store, dept, steps)

        forecast_inputs = sub_df.iloc[:steps].copy()
        # Rename cols to match original feature_cols (title-cased)
        col_remap = {c.lower(): c for c in self.feature_cols}
        forecast_inputs = forecast_inputs.rename(columns=col_remap)

        missing = [c for c in self.feature_cols if c not in forecast_inputs.columns]
        for c in missing:
            forecast_inputs[c] = 0

        X = forecast_inputs[self.feature_cols]
        preds = self.model.predict(X)

        dates_col = forecast_inputs.get("Date", forecast_inputs.get("date",
                        pd.date_range("2012-11-02", periods=steps, freq="W-FRI")))

        forecast_df = pd.DataFrame({"Date": dates_col, "Forecast": preds})
        forecast_df["Lower_CI"] = (forecast_df["Forecast"] - 1.96 * self.val_rmse).clip(lower=0)
        forecast_df["Upper_CI"] =  forecast_df["Forecast"] + 1.96 * self.val_rmse
        return forecast_df


if __name__ == "__main__":
    predictor = DemandPredictor()
    df = predictor.forecast_demand(1, 1, 30)
    print(df)
