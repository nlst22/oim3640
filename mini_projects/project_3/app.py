import os
from pathlib import Path

from dotenv import load_dotenv
from flask import Flask, render_template, request

try:
    from .services import TransitLookupError, find_nearest_stop, geocode_location
except ImportError:
    from services import TransitLookupError, find_nearest_stop, geocode_location


ROOT_DIR = Path(__file__).resolve().parents[2]
load_dotenv(ROOT_DIR / ".env")


def create_app() -> Flask:
    app = Flask(__name__)
    app.config["MAPBOX_ACCESS_TOKEN"] = os.getenv("MAPBOX_ACCESS_TOKEN", "").strip()
    app.config["MBTA_API_KEY"] = os.getenv("MBTA_API_KEY", "").strip()
    app.config["SECRET_KEY"] = os.getenv("FLASK_SECRET_KEY", "dev-secret-key")

    @app.route("/", methods=["GET", "POST"])
    def index():
        result = None
        error = None
        query = ""

        if request.method == "POST":
            query = request.form.get("location", "").strip()
            if not query:
                error = "Enter a location or address to search."
            else:
                try:
                    place = geocode_location(query, mapbox_token=app.config["MAPBOX_ACCESS_TOKEN"])
                    nearest_stop = find_nearest_stop(
                        latitude=place["latitude"],
                        longitude=place["longitude"],
                        api_key=app.config["MBTA_API_KEY"],
                    )
                    result = {
                        "query": query,
                        "searched_place": place,
                        "nearest_stop": nearest_stop,
                    }
                except TransitLookupError as exc:
                    error = str(exc)
                except Exception:
                    error = "Something unexpected happened while looking up the nearest stop."

        return render_template(
            "index.html",
            error=error,
            result=result,
            query=query,
            mapbox_token=app.config["MAPBOX_ACCESS_TOKEN"],
        )

    return app


app = create_app()


if __name__ == "__main__":
    app.run(debug=True)
