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

## Autograder Timeline

### November 11, 2025 - Autograder Run
```
=== SCORE BREAKDOWN ===
SCORE part=part1 metric=program_exists points=1/1
SCORE part=part1 metric=zip_table_created points=2/2
SCORE part=part1 metric=county_table_created points=2/2
SCORE part=part1 metric=zip_schema points=1/1
SCORE part=part1 metric=county_schema points=1/1
SCORE part=part1 metric=zip_rows points=1/1
SCORE part=part1 metric=county_rows points=1/1
SCORE part=part1 metric=wy_select points=1/1
SCORE part=part1 metric=hw4test_created points=2/2
SCORE part=part1 metric=hw4test_rows points=1/1
SCORE part=part1 metric=hw4test_schema points=1/1
SCORE part=part1 metric=hw4test_select points=1/1
PART1_TOTAL 15/15
SCORE part=part2 metric=link_format points=2/2
SCORE part=part2 metric=url_get points=2/2
SCORE part=part2 metric=url_post points=2/2
SCORE part=part2 metric=obesity points=0/10
SCORE part=part2 metric=poverty points=0/4
SCORE part=part2 metric=fpm points=0/2
SCORE part=part2 metric=teapot1 points=0/2
SCORE part=part2 metric=teapot2 points=0/1
SCORE part=part2 metric=teapot3 points=0/1
SCORE part=part2 metric=teapot4 points=0/1
SCORE part=part2 metric=ziponly points=0/2
SCORE part=part2 metric=notfound points=0/2
SCORE part=part2 metric=wrong_endpoint points=0/2
SCORE part=part2 metric=no500 points=0/2
PART2_TOTAL 6/35
OVERALL_TOTAL 21/50
```

### January 6, 2026
Score on Canvas still shows 21/50.
