"""Collect businesses from OpenStreetMap using the Overpass API."""
import time
import requests

OVERPASS_URL = "https://overpass-api.de/api/interpreter"
CATEGORY_KEYS = ("shop", "amenity", "office", "tourism", "craft")


def build_query(city, timeout=60):
    """Overpass QL: every named shop/amenity/office/etc. inside the city area."""
    filters = "\n".join(
        f'  nwr["{key}"]["name"](area.a);' for key in CATEGORY_KEYS
    )
    return f"""
[out:json][timeout:{timeout}];
area["name"="{city}"]["boundary"="administrative"]->.a;
(
{filters}
);
out center tags;
"""


def parse_element(el, city):
    """Convert one raw Overpass element into a lead dict (or None to skip)."""
    tags = el.get("tags", {})
    name = tags.get("name")
    if not name:
        return None

    category = next((tags[k] for k in CATEGORY_KEYS if k in tags), None)
    center = el.get("center", {})
    street = " ".join(
        p for p in (tags.get("addr:housenumber"), tags.get("addr:street")) if p
    )
    address = ", ".join(p for p in (street, tags.get("addr:suburb")) if p)

    return {
        "osm_id": f"{el['type']}/{el['id']}",
        "name": name,
        "category": category,
        "city": city,
        "address": address or None,
        "phone": tags.get("phone") or tags.get("contact:phone"),
        "email": tags.get("email") or tags.get("contact:email"),
        "website": (
            tags.get("website") or tags.get("contact:website") or tags.get("url")
        ),
        "lat": el.get("lat", center.get("lat")),
        "lon": el.get("lon", center.get("lon")),
    }


def fetch_leads(city, retries=3):
    """Fetch and parse leads for a city. Retries when Overpass is busy."""
    query = build_query(city)
    for attempt in range(1, retries + 1):
        resp = requests.post(OVERPASS_URL, data={"data": query}, timeout=90)
        if resp.status_code in (429, 504):  # rate limited / server busy
            time.sleep(5 * attempt)
            continue
        resp.raise_for_status()
        elements = resp.json().get("elements", [])
        leads = (parse_element(e, city) for e in elements)
        return [l for l in leads if l]
    raise RuntimeError("Overpass API is busy, try again in a few minutes.")
