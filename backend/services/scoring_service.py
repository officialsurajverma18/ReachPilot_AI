"""Transparent, rule-based score: no unsubstantiated ML training claim is made."""
def score_business(business):
    rating = float(business.get("rating") or 0)
    reviews = int(business.get("review_count") or 0)
    website = bool(business.get("website"))
    phone = bool(business.get("phone"))
    factors, score = [], 0
    if 3.8 <= rating <= 4.8: score += 28; factors.append("Healthy public rating (+28)")
    elif rating >= 3.4: score += 14; factors.append("Acceptable public rating (+14)")
    if 20 <= reviews <= 500: score += 30; factors.append("Established review volume (+30)")
    elif reviews >= 10: score += 15; factors.append("Some customer validation (+15)")
    if website: score += 20; factors.append("Website available (+20)")
    else: factors.append("No website found — digital-presence opportunity")
    if phone: score += 12; factors.append("Direct phone contact available (+12)")
    score = min(100, score)
    priority = "High" if score >= 70 else "Medium" if score >= 40 else "Low"
    return score, priority, factors
