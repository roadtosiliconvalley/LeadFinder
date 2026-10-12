"""SQLite storage for leads."""
import sqlite3
from contextlib import closing

DB_PATH = "leads.db"

SCHEMA = """
CREATE TABLE IF NOT EXISTS leads (
    osm_id   TEXT PRIMARY KEY,
    name     TEXT NOT NULL,
    category TEXT,
    city     TEXT,
    address  TEXT,
    phone    TEXT,
    email    TEXT,
    website  TEXT,
    lat      REAL,
    lon      REAL,
    score    INTEGER DEFAULT 0
);
"""


def connect(path=DB_PATH):
    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row
    return conn


def init_db(path=DB_PATH):
    with closing(connect(path)) as conn:
        conn.executescript(SCHEMA)
        conn.commit()


def upsert_leads(leads, path=DB_PATH):
    """Insert new leads or update existing ones (matched by osm_id)."""
    sql = """
    INSERT INTO leads (osm_id, name, category, city, address, phone, email,
                       website, lat, lon, score)
    VALUES (:osm_id, :name, :category, :city, :address, :phone, :email,
            :website, :lat, :lon, :score)
    ON CONFLICT(osm_id) DO UPDATE SET
        name=excluded.name, category=excluded.category, city=excluded.city,
        address=excluded.address, phone=excluded.phone, email=excluded.email,
        website=excluded.website, lat=excluded.lat, lon=excluded.lon,
        score=excluded.score
    """
    with closing(connect(path)) as conn:
        conn.executemany(sql, leads)
        conn.commit()
    return len(leads)


def get_leads(min_score=1, category=None, path=DB_PATH):
    query = "SELECT * FROM leads WHERE score >= ?"
    params = [min_score]
    if category:
        query += " AND category = ?"
        params.append(category)
    query += " ORDER BY score DESC, name"
    with closing(connect(path)) as conn:
        return [dict(r) for r in conn.execute(query, params)]


def get_categories(path=DB_PATH):
    with closing(connect(path)) as conn:
        rows = conn.execute(
            "SELECT DISTINCT category FROM leads WHERE category IS NOT NULL ORDER BY category"
        )
        return [r[0] for r in rows]
