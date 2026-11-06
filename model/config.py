from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent

DATA_DIR = PROJECT_ROOT / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
MODEL_DIR = PROJECT_ROOT / "saved_models"

# Change this when your real dataset is placed in data/raw/
DATA_FILE = RAW_DATA_DIR / "weather.csv"
MODEL_FILE = MODEL_DIR / "weather_model.joblib"

# Target predicted by the first baseline model.
TARGET_COLUMN = "temperature"

# Input columns. The preprocessing script will use only columns
# that actually exist in the dataset.
FEATURE_COLUMNS = [
    "humidity",
    "pressure",
    "wind_speed",
    "wind_direction",
    "rainfall",
    "cloud_cover",
    "temperature",
]

TEST_SIZE = 0.20
RANDOM_STATE = 42
N_ESTIMATORS = 300
