"""Command-line entry point.

Examples:
    python main.py collect --city Nairobi
    python main.py export --format xlsx --min-score 60
    python main.py serve
"""
import argparse
import os

import db
from collector import fetch_leads
from export import to_csv, to_excel
from scoring import score_lead


def cmd_collect(args):
    db.init_db()
    leads = fetch_leads(args.city)
    for lead in leads:
        lead["score"] = score_lead(lead)
    db.upsert_leads(leads)
    hot = sum(1 for l in leads if l["score"] >= 60)
    print(f"Saved {len(leads)} businesses in {args.city} ({hot} strong leads).")


def cmd_export(args):
    leads = db.get_leads(args.min_score)
    os.makedirs("exports", exist_ok=True)
    path = f"exports/leads.{args.format}"
    (to_excel if args.format == "xlsx" else to_csv)(leads, path)
    print(f"Exported {len(leads)} leads to {path}")


def cmd_serve(_args):
    from app import app
    db.init_db()
    app.run(debug=True)


def main():
    parser = argparse.ArgumentParser(description="Find businesses without a website.")
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("collect", help="fetch businesses for a city")
    p.add_argument("--city", required=True)
    p.set_defaults(func=cmd_collect)

    p = sub.add_parser("export", help="export leads to a file")
    p.add_argument("--format", choices=["csv", "xlsx"], default="csv")
    p.add_argument("--min-score", type=int, default=1)
    p.set_defaults(func=cmd_export)

    p = sub.add_parser("serve", help="start the Flask dashboard")
    p.set_defaults(func=cmd_serve)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
