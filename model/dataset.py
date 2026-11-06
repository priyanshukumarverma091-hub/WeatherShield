from pathlib import Path
import pandas as pd


def load_csv(path):
    """Generic CSV loader for weather datasets."""
    path = Path(path)

    if not path.exists():
        raise FileNotFoundError(f"Dataset not found: {path}")

    df = pd.read_csv(path)

    if df.empty:
        raise ValueError("Dataset is empty.")

    df.columns = [
        str(c).strip().lower().replace(" ", "_")
        for c in df.columns
    ]

    return df
