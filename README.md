# HW4 - API Prototyping with Generative AI

## Overview
This project implements a county health data API endpoint that queries health statistics by ZIP code and measure name.

## Files
- `csv_to_sqlite.py` - Script to convert CSV files to SQLite database
- `link.txt` - URL to deployed API endpoint
- `county-api/api.py` - FastAPI application for the `/county_data` endpoint
- `vercel.json` - Vercel deployment configuration

## API Usage
POST to `/county_data` with JSON body:
```json
{"zip": "02138", "measure_name": "Adult obesity"}
```

## Deployment
Deployed on Vercel at: https://emmamiao-hw4.vercel.app/county_data
