import requests
from flask import current_app
from backend.utils.normalization import normalize_business
from backend.utils.deduplication import deduplicate_businesses


def search_businesses(keyword, location, category="", limit=20):
    key = current_app.config.get("GOOGLE_MAPS_API_KEY")
    query = " ".join(part for part in (keyword, category, location) if part).strip()
    if not key:
        raise RuntimeError("Google Maps is not configured. Set GOOGLE_MAPS_API_KEY on the server.")
    response = requests.post("https://places.googleapis.com/v1/places:searchText", headers={"X-Goog-Api-Key": key, "X-Goog-FieldMask": "places.id,places.displayName,places.formattedAddress,places.internationalPhoneNumber,places.websiteUri,places.googleMapsUri,places.rating,places.userRatingCount,places.primaryTypeDisplayName"}, json={"textQuery": query, "maxResultCount": min(max(int(limit), 1), 20)}, timeout=20)
    response.raise_for_status()
    return deduplicate_businesses([normalize_business(place, category, location, query) for place in response.json().get("places", [])])
