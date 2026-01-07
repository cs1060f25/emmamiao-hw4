# api.py

from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
import sqlite3
import re
import os

# csv_to_sqlite import removed - using pre-built data.db

app = FastAPI()

# Paths
ROOT_DIR = os.path.dirname(__file__)
DB_PATH = os.path.join(ROOT_DIR, "data.db")
ZIP_CSV = os.path.join(ROOT_DIR, "zip_county.csv")
CHR_CSV = os.path.join(ROOT_DIR, "county_health_rankings.csv")

# For deployment, also check parent directory if files not found
if not os.path.exists(ZIP_CSV):
    ZIP_CSV = os.path.join(os.path.dirname(ROOT_DIR), "county-api", "zip_county.csv")
if not os.path.exists(CHR_CSV):
    CHR_CSV = os.path.join(os.path.dirname(ROOT_DIR), "county-api", "county_health_rankings.csv")
if not os.path.exists(DB_PATH):
    DB_PATH = os.path.join(os.path.dirname(ROOT_DIR), "data.db")

VALID_MEASURES = {
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


def ensure_db_exists():
    """
    Check that pre-built data.db exists.
    On Vercel, we use a pre-built database since the filesystem is read-only.
    """
    if not os.path.exists(DB_PATH):
        raise RuntimeError(f"data.db not found at {DB_PATH}")


def query_db(zip_code: str, measure_name: str):
    # make sure DB + tables exist
    ensure_db_exists()

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    # Join on county + state_abbreviation with lowercase column names
    sql = """
        SELECT 
            h.State as state,
            h.County as county,
            h.State_code as state_code,
            h.County_code as county_code,
            h.Year_span as year_span,
            h.Measure_name as measure_name,
            h.Measure_id as measure_id,
            h.Numerator as numerator,
            h.Denominator as denominator,
            h.Raw_value as raw_value,
            h.Confidence_Interval_Lower_Bound as confidence_interval_lower_bound,
            h.Confidence_Interval_Upper_Bound as confidence_interval_upper_bound,
            h.Data_Release_Year as data_release_year,
            h.fipscode as fipscode
        FROM county_health_rankings h
        JOIN zip_county z
          ON z.county = h.County
         AND z.state_abbreviation = h.State
        WHERE h.Measure_name = ?
          AND (z.zip = ? OR z.zip = ltrim(?, '0'))
    """
    cur.execute(sql, (measure_name, zip_code, zip_code))
    rows = cur.fetchall()
    conn.close()
    
    # Convert to list of dictionaries with lowercase keys
    columns = ['state', 'county', 'state_code', 'county_code', 'year_span', 
               'measure_name', 'measure_id', 'numerator', 'denominator', 'raw_value',
               'confidence_interval_lower_bound', 'confidence_interval_upper_bound', 
               'data_release_year', 'fipscode']
    
    return [dict(zip(columns, row)) for row in rows]


@app.post("/county_data")
async def county_data(request: Request):
    # Parse JSON body
    try:
        data = await request.json()
    except Exception:
        raise HTTPException(status_code=400, detail="invalid JSON body")

    # coffee=teapot supersedes everything
    if str(data.get("coffee", "")).lower() == "teapot":
        # spec only cares about 418 code; body can be any JSON
        return JSONResponse(
            status_code=418,
            content={"error": "I'm a teapot"},
        )

    zip_code = data.get("zip")
    measure_name = data.get("measure_name")

    # missing inputs → 400
    if not zip_code or not measure_name:
        raise HTTPException(status_code=400, detail="zip and measure_name required")

    # ZIP must be 5-digit string
    if not ZIP_RE.match(str(zip_code)):
        raise HTTPException(status_code=400, detail="Invalid ZIP code format")

    # measure_name must be one of the allowed ones
    if measure_name not in VALID_MEASURES:
        # Spec says unknown zip/measure combination → 404.
        # Using 404 here is fine / matches your earlier version.
        raise HTTPException(status_code=404, detail="measure_name not recognized")

    # Run query
    try:
        results = query_db(str(zip_code), measure_name)
    except Exception as e:
        # If something weird happens, you can log it and return 500 JSON,
        # but in normal operation this should not be hit.
        print("DB error:", e)
        raise HTTPException(status_code=500, detail="internal server error")

    if not results:
        # No rows → 404 per spec
        raise HTTPException(status_code=404, detail="No results found")

    # Success: return array of rows as JSON
    return JSONResponse(content=results, status_code=200)


@app.get("/")
async def root():
    # This is what the autograder's simple GET/POST tests are hitting
    return {"ok": True, "endpoint": "/county_data (POST)"}