from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
import sqlite3
import re

app = FastAPI()

DB_PATH = "data.db"

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

def query_db(zip_code: str, measure_name: str):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    # Join on county + state_abbreviation instead of county_code.
    # Also handle ZIPs that may be stored without a leading 0: compare both the 5-digit and ltrimmed version.
    sql = """
        SELECT h.*
        FROM county_health_rankings h
        JOIN zip_county z
          ON z.county = h.county
         AND z.state_abbreviation = h.state
        WHERE h.measure_name = ?
          AND (z.zip = ? OR z.zip = ltrim(?, '0'))
    """
    cur.execute(sql, (measure_name, zip_code, zip_code))
    rows = cur.fetchall()
    conn.close()
    return [dict(row) for row in rows]

@app.post("/county_data")
async def county_data(request: Request):
    data = await request.json()

    if data.get("coffee") == "teapot":
        raise HTTPException(status_code=418, detail="I'm a teapot")

    zip_code = data.get("zip")
    measure_name = data.get("measure_name")

    if not zip_code or not measure_name:
        raise HTTPException(status_code=400, detail="zip and measure_name required")

    if not ZIP_RE.match(zip_code):
        raise HTTPException(status_code=400, detail="Invalid ZIP code format")
    if measure_name not in VALID_MEASURES:
        raise HTTPException(status_code=404, detail="measure_name not recognized")

    results = query_db(zip_code, measure_name)
    if not results:
        raise HTTPException(status_code=404, detail="No results found")

    return JSONResponse(content=results)
