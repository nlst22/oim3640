# Project 3: Nearest MBTA Stop Finder

This first draft is a Flask web app that:

- accepts a user-entered location or street address
- geocodes the location with Mapbox when a token is available
- falls back to OpenStreetMap geocoding when no Mapbox token is set
- queries the MBTA API for the closest stop
- reports wheelchair accessibility information
- optionally renders a Mapbox map showing both points

## Live link
https://oim3640-1-3wrv.onrender.com

## Project structure

- `app.py`: Flask app and routes
- `services.py`: API integrations and helper logic
- `templates/`: Jinja templates
- `static/`: CSS styling
- `requirements.txt`: Python dependencies

## Environment variables

Add these to the repo-level `.env` file:

```env
MAPBOX_ACCESS_TOKEN=your_mapbox_token_here
MBTA_API_KEY=
FLASK_SECRET_KEY=change-me
```

`MBTA_API_KEY` is optional because the MBTA API can be used without one for this project.

## Run locally

From the repository root:

```powershell
pip install -r mini_projects/project_3/requirements.txt
python mini_projects/project_3/app.py
```

Then open `http://127.0.0.1:5000`.
