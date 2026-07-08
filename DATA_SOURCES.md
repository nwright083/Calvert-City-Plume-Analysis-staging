# External data sources & files

Everything this project depends on that comes from **outside the code**. Three categories:

1. **In the repo already** — committed, just update periodically.
2. **Needed for full local runs, NOT in the repo** — the EPA AQS monitor CSVs (too large to commit;
   they live on Google Drive). The cloud/nightly pipeline runs fine without them.
3. **Fetched automatically at run time** — weather, HYSPLIT, eccodes. No maintenance.

> **Handoff action items** are called out in **bold** below (get your own AQS key; get access to the
> Drive folder; know how to refresh the yearly TRI data).

---

## 1. Committed to the repo (update periodically)

| File | What it is | Source | Used for | Refresh |
|---|---|---|---|---|
| `Marshall County Facility Release.csv` | **EPA TRI emissions** (Toxics Release Inventory), **2024**, all facilities in Marshall County | EPA TRI — [TRI Explorer](https://enviro.epa.gov/triexplorer/) / [TRI data files](https://www.epa.gov/toxics-release-inventory-tri-program/tri-data-and-tools) | Facility locations + per-chemical **stack/fugitive air release rates** (the emission source of truth) | EPA publishes a new year ~each fall (2025 finalizes ~fall 2026). Download the newer year, keep the same columns/filename, and re-run all dates. |
| `CalvertDailyVOCS_DateEnding6.30.2025.xlsx` | The research group's **own VOC canister sampling** (sites CC_18 Calvert City Elementary, CC_20 Johnson-Riley, CC_21 LWD) | Internal (SRSP air-monitoring program) | The **VOC monitor overlay** (nearest available sample per date) | When new sampling is collected, export a new xlsx and update the filename referenced in `calvert_plume_engine_one_day.py` (search `CalvertDailyVOCS`). |
| `api2arl.cfg` | HYSPLIT `api2arl_v6` GRIB→ARL variable-mapping config | HYSPLIT distribution (tuned for HRRR) | Weather conversion | Rarely — only if HRRR fields change. |

---

## 2. EPA AQS ambient-monitor data — NOT in the repo

The hourly EPA AQS CSVs (`hourly_<code>_<year>.csv`) are **git-ignored** (~1.5 GB each) and live on the
project **Google Drive**, not in the repo. They power the EPA monitor overlays (PM2.5, ozone, SO₂, NO₂, …)
— but **only for older dates**, because AQS publishes months late. The **nightly/cloud runs don't use them
at all** (they're not on the runner), so recent dates simply show the local VOC layer instead. They only
matter if you run the engine **locally** and want the EPA overlays populated.

| Item | Detail |
|---|---|
| **File pattern** | `hourly_88101_2025.csv` (PM2.5), `hourly_44201_*.csv` (Ozone), `hourly_42401` (SO₂), `hourly_42602` (NO₂), `hourly_81102` (PM10), `hourly_NONOxNOy` (NO/NOₓ) — one per parameter per year |
| **Where they live** | Project Google Drive: `…/My Drive/Med school/SRSP Project/Plume Analysis/` (see `_DRIVE_DIR` in the engine). The engine reads them from the working dir if present, else that Drive path. |
| **How to (re)generate** | `python3 fetch_aqs_data.py --years 2024,2025` — pulls them from the [EPA AQS API](https://aqs.epa.gov/aqsweb/documents/data_api.html) for Kentucky counties Marshall/McCracken/Livingston |
| **⚠️ Credentials** | `fetch_aqs_data.py` currently defaults to a **personal AQS email + key** (lines ~184–185). **Get your own free key** (register at the AQS API link above) and pass `--email you@… --key yourkey`, or edit the defaults. Don't rely on the committed one. |
| **Handoff** | **Either** get shared access to the Drive folder for the existing CSVs, **or** just re-fetch them with your own key. |

---

## 3. Fetched automatically at run time (no maintenance)

| Dependency | Source | When |
|---|---|---|
| **NOAA HRRR weather** (3-km hourly analysis GRIB2) | NOAA HRRR archive on AWS S3, via the [Herbie](https://github.com/blaylockbk/Herbie) library | Every run, per simulated day (streamed + deleted) |
| **HYSPLIT** (`hysplit.v5.4.2_x86_64_public`, static Linux build) | NOAA public URL (`ready.noaa.gov/…/hysplit.v5.4.2_x86_64_public.tar.gz`), verified by SHA1 | CI: first run then cached. Locally: install once and point `HYSPLIT_ROOT` at it. |
| **eccodes 2.17.0 definitions** | ECMWF eccodes 2.17.0 source (GitHub) — must match HYSPLIT's embedded eccodes | CI: first run then cached |
| Python packages | `requirements-ci.txt` (Herbie, xarray, cfgrib, pandas, openpyxl, …) | `pip install -r requirements-ci.txt` |

**No secrets are required** for the core pipeline — HYSPLIT is a public URL and HRRR is open data. The only
credential anywhere is the optional AQS key above.

---

## Quick handoff checklist for the AQS/Drive pieces
- [ ] Register your own **EPA AQS API key** (free) and update `fetch_aqs_data.py` defaults or pass flags.
- [ ] Decide: share the existing AQS CSVs from Google Drive, **or** re-fetch with `fetch_aqs_data.py`.
- [ ] Note the **TRI refresh** cadence (yearly) so emissions don't go stale.
- [ ] Keep collecting/updating the **VOC xlsx** as new sampling comes in.
