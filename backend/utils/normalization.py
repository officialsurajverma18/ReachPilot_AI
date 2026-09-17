from urllib.parse import quote


def normalize_business(item, category="", location="", query=""):
    name = (item.get("name") or item.get("displayName", {}).get("text") or "").strip()
    place_id = item.get("id") or item.get("place_id") or ""
    address = item.get("formattedAddress") or item.get("address") or ""
    website = item.get("websiteUri") or item.get("website") or ""
    maps_url = item.get("googleMapsUri") or item.get("maps_url") or ""
    if not maps_url and (name or address):
        maps_url = f"https://www.google.com/maps/search/?api=1&query={quote(f'{name} {address}'.strip())}"
    return {"place_id": place_id, "name": name, "category": category or item.get("primaryTypeDisplayName", {}).get("text", ""),
            "location": location, "address": address, "phone": item.get("internationalPhoneNumber") or item.get("phone", ""),
            "website": website, "maps_url": maps_url, "rating": item.get("rating") or 0,
            "review_count": item.get("userRatingCount") or item.get("review_count") or 0, "source_query": query}
