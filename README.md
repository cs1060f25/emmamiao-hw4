# Homework 4 — API Prototyping with Generative AI  
**Course:** CS1060 (Fall 2025)  
**Author:** Emma Miao  
**Repository:** `emmamiao-hw4`

---

## 🧠 Overview
This project builds and deploys an API prototype that merges two public datasets — **ZIP code to county mappings** and **County Health Rankings** — into a unified SQLite database and exposes a `/county_data` endpoint through Flask.

The implementation satisfies all assignment requirements:
- ✅ `csv_to_sqlite.py` converts valid CSVs into tables in `data.db`
- ✅ `/county_data` endpoint returns health data filtered by ZIP and measure
- ✅ Proper handling of all required HTTP status codes (400, 404, 418)
- ✅ Input sanitization with parameterized SQL queries
- ✅ Fully tested locally and deployable to Render or Vercel

---

## ⚙️ File Structure
```
emmamiao-hw4/
├── csv_to_sqlite.py          # Converts CSV files → SQLite tables
├── county-api/
│   ├── app.py                # Flask API implementing /county_data
│   ├── data.db               # Generated database (local testing)
│   ├── vercel.json           # (Optional) Config for Vercel deployment
├── requirements.txt          # Flask + gunicorn dependencies
├── .gitignore
├── link.txt                  # URL to deployed API (no query params)
└── README.md                 # You are here
```

---

## 🧩 Part 1 — CSV → SQLite Conversion
Build `data.db` from the two required CSVs:

```bash
python3 csv_to_sqlite.py data.db zip_county.csv
python3 csv_to_sqlite.py data.db county_health_rankings.csv
```

Check the result:
```bash
sqlite3 data.db ".tables"
# → zip_county  county_health_rankings
```

---

## 🌐 Part 2 — Flask API Endpoint

### `/county_data` (POST)
**Request JSON:**
```json
{
  "zip": "02138",
  "measure_name": "Adult obesity"
}
```

**Response (sample):**
```json
[
  {
    "county": "Middlesex County",
    "state": "MA",
    "measure_name": "Adult obesity",
    "raw_value": "0.23",
    "year_span": "2009"
  }
]
```

### Error Handling
| Case | Description | HTTP Code |
|------|--------------|-----------|
| Missing `zip` or `measure_name` | Bad request | 400 |
| `"coffee": "teapot"` supplied | I’m a teapot (Easter egg) | 418 |
| No matching results | Not found | 404 |

---

## 🚀 Local Testing

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Build DB
python3 csv_to_sqlite.py data.db zip_county.csv
python3 csv_to_sqlite.py data.db county_health_rankings.csv

# Run API
export DB_PATH="$(pwd)/county-api/data.db"
python3 -m flask --app county-api/app.py run --port 5001
```

Then test in another terminal:
```bash
curl -s -X POST -H 'Content-Type: application/json' \
  -d '{"zip":"02138","measure_name":"Adult obesity"}' \
  http://127.0.0.1:5001/county_data | python3 -m json.tool
```

---

## ☁️ Deployment

The API can be deployed on **Render** or **Vercel**.  
Include the live endpoint (no query parameters) in `link.txt`.

Example `link.txt`:
```
https://emmamiao-hw4.onrender.com/county_data
```

Environment variable used during deployment:
```
DB_PATH=/opt/render/project/src/data.db
```

---

## ✅ Validation Checklist
- [x] `csv_to_sqlite.py` works on arbitrary valid CSVs  
- [x] `/county_data` meets spec for 400/404/418 behavior  
- [x] Uses parameterized SQL queries for safety  
- [x] Correct output schema and filtering  
- [x] Repo includes all required top-level files  

---

## 📚 References
- RowZero Zip Code → County Dataset (Feb 2025)  
- County Health Rankings & Roadmaps Analytic Data (Feb 2025)  
- Flask Docs: https://flask.palletsprojects.com  
- SQLite Docs: https://docs.python.org/3/library/sqlite3.html  
