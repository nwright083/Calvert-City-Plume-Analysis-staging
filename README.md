# Calvert City Plume Analysis

An auto-updating public web dashboard that models the **airborne dispersion and ground deposition of
industrial chemicals** released from the facilities in Calvert City, Kentucky, and shows how the plume
moves over the surrounding community (Paducah, Benton, Marshall/McCracken/Livingston counties) each day.

Built for the SRSP environmental-health research project. Every night it simulates the **previous local
(Central-time) day** with NOAA weather + NOAA's HYSPLIT dispersion model, and publishes an interactive
Leaflet map to **GitHub Pages**.

- **Live site:** `https://<owner>.github.io/<repo>/` (GitHub Pages, source = GitHub Actions)
- **Runs itself:** nightly via `.github/workflows/daily-plume.yml` — no server, no cost (public repo)
- **Companion tool:** an "Odor Forecast" is linked from the control panel (separate repo)

---

## Table of contents
1. [Quick start](#quick-start)
2. [How it works (the nightly pipeline)](#how-it-works-the-nightly-pipeline)
3. [Repository layout](#repository-layout)
4. [Where to change things (config)](#where-to-change-things-config)
5. [Data model](#data-model)
6. [Methodology (the science)](#methodology-the-science)
7. [Running & operating it](#running--operating-it)
8. [Common maintenance tasks](#common-maintenance-tasks)
9. [Gotchas & hard-won lessons](#gotchas--hard-won-lessons-read-before-editing-the-pipeline)
10. [Known limitations](#known-limitations)
11. [Handoff / open items](#handoff--open-items)

---

## Quick start

**View the site locally** (the site fetches JSON, which browsers block over `file://`, so it needs a
tiny local server):

```bash
# double-click "View Locally.command"  — OR —
cd site && python3 -m http.server 8123   # then open http://localhost:8123
```

**Re-run one date locally** (needs a local HYSPLIT install + internet for weather — see
[Running & operating it](#running--operating-it)):

```bash
python3 calvert_plume_engine_one_day.py --date 2026-07-04   # simulate one day → writes site/data/dates/2026-07-04.json
python3 calvert_plume_engine_one_day.py --build-site        # rebuild index.html + app.js + manifest.json
```

**In the cloud (normal operation):** nothing — the nightly GitHub Action does everything. To force a run,
use **Actions → "Nightly plume update" → Run workflow** (inputs: `date`, `force`, `days_back`).

---

## How it works (the nightly pipeline)

Each night on a throwaway GitHub-hosted Linux runner (`.github/workflows/daily-plume.yml`, cron `0 7 * * *`
= 07:00 UTC ≈ 1–2 AM Central):

1. **Fetch tools** — download NOAA's public static HYSPLIT build (`hysplit.v5.4.2_x86_64_public`) and the
   matching **eccodes 2.17.0** GRIB definitions (both cached between runs).
2. **Weather** — for the target **local (Central) calendar day**, stream 24 hourly NOAA **HRRR** analysis
   files (via [Herbie](https://github.com/blaylockbk/Herbie)), converting each to a HYSPLIT `.ARL` met file
   and deleting the GRIB immediately (disk-frugal). The window is local-midnight-to-midnight, so it spans
   two UTC dates (e.g. 05:00 UTC → 05:00 UTC next day in summer/CDT).
3. **Dispersion** — run HYSPLIT (`hycs_std`):
   - **Particles** — one run per facility (elevated *stack* + ground *fugitive* sources) dumping particle
     positions hourly (`PARDUMP`), used to build the animated wind field.
   - **Deposition** — one run per *facility × chemical × source* producing a concentration grid (`cdump`),
     rendered to contours by `concplot` → KML → GeoJSON. Two products: **soil deposition** (g/m², cumulative)
     and **ground-level air** (g/m³, per hour).
4. **Assemble** — write a compact per-date **bundle** `site/data/dates/{date}.json` (facilities, wind grid,
   deposition/air footprints, monitor overlays).
5. **Build the site** — regenerate `site/index.html`, `site/app.js`, and `site/data/manifest.json` from all
   bundles; apply **retention** (keep newest 30 daily dates + pinned showcase days, prune the rest).
6. **Publish** — commit `site/` back to the branch (this *is* the rolling data store) and deploy to Pages.

The engine that does 2–5 is **`calvert_plume_engine_one_day.py`**; **`daily_update.py`** is the thin
orchestrator that decides which date(s) to run and tees logs.

---

## Repository layout

| Path | Role |
|---|---|
| `calvert_plume_engine_one_day.py` | **The engine.** Weather → HYSPLIT → GeoJSON → per-date bundle, plus the entire front-end (HTML/CSS/JS is a template string here, split into `site/index.html` + `site/app.js` at build time). |
| `daily_update.py` | **Orchestrator.** Picks the target date(s) (yesterday, or `--date`), runs the engine, rebuilds the site, exits with meaningful codes. Same script runs locally and in CI. |
| `.github/workflows/daily-plume.yml` | **The nightly CI.** Installs tools, runs `daily_update.py`, commits `site/` back, deploys Pages. |
| `Marshall County Facility Release.csv` | **TRI emissions data** (EPA Toxics Release Inventory, 2024) — per-facility, per-chemical stack/fugitive air release rates. The emissions source of truth. |
| `CalvertDailyVOCS_DateEnding6.30.2025.xlsx` | Local **VOC canister monitor** data (the research group's own sampling; ends 2025-06-30). |
| `fetch_aqs_data.py` | Optional helper to pull **EPA AQS** ambient-monitor CSVs (PM2.5, ozone, etc.). Not run by the nightly. |
| `api2arl.cfg` | Config for HYSPLIT's `api2arl_v6` GRIB→ARL converter. |
| `requirements-ci.txt` | Python deps for CI (Herbie, xarray, cfgrib, pandas, …). |
| `View Locally.command` | Double-clickable local preview server (macOS). |
| `site/` | **The published site.** `index.html` + `app.js` (fetch shell), `data/manifest.json` (date list), `data/dates/*.json` (per-date bundles = the rolling data store). |

Everything transient (weather cache, ARL/GRIB files, HYSPLIT install, `run_*/` scratch dirs, logs, EPA
CSVs) is **git-ignored** — see `.gitignore`.

---

## Where to change things (config)

All near the top of `calvert_plume_engine_one_day.py` unless noted:

| To change… | Edit |
|---|---|
| **Which chemicals are modeled** | `DEFAULT_ACTIVE_CHEMICALS` (the 13). Each also needs an entry in `CHEMICAL_PROPERTIES`, `DEP_CHEMICAL_TAGS` (a ≤4-char HYSPLIT species code), `DEP_CHEMICAL_SLUGS`, `CHEMICAL_DEPOSITION`, and `CHEMICAL_DISPLAY_NAMES`. See [Add a chemical](#common-maintenance-tasks). |
| **Facilities / emissions** | `FACILITIES` dict (name, coords, `csv_match_name`) + the TRI CSV. A facility emitting *none* of the modeled chemicals is auto-dropped from the map. |
| **Curated "showcase" days** | `PINNED_DATES` — kept forever (never pruned), shown with a label in the picker. |
| **Rolling-window length** | `ROLLING_WINDOW_DAYS = 30` (≈ a month of daily dates). |
| **Run time of night** | the `cron` in `.github/workflows/daily-plume.yml`. |
| **Timezone / windowing** | hard-coded to **America/Chicago** (Central, DST-aware) throughout. Each simulated "day" is a local calendar day, midnight→midnight. |
| **Deposition parallelism** | auto-scales to RAM (~1 worker / 12 GB); override with env `PLUME_DEP_WORKERS`. |
| **Vet-clinic landmarks** | `VET_CLINICS` list. |

---

## Data model

**Per-date bundle** — `site/data/dates/{YYYY-MM-DD}.json` (~5–13 MB):

```
{
  "date": "2026-07-04",
  "plumes": {
    "facilities":        [ {name, lat, lon, color, chemicals:[{chemical, stack_lbs, fugitive_lbs, ...}], ...} ],
    "wind_grid_stack":   [ 24 hours x 20x20 cells of {dLat,dLon,sLat,sLon} ],   # animated-particle wind field
    "wind_grid_fugitive":[ ... ],
    "grid_info":         {grid_size, lat/lon bounds},
    "chemical_properties": { ... }
  },
  "monitors": { "PM2.5": {stations...}, "VOCs": {...}, ... },        # AQS + local VOC overlays
  "dep": { "manifest": {...}, "files": { "combined_vinyl_chloride.json": <GeoJSON>, ... } }   # deposition/air footprints
}
```

- **Particles are NOT stored** — the front-end *animates* them client-side from the wind grid.
- Deposition GeoJSON `metadata.start_hour = 1` marks a **Central-windowed** bundle (a legacy `2` means the
  older UTC-day windowing — should not occur anymore).

**Manifest** — `site/data/manifest.json`: `{generated_at, newest, dates:[{date, label?, pinned?}]}`. Drives
the date picker (newest first). **Retention** in `build_site()` keeps the newest `ROLLING_WINDOW_DAYS`
daily dates + all `PINNED_DATES` and deletes the rest on every run.

---

## Methodology (the science)

- **Weather:** NOAA **HRRR** (3-km CONUS) hourly **analysis** fields (`fxx=0`), not forecasts — so the most
  recent complete day is *yesterday*. Converted to HYSPLIT ARL with `api2arl_v6` (eccodes 2.17.0).
- **Transport:** NOAA **HYSPLIT** v5.4.2, a Lagrangian particle dispersion model. Two release types per
  facility: an **elevated stack** (15 m) and a **ground-level fugitive/area** source (2 m). Emission rates
  come from the facility's **2024 TRI** stack/fugitive air releases, split per chemical.
- **Chemicals (13):** vinyl chloride, ethylene dichloride (1,2-DCA), benzene, 1,3-butadiene, xylenes,
  tetrachloroethylene, 1,2,4-trichlorobenzene, chlorine, ammonia, naphthalene, ethylene oxide,
  dichloromethane, carbon tetrachloride. Each has literature molecular-weight, dry-deposition velocity,
  Henry's-law solubility, reactivity and half-life (`CHEMICAL_PROPERTIES` + `CHEMICAL_DEPOSITION`).
- **Footprints:** HYSPLIT concentration grids → `concplot` contour bands → GeoJSON polygons. **Soil
  deposition** accumulates over the day; **ground-level air** is per-hour breathing-zone concentration.
- **Particle animation:** tracers advected by an hourly wind field derived from the HYSPLIT particle
  displacements, plus a small, tuned turbulent diffusion so the cloud reads as a realistic spreading plume.
- **Time:** displayed in **Calvert City local time** (Central, CST/CDT). Each day is a local calendar day.
- **Monitors:** EPA **AQS** ambient stations (publish months late, so recent days show none) + the group's
  local **VOC** canister samples (nearest available sample; grayed-out when > 14 days from the shown date).

---

## Running & operating it

### In the cloud (normal)
The nightly Action handles everything. **Manual runs:** Actions → *Nightly plume update* → *Run workflow*:
- `date` — a single `YYYY-MM-DD`, or a comma list (`2024-01-08,2025-02-15`); blank = yesterday.
- `force` — `true` to re-simulate a date whose bundle already exists (e.g. refreshing a pinned day).
- `days_back` — ensure the last N days exist (default 1).

Runs are serialized (concurrency group) and stream their logs live. The commit step **rebuilds the site
from the union** of its fresh bundles + whatever else is on the branch, so overlapping runs can't clobber
each other. A run's data is only ever lost if the whole runner dies before the commit step.

### Locally (for development)
Requires a local HYSPLIT install (Mac or Linux) and the Python deps:
- Point the engine at it with env `HYSPLIT_ROOT` (default `/Users/.../hysplit`). Weather is downloaded on
  demand; a local run keeps the GRIB cache (`--no-stream`) instead of streaming.
- `python3 daily_update.py --date 2026-07-04` runs one date end-to-end, then rebuilds the site.
- `python3 calvert_plume_engine_one_day.py --build-site` just rebuilds the front-end from existing bundles
  (fast; no HYSPLIT needed) — the quickest way to preview front-end/CSS/JS changes.

---

## Common maintenance tasks

**Add a modeled chemical** — add its uppercase TRI name to **five** places in
`calvert_plume_engine_one_day.py`, then re-run the dates you want it on:
`DEFAULT_ACTIVE_CHEMICALS`, `CHEMICAL_PROPERTIES`, `DEP_CHEMICAL_TAGS` (unique ≤4-char code),
`DEP_CHEMICAL_SLUGS`, `CHEMICAL_DEPOSITION`, and a friendly label in `CHEMICAL_DISPLAY_NAMES`. The
front-end filter list derives from `DEFAULT_ACTIVE_CHEMICALS`, so it updates automatically.

**Change the rolling window** — edit `ROLLING_WINDOW_DAYS`; pruning happens on the next build.

**Add/replace a pinned showcase day** — edit `PINNED_DATES`, then force-run that date.

**Refresh TRI emissions** (when EPA publishes a newer year) — replace `Marshall County Facility Release.csv`
and re-run all dates. (As of writing, 2024 is the latest *complete* TRI; 2025 finalizes ~fall 2026.)

**Front-end tweak** — edit the template inside `generate_web_visualization()` (it's the big f-string), then
`--build-site` and preview locally. The JS lives in that template and is split out to `site/app.js`.

---

## Gotchas & hard-won lessons (read before editing the pipeline)

These each cost real debugging time — the fixes are in the code with comments, but know they exist:

- **`SETUP.CFG` case-sensitivity.** HYSPLIT reads its namelist as **`SETUP.CFG`** (uppercase). macOS's
  case-insensitive filesystem hides this; **Linux (CI) is case-sensitive**, so a lowercase `SETUP.cfg` is
  silently ignored → HYSPLIT falls back to defaults (`ndump=0` → **no PARDUMP** → empty particle animation).
  The engine writes **both casings**. Any HYSPLIT config file is at risk of this.
- **eccodes version pinning.** `api2arl_v6` embeds **eccodes 2.17.0**; feeding it a *newer* system eccodes'
  definition files **segfaults** every GRIB conversion. CI fetches the matching 2.17.0 definitions.
- **Deposition OOM (`exit 143`).** A wide-plume day rendering many big `concplot`/ghostscript contours in
  parallel can exceed the 16 GB runner → the OS kills it. Deposition workers **auto-scale to RAM**
  (~1 per 12 GB); on the 16 GB runner that's 1 (serial, slower, safe).
- **Commit push races.** Runs take hours and every run regenerates the shared `manifest/index/app.js`, so a
  naive `git push` (or even a rebase) conflicts and can lose a whole run. The commit step **resets to latest
  `main`, overlays only its fresh per-date bundles, and rebuilds** — conflict-proof.
- **Central-day windowing & frame indexing.** The sim window is a *local* calendar day (crosses UTC
  midnight), and particle/wind/deposition frames are indexed **start-relative** (frame 0 = local midnight),
  *not* by absolute UTC hour. `daily_update` targets "yesterday **Central**."
- **HRRR availability.** Only *analysis* (past) data is used; today would be a forecast. Yesterday is always
  complete by the ~07:00 UTC run.
- **`par2asc` time-format parsing.** macOS and Linux HYSPLIT builds format the dump time slightly
  differently; the parser takes the hour as the token *before* the first colon to handle both.

---

## Known limitations

- **Recent EPA monitors are empty** — AQS publishes months late, so new days show only the local VOC layer.
  The AQS CSVs also aren't on the CI runner (too large), so CI-built dates have no AQS overlay regardless.
- **Formaldehyde is not modeled** — the local facilities emit ~0 lbs/yr of it *to air*; the cancer-risk from
  formaldehyde is dominated by *secondary* atmospheric formation, which a primary-emission dispersion model
  can't represent.
- **Metals (nickel, chromium, cadmium) not modeled** — they need particulate treatment, not gas dispersion.
- **"HYSPLIT Failed" for some chemical/source combos** is expected, not a bug — it means that low-emission or
  fast-depositing source produced no mappable footprint that day (empty `cdump`). Its particles still animate.
- **Particle animation ≠ HYSPLIT internals** — it's a faithful visualization of the wind field + tuned
  diffusion, not the model's exact 3-D particle state (which isn't extracted). Height shown is *release*
  height, not tracked altitude.

---

## Handoff / open items

- **Production cutover** — this repo is the staging/proving ground. To hand it to production, point the
  Pages deploy at the destination repo (or make the destination repo track this one). Enable Pages with
  source = *GitHub Actions* and confirm `permissions: contents/pages/id-token: write` in the workflow.
- **AQS credentials** — `fetch_aqs_data.py` has a default `--email`/`--key`; if you automate AQS pulls, move
  the key to a GitHub Actions secret. (Low sensitivity — free, rate-limited key — but don't hard-code it.)
- **No secrets required** for the core pipeline: the HYSPLIT build is a public NOAA URL, and everything else
  is public data.
- **A few clearly-labeled `/* COMMENTED OUT … kept as reference */` blocks** remain in the front-end
  template (superseded particle/deposition approaches). They're inert; leave or delete at your discretion.

For the science/context, the contact is the SRSP project lead. Nightly failures email the repo owner
automatically (GitHub Actions default).
