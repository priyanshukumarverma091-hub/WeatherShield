# Weather Backend - Open-Meteo Integrated

## Structure

```text
backend/
├── __init__.py
├── config.py
├── routes/
│   ├── __init__.py
│   └── weather_routes.py
└── services/
    ├── __init__.py
    └── weather_service.py

.env.example
requirements.txt
```

## APIs configured

- Open-Meteo Forecast
- Open-Meteo Geocoding
- Open-Meteo Air Quality
- IMD
- NASA EONET
- GDACS

Only Open-Meteo Forecast, Geocoding and Air Quality are integrated
in this version. The other API settings are prepared in `.env.example`
for later integration.

## Endpoints

### Weather

```text
GET /api/weather?city=Jaipur
```

### Air quality

```text
GET /api/air-quality?city=Jaipur
```

## Setup

Copy:

```text
.env.example
```

to:

```text
.env
```

Then install:

```bash
pip install -r requirements.txt
```

## Register routes in app.py

Your Flask application should contain:

```python
from dotenv import load_dotenv
from backend.routes.weather_routes import weather_bp

load_dotenv()

app.register_blueprint(weather_bp)
```

## Example response flow

```text
Jaipur
  ↓
Geocoding API
  ↓
26.91, 75.79
  ↓
Forecast API
  ↓
Current + Hourly + 7 Day Forecast
  ↓
JSON
  ↓
Frontend
```

Open-Meteo supports current/hourly/daily weather variables including
temperature, humidity, precipitation, pressure, cloud cover, wind,
gusts and visibility. Geocoding resolves city names to coordinates.
Air Quality provides AQI and pollutant variables.
