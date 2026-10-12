import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

import db
from collector import parse_element
from scoring import score_lead


def test_website_scores_zero():
    assert score_lead({"name": "A", "website": "https://a.co.ke"}) == 0


def test_no_website_scores_high():
    lead = {"name": "A", "phone": "0700", "email": "a@a.com",
            "address": "1 Main St", "category": "restaurant"}
    assert score_lead(lead) == 100


def test_basic_no_website():
    assert score_lead({"name": "A"}) == 50


def test_parse_element_extracts_fields():
    el = {"type": "node", "id": 1, "lat": -1.2, "lon": 36.8,
          "tags": {"name": "Mama Shop", "shop": "convenience",
                   "addr:street": "Moi Ave", "contact:phone": "0711"}}
    lead = parse_element(el, "Nairobi")
    assert lead["osm_id"] == "node/1"
    assert lead["category"] == "convenience"
    assert lead["phone"] == "0711"
    assert lead["website"] is None


def test_parse_element_skips_unnamed():
    assert parse_element({"type": "node", "id": 2, "tags": {"shop": "x"}}, "Nairobi") is None


def test_db_roundtrip(tmp_path):
    path = str(tmp_path / "t.db")
    db.init_db(path)
    lead = {"osm_id": "node/1", "name": "A", "category": "cafe", "city": "N",
            "address": None, "phone": None, "email": None, "website": None,
            "lat": 0, "lon": 0, "score": 55}
    db.upsert_leads([lead], path)
    db.upsert_leads([{**lead, "score": 70}], path)  # update, not duplicate
    rows = db.get_leads(1, path=path)
    assert len(rows) == 1 and rows[0]["score"] == 70
