# AI Context — Calvert City Plume Analysis

Last updated: 2026-07-02. Authoritative handoff for any AI working on this project. Read before editing.

## Project
Environmental-health (SRSP) dashboard for industrial atmospheric dispersion in Calvert City, KY.
Pipeline: Python runs HYSPLIT (NOAA HRRR met) → generates a **single self-contained `index.html`**
(Leaflet + canvas particle animation + deposition/air footprints). Owner: Nick Wright.

## Branches
- `main` = `7a53e74` — clean particle-only baseline. Untouched.
- `native-deposition` = **ACTIVE branch** — all the deposition work below lives here.
- `deposition-attempt-1` = archived Round 8 (scrapped). Don't resume/delete.

## ⚠️ THREE-FILE SYNC RULE (critical)
The simulation JS lives in THREE files that must stay identical:
1. `calvert_plume_engine.py` — multi-day engine (HTML template uses Python `.format()`; JS braces are
   escaped `{{`/`}}`; `{VAR}` are real format vars).
2. `calvert_plume_engine_one_day.py` — single-day engine, **the fast regen path**.
3. `index.html` — generated output.
After any JS change: edit BOTH `.py` templates (escaped) then regen: `python3 calvert_plume_engine_one_day.py --regen-html` (answer `n` to "re-run simulation"). Regen rebuilds `index.html` from the one-day template, so index.html auto-syncs to it; the multi-day template must be mirrored by hand.

---

## DEPOSITION SYSTEM (what's been built — all on `native-deposition`)

### Concept: two footprint layers, per facility × per chemical, from native HYSPLIT
Stop hand-rolling contours. HYSPLIT computes the field; `concplot` emits contoured KML polygons; we
convert KML→GeoJSON and render with Leaflet. Two layers per run:
- **Soil Deposition (g/m²)** = cdump **level 0**, cumulative (`concplot -r2`).
- **Ground-Level Air (g/m³)** = cdump **level 10 m**, per-hour (`concplot -r0`).

