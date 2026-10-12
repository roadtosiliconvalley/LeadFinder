"""Lead scoring: higher score = better prospect for web design services."""

# Business types that usually benefit most from a website.
HIGH_VALUE_CATEGORIES = {
    "restaurant", "cafe", "hotel", "guest_house", "clinic", "doctors",
    "dentist", "pharmacy", "school", "kindergarten", "college", "hairdresser",
    "beauty", "gym", "car_repair", "lawyer", "estate_agent",
}


def has_website(lead):
    return bool((lead.get("website") or "").strip())


def score_lead(lead):
    """Return an integer 0-100. Businesses that already have a website score 0."""
    if has_website(lead):
        return 0
    score = 50  # no web presence is the main signal
    if lead.get("phone"):
        score += 20  # reachable
    if lead.get("email"):
        score += 10
    if lead.get("address"):
        score += 5
    if lead.get("category") in HIGH_VALUE_CATEGORIES:
        score += 15
    return min(score, 100)
