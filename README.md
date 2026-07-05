# Calvert City Plume Analysis — staging (auto-updating)

Fetch-based dashboard that auto-updates nightly via GitHub Actions (`.github/workflows/daily-plume.yml`):
simulates yesterday's HYSPLIT dispersion, writes a per-date JSON bundle under `site/data/dates/`, and
rebuilds the fetch site (`site/index.html` + `site/app.js` + `site/data/manifest.json`). Keeps a rolling
30 days plus pinned curated days. GitHub Pages serves `site/`.

Local preview: double-click **View Locally.command** (browsers block fetch on file://).
Manual date run: `python3 calvert_plume_engine_one_day.py --date YYYY-MM-DD` then `--build-site`.
