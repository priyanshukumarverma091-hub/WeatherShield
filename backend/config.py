import os


class BackendConfig:
    OPEN_METEO_BASE_URL = os.getenv(
        "OPEN_METEO_BASE_URL",
        "https://api.open-meteo.com/v1/forecast",
    )

    OPEN_METEO_GEOCODING_URL = os.getenv(
        "OPEN_METEO_GEOCODING_URL",
        "https://geocoding-api.open-meteo.com/v1/search",
    )

    OPEN_METEO_AIR_QUALITY_URL = os.getenv(
        "OPEN_METEO_AIR_QUALITY_URL",
        "https://air-quality-api.open-meteo.com/v1/air-quality",
    )

    IMD_API_BASE_URL = os.getenv(
        "IMD_API_BASE_URL",
        "https://api.imd.gov.in",
    )

    IMD_API_KEY = os.getenv("IMD_API_KEY", "")

    NASA_EONET_URL = os.getenv(
        "NASA_EONET_URL",
        "https://eonet.gsfc.nasa.gov/api/v3/events",
    )

    GDACS_API_BASE_URL = os.getenv(
        "GDACS_API_BASE_URL",
        "https://www.gdacs.org/gdacsapi",
    )

    MODEL_PATH = os.getenv(
        "MODEL_PATH",
        "saved_models/weather_model.joblib",
    )

    REQUEST_TIMEOUT = int(os.getenv("REQUEST_TIMEOUT", "15"))
