#!/bin/bash
set -e

echo "=== ✅ Valid request (02138, Adult obesity) ==="
curl -s -H "content-type: application/json" \
  -d '{"zip":"02138","measure_name":"Adult obesity"}' \
  http://127.0.0.1:8000/county_data | jq . || true

echo -e "\n=== ☕ Teapot test (418) ==="
curl -s -w "\nHTTP %{http_code}\n" -H "content-type: application/json" \
  -d '{"zip":"02138","measure_name":"Adult obesity","coffee":"teapot"}' \
  http://127.0.0.1:8000/county_data

echo -e "\n=== 🚫 Missing fields (400) ==="
curl -s -w "\nHTTP %{http_code}\n" -H "content-type: application/json" \
  -d '{"zip":"02138"}' \
  http://127.0.0.1:8000/county_data

echo -e "\n=== ❌ Invalid measure (404) ==="
curl -s -w "\nHTTP %{http_code}\n" -H "content-type: application/json" \
  -d '{"zip":"02138","measure_name":"Adult obesitee"}' \
  http://127.0.0.1:8000/county_data
