# ============================================================
# WEATHER INTELLIGENCE SYSTEM
# Flask Application
# ============================================================

import os
from pathlib import Path

from flask import Flask, render_template, jsonify
from flask_cors import CORS
from dotenv import load_dotenv


# ============================================================
# PROJECT ROOT
# ============================================================

BASE_DIR = Path(__file__).resolve().parent


# ============================================================
# LOAD ENVIRONMENT VARIABLES
# ============================================================

ENV_FILE = BASE_DIR / ".env"

if ENV_FILE.exists():
    load_dotenv(ENV_FILE)
else:
    load_dotenv()


# ============================================================
# IMPORTANT PROJECT PATHS
# ============================================================

TEMPLATES_DIR = BASE_DIR / "templates"
BACKEND_DIR = BASE_DIR / "backend"
MODEL_DIR = BASE_DIR / "model"


# ============================================================
# CREATE FLASK APPLICATION
# ============================================================

app = Flask(
    __name__,
    template_folder=str(TEMPLATES_DIR)
)

CORS(app)


# ============================================================
# APPLICATION CONFIGURATION
# ============================================================

app.config["JSON_SORT_KEYS"] = False


# ============================================================
# STARTUP CHECKS
# ============================================================

print()
print("=" * 65)
print("        WEATHER INTELLIGENCE SYSTEM")
print("=" * 65)
print()

print(f"[ROOT]      {BASE_DIR}")
print(f"[TEMPLATES] {TEMPLATES_DIR}")
print(f"[BACKEND]   {BACKEND_DIR}")
print(f"[MODEL]     {MODEL_DIR}")
print()


# ============================================================
# TEMPLATE CHECK
# ============================================================

INDEX_FILE = TEMPLATES_DIR / "index.html"

if INDEX_FILE.exists():

    print("[OK] index.html found")

else:

    print("[WARNING] index.html not found")
    print(f"[WARNING] Expected location:")
    print(f"           {INDEX_FILE}")


# ============================================================
# REGISTER WEATHER API ROUTES
# ============================================================

try:

    from backend.routes.weather_routes import weather_bp

    app.register_blueprint(weather_bp)

    print("[OK] Weather API routes loaded")

except Exception as e:

    print("[ERROR] Weather API routes could not be loaded")
    print(f"[ERROR] {e}")


# ============================================================
# HOME PAGE
# ============================================================

@app.route("/", methods=["GET"])
def home():

    return render_template("index.html")


# ============================================================
# HEALTH CHECK
# ============================================================

@app.route("/health", methods=["GET"])
def health():

    return jsonify({
        "status": "ok",
        "application": "Weather Intelligence System",
        "weather_api": "active"
    })


# ============================================================
# APPLICATION STATUS
# ============================================================

@app.route("/api/status", methods=["GET"])
def api_status():

    return jsonify({
        "status": "online",
        "service": "Weather Intelligence System",
        "weather": True,
        "emergency_ui": True,
        "model": True
    })


# ============================================================
# API 404 HANDLER
# ============================================================

@app.errorhandler(404)
def not_found(error):

    return jsonify({
        "success": False,
        "status": "error",
        "message": "Route not found"
    }), 404


# ============================================================
# INTERNAL SERVER ERROR HANDLER
# ============================================================

@app.errorhandler(500)
def server_error(error):

    return jsonify({
        "success": False,
        "status": "error",
        "message": "Internal server error"
    }), 500


# ============================================================
# APPLICATION START
# ============================================================

if __name__ == "__main__":

    # --------------------------------------------------------
    # PORT
    # --------------------------------------------------------

    port = int(
        os.getenv(
            "PORT",
            "5000"
        )
    )

    # --------------------------------------------------------
    # DEBUG
    # --------------------------------------------------------

    debug = (
        os.getenv(
            "FLASK_DEBUG",
            "True"
        ).strip().lower() == "true"
    )

    # --------------------------------------------------------
    # STARTUP INFORMATION
    # --------------------------------------------------------

    print()
    print("=" * 65)
    print("        WEATHER INTELLIGENCE SYSTEM")
    print("=" * 65)
    print()

    print(f"  Server   : http://127.0.0.1:{port}")
    print(f"  Debug    : {debug}")
    print()

    print("  Available:")
    print()
    print("  [WEB]")
    print("      /")
    print()
    print("  [HEALTH]")
    print("      /health")
    print()
    print("  [STATUS]")
    print("      /api/status")
    print()
    print("  [WEATHER]")
    print("      /api/weather?city=Jaipur")
    print()
    print("  [AQI]")
    print("      /api/air-quality?city=Jaipur")
    print()

    print("=" * 65)
    print()

    # --------------------------------------------------------
    # RUN FLASK
    # --------------------------------------------------------

    app.run(
        host="0.0.0.0",
        port=port,
        debug=debug
    )