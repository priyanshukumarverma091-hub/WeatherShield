from flask import Blueprint, jsonify, request

from backend.services.weather_service import WeatherService


weather_bp = Blueprint(
    "weather_bp",
    __name__,
    url_prefix="/api",
)

weather_service = WeatherService()


@weather_bp.route("/weather", methods=["GET"])
def get_weather():
    """
    GET /api/weather?city=Jaipur

    Returns current weather, hourly forecast, daily forecast,
    and coordinates resolved through Open-Meteo geocoding.
    """
    city = request.args.get("city", "").strip()

    if not city:
        return jsonify({
            "success": False,
            "error": "City is required",
        }), 400

    try:
        data = weather_service.get_weather(city)

        return jsonify({
            "success": True,
            "data": data,
        }), 200

    except ValueError as exc:
        return jsonify({
            "success": False,
            "error": str(exc),
        }), 404

    except Exception as exc:
        return jsonify({
            "success": False,
            "error": str(exc),
        }), 502


@weather_bp.route("/air-quality", methods=["GET"])
def get_air_quality():
    """
    GET /api/air-quality?city=Jaipur
    """
    city = request.args.get("city", "").strip()

    if not city:
        return jsonify({
            "success": False,
            "error": "City is required",
        }), 400

    try:
        data = weather_service.get_air_quality(city)

        return jsonify({
            "success": True,
            "data": data,
        }), 200

    except ValueError as exc:
        return jsonify({
            "success": False,
            "error": str(exc),
        }), 404

    except Exception as exc:
        return jsonify({
            "success": False,
            "error": str(exc),
        }), 502
