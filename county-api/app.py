import os, re, sqlite3
from flask import Flask, request, jsonify, abort

app = Flask(__name__)

# Per-spec allowed measure names
ALLOWED_MEASURES = {
    "Violent crime rate",
    "Unemployment",
    "Children in poverty",
    "Diabetic screening",
    "Mammography screening",
    "Preventable hospital stays",
    "Uninsured",
    "Sexually transmitted infections",
    "Physical inactivity",
    "Adult obesity",
    "Premature Death",
    "Daily fine particulate matter",
}

ZIP_RE = re.compile(r"^\d{5}$")

# Where the DB lives (overrideable via env for deployment)
DB_PATH = os.environ.get("DB_PATH", os.path.join(os.path.dirname(__file__), "..", "data.db"))

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

@app.post("/county_data")
def county_data():
    # Must accept application/json
    try:
        body = request.get_json(force=True, silent=False) or {}
    except Exception:
        return jsonify({"error": "bad request"}), 400

    # 418 Easter egg supersedes everything
    if str(body.get("coffee", "")).lower() == "teapot":
        return jsonify({"error": "I’m a teapot"}), 418

    # Required inputs
    zip_code = body.get("zip")
    measure_name = body.get("measure_name")

    if not zip_code or not measure_name:
        return jsonify({"error": "zip and measure_name are required"}), 400
    if not ZIP_RE.match(str(zip_code)):
        return jsonify({"error": "zip must be a 5-digit string"}), 400
    if measure_name not in ALLOWED_MEASURES:
        return jsonify({"error": "measure_name not allowed"}), 400

    # Parameterized SQL (sanitized) — join via county + state_abbreviation
    sql = """
    SELECT chr.*
    FROM county_health_rankings AS chr
    WHERE chr.measure_name = ?
      AND EXISTS (
        SELECT 1
        FROM zip_county AS z
        WHERE z.zip = ?
          AND z.county = chr.county
          AND z.state_abbreviation = chr.state
      );
    """
    params = (measure_name, zip_code)

    with get_db() as con:
        rows = con.execute(sql, params).fetchall()

    if not rows:
        return jsonify({"error": "zip/measure_name not found"}), 404

    return jsonify([dict(r) for r in rows]), 200

# Default 404 & 400 JSON
@app.errorhandler(404)
def _404(_):
    return jsonify({"error": "not found"}), 404

@app.errorhandler(400)
def _400(_):
    return jsonify({"error": "bad request"}), 400

# Optional liveness check
@app.get("/")
def root():
    return jsonify({"ok": True, "endpoint": "/county_data (POST)"}), 200
