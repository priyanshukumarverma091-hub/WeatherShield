import sys
from pathlib import Path

import joblib
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from model.config import (
    DATA_FILE,
    MODEL_DIR,
    MODEL_FILE,
    TARGET_COLUMN,
    FEATURE_COLUMNS,
    TEST_SIZE,
    RANDOM_STATE,
    N_ESTIMATORS,
)
from model.preprocessing import load_dataset, prepare_features
from model.model import build_model


def main():
    print("=" * 60)
    print("WEATHER MODEL TRAINING")
    print("=" * 60)

    if not DATA_FILE.exists():
        raise FileNotFoundError(
            f"\nDataset not found:\n{DATA_FILE}\n\n"
            "Put your CSV dataset in data/raw/weather.csv "
            "or change DATA_FILE in model/config.py."
        )

    df = load_dataset(DATA_FILE)

    X, y, used_features, imputer, scaler = prepare_features(
        df,
        FEATURE_COLUMNS,
        TARGET_COLUMN,
    )

    print(f"Dataset rows: {len(df)}")
    print(f"Training rows: {len(X)}")
    print(f"Target: {TARGET_COLUMN}")
    print(f"Features: {used_features}")

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=TEST_SIZE,
        random_state=RANDOM_STATE,
    )

    model = build_model(
        random_state=RANDOM_STATE,
        n_estimators=N_ESTIMATORS,
    )

    print("\nTraining model...")
    model.fit(X_train, y_train)

    predictions = model.predict(X_test)

    mae = mean_absolute_error(y_test, predictions)
    rmse = mean_squared_error(y_test, predictions) ** 0.5
    r2 = r2_score(y_test, predictions)

    print("\nEVALUATION")
    print("-" * 40)
    print(f"MAE  : {mae:.4f}")
    print(f"RMSE : {rmse:.4f}")
    print(f"R2   : {r2:.4f}")

    MODEL_DIR.mkdir(parents=True, exist_ok=True)

    artifact = {
        "model": model,
        "imputer": imputer,
        "scaler": scaler,
        "features": used_features,
        "target": TARGET_COLUMN,
    }

    joblib.dump(artifact, MODEL_FILE)

    print("\nModel saved:")
    print(MODEL_FILE)


if __name__ == "__main__":
    main()
