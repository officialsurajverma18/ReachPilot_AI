def deduplicate_businesses(items):
    seen, result = set(), []
    for item in items:
        key = (item.get("place_id") or f"{item.get('name','').lower()}|{item.get('address','').lower()}").strip()
        if key and key not in seen:
            seen.add(key)
            result.append(item)
    return result
