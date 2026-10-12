"""Export leads to CSV or Excel."""
import csv
from openpyxl import Workbook

FIELDS = ["name", "category", "city", "address", "phone", "email", "score"]


def to_csv(leads, path):
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(leads)
    return path


def to_excel(leads, path):
    wb = Workbook()
    ws = wb.active
    ws.title = "Leads"
    ws.append(FIELDS)
    for lead in leads:
        ws.append([lead.get(f) for f in FIELDS])
    wb.save(path)
    return path
