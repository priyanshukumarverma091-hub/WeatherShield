import pandas as pd
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler


def load_dataset(path):
    """Load a CSV weather dataset."""
    df = pd.read_csv(path)

    if df.empty:
        raise ValueError("Dataset is empty.")

    # Normalize column names.
    df.columns = [
        str(col).strip().lower().replace(" ", "_")
        for col in df.columns
    ]

    return df


def prepare_features(df, feature_columns, target_column):
    """
    Select available numeric weather features and target.

    This intentionally avoids assuming one exact dataset schema.
    """
    if target_column not in df.columns:
        raise ValueError(
            f"Target column '{target_column}' not found. "
            f"Available columns: {list(df.columns)}"
        )

    available = [
        col for col in feature_columns
        if col in df.columns and col != target_column
    ]

    if not available:
        raise ValueError(
            "No usable feature columns found. "
            f"Available columns: {list(df.columns)}"
        )

    data = df[available + [target_column]].copy()

    for col in available + [target_column]:
        data[col] = pd.to_numeric(data[col], errors="coerce")

    data = data.dropna(subset=[target_column])

    X = data[available]
    y = data[target_column]

    imputer = SimpleImputer(strategy="median")
    scaler = StandardScaler()

    X_imputed = imputer.fit_transform(X)
    X_scaled = scaler.fit_transform(X_imputed)

    return X_scaled, y, available, imputer, scaler
