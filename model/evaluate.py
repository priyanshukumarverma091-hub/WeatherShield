import sys
from pathlib import Path

import joblib
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from model.config import MODEL_FILE, DATA_FILE
from model.preprocessing import load_dataset


def main():
    if not MODEL_FILE.exists():
        raise FileNotFoundError(
            "Trained model not found. Run: python -m model.train"
        )

    artifact = joblib.load(MODEL_FILE)
    model = artifact["model"]
    imputer = artifact["imputer"]
    scaler = artifact["scaler"]
    features = artifact["features"]
    target = artifact["target"]

    df = load_dataset(DATA_FILE)

    missing = [col for col in features + [target] if col not in df.columns]
    if missing:
        raise ValueError(f"Missing columns: {missing}")

    X = df[features].copy()
    y = df[target].copy()

    for col in features + [target]:
        df[col] = __import__("pandas").to_numeric(
            df[col], errors="coerce"
        )

    X = df[features]
    y = df[target]

    valid = y.notna()
    X = X.loc[valid]
    y = y.loc[valid]

    X = imputer.transform(X)
    X = scaler.transform(X)

    predictions = model.predict(X)

    print("=" * 60)
    print("WEATHER MODEL EVALUATION")
    print("=" * 60)
    print(f"MAE  : {mean_absolute_error(y, predictions):.4f}")
    print(f"RMSE : {mean_squared_error(y, predictions) ** 0.5:.4f}")
    print(f"R2   : {r2_score(y, predictions):.4f}")


if __name__ == "__main__":
    main()
