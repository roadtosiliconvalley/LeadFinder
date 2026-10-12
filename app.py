"""Flask dashboard for browsing and exporting leads."""
import io
from flask import Flask, render_template_string, request, Response
import db
from export import FIELDS

app = Flask(__name__)

PAGE = """
<!doctype html>
<title>LeadFinder</title>
<style>
  body{font-family:system-ui,sans-serif;margin:2rem;color:#222}
  table{border-collapse:collapse;width:100%}
  th,td{border-bottom:1px solid #ddd;padding:.5rem;text-align:left}
  th{background:#f4f4f4} form{margin-bottom:1rem}
  .score{font-weight:bold}
</style>
<h1>LeadFinder</h1>
<form method="get">
  Min score <input type="number" name="min_score" value="{{ min_score }}" min="0" max="100">
  Category
  <select name="category">
    <option value="">All</option>
    {% for c in categories %}
      <option value="{{ c }}" {{ 'selected' if c == category else '' }}>{{ c }}</option>
    {% endfor %}
  </select>
  <button>Filter</button>
  <a href="/export.csv?min_score={{ min_score }}&category={{ category or '' }}">Download CSV</a>
</form>
<p>{{ leads|length }} leads</p>
<table>
  <tr>{% for f in fields %}<th>{{ f }}</th>{% endfor %}</tr>
  {% for l in leads %}
  <tr>{% for f in fields %}<td class="{{ 'score' if f == 'score' }}">{{ l[f] or '' }}</td>{% endfor %}</tr>
  {% endfor %}
</table>
"""


def _filters():
    min_score = request.args.get("min_score", default=1, type=int)
    category = request.args.get("category") or None
    return min_score, category


@app.route("/")
def index():
    min_score, category = _filters()
    return render_template_string(
        PAGE,
        leads=db.get_leads(min_score, category),
        categories=db.get_categories(),
        fields=FIELDS,
        min_score=min_score,
        category=category,
    )


@app.route("/export.csv")
def export_csv():
    import csv
    min_score, category = _filters()
    buf = io.StringIO()
    writer = csv.DictWriter(buf, fieldnames=FIELDS, extrasaction="ignore")
    writer.writeheader()
    writer.writerows(db.get_leads(min_score, category))
    return Response(
        buf.getvalue(),
        mimetype="text/csv",
        headers={"Content-Disposition": "attachment; filename=leads.csv"},
    )


if __name__ == "__main__":
    db.init_db()
    app.run(debug=True)
