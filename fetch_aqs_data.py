#!/usr/bin/env python3
"""
fetch_aqs_data.py

Fetches hourly air quality data from the EPA Air Quality System (AQS) API for
Calvert City, Kentucky (Marshall County) and surrounding counties (McCracken, Livingston)
for the years 2024 and 2025. Maps the API JSON fields to the exact CSV schema
expected by the HYSPLIT Calvert City Plume Engine.
"""

import os
import sys
import csv
import json
import argparse
import requests
import time

# Target location parameters
STATE_FIPS = "21"  # Kentucky
COUNTIES = {
    "157": "Marshall",
    "145": "McCracken",
    "139": "Livingston"
}

# Parameter mapping: each entry is (param_code, output_filename_prefix, display_name)
PARAMETERS = [
    ("88101", "hourly_88101",     "PM2.5"),
    ("44201", "hourly_44201",     "Ozone"),
    ("42401", "hourly_42401",     "SO2"),
    ("42602", "hourly_42602",     "NO2"),
    ("81102", "hourly_81102",     "PM10"),
    ("42601", "hourly_NONOxNOy",  "NO"),
    ("42603", "hourly_NONOxNOy",  "NOx"),
]

# Standard CSV headers expected by the plume engine
CSV_HEADERS = [
    "State Code", "County Code", "Site Num", "Parameter Code", "POC",
    "Latitude", "Longitude", "Datum", "Parameter Name", "Date Local",
    "Time Local", "Date GMT", "Time GMT", "Sample Measurement", "Units of Measure",
    "MDL", "Uncertainty", "Qualifier", "Method Type", "Method Code",
    "Method Name", "State Name", "County Name", "Date of Last Change"
]


def query_aqs(email, key, param, bdate, edate, state, county, max_retries=3):
    """Makes a GET request to the AQS sampleData/byCounty endpoint with retries."""
    url = "https://aqs.epa.gov/data/api/sampleData/byCounty"
    params = {
        "email": email, "key": key, "param": param,
        "bdate": bdate, "edate": edate, "state": state, "county": county
    }
    for attempt in range(max_retries):
        try:
            resp = requests.get(url, params=params, timeout=180)
            if resp.status_code != 200:
                print(f" HTTP {resp.status_code}", end="", flush=True)
                time.sleep(5 * (attempt + 1))
                continue
            data = resp.json()
            header = data.get("Header", [{}])
            if isinstance(header, list):
                header = header[0]
            status = header.get("status", "")
            if "Success" in status:
                return data.get("Data", [])
            elif "no data" in status.lower():
                return []
            elif "Invalid" in status:
                print(f" INVALID: {status}", end="", flush=True)
                return None
            else:
                print(f" [{status}]", end="", flush=True)
                time.sleep(5)
                continue
        except requests.exceptions.Timeout:
            print(f" TIMEOUT", end="", flush=True)
            time.sleep(10)
        except Exception as e:
            print(f" ERR({e})", end="", flush=True)
            time.sleep(5)
    return None


def map_record_to_row(record):
    """Maps an AQS JSON record to a CSV row matching CSV_HEADERS."""
    county_code = str(record.get("county_code", "")).strip().zfill(3)
    county_name = record.get("county", "").strip()
    if not county_name and county_code in COUNTIES:
        county_name = COUNTIES[county_code]

    # Handle null sample_measurement
    sample_meas = record.get("sample_measurement")
    if sample_meas is None:
        sample_meas = ""
    else:
        sample_meas = str(sample_meas)

    # API returns 'detection_limit' which maps to the CSV 'MDL' column
    mdl = record.get("detection_limit", "")
    if mdl is None:
        mdl = ""

    uncertainty = record.get("uncertainty", "")
    if uncertainty is None:
        uncertainty = ""

    qualifier = record.get("qualifier", "")
    if qualifier is None:
        qualifier = ""

    return [
        str(record.get("state_code", "")).strip().zfill(2),
        county_code,
        str(record.get("site_number", "")).strip().zfill(4),
        str(record.get("parameter_code", "")).strip(),
        str(record.get("poc", "")),
        str(record.get("latitude", "")),
        str(record.get("longitude", "")),
        record.get("datum", "WGS84") or "WGS84",
        record.get("parameter", "").strip(),
        record.get("date_local", "").strip(),
        record.get("time_local", "").strip(),
        record.get("date_gmt", "").strip(),
        record.get("time_gmt", "").strip(),
        sample_meas,
        (record.get("units_of_measure") or "").strip(),
        str(mdl),
        str(uncertainty),
        str(qualifier),
        (record.get("method_type") or "").strip(),
        str(record.get("method_code", "")).strip(),
        (record.get("method") or "").strip(),
        (record.get("state") or "Kentucky").strip(),
        county_name,
        (record.get("date_of_last_change") or "").strip()
    ]


