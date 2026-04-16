from __future__ import annotations

import math
from typing import Any

import requests


MAPBOX_GEOCODE_URL = "https://api.mapbox.com/search/geocode/v6/forward"
NOMINATIM_GEOCODE_URL = "https://nominatim.openstreetmap.org/search"
MBTA_STOPS_URL = "https://api-v3.mbta.com/stops"


class TransitLookupError(Exception):
    """Raised when an external API lookup fails in a user-facing way."""


def geocode_location(query: str, mapbox_token: str = "") -> dict[str, Any]:
    if mapbox_token:
        place = _geocode_with_mapbox(query, mapbox_token)
        if place:
            return place

    place = _geocode_with_nominatim(query)
    if place:
        return place

    raise TransitLookupError("No matching location was found. Try a more specific address.")


def _geocode_with_mapbox(query: str, token: str) -> dict[str, Any] | None:
    try:
        response = requests.get(
            MAPBOX_GEOCODE_URL,
            params={
                "q": query,
                "limit": 1,
                "access_token": token,
                "country": "US",
            },
            timeout=15,
        )
        response.raise_for_status()
    except requests.RequestException as exc:
        raise TransitLookupError("Mapbox geocoding failed. Check your token or try again.") from exc

    data = response.json()
    features = data.get("features", [])
    if not features:
        return None

    feature = features[0]
    coordinates = feature.get("geometry", {}).get("coordinates", [])
    if len(coordinates) < 2:
        return None

    props = feature.get("properties", {})
    return {
        "name": feature.get("properties", {}).get("full_address")
        or feature.get("properties", {}).get("name")
        or query,
        "latitude": coordinates[1],
        "longitude": coordinates[0],
        "source": "Mapbox",
        "confidence": props.get("match_code", {}).get("confidence"),
    }


def _geocode_with_nominatim(query: str) -> dict[str, Any] | None:
    try:
        response = requests.get(
            NOMINATIM_GEOCODE_URL,
            params={
                "q": query,
                "format": "jsonv2",
                "limit": 1,
            },
            headers={"User-Agent": "oim3640-project-3-demo"},
            timeout=15,
        )
        response.raise_for_status()
    except requests.RequestException as exc:
        raise TransitLookupError("Geocoding failed. Please try again in a moment.") from exc

    matches = response.json()
    if not matches:
        return None

    place = matches[0]
    return {
        "name": place.get("display_name", query),
        "latitude": float(place["lat"]),
        "longitude": float(place["lon"]),
        "source": "OpenStreetMap",
        "confidence": None,
    }


def find_nearest_stop(latitude: float, longitude: float, api_key: str = "") -> dict[str, Any]:
    headers = {}
    if api_key:
        headers["x-api-key"] = api_key

    try:
        response = requests.get(
            MBTA_STOPS_URL,
            params={
                "filter[latitude]": latitude,
                "filter[longitude]": longitude,
                "filter[radius]": 0.03,
                "sort": "distance",
                "page[limit]": 1,
                "fields[stop]": "name,latitude,longitude,wheelchair_boarding,address,municipality",
            },
            headers=headers,
            timeout=15,
        )
        response.raise_for_status()
    except requests.RequestException as exc:
        raise TransitLookupError("The MBTA stop lookup failed. Please try again.") from exc

    stops = response.json().get("data", [])
    if not stops:
        raise TransitLookupError("No MBTA stop was found near that location.")

    stop = stops[0]
    attrs = stop.get("attributes", {})
    stop_lat = attrs.get("latitude")
    stop_lon = attrs.get("longitude")

    return {
        "id": stop.get("id"),
        "name": attrs.get("name", "Unknown stop"),
        "latitude": stop_lat,
        "longitude": stop_lon,
        "address": attrs.get("address"),
        "municipality": attrs.get("municipality"),
        "wheelchair_status": describe_wheelchair_boarding(attrs.get("wheelchair_boarding")),
        "distance_miles": calculate_distance_miles(latitude, longitude, stop_lat, stop_lon)
        if stop_lat is not None and stop_lon is not None
        else None,
    }


def describe_wheelchair_boarding(value: int | None) -> str:
    lookup = {
        0: "No accessibility information available",
        1: "Wheelchair accessible",
        2: "Not wheelchair accessible",
    }
    return lookup.get(value, "Accessibility information unavailable")


def calculate_distance_miles(
    start_lat: float, start_lon: float, end_lat: float, end_lon: float
) -> float:
    earth_radius_miles = 3958.8
    start_lat_r = math.radians(start_lat)
    end_lat_r = math.radians(end_lat)
    delta_lat = math.radians(end_lat - start_lat)
    delta_lon = math.radians(end_lon - start_lon)

    haversine = (
        math.sin(delta_lat / 2) ** 2
        + math.cos(start_lat_r) * math.cos(end_lat_r) * math.sin(delta_lon / 2) ** 2
    )
    arc = 2 * math.atan2(math.sqrt(haversine), math.sqrt(1 - haversine))
    return round(earth_radius_miles * arc, 2)
