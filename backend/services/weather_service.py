# ============================================================
# WEATHER SERVICE
# Open-Meteo Weather + Air Quality Integration
# ============================================================

import requests

from backend.config import BackendConfig


class WeatherService:
    """
    Weather API integration layer.

    Flow:

        City
          ↓
        Open-Meteo Geocoding
          ↓
        Latitude / Longitude
          ↓
        Open-Meteo Forecast
          ↓
        Weather JSON
    """

    # ========================================================
    # DEFAULT API URLS
    # ========================================================

    DEFAULT_GEOCODING_URL = (
        "https://geocoding-api.open-meteo.com/v1/search"
    )

    DEFAULT_WEATHER_URL = (
        "https://api.open-meteo.com/v1/forecast"
    )

    DEFAULT_AIR_QUALITY_URL = (
        "https://air-quality-api.open-meteo.com/v1/air-quality"
    )

    # ========================================================
    # INITIALIZATION
    # ========================================================

    def __init__(self):

        self.timeout = getattr(
            BackendConfig,
            "REQUEST_TIMEOUT",
            15
        )

        self.geocoding_url = getattr(
            BackendConfig,
            "OPEN_METEO_GEOCODING_URL",
            self.DEFAULT_GEOCODING_URL
        )

        self.weather_url = getattr(
            BackendConfig,
            "OPEN_METEO_BASE_URL",
            self.DEFAULT_WEATHER_URL
        )

        self.air_quality_url = getattr(
            BackendConfig,
            "OPEN_METEO_AIR_QUALITY_URL",
            self.DEFAULT_AIR_QUALITY_URL
        )

        self.session = requests.Session()

        self.session.headers.update({
            "User-Agent": "Weather-Intelligence-System/1.0"
        })

    # ========================================================
    # HELPER - API REQUEST
    # ========================================================

    def _get(self, url, params):

        try:

            response = self.session.get(
                url,
                params=params,
                timeout=self.timeout
            )

            response.raise_for_status()

            return response.json()

        except requests.exceptions.Timeout:

            raise RuntimeError(
                "Weather API request timed out. "
                "Please try again."
            )

        except requests.exceptions.ConnectionError:

            raise RuntimeError(
                "Could not connect to Open-Meteo. "
                "Please check your internet connection."
            )

        except requests.exceptions.HTTPError as exc:

            status_code = (
                exc.response.status_code
                if exc.response is not None
                else "unknown"
            )

            error_text = ""

            try:
                error_data = exc.response.json()

                error_text = (
                    error_data.get("reason")
                    or error_data.get("error")
                    or ""
                )

            except Exception:
                pass

            if error_text:

                raise RuntimeError(
                    f"Open-Meteo API error "
                    f"({status_code}): {error_text}"
                )

            raise RuntimeError(
                f"Open-Meteo API error "
                f"(HTTP {status_code})"
            )

        except ValueError:

            raise RuntimeError(
                "Open-Meteo returned invalid JSON."
            )

    # ========================================================
    # GEOCODING
    # ========================================================

    def geocode_city(self, city):

        city = str(city).strip()

        if not city:

            raise ValueError(
                "City is required."
            )

        params = {
            "name": city,
            "count": 1,
            "language": "en",
            "format": "json"
        }

        result = self._get(
            self.geocoding_url,
            params
        )

        locations = result.get(
            "results",
            []
        )

        if not locations:

            raise ValueError(
                f"Location not found: {city}"
            )

        location = locations[0]

        return {
            "name": location.get("name"),
            "latitude": location.get("latitude"),
            "longitude": location.get("longitude"),
            "country": location.get("country"),
            "country_code": location.get("country_code"),
            "admin1": location.get("admin1"),
            "timezone": location.get("timezone")
        }

    # ========================================================
    # WEATHER
    # ========================================================

    def get_weather(self, city):

        # ----------------------------------------------------
        # STEP 1: GET LOCATION
        # ----------------------------------------------------

        location = self.geocode_city(city)

        latitude = location.get("latitude")
        longitude = location.get("longitude")

        if latitude is None or longitude is None:

            raise RuntimeError(
                "Could not resolve latitude/longitude."
            )

        # ----------------------------------------------------
        # STEP 2: WEATHER PARAMETERS
        # ----------------------------------------------------

        params = {

            "latitude": latitude,

            "longitude": longitude,

            # Current weather
            "current": ",".join([
                "temperature_2m",
                "relative_humidity_2m",
                "apparent_temperature",
                "precipitation",
                "rain",
                "weather_code",
                "cloud_cover",
                "pressure_msl",
                "wind_speed_10m",
                "wind_direction_10m",
                "wind_gusts_10m",
                "visibility"
            ]),

            # Hourly weather
            "hourly": ",".join([
                "temperature_2m",
                "relative_humidity_2m",
                "precipitation_probability",
                "precipitation",
                "rain",
                "weather_code",
                "cloud_cover",
                "pressure_msl",
                "wind_speed_10m",
                "wind_direction_10m",
                "wind_gusts_10m"
            ]),

            # Daily weather
            "daily": ",".join([
                "weather_code",
                "temperature_2m_max",
                "temperature_2m_min",
                "apparent_temperature_max",
                "apparent_temperature_min",
                "sunrise",
                "sunset",
                "precipitation_sum",
                "rain_sum",
                "precipitation_probability_max",
                "wind_speed_10m_max",
                "wind_gusts_10m_max"
            ]),

            "timezone": "auto",

            "forecast_days": 7
        }

        # ----------------------------------------------------
        # STEP 3: CALL OPEN-METEO
        # ----------------------------------------------------

        weather = self._get(
            self.weather_url,
            params
        )

        # ----------------------------------------------------
        # STEP 4: RETURN CLEAN RESPONSE
        # ----------------------------------------------------

        return {
            "location": location,

            "source": "Open-Meteo",

            "timezone": weather.get(
                "timezone"
            ),

            "elevation": weather.get(
                "elevation"
            ),

            "current": weather.get(
                "current",
                {}
            ),

            "current_units": weather.get(
                "current_units",
                {}
            ),

            "hourly": weather.get(
                "hourly",
                {}
            ),

            "hourly_units": weather.get(
                "hourly_units",
                {}
            ),

            "daily": weather.get(
                "daily",
                {}
            ),

            "daily_units": weather.get(
                "daily_units",
                {}
            )
        }

    # ========================================================
    # AIR QUALITY
    # ========================================================

    def get_air_quality(self, city):

        # ----------------------------------------------------
        # STEP 1: GET LOCATION
        # ----------------------------------------------------

        location = self.geocode_city(city)

        latitude = location.get("latitude")
        longitude = location.get("longitude")

        if latitude is None or longitude is None:

            raise RuntimeError(
                "Could not resolve latitude/longitude."
            )

        # ----------------------------------------------------
        # STEP 2: AIR QUALITY PARAMETERS
        # ----------------------------------------------------

        params = {

            "latitude": latitude,

            "longitude": longitude,

            "current": ",".join([
                "european_aqi",
                "us_aqi",
                "pm10",
                "pm2_5",
                "carbon_monoxide",
                "nitrogen_dioxide",
                "sulphur_dioxide",
                "ozone"
            ]),

            "hourly": ",".join([
                "european_aqi",
                "us_aqi",
                "pm10",
                "pm2_5",
                "ozone",
                "nitrogen_dioxide"
            ]),

            "timezone": "auto"
        }

        # ----------------------------------------------------
        # STEP 3: CALL OPEN-METEO AIR QUALITY
        # ----------------------------------------------------

        air = self._get(
            self.air_quality_url,
            params
        )

        # ----------------------------------------------------
        # STEP 4: RETURN RESPONSE
        # ----------------------------------------------------

        return {
            "location": location,

            "source": "Open-Meteo Air Quality",

            "timezone": air.get(
                "timezone"
            ),

            "current": air.get(
                "current",
                {}
            ),

            "current_units": air.get(
                "current_units",
                {}
            ),

            "hourly": air.get(
                "hourly",
                {}
            ),

            "hourly_units": air.get(
                "hourly_units",
                {}
            )
        }