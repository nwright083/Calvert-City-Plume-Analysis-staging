#!/usr/bin/env python3
"""Nightly orchestrator for the Calvert City plume site.

Simulates recent day(s) with the engine, writes per-date bundles, then rebuilds the fetch-based site
(the engine's build_site applies retention: newest ROLLING_WINDOW_DAYS daily dates + the pinned curated
days, pruning the rest). Designed to run identically on the dev Mac (launchd/manual) and in GitHub
Actions. HRRR analysis for a full day is complete after the day ends, so the target is *yesterday* (UTC)
— forecasting today would be inaccurate.

Usage:
  python3 daily_update.py                  # run yesterday (UTC) if not already done, then rebuild site
  python3 daily_update.py --date 2026-07-02
  python3 daily_update.py --days-back 5     # ensure the last 5 days exist (skips ones already done)
  python3 daily_update.py --max-runs 2      # cap simulations per invocation (runner time budget)
  python3 daily_update.py --no-stream       # dev Mac: keep the GRIB cache instead of streaming

Exit codes: 0 = success (or nothing to do), 1 = some date(s) failed but site rebuilt, 2 = build-site failed.
"""
import argparse
import datetime
import os
import subprocess
import sys

WORKSPACE = os.path.dirname(os.path.abspath(__file__))
ENGINE = os.path.join(WORKSPACE, "calvert_plume_engine_one_day.py")
BUNDLE_DIR = os.path.join(WORKSPACE, "site", "data", "dates")
LOG_DIR = os.path.join(WORKSPACE, "logs")


def bundle_exists(date_str: str) -> bool:
    return os.path.exists(os.path.join(BUNDLE_DIR, f"{date_str}.json"))


def run_engine(engine_args, log_path: str) -> int:
    """Run the engine with engine_args, teeing output to both the console and a per-date log file."""
    os.makedirs(os.path.dirname(log_path), exist_ok=True)
    stamp = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    header = f"\n\n===== {stamp} :: engine {' '.join(engine_args)} =====\n"
    print(header.strip(), flush=True)
    with open(log_path, "a", encoding="utf-8") as log:
        log.write(header)
        log.flush()
        # -u: force the child engine's stdout unbuffered so its progress streams live into the CI
        # log (block-buffered pipes otherwise hide ~1.5 h of output until the process exits).
        proc = subprocess.Popen(
            [sys.executable, "-u", ENGINE] + engine_args, cwd=WORKSPACE,
            stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, bufsize=1,
        )
        for line in proc.stdout:
            sys.stdout.write(line)
            sys.stdout.flush()   # stream live to the CI log instead of buffering
            log.write(line)
        proc.wait()
    return proc.returncode


def main() -> int:
    ap = argparse.ArgumentParser(description="Nightly plume-site updater.")
    ap.add_argument("--date", default=None, help="Specific date YYYY-MM-DD to run (default: yesterday UTC).")
    ap.add_argument("--days-back", type=int, default=1, help="Ensure the last N days exist (default 1).")
    ap.add_argument("--max-runs", type=int, default=2, help="Max simulations per invocation (default 2).")
    ap.add_argument("--no-stream", action="store_true", help="Keep the GRIB cache (skip --stream-weather).")
    ap.add_argument("--force", action="store_true", help="Re-simulate target date(s) even if a bundle already exists (e.g. to refresh pinned days after a model change).")
    a = ap.parse_args()

    # Target dates are Calvert City (Central) calendar days, so "yesterday" is yesterday LOCAL.
    from zoneinfo import ZoneInfo
    today = datetime.datetime.now(ZoneInfo("America/Chicago")).date()
    if a.date:
        targets = [d.strip() for d in a.date.split(",") if d.strip()]
    else:
        # Oldest-first so a partially-filled window backfills from the far edge inward.
        targets = [(today - datetime.timedelta(days=off)).isoformat() for off in range(a.days_back, 0, -1)]

    todo = targets if a.force else [d for d in targets if not bundle_exists(d)]
    build_log = os.path.join(LOG_DIR, "build-site.log")

    if not todo:
        print(f"All target dates already have bundles: {targets}. Rebuilding site only.")
        return 0 if run_engine(["--build-site"], build_log) == 0 else 2

    # A forced run (e.g. refreshing all pinned days) runs every listed date; the runner-time cap
    # only guards the automatic nightly backfill.
    if not a.force:
        todo = todo[: a.max_runs]
    print(f"Dates to simulate this run: {todo}")

    weather_flags = [] if a.no_stream else ["--stream-weather"]
    failures = []
    for d in todo:
        log_path = os.path.join(LOG_DIR, f"daily_{d}.log")
        rc = run_engine(["--date", d] + weather_flags + ["--cleanup", "--no-build-site"], log_path)
        if rc != 0:
            print(f"  ✗ {d} FAILED (exit {rc}). Log: {log_path}")
            failures.append(d)
        else:
            print(f"  ✓ {d} simulated.")

    # Rebuild the site from whatever bundles now exist (writes manifest + index.html + app.js, prunes old).
    if run_engine(["--build-site"], build_log) != 0:
        print("✗ build-site FAILED.")
        return 2

    if failures:
        print(f"Completed with {len(failures)} failed date(s): {failures}")
        return 1
    print("Nightly update complete.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
