# LeadFinder

A Python tool that finds local businesses **without a website**, scores them as
potential web-design leads, and lets you browse and export them.

Built for freelancers and small agencies who want a ready list of prospects
instead of searching business by business.

## How it works

1. **Collect**: queries OpenStreetMap's [Overpass API](https://overpass-api.de/) for every named
   shop, amenity, office, tourism and craft business in a city.
2. **Score**: `scoring.py` gives each business 0-100. No website is the main signal;
   having a phone, email, address, or a high-value category (restaurant, clinic, school...) raises it.
   Businesses that already have a website score 0.
3. **Store**: results are saved in SQLite (`leads.db`), updated in place on re-runs.
4. **Browse / export**: a Flask dashboard with filters, plus CSV and Excel export.

## Setup

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Usage

```bash
python main.py collect --city Nairobi        # fetch + score businesses
python main.py serve                         # dashboard at http://127.0.0.1:5000
python main.py export --format xlsx --min-score 60
```

## Project structure

| File | Purpose |
|------|---------|
| `collector.py` | Overpass API query and parsing |
| `scoring.py` | Lead scoring rules |
| `db.py` | SQLite storage |
| `export.py` | CSV / Excel export |
| `app.py` | Flask dashboard |
| `main.py` | Command-line interface |
| `tests/` | pytest tests |

## Tests

```bash
pytest
```

## Limitations

- Data comes from OpenStreetMap, so coverage varies by area and some businesses may
  have a website that was never added to the map.
- City names must match the OSM administrative boundary name.

## Ideas for next steps

- Optional Google Places collector for better coverage
- Check each lead's website tag for dead links
- Email outreach templates

## AI assistance

Parts of this project were written with help from Claude (Anthropic) and reviewed and tested by me.