def validate_csv(filepath):
    """Performs validation checks on the saved CSV file."""
    if not os.path.exists(filepath):
        print(f"  FAIL: File does not exist")
        return False
    with open(filepath, "r", encoding="utf-8") as f:
        reader = list(csv.reader(f))
    if len(reader) < 2:
        print(f"  Header only (0 data rows)")
        return True
    headers = reader[0]
    if headers != CSV_HEADERS:
        print(f"  FAIL: Header mismatch!")
        return False
    data_rows = reader[1:]
    total = len(data_rows)
    missing = sum(1 for r in data_rows if r[13] == "" or r[13] == "None")
    negative = 0
    for r in data_rows:
        try:
            if r[13] and float(r[13]) < 0:
                negative += 1
        except (ValueError, IndexError):
            pass
    dates = sorted(set(r[9] for r in data_rows))
    counties = sorted(set(r[1] for r in data_rows))
    params = sorted(set(r[3] for r in data_rows))
    county_names = [COUNTIES.get(c, c) for c in counties]
    date_range = f"{dates[0]} to {dates[-1]}" if dates else "none"

    print(f"  ✓ {total} rows | {county_names} | params {params} | {date_range} ({len(dates)} days)")
    if missing:
        print(f"    ⚠ {missing} null measurements")
    if negative:
        print(f"    ⚠ {negative} negative measurements")
    return True


def main():
    parser = argparse.ArgumentParser(
        description="Fetch EPA AQS hourly air quality data for Calvert City, KY region."
    )
    parser.add_argument("--email", default="nawrig04@louisville.edu")
    parser.add_argument("--key", default="taupegazelle46")
    parser.add_argument("--years", default="2024,2025")
    parser.add_argument("--output-dir", default=".")
    args = parser.parse_args()

    years = [y.strip() for y in args.years.split(",") if y.strip()]
    output_dir = os.path.abspath(args.output_dir)

    print("=" * 70)
    print("EPA AQS Hourly Data Fetcher — Calvert City, KY")
    print("=" * 70)
    print(f"Years:    {years}")
    print(f"Counties: {COUNTIES}")
    print(f"Params:   {[(p[0], p[2]) for p in PARAMETERS]}")
    print(f"Output:   {output_dir}")
    print()

    # Accumulate rows per output file
    file_rows = {}
    total_api_calls = 0
    total_records = 0

    for year in years:
        bdate = f"{year}0101"
        edate = f"{year}1231"

        for param_code, file_prefix, display_name in PARAMETERS:
            filename = f"{file_prefix}_{year}.csv"
            filepath = os.path.join(output_dir, filename)

            for county_code, county_name in COUNTIES.items():
                label = f"[{year}] {display_name:6s} ({param_code}) | {county_name:12s}"
                print(f"{label}...", end="", flush=True)

                records = query_aqs(
                    args.email, args.key, param_code,
                    bdate, edate, STATE_FIPS, county_code
                )
                total_api_calls += 1

                if records is None:
                    print(" FAILED")
                elif len(records) == 0:
                    print(" no data")
                else:
                    print(f" {len(records):,} records")
                    total_records += len(records)
                    if filepath not in file_rows:
                        file_rows[filepath] = []
                    for rec in records:
                        file_rows[filepath].append(map_record_to_row(rec))

                # Small delay to be kind to the API
                time.sleep(0.5)

    # Write output files
    print()
    print("=" * 70)
    print("Writing & Validating Output Files")
    print("=" * 70)

    for filepath in sorted(file_rows.keys()):
        rows = file_rows[filepath]
        basename = os.path.basename(filepath)
        print(f"\n{basename} ({len(rows):,} rows)...")
        with open(filepath, "w", encoding="utf-8", newline="") as f:
            writer = csv.writer(f, quoting=csv.QUOTE_ALL)
            writer.writerow(CSV_HEADERS)
            writer.writerows(rows)
        validate_csv(filepath)

    # Create empty placeholders for VOCs and HAPs (not queryable by simple param code)
    for year in years:
        for tag in ["VOCS", "HAPS"]:
            filename = f"hourly_{tag}_{year}.csv"
            filepath = os.path.join(output_dir, filename)
            if filepath not in file_rows:
                print(f"\n{filename} — empty placeholder (no simple AQS param code)")
                with open(filepath, "w", encoding="utf-8", newline="") as f:
                    writer = csv.writer(f, quoting=csv.QUOTE_ALL)
                    writer.writerow(CSV_HEADERS)

    print()
    print("=" * 70)
    print(f"COMPLETE: {total_api_calls} API calls, {total_records:,} total records retrieved")
    print("=" * 70)


if __name__ == "__main__":
    main()
