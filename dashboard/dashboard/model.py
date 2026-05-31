from pathlib import Path
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
import joblib

BASE_DIR = Path(__file__).parent
MODELS_DIR = BASE_DIR / "models"
MODELS_DIR.mkdir(exist_ok=True)
MODEL_PATH = MODELS_DIR / "sales_model.pkl"


def _prepare_features(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    if "date" in df.columns:
        df["date"] = pd.to_datetime(df["date"])
        df["dow"] = df["date"].dt.dayofweek
        df["month"] = df["date"].dt.month
    # One-hot encode city and category
    X = pd.get_dummies(df[["city", "category"]].astype(str))
    if "dow" in df.columns:
        X["dow"] = df["dow"].values
        X["month"] = df["month"].values
    return X


def train_and_save(df: pd.DataFrame):
    df = df.copy()
    if df.empty:
        raise ValueError("Dataframe is empty")
    X = _prepare_features(df)
    y = df["sales"].values
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = RandomForestRegressor(n_estimators=50, random_state=42)
    model.fit(X_train, y_train)
    payload = {"model": model, "columns": X.columns.tolist()}
    joblib.dump(payload, MODEL_PATH)
    return payload


def load_or_train(df: pd.DataFrame = None):
    if MODEL_PATH.exists():
        try:
            payload = joblib.load(MODEL_PATH)
            return payload
        except Exception:
            pass
    if df is None:
        # try to load data file
        data_path = BASE_DIR / "data" / "sales.csv"
        if data_path.exists():
            df = pd.read_csv(data_path, parse_dates=["date"]) if "date" in open(data_path).read() else pd.read_csv(data_path)
            if "date" in df.columns:
                df["date"] = pd.to_datetime(df["date"])
    if df is None:
        raise ValueError("No data available to train the model")
    return train_and_save(df)


def predict(payload, city: str, category: str, date):
    # Build feature vector matching training columns
    cols = payload["columns"]
    row = {}
    for c in cols:
        row[c] = 0
    # set city and category one-hot
    city_col = f"city_{city}"
    cat_col = f"category_{category}"
    if city_col in cols:
        row[city_col] = 1
    if cat_col in cols:
        row[cat_col] = 1
    if date is not None:
        dow = pd.to_datetime(date).dayofweek
        month = pd.to_datetime(date).month
        if "dow" in cols:
            row["dow"] = dow
        if "month" in cols:
            row["month"] = month
    X = pd.DataFrame([row], columns=cols)
    pred = payload["model"].predict(X)[0]
    return float(pred)