### Chemicals (9): `CHEMICAL_DEPOSITION` dict (top of both engines)
Vinyl chloride, 1,2-dichloroethane, benzene, 1,3-butadiene, xylenes, tetrachloroethylene,
1,2,4-trichlorobenzene, chlorine, ammonia. Each has gas-phase dry-dep (Vd, mol wt, Henry's),
wet-scavenging (chlorine/ammonia only — VOC wet params are 0 per user-vetted corrections), half-life,
depositor_class. Tags/slugs in `DEP_CHEMICAL_TAGS` / `DEP_CHEMICAL_SLUGS`.

### ⭐ THE BIG GOTCHA — hourly works; the "macOS 12h limit" was a SYNTAX BUG
The CONTROL averaging line is `type HH MM`. The old `01 00 00` = type 1 / **0-minute** interval →
SIGFPE crash (this, NOT deposition, caused all the earlier crashes). **Correct hourly = `00 01 00`**
(type 0 avg, 1 h). Hourly runs fine on macOS → **23 frames** (hours 2–24). No Windows needed.

### CONTROL config (`write_deposition_control_file`, both engines)
- 23-h run from 01:00; emit per chemical at its `stack_g_hr`.
- Grid: center = `MAP_CENTER` (fixed, all chemicals aligned), spacing `DEP_GRID_SPACING=0.03`
  (~3.3 km ≈ HRRR's 3 km — finer = false precision), span `DEP_GRID_SPAN=4.0` (~440 km).
  These constants are DECOUPLED from `WEATHER_BOX_RADIUS_KM` (which still governs particles).
- Output levels: `0` then `10`. Sampling `00 01 00` (hourly).
- Met (ARL) is **full-CONUS HRRR** (`api2arl_v6 -z1`, no bbox) → grid can be large with NO weather
  re-download. Bigger grid was the fix for the "straight-edge clip".

### concplot (`run_concplot_kml`)
Compiled binary `/Users/nawrig04/hysplit/exec/concplot` (NOT concplot.py — needs missing module).
Flags: `-a3` (KML) `-f0` (all frames one file) `-g0 -d1 -k1` `-c1` (FIXED contour levels → consistent
bands across frames; differ per chemical) `-w2` (smoothing). dep: `-b0 -t0 -r2`; air: `-b10 -t10 -r0`.

### KML→GeoJSON (`parse_kml_to_features` + `extract_band_values`)
- concplot KML has 4 boilerplate folders (Source/Weather/Smoke/AQI) before the real frame folders →
  parser counts only contour-bearing folders so `hour_frame` = 0..22 (frame k = sim hour k+2).
- Band semantics: **lower band number = HIGHER concentration** (smaller, near source). conc1=highest,
  conc5=lowest. (Verified by extents + KML legend.)
- `extract_band_values(kml)` reads the legend `Contour Level: X mass/m²` → `{band: value g/m²|g/m³}`.
  Stored in GeoJSON `metadata.band_values = {dep:{...}, air:{...}}`. Differs per chemical.
- Vertices decimated every-2nd, coords rounded 4 dp.

### Outputs & embedding
- `generate_deposition_outputs` → `output/geojson/{date}/{facslug}_{chemslug}.json` (FeatureCollection;
  features tagged `{layer, hour_frame, band, chem, fac_name, fac_id}`; metadata incl. `num_frames`,
  `start_hour`, `band_values`). Plus `manifest.json`.
- `run_deposition_pipeline()` loops facility×chemical, runs HYSPLIT+concplot+parse. **~55 min** for the
  full set at 4°/0.03° (HYSPLIT ~203 s/chemical is the bottleneck; concplot ~17 s).
- **MUST embed inline**: `build_deposition_archive(dates)` reads the geojson back and injects
  `const depositionArchive = {…}` into the HTML (next to `historicalSimulationArchive`). **fetch() of
  local files is blocked under file://**, so external fetch does NOT work — inline only. index.html is
  ~15 MB now (fine locally).

### FRONTEND (in all 3 files)
- Basemap: **CartoDB Voyager** (light, streets/rivers). `minZoom: 7`. Particles get a dark contrast
  halo so light colors read on the light map.
- Two panes BELOW the particle canvas (overlayPane z=400): `airPane` (z245), `depPane` (z250) →
  particles on top. **Master transparency = the whole-pane CSS opacity** (`footprintOpacity ×
  globalIntensity`) so stacked chemicals/bands DON'T compound; per-polygon fillOpacity is cross-fade
  only. `FOOTPRINT OPACITY` slider (sandbox), default 0.45.
- Color ramps go **intense→faint** (band1 deep red/blue → faint).
- **Band visibility = value-based** (`VISIBLE_DECADE_RATIO = 32`): a band draws only if its
  `band_values` ≥ peakValue/32 (≈ within 1.5 decades of that footprint's peak). Replaced the old
  band-NUMBER `HIDE_OUTER_BANDS`, which broke on combined footprints: `concplot -c1` auto-scaled some
  combined fields (e.g. ammonia) to **2-decade** contour steps (1e-5,1e-7,1e-9,1e-11), so "band 3"
  landed at a faint 1e-7 that spread ~3° and clipped the grid into a "square". The value threshold is
  robust to that. (Deeper fix if ever needed: explicit fixed `-v` levels shared across all modes so
  combined/stack/fugitive are directly comparable.)
- Animation: real 23 hourly frames keyed to the slider; cross-fade between consecutive frames; fade-in
  over first 2 h. `refreshDepLayers()` (throttled via `maybeAnimateDep` in the tick loop).
- **Hover readout** (`#dep-readout`, `depHitIndex`, `depPointInRing`, mousemove handler): point-in-
  polygon → per chemical shows the **decade range** ("0.10–1.00 µg/m²", because contours are binned)
  and, for multi-facility chemicals, **facility contribution %** (2a — summed band levels, approximate).

---

## ✅ COMPLETED: 2b — true merged contour per chemical (via `concadd`)

**What it does:** Map colors reflect the true combined concentration field where facilities overlap
(previously overlapping per-facility footprints blended visually but band levels didn't add).

**Backend (`build_combined_chemical_outputs`, both engines):**
- Groups per-facility cdumps by chemical, chains `concadd` to sum them into one merged cdump.
- Runs `concplot` + KML→GeoJSON on the merged result → `combined_{chemslug}.json`.
- Manifest gets `combined_entries` array alongside per-facility `entries` (both kept).
- `build_deposition_archive` embeds both `entries` + `combined_entries` files inline.

**Frontend (`refreshDepLayers`, all 3 files):**
- DRAWS from `combined_entries` (one footprint per chemical, true merged field).
- Falls back to `entries` if `combined_entries` absent (backward compat).
- `depHitIndex` = hit-test index from drawn COMBINED footprints → accurate combined value.
- `perFacHitIndex` = SECOND hit-test index from per-facility files (embedded, NOT drawn) → hover
  attribution % breakdown. Hit-tested on mousemove even though not rendered.
- Hover readout: headline = true combined concentration (from `depHitIndex`), sub-rows = per-facility
  attribution % (from `perFacHitIndex`, shown only when multiple facilities contribute).

---

## ✅ COMPLETED: Unified Chemical & Facility Toggles (Linked Controls)

**What it does:** Linked controls allow turning off entire chemicals or entire facilities globally, affecting both the active particle system and deposition footprints in one click.

**Chemical Filters Section (all 3 files):**
- Moved the `dep-chem-list` container out of "Footprint Layers" into a new, prominent **"CHEMICAL FILTERS"** section in the main sidebar.
- Toggling a global chemical pill:
  - Dynamically updates `depActiveChem` (hides/shows the deposition footprint).
  - Syncs the active state across all facilities (`activeChemicals[fac.id][chem] = checked`).
  - Automatically checks/unchecks the per-facility checkboxes in the point sources legend.
  - Instantly prunes active particles of that chemical and updates `drawParticles()`.
- Toggling a per-facility checkbox (`.chem-chk`):
  - Still acts as a fine-grained override (turns that chemical off only for that facility's particles).
  - If a chemical is checked ON for a facility and the global pill was unchecked, it automatically turns the global pill ON to ensure visibility of particles/footprints.

**Facility Toggles Section (all 3 files):**
- The facility visible toggle ("VISIBLE" / "HIDDEN" button in the point sources legend):
  - Hides/shows the facility's active particles.
  - Dynamically hides/shows the facility's map pin marker (`facilityMarkers[fac.id]`).
  - Skips the facility in the `perFacHitIndex` loop, automatically removing its contribution from the deposition hover readout.

**Chemical Defaults Whitelist (both engine backends):**
- Updated `DEFAULT_ACTIVE_CHEMICALS` to exactly match the 9 chemicals present in the deposition / chemical filters list. On load, only these 9 chemicals default to checked (active) in both the particle simulation and the chemical filters panel. Other trace facility compounds default to unchecked.

---

## ✅ COMPLETED: Dual-Source Deposition Modeling (Stack + Fugitive)

**What it does:** HYSPLIT models elevated stack emissions and ground-level fugitive leaks independently, producing separate contours that link directly to the Plume Display Mode select dropdown in the UI.

**Backend (`run_deposition_pipeline` and `build_combined_chemical_outputs`, both engines):**
- Reverted `write_deposition_control_file` back to a single-source configuration.
- `run_deposition_pipeline` splits each facility-chemical pair into up to two separate simulations:
  - **Stack Run**: elevated at facility height emitting `stack_g_hr` (outputs `{fac_slug}_{chem_slug}_stack.json`).
  - **Fugitive Run**: ground-level at `2.0`m emitting `fugitive_g_hr` (outputs `{fac_slug}_{chem_slug}_fugitive.json`).
- Added a `cdump` caching skip check in the single run helper. If a valid, non-empty `cdump` exists for a suffix folder, HYSPLIT execution is skipped, instantly loading cached results.
- Spawns simulations in parallel with `ThreadPoolExecutor` using `max_workers = 2` to maximize performance on Apple Silicon while keeping RAM footprint low (avoiding OOM memory pressure from concurrent reads on the 13.3 GB weather file).
- `build_combined_chemical_outputs` sum-merges facility outputs using `concadd` into three combined footprints per chemical:
  - `combined_{chem_slug}.json` (all stack + all fugitive)
  - `combined_stack_{chem_slug}.json` (all stack only)
  - `combined_fugitive_{chem_slug}.json` (all fugitive only)
- Manifest registers `combined_entries` and individual entries tagged with `"source_type"`.

**Frontend (`refreshDepLayers`, all 3 files):**
- Binds `#display-mode-select` event listener to trigger `refreshDepLayers()`.
- Inside `refreshDepLayers()`, retrieves `displayMode`:
  - Draws the corresponding combined chemical footprint: `combined` → total, `stack` → stack-only, `fugitive` → fugitive-only.
  - Filters `perFacHitIndex` by `displayMode` so that the HUD hover attribution breakdown accurately reflects the selected mode. (Combined mode includes both sources, whereas Stack and Fugitive modes filter to show only their respective source attributions).

---

## ✅ FIXED 2026-06-30: frozen-page bug (missing toggle elements + TDZ)
Symptom: clock stuck at 12:00, 0 particles. Console showed `Cannot read properties of null
(reading 'checked')` + `Cannot access 'showParticles'/'showDeposition' before initialization`.
Root cause (other AI's dual-source frontend): JS referenced toggle elements that **don't exist** in
the HTML — `particles-toggle`, `deposition-toggle`, `deposition-source-select`, `deposition-legend`,
`deposition-source-container`. `getElementById(...).checked`/`.addEventListener` on `null` halted init
(so `tick` never started). Also `let showParticles/showDeposition` were declared mid-script but used
earlier by `drawParticles`/`updateTooltip` (which Leaflet fires during map init) → temporal-dead-zone.
Fix (one-day engine): declare `let showParticles=true; showDeposition=true` early (line ~3406, before
the map); null-guard every reference to those 5 missing IDs. Verified by running the real app JS in
Node with a stub that returns `null` for exactly those IDs → init + `tick()` run clean.
**UPDATE 2026-07-01:** `particles-toggle` now DOES exist — added as the "Particle Simulation" switch in
the LAYERS section (see below), wired to `showParticles` + `drawParticles()`. The null-guards remain
(harmless; the sim_harness stub still returns null for it). The other 4 IDs are still absent.
Diagnosis method (reusable): extract the two `<script>` blocks (data ~58MB + logic ~110KB) from
index.html, eval `data + logic` in Node with a Proxy DOM/Leaflet stub, replace the boot
`loadDepManifest(activeDate);` with a guarded `tick(16)` to surface the loop's runtime error. Scripts in
the scratchpad (`harness6.js`). **Tick is also crash-proofed** (try/catch around particle/dep/draw) so
a future throw can't freeze the loop again — BUT `updateHUD()` is still unwrapped; real init errors must
still be fixed, not relied on.

## ✅ FIXED 2026-06-30: vector layers off-center on ZOOM (the real root cause)
Symptom: deposition contours AND air-monitor circles drift off-center on zoom in/out; **a pan snaps
them back**; facility *markers* stay correct. Classic Leaflet **zoom-animation** desync — animated zoom
leaves SVG vector layers mid-transform; markers reposition individually so they're fine; any
`move`/`moveend` recomputes the vector positions. Fix: **`zoomAnimation: false`** in the `L.map(...)`
options (one-day engine, ~line 3421). Zoom is now instant but every layer stays aligned at all zooms.
(The earlier heatmap-disable below was a separate, also-valid cleanup but was NOT the cause of the
zoom drift — this was.)

## ✅ FIXED 2026-06-30: deposition "shifts right" on zoom-out
There are TWO deposition renderers: (1) my **GeoJSON contour footprints** (depPane/airPane via
`refreshDepLayers`) — vector, lat/lng-anchored, correct at all zooms; (2) the other AI's
**`leaflet.heat` heatmap** (`depositionHeatLayer`, the smooth blurry blob) — canvas with a **fixed
PIXEL radius**, so it visually drifts off the sources when zooming out, and it duplicates layer (1).
Fix: **`renderDepositionHeatmap` early-returns (disabled)** in the one-day engine — only the correct
contour footprints render now. The heatmap is the other AI's "live/reference deposition" viz and is
tied to particles; re-enable/rework it (with proper zoom handling, e.g. meters-based radius or
re-render on zoomend) during the particle pass if wanted. `leaflet.heat` is loaded at index.html head.

## ✅ PARTICLE SIMULATION REWORK — BUILT & DEBUGGED 2026-06-30 (continue tuning)

**STATUS: the rework is implemented and the app WORKS. Particles spawn ∝ emission, advect on the HYSPLIT
wind, are gated by the air footprint, fade/deposit, and now RENDER.** A prior AI built it but left it
broken; this session fixed 4 crash/parse bugs (below), tuned it, and verified headlessly. The design spec
+ turnkey notes below are kept as the authoritative reference for the model.

### 4 bugs found & fixed this session (all were silent — swallowed by tick()'s try/catch)
1. **`updateTooltip` unbalanced `}`** (other AI's botched `/* */` comment) → whole `<script>` failed to
   PARSE → nothing ran. Fixed: removed the stray brace; `tooltip.style.display='none'` now lives in the
   else-block. `node --check` clean.
2. **`interpolateGrid` trusted `GRID_SIZE` (20) but the embedded wind grid is jagged/smaller** (stack is
   10×10 and worse, 25 hrs; fugitive is clean 20×20×24). `grid[y][x]===undefined` → threw on EVERY
   particle → `advect` died silently → **particles spawned but never moved (piled at sources).** Fixed:
   `interpolateGrid` now derives `rows/cols` from the actual slice + per-row ZERO fallback. Ported to
   BOTH engines.
3. **Frame-rate-dependent mass decay**: outside-footprint `p.mass *= 0.85` was PER-CALL → at 60fps a
   particle died in a fraction of a sim-hour. Fixed: time-based `*= exp(-dtHours/0.55)` (≈1.5h to death)
   + inside lerp `1-exp(-dtHours/0.25)`. Frame-rate independent.
4. **`drawParticles` referenced undefined `pt`, `bkt`, `baseR`** (abandoned bucket optimization) → threw
   every frame → **particles invisible while HUD still counted them** (user's "invisible particles"
   report). Fixed: rewrote the draw loop to use the per-frame linear lat/lon→pixel calibration
   (`originX/originY/pxPerLon/pxPerLat`) + dark halo + facility-color dot. 97% of particles render.

### Tuning applied (one-day engine)
`SAFETY_MAX_AGE 720→1440` (particles ride the full day), `TURB_BASE 0.0025→0.0035`,
`TURB_GROWTH 0.0015→0.004`, `TURB_MAX 0.012→0.05`, `SPREAD_KICK 1.2→2.5` (HYSPLIT-derived dispersion to
fill the footprint). `MAX_ACTIVE=8000`, `BASE_SPAWN_COUNT=12`.

### ⭐ KEY FINDING — a full RE-RUN is NOT the fix for reach
Measured per-type transport: the **clean** fugitive grid (0.45° max, 0.021°/hr) barely beats the
**jagged stale** stack grid (0.28°, 0.013°/hr). Both have light winds this date (~0.037°/hr ≈ 1 m/s).
So regenerating clean wind data would NOT make particles reach much further. The real limiter: the
HYSPLIT footprint EDGE is its *dispersive leading tail* growing over the whole day; matching it with
gated source-streamed particles needs drift ≈ footprint-growth-rate, which only the fastest particles
hit under light winds. **Result:** inner/breathing-zone air footprint fills well (several facilities
airFill 0.7–1.6), but the largest chlorine/ammonia footprint EDGES fill only ~0.2–0.4. This is a
realism/tuning frontier for the USER to judge visually — NOT a bug, and NOT fixable by a re-run.
(Disk note: 39 GB free, 91% full; only `MET_20250308.ARL` needed for the active date — the other 6 MET
files are 75 GB of reclaimable space if a re-run is ever wanted.)

### How to verify (headless, reusable)
`scratchpad/sim_harness.js` boots data+logic in Node (id-aware DOM stub), drives the REAL
spawnBatch/advect to steady state, then reports: footprint fill % per facility (vs VISIBLE bands using
`VISIBLE_DECADE_RATIO=32`), transport by type, death-cause, and a `drawParticles()` smoke test. Re-extract
`data.js`/`logic.js` from the two `<script>` blocks after each regen. **`harness6.js`'s `tick(16)` passes
even when broken (dtHours=0 → no particle exercised) — use sim_harness.js to actually exercise motion.**

### Still open on particles
- **Large-footprint edge fill** (chlorine/ammonia): tuning frontier — needs user's visual call on how
  aggressive to make dispersion vs. plume-tightness. Pushing TURB/SPREAD higher fills more but looks
  noisier; the time-dependent gating caps reach regardless.
- **Multi-day engine sync:** only the `interpolateGrid` crash fix was ported. Its particle code is
  PRE-rework (MAX_ACTIVE 4000, two-path advect, old constants) — needs full reconciliation.

---
### (Original design spec — LOCKED with user 2026-06-30, now IMPLEMENTED) ▼

**Goal:** replace the particle system with HYSPLIT-driven, continuously-streaming particles that look
*alive* (smooth individual motion, NO flicker) and **visibly fill the Ground-Level Air footprint and
reach the Soil Deposition extent** — so you can see particles actually travel out there and deposit.

**User decisions (final):**
- **Source of truth = HYSPLIT, NOT custom JS physics.** The user explicitly does not want us
  "calculating our own stuff" for deposition/fade.
- **Density, extent & fade come from the HYSPLIT air-concentration field** (the Ground-Level Air
  footprint, per facility×chemical, per hour). It's already dense-near-source / thin-at-edges and each
  chemical reaches exactly as far as it really travels (VOCs far; chlorine/ammonia close), so it gives
  "a ton near the sources dying off, some reaching the far edges" automatically — per chemical.
- **Motion = advect along the HYSPLIT/HRRR wind field** (`PLUME_DATA.wind_grid_stack` /
  `wind_grid_fugitive`, already exported) each frame → smooth, individual, flicker-free. (User accepts
  this as "using HYSPLIT" since it's HYSPLIT's own wind, not invented physics.)
- **Spawn continuously from each facility, rate ∝ emission** (hourly TRI). Bigger emitter = denser stream.
- **Fade/"die into the ground" where the HYSPLIT concentration drops** (plume edge). Chemical-specific
  comes for free from the per-chemical footprint.
- **Color by facility** (current behavior, `fac.color`).
- **HARD REQUIREMENT:** over the animation the particle cloud must FILL the air footprint and reach the
  deposition footprint — don't let it collapse to a thin trail. (This is the user's correctness check.)

**Recommended implementation (no HYSPLIT re-run needed for v1 — reuse existing data):**
1. Particle lifecycle: spawn at facility (rate ∝ emission) → each frame advect by the wind field
   (bilinear in space, lerp in time between hours) **+ small turbulent spread** so they fan out to fill
   the plume width.
2. **Gate lifetime by the HYSPLIT air footprint:** a particle is ALIVE while inside that chemical's
   current-hour Ground-Level-Air contour; its opacity ∝ which band it's in (faint at the edges); it
   FADES/dies when it exits the footprint (or drops below the visible band). This forces particles to
   fill the plume and reach its true extent, and gives chemical-specific reach for free. Reuse the
   existing point-in-polygon machinery (`depPointInRing`, the air features in `depGeoJsonCache`,
   `band_values`) — same data the footprints already use.
3. Keep cross-fading footprint frames hourly; particles read the current-hour air footprint for gating.
4. Respect existing controls: chemical filters (`depActiveChem`/`activeChemicals`), facility visibility
   (`activeFacilities`), and PLUME DISPLAY MODE (combined/stack/fugitive → which footprint to gate against).
5. **Comment out / keep (do NOT delete)** the old particle code as reference: `updateHysplitParticles`
   (PARDUMP replay — flickered), the sandbox `spawnBatch`/`advect`, and `liveDepGrid`/heatmap.
6. Optional polish later: export raw gridded air concentration (con2asc on the level-10 cdumps) for a
   smoother density field than the contour bands.

### Code-level build notes (TURNKEY — all in `calvert_plume_engine_one_day.py`, mirror to multi-day, regen)
Build it as a **modification of the existing sandbox path** (spawn+advect already exist); the only new
logic is **footprint gating** for lifetime/opacity. Reuse, don't reinvent:
- **Motion is already done:** `getWind(time, lat, lon, type)` (~line 4630) returns
  `{dLat, dLon, sLat, sLon}` — HYSPLIT-derived median displacement **and spread (sLat/sLon = turbulent
  fan-out)**. `advect(dtHours)` (~4930) already moves `particles` with it. So advection + spread = free.
- **Particle object** (from `spawnBatch`, ~4694): `{id, lat, lon, ht, birth, fac(idx), chem(name),
  col(fac.color), type('stack'|'fugitive'), mass(1.0), tLat, tLon}`. `drawParticles` (~5026) renders by
  `p.col`, opacity from age/mass.
- **Spawn ∝ emission** already happens (sandbox `spawnBatch(dtHours)` scales count by facility emission;
  `numpar` logic). Keep it. Default `particleSource='sandbox'` (NOT 'hysplit'); comment out
  `updateHysplitParticles` (PARDUMP replay).
- **NEW — footprint gating helper.** Add `airBandAtPoint(facName, chem, srcType, lat, lon)`:
  1. find the air GeoJSON for that source: manifest entry where `{fac_name,chem,source_type}` match →
     `depGeoJsonCache[file]` (files like `westlake_vinyls_chlorine_stack.json`). Build a
     `(facName|chem|srcType) → file` lookup once.
  2. currentFrame = `floor(playbackTime - (md.start_hour||2))` clamped to `[0, num_frames-1]`.
  3. of that file's features with `layer==='air' && hour_frame===currentFrame`, point-in-polygon test
     with `depPointInRing(lat,lng,ring)` (exists); return the **lowest band number** containing the
     point (highest concentration), or `null` if outside the footprint.
- **NEW — gate lifetime in `advect`** (or a new `updateFieldGatedParticles`): after moving each
  particle, `const b = airBandAtPoint(facName, p.chem, p.type, p.lat, p.lon);`
  - `b === null` (outside plume) → particle is dying: `p.mass -= fast` (e.g. ×0.85/frame) → remove at ≤0.
  - inside → set opacity target ∝ band (low band# = near source = bright; high band# = edge = faint),
    e.g. `p.mass = lerp(p.mass, bandToBrightness(b), 0.2)`.
  This gates particles to the HYSPLIT plume → they fill it, reach its true extent, fade at the edge, and
  get chemical-specific reach for free. (Optional: re-seed/boost spawn so density tracks the footprint.)
- **Wire to controls:** skip a particle's chem if `!depActiveChem.has(p.chem)` or
  `activeChemicals[p.fac]?.[p.chem]===false`; skip facility if `activeFacilities[p.fac]===false`; gate
  against the footprint whose `source_type` matches `displayMode` (`display-mode-select`: combined uses
  both stack+fugitive footprints, else match `p.type`).
- **Verify:** particles dense at sources, thinning outward, filling the Ground-Level-Air footprint and
  reaching the Soil-Deposition edge; per-chemical reach (VOCs far, chlorine/ammonia close); no flicker;
  toggles/filters/display-mode all affect particles. Use the headless harness pattern (see freeze-fix
  section) to confirm `tick()` runs clean before handing back.

**Rejected:** PARDUMP-replay (the old approach — flickers because hourly snapshots + recycled IDs);
pure free wind-advection without footprint gating (forms a thin trail, doesn't fill the plume).

**Three-file sync** applies. Roll the two open items below into this same pass.

## ✅ FIXED 2026-07-01: ghost/double popup + particle zoom drift (commit b719c05)

**Ghost deposition popup (Bug A):** Two hover systems both fired on `mousemove`:
- `#dep-readout` — the HYSPLIT-polygon hover with per-facility % attribution + combined soil/air values. **KEPT.**
- `updateTooltip`'s `else { if (showDeposition && liveDepMax > 0) { … "🌡️ Surface Deposition" … } }` block — old
  particle-accumulated `liveDepGrid` tooltip from a previous approach. **REMOVED.** `updateTooltip` now only shows
  the particle-hover (if a particle is under the cursor); otherwise `tooltip.style.display='none'`. No more
  double/ghost popup when hovering deposition footprints.

**Particle zoom/pan drift (Bug B) — FINAL fix 2026-07-01:** The canvas is in Leaflet's `overlayPane`, which
Leaflet moves with a GPU `transform: translate3d(...)`. The old code positioned the CANVAS with
`canvas.style.left/top` (layout+paint). **Mixing a `transform`-moved pane with a `left/top`-moved child makes the
two composite on different timelines during/after GPU zoom/pan → the whole canvas (all particles) lands ~1.5°
(~165 km) off and can stay offset until a repaint.** Two dead-end attempts first: (a) moving the canvas to
`map.getContainer()` — made particles INVISIBLE, reverted; (b) a `requestAnimationFrame` deferral on `zoomend` —
no effect. **The fix that works** (mirrors Leaflet's own `L.Canvas` renderer): keep the canvas in `overlayPane`
but position it with `L.DomUtil.setPosition(canvas, map.containerPointToLayerPoint([0,0]))` (a translate3d
transform, so it composites WITH the pane), and project each particle exactly with
`map.latLngToContainerPoint(L.latLng(p.lat,p.lon))` (canvas top-left is pinned to container [0,0], so a container
point IS a canvas pixel). Removed the old 3-projection linear calibration entirely (`latLngToLayerPoint`,
`pxPerLon/pxPerLat/originX/originY` all gone) and the rAF wrapper. `resizeCanvas` only reassigns width/height when
`map.getSize()` changes. Particles now stay locked to the map at every zoom/pan (user-confirmed). Render and hover
(`updateTooltip`) share one exact projection.

Deployed: both `native-deposition` (Gitea) and `github:main` (GitHub Pages) updated. Headless verified:
`drawError: null`, ~97% render, `node --check` clean. (The earlier b719c05 container-move deploy is superseded.)

## ✅ INVESTIGATED 2026-07-01: particle reach vs Ground-Level Air footprint edge — NOT A BUG (no change)
User asked why particles don't line up with the far edge of the air footprint. Traced it end-to-end:
- **Particles advect on the MEDIAN hourly wind** (`build_wind_grid_for_filter` ~2221: `global_dlat =
  all_dlats[n//2]`). By construction half of HYSPLIT's real particles moved farther each hour; the contour's outer
  edge is drawn by that faster/more-dispersed tail. A median trajectory reaches the plume's dense CORE, not the
  leading edge → edge shortfall is expected & physically faithful, not miscalibrated.
- **The far edge is the lowest band.** Harness: particle reach ~0.25–0.58°, VISIBLE-band footprint ~0.24–1.37°
  (particles fill 28–167% of it; several facilities OVERSHOOT), but the FULL footprint is ~2.3–2.8° because its
  outer ~75% is the faintest 1e-9…1e-11 g/m³ bands hidden by `VISIBLE_DECADE_RATIO=32`.
- **Vertical nuance:** gating uses the 10 m ground-level air contour (`airBandAtPoint`, `props.layer==='air'`), so a
  stack particle genuinely aloft (100–300 m) that's carried past the ground-level plume is currently FADED OUT by
  the gate. User was OK with "higher & further out" particles but **chose to LEAVE AS-IS (accuracy over fill)** when
  offered a vertical-gate relaxation or a dispersion boost. No code change made. If ever revisited: relax the gate
  for elevated stack particles (most honest), or raise `SPREAD_KICK`/`TURB_*` for a fuller (noisier) look.

## ✅ SLIMMED 2026-07-01: index.html 58 MB → 33 MB (faster load)
User reported slow load. Two safe wins in the embed step (`calvert_plume_engine_one_day.py` ~2440):
(1) `historicalSimulationArchive` was `json.dumps(indent=2)` — ~18 MB of pure whitespace the browser had
to parse; switched both archives to `separators=(',', ':')` (compact). (2) Dropped `PLUME_DATA.particles`
(~3 MB raw PARDUMP timelines) from the embed — it only fed the commented-out `updateHysplitParticles`
replay, so it was dead weight (`_d['plumes'].pop('particles', None)` before dump). Verified headless:
`drawError: null`, ~97% render, no INIT_ERROR, `"particles":` gone from data. `deposition_grid` (6.65 MB)
was KEPT — still referenced by live code. Also fixed the FOOTPRINT LAYERS ⓘ tooltip: removed the false
"Frames update every 12h (macOS HYSPLIT constraint)" → "hourly (23 frames, sim hours 2–24)".

## ✅ UI 2026-07-01: "LAYERS" panel — 3 toggles + instant custom tooltip
Renamed the sidebar "FOOTPRINT LAYERS" → **"LAYERS"** and added a **Particle Simulation** toggle
(`id="particles-toggle"`, checked) beside Soil Deposition (`dep-layer-toggle`) and Ground-Level Air
(`air-layer-toggle`). Wired next to the other two (~3586): `showParticles = checked; drawParticles();`
(hides/shows particles; the sim keeps spawning/advecting underneath). Replaced the ⓘ **native `title=`**
tooltip (browsers delay it 3–4 s) with a **custom instant CSS popup** (`.dep-info-btn`→`.info-pop`,
`:hover`, z-index 10000) that explains all three layers AND how they differ (deposition accumulates /
air per-hour / particles animate continuously; footprints = HYSPLIT contours, particles = HYSPLIT wind).

## ✅ 2026-07-01: Embed ONLY modeled chemicals + drop unmodeled-only facilities
Non-default TRI chemicals were only modeled by the old particle method and could be toggled on to
flood the UI. Now the embed includes ONLY `DEFAULT_ACTIVE_CHEMICALS` (the 9 HYSPLIT-modeled species);
all other TRI compounds are dropped so they can't be shown. A facility that emits none of the 9 is
dropped from the map + point-source list. **Nothing is deleted from source** — the full `FACILITIES`
dict + TRI CSV stay; to re-add, put a chemical back in `DEFAULT_ACTIVE_CHEMICALS` and rerun.

Implementation — one shared helper `build_embedded_facilities()` (used by BOTH `compile_data_for_json`
AND the `--regen-html` fast path at ~5860, so they never diverge):
- Keeps chemicals whose name ∈ `DEFAULT_ACTIVE_CHEMICALS`; drops facilities with none.
- Re-indexes kept facilities to dense ids 0..M-1 and records `self.orig_to_new_fac_id`.
- `build_deposition_archive` remaps each manifest **entry**'s `fac_id` via that map (JS reads
  `entry.fac_id` only from the manifest, lines ~3800; combined entries stay `fac_id:-1`). On-disk
  manifests keep original ids — remap is in-memory per build (idempotent across regens).
- **Result: 12 → 8 facilities.** Dropped: CC Metals & Alloys, Sekisui, Wacker (0 modeled chems),
  Carbide Industries (only the mock `"SIMULATED POINT-SOURCE SPECIES"`, no HYSPLIT footprint).
- ⚠️ **Density gotcha (fixed):** JS spawn ratio = `chem_lbs / maxFacLbs`, and `maxFacLbs` was the max
  over EMBEDDED facilities' `total_lbs`. Dropping high-emission facilities (one had 720,080 lbs) shrank
  it → ~3× more particles. Fix: `total_lbs` stays the FULL per-facility total (not modeled-only), AND
  the density anchor is embedded from Python (`{max_fac_lbs_ref}` = `self.max_facility_lbs`, max over
  ALL 12) so `const maxFacLbs = Math.max({max_fac_lbs_ref}, ...)`. Particle density unchanged (~1500).
- No JS logic changes needed otherwise — markers/list/filters/particles are all data-driven off
  `PLUME_DATA.facilities`.

## ✅ 2026-07-01: Removed Simulation Sandbox + added Veterinary Clinic landmarks
**Sandbox removed:** the "⚙ Simulation Sandbox" panel (density/size/opacity/footprint-opacity sliders)
+ its `initSandbox()` IIFE are deleted so viewers can't alter the model. The `getSandbox*()` getters
already null-guard → they return their built-in defaults (density 1.0, size `BASE_PARTICLE_RADIUS_PIXELS`,
opacities 0.70), and `footprintOpacity` stays 0.45. `.sandbox-*` CSS left in place (harmless, unused).

**Veterinary clinics (LOCATIONS layer):** 15 clinics in `VET_CLINICS` (module-level, near
`DEFAULT_ACTIVE_CHEMICALS`; name/address/lat/lon). Geocoded via OSM Nominatim + US Census geocoder
(3 rural ones). Embedded as `const VET_CLINICS` (next to depositionArchive). Rendered as anchored
Leaflet markers (markerPane → NO zoom drift) in a `vetClinicLayer` LayerGroup, custom teal-pin +
white-paw + red-cross SVG divIcon (`vetIcon`, `.vet-clinic-divicon`). Click → popup (`vetPopupHtml`)
with name, address, and **soil deposition at that point** via `soilDepAtPoint(lat,lon)` (reuses
`depHitIndex` drawn combined dep footprints + `depPointInRing` + `fmtConc`; risk from min band). New
sidebar **LOCATIONS** collapsible (under LAYERS) with a **Veterinary Clinics** toggle
(`vet-clinics-toggle`, default on) + collapse arrow (`locations-toggle`/`-body`/`-arrow`). To add more
landmark types later: extend the LOCATIONS body + add another LayerGroup. Particle density unchanged
(~1500); file still ~33 MB.

## ✅ 2026-07-02: THREE simulation days + clinic deposition popups (public release build)
**Multi-date (switchable):** the embed now carries THREE days, chosen so soil deposition demonstrably
reaches the vet clinics on real weather:
- **2024-01-08** (DEFAULT / `START_DATE`) — storm with 24 h of *easterly* wind (plume blows WEST) + rain
  → heavy deposition over the Paducah clinic cluster. Visible footprint covers 11/15 clinics (9 of the
  Paducah cluster) with the CLEAN ratio-32 footprint (no expansion needed).
- **2025-02-15** — heavy rain (83 mm) but plume went north; 12/15 via popups.
- **2025-03-08** — original; SE toward Benton; 15/15 via popups.
- Date picker is now a **`<select>`** (was `<input type=date>`) populated from
  `Object.keys(historicalSimulationArchive)` (initDatePicker); switching hot-swaps plumes + deposition.
- **How days were picked:** trajectory previews (`hyts_std`, needs `bdyfiles/ASCDATA.CFG` in the run
  dir) show plume direction cheaply; then Open-Meteo archive API (free, no key, via curl — Python
  urllib TLS is broken on this Mac; DON'T disable TLS verification, the classifier blocks it) scans a
  year of Paducah hourly wind+precip to rank days by westward transport + rain. Clinics are mostly
  W/WNW of the source → need EASTERLY winds. Scan/measure scripts in `scratchpad/`.
- **How to add a day:** set `START_DATE`/`END_DATE` to it, run the full pipeline (auto-downloads HRRR
  if the `MET_YYYYMMDD.ARL` is absent; `dep_runs/{date}/` is date-namespaced so no stale-cdump bug),
  then MERGE with existing dates: extract each date's `historicalSimulationArchive` block from its
  index.html and call `generate_web_visualization({{all dates}})` — or just `--regen-html`, which now
  preserves EVERY embedded date (it reads all keys, rebuilds facilities per date, embeds all). Both
  `output/geojson/{date}/` dirs must be on disk. Merge drivers: `scratchpad/merge_dates.py`, `merge3.py`.

**Veterinary-clinic landmarks (already in place, see the 2026-07-01 LOCATIONS entry):** `VET_CLINICS`
(15, geocoded) render as anchored markers. **Click a clinic → popup** shows name, address, and the REAL
soil deposition there: `soilDepAtPoint()` queries the combined dep footprints across ALL bands (not the
drawn/visible subset) at the current frame + display mode → returns a per-chemical value list. The popup
shows the top chemical + level (`depRisk()`), then a clickable **"+N more ▾"** (`toggleVetChems()`) that
expands the full per-chemical breakdown with concentrations (`.vp-more`/`.vp-chemlist`/`.vp-chemrow`).
On 2024-01-08 e.g. Animal Wellness reads vinyl chloride Moderate + 7 more.

**Footprint visibility:** `DEP_VISIBLE_DECADE_RATIO` was tried at 100 to push the drawn footprint toward
the clinics but that reintroduced the grid "square" (tetrachloroethylene's 2-decade band reaches ~232 km,
past the ~220 km grid half-span). Kept at **32** (same as air). The right lever is choosing days whose
HIGH-concentration deposition actually blows over the clinics, not loosening the filter.

**Size — 3 full days at ~21 MB** (was 33 MB/day). Wins (all in `build_deposition_archive` /
`generate_web_visualization`): (1) **`EMBED_PER_FACILITY_FOOTPRINTS = False`** — drop the per-facility
footprint files (~55% of the deposition data / 25 MB). They fed only particle GATING (which falls back
to the COMBINED footprints in `airBandAtPoint`) and the per-facility % attribution in the deposition
hover readout (the ONLY feature lost — combined value, clinic popups, drawn footprints all unaffected).
Also clears `manifest["entries"]` so `airBandAtPoint` doesn't hit a dangling per-facility key and returns
combined instead. Set the flag True to restore (→ ~46 MB). (2) dropped `particles` + dead `deposition_grid`.
(3) compact JSON + `_slim_geojson()` (3 dp coords + decimate rings >8 pts). `MET_20250309..14.ARL` deleted
to free disk; `MET_20250308/0215/20240108.ARL` remain.

**✅ Heat/battery fixed (2026-07-02):** the `tick` loop repainted every rAF (pegged GPU/WindowServer,
esp. 120 Hz ProMotion). Fixes: (1) `document.hidden` guard skips all work when the tab's backgrounded
(+ `visibilitychange` nulls `lastTimestamp`); (2) `drawParticles()` + tooltip refresh moved INSIDE
`if (isPlaying)` so idle doesn't repaint (safe — every interaction handler calls `drawParticles()`
itself); (3) **`FRAME_MIN_MS = 1000/60`** caps the sim+render to 60 fps (halves 120 Hz load); (4) removed
the dead per-particle `liveDepGrid` accumulation (string+Map ops ×1500/frame, fed only the disabled
heatmap); (5) `maybeAnimateDep` real-time throttle (~150 ms, was ~12×/sec SVG rebuild).
⚠️ **Frame-rate-independent turbulence (`randCorr` in `advect`):** the random-walk jitter is scaled by
`sqrt(hourRate/(120·dtHours))` so its DIFFUSION matches the 120 fps reference at any fps. Without it, a
plain `*dtHours` random step jitters harder + over-diffuses at low fps — that's what made the 30 fps cap
look "shaky" and spread particles past the footprint late in the day. Deterministic advection still uses
full `dtHours`. If you ever change the fps cap, keep this.

## ⚠️ OPEN ITEMS (do in the particle-rework pass)
1. **Further slim the ~33 MB embed** — depositionArchive is still ~27 MB of GeoJSON. Next levers (riskier,
   affect visuals/hover/gating): decimate contour vertices harder, round coords to 3 dp, or embed only the
   footprints actually drawn (drop per-facility files used only for hover attribution + gating).
2. **`-v` fixed contour levels** (user-requested "correct fix"): `concplot -c1` auto-scales levels per
   field, so combined/stack/fugitive aren't level-for-level comparable (combined ammonia got 2-decade
   steps). Switch to explicit shared `-v` levels so band N = same g/m² everywhere. (The
   `VISIBLE_DECADE_RATIO=32` value-threshold already removed the "square" robustly in the meantime.)
3. **Multi-day engine (`calvert_plume_engine.py`) has DIVERGED** from one-day and was NOT given the
   missing-element/TDZ fix (it has different particle/heatmap code). index.html is generated from the
   ONE-DAY engine, so the app works, but the two are out of sync — reconcile during the rework.

## Scratch to clean before shipping
POC dirs under `plume-analysis/`: `poc_*`, `dep_runs/` and `output/geojson/` are generated (gitignore).
`/private/tmp/.../scratchpad/` has helper scripts (calib.py, reparse_bands.py, full_run.log).

## Key paths
HYSPLIT exec `/Users/nawrig04/hysplit/exec/` (hycs_std, concplot, concadd, con2asc, api2arl_v6).
Plan file: `/Users/nawrig04/.gemini/antigravity-ide/brain/a0d0cb3c-560d-4384-916f-564eac407ee0/implementation_plan.md`.
