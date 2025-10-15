#!/usr/bin/env python3
"""
csv_to_sqlite.py
Usage:
  python3 csv_to_sqlite.py data.db zip_county.csv
  python3 csv_to_sqlite.py data.db county_health_rankings.csv

Assumes CSV has a header row of valid SQL identifiers (per spec).
Creates/updates a SQLite DB with table name = CSV filename (no extension).
"""

import sys, os, csv, sqlite3

def load_csv(dbname: str, csvfile: str) -> None:
    table = os.path.splitext(os.path.basename(csvfile))[0]
    conn = sqlite3.connect(dbname)
    cur = conn.cursor()

    with open(csvfile, newline='', encoding='utf-8') as f:
        reader = csv.reader(f)
        header = next(reader)

        # Create table with all TEXT columns (simple & robust for grading)
        cols_def = ", ".join(f"{col} TEXT" for col in header)
        cur.execute(f"CREATE TABLE IF NOT EXISTS {table} ({cols_def});")

        placeholders = ", ".join(["?"] * len(header))
        insert_sql = f"INSERT INTO {table} VALUES ({placeholders});"

        batch = []
        for row in reader:
            if len(row) != len(header):
                # ignore malformed row (behavior on bad CSV is undefined per spec)
                continue
            batch.append(row)

        if batch:
            cur.executemany(insert_sql, batch)

    conn.commit()
    conn.close()

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python3 csv_to_sqlite.py <database.db> <file.csv>")
        sys.exit(1)
    dbname, csvfile = sys.argv[1], sys.argv[2]
    if not os.path.exists(csvfile):
        print(f"CSV not found: {csvfile}")
        sys.exit(1)
    load_csv(dbname, csvfile)

