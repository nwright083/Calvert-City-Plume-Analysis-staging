# ==============================================================================
# GLOBAL CONFIGURATION COMPONENT (CALVERT CITY PLUME SANDBOX)
# ==============================================================================
# --- MULTI-DATE BATCH PROCESSING CONTROLS ---
import os
START_DATE = "2024-01-08"  # default target date (YYYY-MM-DD); override per-run with --date
END_DATE = "2024-01-08"    # end of an inclusive date range (equal to START_DATE for a single day)

# Portable roots: default to the developer Mac, overridable by env vars for CI / other machines.
# HYSPLIT_ROOT is the install dir holding exec/, graphics/, bdyfiles/, share/eccodes/.
HYSPLIT_ROOT = os.environ.get("HYSPLIT_ROOT", "/Users/nawrig04/hysplit")
WEATHER_CACHE_DIR = os.environ.get("PLUME_WEATHER_CACHE", "~/hysplit/weather_cache")  # NOAA HRRR grids
WEATHER_BOX_RADIUS_KM = 50  # Bounding box size for local weather cropping

# --- LOCAL TRI EMISSIONS DATA PATH ---
# Workspace defaults to the script's own directory (the repo checkout on CI); override with PLUME_WORKSPACE.
_WORKSPACE_DIR = (os.environ.get("PLUME_WORKSPACE") or os.path.dirname(os.path.abspath(__file__))).rstrip("/") + "/"
_DRIVE_DIR = "/Users/nawrig04/Library/CloudStorage/GoogleDrive-wrightnicholas4@gmail.com/My Drive/Med school/SRSP Project/Plume Analysis/"

# Prefer local workspace copy; fall back to Google Drive only if local is missing
_local_tri = os.path.join(_WORKSPACE_DIR, "Marshall County Facility Release.csv")
LOCAL_TRI_CSV_PATH = _local_tri if os.path.exists(_local_tri) else os.path.join(_DRIVE_DIR, "Marshall County Facility Release.csv")

# --- DEFAULT ACTIVE HIGH-PRIORITY WHITELIST ---
# Chemicals on this list default to CHECKED (active) on map load. All other chemicals default to UNCHECKED.
DEFAULT_ACTIVE_CHEMICALS = [
    "VINYL CHLORIDE", "1,2-DICHLOROETHANE", "BENZENE", "1,3-BUTADIENE",
    "XYLENE (MIXED ISOMERS)", "TETRACHLOROETHYLENE", "1,2,4-TRICHLOROBENZENE",
    "CHLORINE", "AMMONIA", "NAPHTHALENE",
    "ETHYLENE OXIDE", "DICHLOROMETHANE", "CARBON TETRACHLORIDE"
]

# Friendly labels for the chemical-filter checkboxes. Injected into the page and derived from
# DEFAULT_ACTIVE_CHEMICALS at render time, so the filter list can NEVER drift from the modeled set
# again (adding a chemical above auto-adds its checkbox). Unlisted names fall back to title-case.
CHEMICAL_DISPLAY_NAMES = {
    "VINYL CHLORIDE": "Vinyl Chloride",
    "1,2-DICHLOROETHANE": "Ethylene Dichloride",
    "BENZENE": "Benzene",
    "1,3-BUTADIENE": "1,3-Butadiene",
    "XYLENE (MIXED ISOMERS)": "Xylenes",
    "TETRACHLOROETHYLENE": "Tetrachloroethylene",
    "1,2,4-TRICHLOROBENZENE": "1,2,4-TCB",
    "CHLORINE": "Chlorine",
    "AMMONIA": "Ammonia",
    "NAPHTHALENE": "Naphthalene",
    "ETHYLENE OXIDE": "Ethylene Oxide",
    "DICHLOROMETHANE": "Dichloromethane",
    "CARBON TETRACHLORIDE": "Carbon Tet",
}

# Embed per-facility deposition footprints in index.html? They are ~55% of the deposition data and are
# used only for particle gating (which falls back to the combined footprints) and the per-facility %
# breakdown in the deposition hover readout. False → much smaller file, losing only that hover-%.
EMBED_PER_FACILITY_FOOTPRINTS = False

# --- ROLLING-WINDOW SITE RETENTION (nightly auto-update) ---
# The site keeps the newest ROLLING_WINDOW_DAYS daily dates PLUS the curated showcase days below
# (kept forever, shown with a label in the date picker). build_site() prunes everything else.
ROLLING_WINDOW_DAYS = 30
PINNED_DATES = {
    "2024-01-08": "Storm — winds from the east (plume over Paducah)",
    "2025-02-15": "Heavy rain — strong deposition",
    "2025-03-08": "Southeast winds (toward Benton)",
}

# --- LANDMARK LOCATIONS: VETERINARY CLINICS ---
# Public-facing landmarks shown on the map (toggleable under LAYERS → LOCATIONS). Coordinates were
# geocoded from the street addresses (OpenStreetMap Nominatim; US Census geocoder for the few
# rural addresses Nominatim missed). Rendered as anchored Leaflet markers (no zoom drift).
VET_CLINICS = [
    {"name": "Ceglinski Animal Clinic",         "address": "5401 Blandville Rd, Paducah, KY 42001",       "lat": 37.05089, "lon": -88.67557},
    {"name": "Calvert City Animal Hospital",    "address": "4267 US-62, Calvert City, KY 42029",          "lat": 37.00378, "lon": -88.34534},
    {"name": "Lone Oak Animal Clinic",          "address": "125 Augusta Ave, Paducah, KY 42003",          "lat": 37.03694, "lon": -88.66204},
    {"name": "Heartland Veterinary Hospital",   "address": "3137 Olivet Church Rd, Paducah, KY 42001",    "lat": 37.07749, "lon": -88.69746},
    {"name": "Lakeland Animal Hospital",        "address": "2044 US-641, Benton, KY 42025",               "lat": 36.84647, "lon": -88.34991},
    {"name": "Companion Animal Hospital",       "address": "1831 US-641, Benton, KY 42025",               "lat": 36.84823, "lon": -88.34994},
    {"name": "Animal Kare Center",              "address": "2625 Olivet Church Rd, Paducah, KY 42001",    "lat": 37.06824, "lon": -88.70188},
    {"name": "Progressive Animal Healthcare",   "address": "2630 James Sanders Blvd, Paducah, KY 42001",  "lat": 37.08079, "lon": -88.68488},
    {"name": "Cummings Veterinary Clinic",      "address": "3800 Clarks River Rd, Paducah, KY 42003",     "lat": 37.04681, "lon": -88.55789},
    {"name": "Flanary Veterinary Clinic",       "address": "200 Eagle Nest Dr, Paducah, KY 42003",        "lat": 37.00849, "lon": -88.50918},
    {"name": "Lyon County Animal Hospital",     "address": "638 Trade Ave, Eddyville, KY 42038",          "lat": 37.08869, "lon": -88.08644},
    {"name": "Paducah Veterinary Clinic",       "address": "3205 Central Ave, Paducah, KY 42001",         "lat": 37.07613, "lon": -88.64278},
    {"name": "Animal Wellness Center",          "address": "120 Cave Thomas Dr, Paducah, KY 42001",       "lat": 37.03130, "lon": -88.67080},
    {"name": "Veterinary Institute of Paducah", "address": "3526 Park Plaza Rd, Paducah, KY 42001",       "lat": 37.08201, "lon": -88.66502},
    {"name": "Equine Vet Services",             "address": "4025 Coleman Cut Rd, Paducah, KY 42001",      "lat": 36.96969, "lon": -88.76676},
]

# --- CHEMICAL-SPECIFIC DEPOSITION PROPERTIES DATABASE ---
# This table stores per-chemical physical parameters used for dry deposition calculations.
#
# ╔════════════════════════════════════════════════════════════════════════════════╗
# ║  ARCHITECTURE NOTE: WEIGHTED-AVERAGE DEPOSITION PER FACILITY                 ║
# ║                                                                              ║
# ║  Currently, HYSPLIT runs ONE simulation per facility with a single pollutant  ║
# ║  species ("POL"). To do truly per-chemical deposition would require running   ║
# ║  HYSPLIT once per chemical × per facility (e.g. 12 × 10+ = 120+ runs/day),   ║
# ║  which is prohibitively slow.                                                ║
# ║                                                                              ║
# ║  CURRENT APPROACH: We compute an EMISSION-WEIGHTED AVERAGE of Vd, mol_wt,    ║
# ║  and reactivity for each facility based on its TRI chemical mix. This gives   ║
# ║  HYSPLIT a single representative deposition velocity per facility that        ║
# ║  reflects the dominant chemicals being emitted.                              ║
# ║                                                                              ║
# ║  FUTURE UPGRADE PATH: To enable per-chemical deposition:                     ║
# ║  1. Define multiple pollutant species in the CONTROL file (one per chemical) ║
# ║  2. Set per-species emission rates from TRI data (stack_g_hr, fugitive_g_hr) ║
# ║  3. Set per-species deposition parameters from this table                    ║
# ║  4. Increase MAXPAR in SETUP.cfg to handle the additional particles          ║
# ║  5. Parse cdump output per-species for species-specific heatmaps             ║
# ║  See HYSPLIT User's Guide §5.3 "Multiple Species" for CONTROL file format.   ║
# ╚════════════════════════════════════════════════════════════════════════════════╝
#
# Parameter descriptions:
#   mol_wt      - Molecular weight (g/mol). Affects diffusivity in resistance model.
#   vd          - Fixed dry deposition velocity (m/s). Rate of gas transfer from air
#                 to surface. Non-reactive VOCs ~0.002-0.004, reactive gases ~0.015-0.020.
#   reactivity  - Surface reactivity ratio (Wesely 1989). 0.0 = non-reactive (most VOCs),
#                 0.1 = intermediate (NO2), 1.0 = highly reactive (O3, Cl2, HF).
#   henry_const - Effective Henry's Law constant (M/atm). Used for FUTURE wet deposition.
#                 Higher = more water-soluble = stronger rain washout.
#                 Pre-populated now so wet deposition is a simple config toggle later.
#
# Literature sources:
#   - Wesely (1989) "Parameterization of surface resistances to gaseous dry deposition"
#   - EPA CMAQ v5.3 chemical mechanism documentation
#   - NIST WebBook for molecular weights and Henry's Law constants
#   - Seinfeld & Pandis (2016) "Atmospheric Chemistry and Physics" Ch. 19
#
CHEMICAL_PROPERTIES = {
    # ── Priority chemicals (DEFAULT_ACTIVE_CHEMICALS) ──
    "VINYL CHLORIDE":       {"mol_wt": 62.5,  "vd": 0.003, "reactivity": 0.0,  "henry_const": 0.039},
    "CHLORINE":             {"mol_wt": 70.9,  "vd": 0.015, "reactivity": 1.0,  "henry_const": 0.062},
    "TRICHLOROETHYLENE":    {"mol_wt": 131.4, "vd": 0.004, "reactivity": 0.0,  "henry_const": 0.0098},
    "1,3-BUTADIENE":        {"mol_wt": 54.1,  "vd": 0.002, "reactivity": 0.0,  "henry_const": 0.013},
    "HYDROGEN FLUORIDE":    {"mol_wt": 20.0,  "vd": 0.020, "reactivity": 1.0,  "henry_const": 8300.0},
    "HYDROCHLORIC ACID":    {"mol_wt": 36.5,  "vd": 0.018, "reactivity": 1.0,  "henry_const": 19000.0},
    "AMMONIA":              {"mol_wt": 17.0,  "vd": 0.010, "reactivity": 0.0,  "henry_const": 62.0},
    "CHLOROFORM":           {"mol_wt": 119.4, "vd": 0.003, "reactivity": 0.0,  "henry_const": 0.25},
    "BENZENE":              {"mol_wt": 78.1,  "vd": 0.003, "reactivity": 0.0,  "henry_const": 0.18},
    "ETHYLENE OXIDE":       {"mol_wt": 44.1,  "vd": 0.005, "reactivity": 0.1,  "henry_const": 7.0},
    # ── Extended chemicals commonly seen in Calvert City TRI data ──
    "METHANOL":             {"mol_wt": 32.0,  "vd": 0.005, "reactivity": 0.0,  "henry_const": 220.0},
    "TOLUENE":              {"mol_wt": 92.1,  "vd": 0.003, "reactivity": 0.0,  "henry_const": 0.15},
    "STYRENE":              {"mol_wt": 104.2, "vd": 0.004, "reactivity": 0.1,  "henry_const": 0.29},
    "ETHYLENE DICHLORIDE":  {"mol_wt": 99.0,  "vd": 0.004, "reactivity": 0.0,  "henry_const": 0.087},
    "1,2-DICHLOROETHANE":   {"mol_wt": 99.0,  "vd": 0.004, "reactivity": 0.0,  "henry_const": 0.087},
    "DICHLOROMETHANE":      {"mol_wt": 84.9,  "vd": 0.003, "reactivity": 0.0,  "henry_const": 0.036},
    "ACETALDEHYDE":         {"mol_wt": 44.1,  "vd": 0.005, "reactivity": 0.0,  "henry_const": 15.0},
    "VINYL ACETATE":        {"mol_wt": 86.1,  "vd": 0.004, "reactivity": 0.0,  "henry_const": 0.5},
    "CYCLOHEXANE":          {"mol_wt": 84.2,  "vd": 0.002, "reactivity": 0.0,  "henry_const": 0.0058},
    "ETHYLBENZENE":         {"mol_wt": 106.2, "vd": 0.003, "reactivity": 0.0,  "henry_const": 0.13},
    "XYLENE (MIXED ISOMERS)": {"mol_wt": 106.2, "vd": 0.003, "reactivity": 0.0, "henry_const": 0.15},
    "NAPHTHALENE":          {"mol_wt": 128.2, "vd": 0.004, "reactivity": 0.0,  "henry_const": 0.022},
    "ACRYLIC ACID":         {"mol_wt": 72.1,  "vd": 0.008, "reactivity": 0.0,  "henry_const": 3400.0},
    "FORMIC ACID":          {"mol_wt": 46.0,  "vd": 0.008, "reactivity": 0.0,  "henry_const": 8900.0},
    "CARBON TETRACHLORIDE": {"mol_wt": 153.8, "vd": 0.002, "reactivity": 0.0,  "henry_const": 0.034},
    # ── Fallback entry for any chemical not explicitly listed ──
    "_DEFAULT":             {"mol_wt": 80.0,  "vd": 0.003, "reactivity": 0.0,  "henry_const": 1.0},
}

# --- UNIVERSAL EPA AIR QUALITY MONITORING CONTROLS ---
TARGET_STATE = "Kentucky"
TARGET_COUNTIES = ["Marshall", "McCracken", "Livingston"]
# Prefer local workspace; fall back to Google Drive only if no local EPA CSVs exist (any year).
import glob as _glob
BASE_DATA_DIR = _WORKSPACE_DIR if _glob.glob(_WORKSPACE_DIR + "hourly_*_*.csv") else _DRIVE_DIR

# Each entry carries the EPA file code; the actual CSV path is built per-run for the ACTIVE date's YEAR
# (hourly_<code>_<year>.csv) — so a 2026 date reads 2026 files, not the hardcoded 2025 ones. Missing
# files degrade gracefully to empty monitors (AQS publishes months late, so recent days show nothing).
EPA_MONITOR_CONFIG = {
    "PM2.5":    {"code": "88101",    "good": 12.0,  "mod": 35.4,  "unhealthy": 55.4},
    "VOCs":     {"code": "VOCS",     "good": 50.0,  "mod": 150.0, "unhealthy": 300.0},
    "Ozone":    {"code": "44201",    "good": 0.054, "mod": 0.070, "unhealthy": 0.085},
    "SO2":      {"code": "42401",    "good": 35.0,  "mod": 75.0,  "unhealthy": 185.0},
    "NO2":      {"code": "42602",    "good": 53.0,  "mod": 100.0, "unhealthy": 360.0},
    "HAPs":     {"code": "HAPS",     "good": 2.0,   "mod": 10.0,  "unhealthy": 25.0},
    "PM10":     {"code": "81102",    "good": 54.0,  "mod": 154.0, "unhealthy": 254.0},
    "NONOxNOy": {"code": "NONOxNOy", "good": 53.0,  "mod": 100.0, "unhealthy": 360.0},
}


# --- ENGINE MODIFIERS & PHYSICS ---
EMISSION_MULTIPLIER = 1.0  # Scales final output mass (e.g., 10.0 simulates a major leak)
RELEASE_HEIGHT_METERS = 15  # Starting vertical height in meters inside the HYSPLIT grid

# --- RENDERING & WEB VISUALIZATION CONTROLS ---
PARTICLES_PER_UNIT_EMISSION = 50  # Density multiplier for visual stream counts
MAX_PARTICLE_AGE_MINUTES = 120  # Lifespan of particle on canvas before complete opacity fade
SANDBOX_LIFESPAN_MINUTES = 360  # JS live-particle lifespan (decoupled from HYSPLIT khmax)
BASE_PARTICLE_RADIUS_PIXELS = 2.5  # Drawing size of individual dots on the map canvas
MAP_ZOOM_LEVEL = 12  # Default Leaflet initial zoom view setting

# # --- DYNAMIC PLUG-AND-PLAY FACILITIES MATRIX ---
# To add a new facility, simply paste a new key-value block below matching the format.
# csv_match_name: The prefix of the facility name as it appears in the TRI CSV export.
# The entire pipeline will dynamically scale to accommodate new entries automatically.
#
# --- HOW TO CONFIGURE OPERATING HOURS SCHEDULES ---
# By default, facilities operate "continuous" (24/7). If a facility operates on a 
# limited shift/discontinuous basis, you can define a shift schedule like this:
#
#     "schedule": {
#         "type": "shift",
#         "start_hour": 8.0,  # 8:00 AM (24-hour decimal float)
#         "end_hour": 17.0    # 5:00 PM (24-hour decimal float)
#     }
#
FACILITIES = {
    "Westlake Vinyls": {
        "coords": (37.04909631633214, -88.33221487571784),
        "color": "#FF00FF",
        "tri_id": "42029WSTLK2468I",
        "csv_match_name": "WESTLAKE VINYLS INC",
        "mock_fallback": {"stack_lbs": 206864, "fugitive_lbs": 0},
        "schedule": "continuous"
    },
    "Westlake PVC Plant": {
        "coords": (37.04497026897765, -88.34947586035418),
        "color": "#DA70D6",
        "tri_id": "42029PCFCWJOHNS",
        "csv_match_name": "WESTLAKE VINYLS INC. - PVC",
        "mock_fallback": {"stack_lbs": 153757, "fugitive_lbs": 0},
        "schedule": "continuous"
    },
    "Arkema Inc": {
        "coords": (37.05626272127821, -88.36652857343046),
        "color": "#00FFFF",
        "tri_id": "42029PNNWLALTON",
        "csv_match_name": "ARKEMA",
        "mock_fallback": {"stack_lbs": 125106, "fugitive_lbs": 0},
        "schedule": "continuous"
    },
    "CC Metals & Alloys": {
        "coords": (37.055574243875, -88.35030650294469),
        "color": "#FF4444",
        "tri_id": "42029SKWLLHIGHW",
        "csv_match_name": "CC METALS",
        "mock_fallback": {"stack_lbs": 58943, "fugitive_lbs": 0},
        "schedule": "continuous"
    },
    "Cymetech Corp": {
        "coords": (37.049673766088034, -88.33079423057185),
        "color": "#FF8C00",
        "tri_id": "42029CYMTC2468I",
        "csv_match_name": "CYMETECH",
        "mock_fallback": {"stack_lbs": 41, "fugitive_lbs": 0},
        "schedule": "continuous"
    },
    "Estron Chemicals": {
        "coords": (37.04510728259582, -88.35514068582937),
        "color": "#32CD32",
        "tri_id": "42029STRNCHIGHW",
        "csv_match_name": "ESTRON",
        "mock_fallback": {"stack_lbs": 24131, "fugitive_lbs": 0},
        "schedule": "continuous"
    },
    "Evonik Corp": {
        "coords": (37.04256178133411, -88.34571245940829),
        "color": "#FF1493",
        "tri_id": "42029DGSSCRTE28",
        "csv_match_name": "EVONIK",
        "mock_fallback": {"stack_lbs": 160390, "fugitive_lbs": 0},
        "schedule": "continuous"
    },
    "ISP Chemicals": {
        "coords": (37.04956777490956, -88.3610257943388),
        "color": "#00FF7F",
        "tri_id": "42029GFCHMHIGHW",
        "csv_match_name": "ISP CHEMICALS",
        "mock_fallback": {"stack_lbs": 241986, "fugitive_lbs": 0},
        "schedule": "continuous"
    },
    "Lubrizol Advanced Materials": {
        "coords": (37.04859077950765, -88.3317972924827),
        "color": "#9370DB",
        "tri_id": "42029NVNNC2468I",
        "csv_match_name": "LUBRIZOL",
        "mock_fallback": {"stack_lbs": 24386, "fugitive_lbs": 0},
        "schedule": "continuous"
    },
    "Sekisui Specialty Chemicals": {
        "coords": (37.043812105671584, -88.35109849432436),
        "color": "#FFD700",
        "tri_id": "42029CLNSL408NM",
        "csv_match_name": "SEKISUI",
        "mock_fallback": {"stack_lbs": 720080, "fugitive_lbs": 0},
        "schedule": "continuous"
    },
    "Wacker Chemical": {
        "coords": (37.04472839351968, -88.3534802959446),
        "color": "#1E90FF",
        "tri_id": "4202WWCKRC412NR",
        "csv_match_name": "WACKER",
        "mock_fallback": {"stack_lbs": 111346, "fugitive_lbs": 0},
        "schedule": "continuous"
    },
    "Carbide Industries": {
        "coords": (37.05339786418546, -88.34285478599523),
        "color": "#FFFF00",
        "tri_id": "42029THCRB3204I",
        "csv_match_name": "CARBIDE",
        "mock_fallback": {"stack_lbs": 85000, "fugitive_lbs": 10000},
        "schedule": "continuous"
    }
}    # ── To add a new facility, paste a new block above matching this format ──

TARGET_ZIP = "42029"
MAP_CENTER = (37.0317, -88.3542)
HYSPLIT_ENGINE_PATH = os.path.join(HYSPLIT_ROOT, "exec", "hycs_std")
GRIB_CONVERTER_PATH = os.path.join(HYSPLIT_ROOT, "exec", "api2arl_v6")
CONCPLOT_PATH = os.path.join(HYSPLIT_ROOT, "exec", "concplot")
CONCADD_PATH = os.path.join(HYSPLIT_ROOT, "exec", "concadd")
HYSPLIT_ARLMAP_PATH = os.path.join(HYSPLIT_ROOT, "graphics", "arlmap")

# Deposition output grid (decoupled from WEATHER_BOX_RADIUS_KM, which governs particles).
# Met (ARL) is full-CONUS HRRR, so the grid can be large with no weather re-download.
# Span 4.0° (~440km) captures the plume's realistic 24h reach; spacing 0.03° (~3.3km) matches
# HRRR's native 3km resolution (finer would be false precision).
DEP_GRID_SPAN = 4.0
DEP_GRID_SPACING = 0.03

DEP_CHEMICAL_TAGS = {
    "VINYL CHLORIDE":           "VCLR",
    "1,2-DICHLOROETHANE":       "EDC",
    "BENZENE":                  "BENZ",
    "1,3-BUTADIENE":            "BUTA",
    "XYLENE (MIXED ISOMERS)":   "XYL",
    "TETRACHLOROETHYLENE":      "PERC",
    "1,2,4-TRICHLOROBENZENE":   "TCB",
    "CHLORINE":                 "CL2",
    "AMMONIA":                  "NH3",
    "NAPHTHALENE":              "NAPH",
    "ETHYLENE OXIDE":           "ETOX",
    "DICHLOROMETHANE":          "DCM",
    "CARBON TETRACHLORIDE":     "CTET",
}

DEP_CHEMICAL_SLUGS = {
    "VINYL CHLORIDE":           "vinyl_chloride",
    "1,2-DICHLOROETHANE":       "12dichloroethane",
    "BENZENE":                  "benzene",
    "1,3-BUTADIENE":            "13butadiene",
    "XYLENE (MIXED ISOMERS)":   "xylene",
    "TETRACHLOROETHYLENE":      "tetrachloroethylene",
    "1,2,4-TRICHLOROBENZENE":   "124trichlorobenzene",
    "CHLORINE":                 "chlorine",
    "AMMONIA":                  "ammonia",
    "NAPHTHALENE":              "naphthalene",
    "ETHYLENE OXIDE":           "ethylene_oxide",
    "DICHLOROMETHANE":          "dichloromethane",
    "CARBON TETRACHLORIDE":     "carbon_tetrachloride",
}

CHEMICAL_DEPOSITION = {
    "VINYL CHLORIDE": {
        "mol_weight": 62.5, "dry_vd_ms": 0.003, "henry_M_atm": 0.069,
        "in_cloud_ratio": 0.0, "below_cloud_s": 0.0, "halflife_days": 1.5,
        "depositor_class": "negligible",
    },
    "1,2-DICHLOROETHANE": {
        "mol_weight": 99.0, "dry_vd_ms": 0.003, "henry_M_atm": 0.11,
        "in_cloud_ratio": 0.0, "below_cloud_s": 0.0, "halflife_days": 83.0,
        "depositor_class": "negligible",
    },
    "BENZENE": {
        "mol_weight": 78.1, "dry_vd_ms": 0.003, "henry_M_atm": 0.18,
        "in_cloud_ratio": 0.0, "below_cloud_s": 0.0, "halflife_days": 9.7,
        "depositor_class": "negligible",
    },
    "1,3-BUTADIENE": {
        "mol_weight": 54.1, "dry_vd_ms": 0.003, "henry_M_atm": 0.058,
        "in_cloud_ratio": 0.0, "below_cloud_s": 0.0, "halflife_days": 1.4,
        "depositor_class": "negligible",
    },
    "XYLENE (MIXED ISOMERS)": {
        "mol_weight": 106.2, "dry_vd_ms": 0.003, "henry_M_atm": 0.21,
        "in_cloud_ratio": 0.0, "below_cloud_s": 0.0, "halflife_days": 0.7,
        "depositor_class": "negligible",
    },
    "TETRACHLOROETHYLENE": {
        "mol_weight": 165.8, "dry_vd_ms": 0.003, "henry_M_atm": 0.027,
        "in_cloud_ratio": 0.0, "below_cloud_s": 0.0, "halflife_days": 117.0,
        "depositor_class": "negligible",
    },
    "1,2,4-TRICHLOROBENZENE": {
        "mol_weight": 181.4, "dry_vd_ms": 0.004, "henry_M_atm": 0.032,
        "in_cloud_ratio": 0.0, "below_cloud_s": 0.0, "halflife_days": 48.0,
        "depositor_class": "low-moderate",
    },
    "CHLORINE": {
        "mol_weight": 70.9, "dry_vd_ms": 0.010, "henry_M_atm": 0.093,
        "in_cloud_ratio": 2.0e5, "below_cloud_s": 3.0e-4, "halflife_days": 0.5,
        "depositor_class": "moderate",
    },
    "AMMONIA": {
        "mol_weight": 17.0, "dry_vd_ms": 0.016, "henry_M_atm": 60.0,
        "in_cloud_ratio": 2.0e5, "below_cloud_s": 5.0e-4, "halflife_days": 30.0,
        "depositor_class": "strong",
    },
    "NAPHTHALENE": {
        # Semivolatile PAH: short atmospheric lifetime (fast OH reaction), modest dry deposition.
        "mol_weight": 128.2, "dry_vd_ms": 0.004, "henry_M_atm": 0.02,
        "in_cloud_ratio": 0.0, "below_cloud_s": 0.0, "halflife_days": 0.7,
        "depositor_class": "low-moderate",
    },
    "ETHYLENE OXIDE": {
        # Volatile, water-soluble gas; low dry deposition, long chemical lifetime (~120 d vs OH).
        "mol_weight": 44.05, "dry_vd_ms": 0.005, "henry_M_atm": 8.4,
        "in_cloud_ratio": 0.0, "below_cloud_s": 0.0, "halflife_days": 120.0,
        "depositor_class": "negligible",
    },
    "DICHLOROMETHANE": {
        # Volatile chlorinated solvent; negligible deposition, atmospheric lifetime ~4-5 months.
        "mol_weight": 84.93, "dry_vd_ms": 0.003, "henry_M_atm": 0.13,
        "in_cloud_ratio": 0.0, "below_cloud_s": 0.0, "halflife_days": 140.0,
        "depositor_class": "negligible",
    },
    "CARBON TETRACHLORIDE": {
        # Extremely persistent, unreactive, volatile; negligible deposition (multi-year lifetime).
        "mol_weight": 153.82, "dry_vd_ms": 0.002, "henry_M_atm": 0.034,
        "in_cloud_ratio": 0.0, "below_cloud_s": 0.0, "halflife_days": 10000.0,
        "depositor_class": "negligible",
    },
}
# ==============================================================================

import os
import sys
import glob
import json
import math
import shutil
import time
import datetime
import subprocess
import argparse
import csv
import xml.etree.ElementTree as ET
from typing import Dict, List, Any

class CalvertCityPlumeEngine:
    """
    Orchestration class for the Calvert City HYSPLIT dispersion modeling and visualization pipeline.
    """
    
    def __init__(self, workspace_dir: str, output_html_name: str = "index.html"):
        """
        Initialize the dispersion engine configuration.
        
        Args:
            workspace_dir: Absolute path to the simulation workspace directory.
            output_html_name: Filename for the generated interactive HTML visualization.
        """
        self.original_workspace_dir = os.path.abspath(workspace_dir)
        self.workspace_dir = self.original_workspace_dir
        
        # Check if workspace_dir has spaces. HYSPLIT and api2arl require space-free paths.
        if " " in self.workspace_dir:
            home_dir = os.path.expanduser("~")
            symlink_path = os.path.join(home_dir, "plume_workspace_link")
            
            # Remove existing link or file if one exists
            if os.path.exists(symlink_path) or os.path.islink(symlink_path):
                try:
                    if os.path.islink(symlink_path):
                        os.unlink(symlink_path)
                    elif os.path.isdir(symlink_path):
                        shutil.rmtree(symlink_path)
                    else:
                        os.remove(symlink_path)
                except Exception as e:
                    print(f"Warning: Could not remove existing link {symlink_path}: {e}")
            
            try:
                os.symlink(self.original_workspace_dir, symlink_path)
                print(f"Created space-free symlink: {symlink_path} -> {self.original_workspace_dir}")
                self.workspace_dir = symlink_path
            except Exception as e:
                print(f"Error creating symlink {symlink_path}: {e}. Proceeding with original path (may fail).")
                
        # Resolve executables from global configuration paths
        self.hycs_std_path = os.path.abspath(HYSPLIT_ENGINE_PATH)
        self.hysplit_exec_dir = os.path.dirname(self.hycs_std_path)
        self.api2arl_path = os.path.abspath(GRIB_CONVERTER_PATH)
        self.par2asc_path = os.path.join(self.hysplit_exec_dir, "par2asc")
        self.output_html_name = output_html_name
        
        # Parse simulation date from START_DATE
        self.set_active_date(START_DATE)
        
        # ecCodes definitions path — required by api2arl_v6 to decode GRIB2 files. Env override wins
        # (e.g. CI uses the apt libeccodes-tools install); else derive from the HYSPLIT tree. The Linux
        # static tarball does NOT bundle eccodes, so on CI this is left unset and the system default
        # (apt: /usr/share/eccodes/definitions) applies — _convert_one_grib only exports the var if the
        # path actually exists.
        self.eccodes_defs_path = os.environ.get("ECCODES_DEFINITION_PATH") or os.path.join(
            os.path.dirname(self.hysplit_exec_dir), "share", "eccodes", "definitions"
        )
        if not os.path.isdir(self.eccodes_defs_path):
            print(f"Note: ecCodes definitions not found at {self.eccodes_defs_path}; "
                  f"api2arl will use the system default (set ECCODES_DEFINITION_PATH to override).")
        
        # Core industrial facilities configuration with dynamic geolocation harvesting
        import pandas as pd
        df_coords = None
        if os.path.exists(LOCAL_TRI_CSV_PATH):
            try:
                df_coords = pd.read_csv(LOCAL_TRI_CSV_PATH)
                print(f"Loaded CSV using pandas for coordinate harvesting: {LOCAL_TRI_CSV_PATH}")
            except Exception as e:
                print(f"Error loading CSV with pandas: {e}")

        self.facilities = []
        for idx, (name, details) in enumerate(FACILITIES.items()):
            lat = details["coords"][0]
            lon = details["coords"][1]
            
            # Dynamic coordinate harvesting (only fallback if manual coordinates are missing/zero)
            if (lat == 0.0 or lon == 0.0) and df_coords is not None and "facility name" in df_coords.columns:
                csv_match = details.get("csv_match_name", "").upper()
                if csv_match:
                    matched_rows = df_coords[df_coords["facility name"].str.upper().str.startswith(csv_match, na=False)]
                    if matched_rows.empty:
                        matched_rows = df_coords[df_coords["facility name"].str.upper().str.contains(csv_match, na=False)]
                    
                    if not matched_rows.empty:
                        row_lat = matched_rows.iloc[0].get("latitude")
                        row_lon = matched_rows.iloc[0].get("longitude")
                        try:
                            # parse absolute values
                            parsed_lat = abs(float(row_lat))
                            parsed_lon = -abs(float(row_lon))  # Longitude in USA is negative
                            if not math.isnan(parsed_lat) and not math.isnan(parsed_lon):
                                lat = parsed_lat
                                lon = parsed_lon
                                print(f"Dynamically harvested coordinates for {name}: ({lat}, {lon})")
                        except Exception as e:
                            print(f"Error parsing coordinates for {name}: {e}")

            self.facilities.append({
                "id": idx,
                "name": name,
                "lat": lat,
                "lon": lon,
                "height": float(RELEASE_HEIGHT_METERS),
                "color": details["color"],
                "tri_id": details["tri_id"],
                "schedule": details.get("schedule", "continuous")
            })
            
        # Grid variables and directories
        # WEATHER_CACHE_DIR supports user home expanding
        self.grib_dir = os.path.expanduser(WEATHER_CACHE_DIR)
        
        # Initialize file system structures
        os.makedirs(self.workspace_dir, exist_ok=True)
        os.makedirs(self.grib_dir, exist_ok=True)
        
        # Parse TRI CSV release data once at initialization
        self.tri_csv_path = LOCAL_TRI_CSV_PATH
        self.tri_data = self.parse_tri_csv()
        
        # Precompute maximum emissions across all facilities for relative scaling
        all_totals = []
        for fac in self.facilities:
            tri_data = self.get_facility_releases(fac["name"])
            releases = tri_data.get("releases", [])
            total_lbs = sum(chem.get("total_lbs", 0.0) for chem in releases)
            all_totals.append(total_lbs)
        self.max_facility_lbs = max(all_totals) if all_totals else 1.0
        if self.max_facility_lbs == 0.0:
            self.max_facility_lbs = 1.0

    def set_active_date(self, date_str: str):
        """
        Set the active simulation date and update all dependent variables and paths.
        """
        self.date_str = date_str
        self.date_obj = datetime.datetime.strptime(self.date_str, "%Y-%m-%d")
        self.met_file_path = os.path.join(self.workspace_dir, f"MET_{self.date_obj.strftime('%Y%m%d')}.ARL")
        
    def parse_tri_csv(self) -> Dict[str, list]:
        """
        Parse the TRI Explorer release CSV file.
        Ingests the local TRI file, harvesting facility locations and emissions.
        """
        if not os.path.exists(self.tri_csv_path):
            print(f"Warning: TRI CSV file not found at {self.tri_csv_path}. Will use mock fallback data.")
            return {}
        
        result = {}
        try:
            with open(self.tri_csv_path, "r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    fac_name = row.get("facility name", "").strip().upper()
                    if not fac_name:
                        continue
                    
                    chem_name = row.get("chemical", "").strip().upper()
                    if not chem_name:
                        continue
                        
                    # Extract fugitive and stack air releases in pounds
                    fugitive_lbs = self._parse_tri_amount(row.get("5.1 - fugitive air", "0"))
                    stack_lbs = self._parse_tri_amount(row.get("5.2 - stack air", "0"))
                    total_lbs = fugitive_lbs + stack_lbs
                    
                    # Calculate grams/hour values
                    conv_factor = 453.59237 / 8760.0
                    fugitive_g_hr = fugitive_lbs * conv_factor
                    stack_g_hr = stack_lbs * conv_factor
                    
                    # Determine default active state status
                    default_active = chem_name in DEFAULT_ACTIVE_CHEMICALS
                    
                    if fac_name not in result:
                        result[fac_name] = []
                        
                    # Consolidate duplicate chemical entries if they exist
                    existing = [c for c in result[fac_name] if c["chemical"] == chem_name]
                    if existing:
                        existing[0]["stack_lbs"] = round(existing[0]["stack_lbs"] + stack_lbs, 2)
                        existing[0]["fugitive_lbs"] = round(existing[0]["fugitive_lbs"] + fugitive_lbs, 2)
                        existing[0]["total_lbs"] = round(existing[0]["total_lbs"] + total_lbs, 2)
                        existing[0]["stack_g_hr"] = round(existing[0]["stack_g_hr"] + stack_g_hr, 4)
                        existing[0]["fugitive_g_hr"] = round(existing[0]["fugitive_g_hr"] + fugitive_g_hr, 4)
                    else:
                        result[fac_name].append({
                            "chemical": chem_name,
                            "stack_lbs": round(stack_lbs, 2),
                            "fugitive_lbs": round(fugitive_lbs, 2),
                            "total_lbs": round(total_lbs, 2),
                            "stack_g_hr": round(stack_g_hr, 4),
                            "fugitive_g_hr": round(fugitive_g_hr, 4),
                            "defaultActive": default_active
                        })
        except Exception as e:
            print(f"Error parsing flat TRI CSV: {e}")
            return {}
            
        print(f"Parsed TRI CSV: {len(result)} facilities loaded from {os.path.basename(self.tri_csv_path)}")
        for fac_key in result:
            print(f"  {fac_key}: {len(result[fac_key])} chemicals")
        return result
    
    @staticmethod
    def _parse_tri_amount(raw_value: str) -> float:
        """Parse a TRI numeric field, handling commas, leading whitespace, and '.' as zero."""
        if not raw_value or raw_value.strip() in (".", "**", "NA", ""):
            return 0.0
        try:
            return float(raw_value.strip().replace(",", ""))
        except (ValueError, TypeError):
            return 0.0
    
    def get_facility_releases(self, facility_name: str) -> Dict[str, Any]:
        """
        Look up a facility's chemical release data from the parsed TRI CSV.
        Matches using the csv_match_name field from the FACILITIES config dict.
        Falls back to mock_fallback data if no CSV match is found.
        
        Matching priority: exact match > startswith > contains, preferring shortest key.
        """
        fac_config = FACILITIES.get(facility_name, {})
        csv_match = fac_config.get("csv_match_name", "")
        
        if csv_match and self.tri_data:
            csv_match_upper = csv_match.upper()
            
            # Try exact match first
            if csv_match_upper in self.tri_data:
                releases = self.tri_data[csv_match_upper]
                sorted_releases = sorted(releases, key=lambda x: x["total_lbs"], reverse=True)
                print(f"CSV match for {facility_name}: {len(sorted_releases)} chemicals (exact match '{csv_match}')")
                return {"fac_name": facility_name, "releases": sorted_releases, "source": "csv"}
            
            # Try startswith, prefer shortest key (most specific)
            candidates = [(k, v) for k, v in self.tri_data.items() 
                          if k.startswith(csv_match_upper) or csv_match_upper in k]
            if candidates:
                # Sort by key length so the most specific (shortest) match wins
                candidates.sort(key=lambda x: len(x[0]))
                best_key, releases = candidates[0]
                sorted_releases = sorted(releases, key=lambda x: x["total_lbs"], reverse=True)
                print(f"CSV match for {facility_name}: {len(sorted_releases)} chemicals (matched '{csv_match}' -> '{best_key}')")
                return {"fac_name": facility_name, "releases": sorted_releases, "source": "csv"}
        
        print(f"No CSV match for {facility_name} (csv_match_name='{csv_match}'). Using mock fallback.")
        return self._get_mock_tri_data(facility_name)
    
    def _get_mock_tri_data(self, facility_name: str) -> Dict[str, Any]:
        """
        Produce a mock emissions record from the facility's embedded mock_fallback config.
        """
        fac_config = FACILITIES.get(facility_name, {})
        mock_data = fac_config.get("mock_fallback", {"stack_lbs": 10000, "fugitive_lbs": 5000})
        stack_lbs = mock_data.get("stack_lbs", 0)
        fugitive_lbs = mock_data.get("fugitive_lbs", 0)
        total_lbs = stack_lbs + fugitive_lbs
        
        conv_factor = 453.59237 / 8760.0
        stack_g_hr = stack_lbs * conv_factor
        fugitive_g_hr = fugitive_lbs * conv_factor
        
        return {
            "fac_name": facility_name.upper(),
            "releases": [
                {
                    "chemical": "SIMULATED POINT-SOURCE SPECIES",
                    "stack_lbs": float(stack_lbs),
                    "fugitive_lbs": float(fugitive_lbs),
                    "total_lbs": float(total_lbs),
                    "stack_g_hr": round(stack_g_hr, 4),
                    "fugitive_g_hr": round(fugitive_g_hr, 4),
                    "defaultActive": True
                }
            ],
            "source": "mock"
        }

    def download_weather_data(self) -> List[str]:
        """
        Retrieve 24 hourly NOAA HRRR GRIB2 files using the Herbie library.
        Bound strictly to self.date_obj and global cache directory structure.
        
        Returns:
            List of absolute paths to downloaded GRIB2 files.
        """
        print(f"Starting NOAA HRRR weather data download via Herbie for {self.date_str}...")
        from herbie import Herbie
        
        grib_files = []
        for hour in range(24):
            dt_hour = self.date_obj.replace(hour=hour)
            date_time_str = dt_hour.strftime("%Y-%m-%d %H:%M")
            print(f"Downloading HRRR grid for simulation hour {hour:02d}:00 ({date_time_str})...")
            try:
                # Retrieve HRRR pressure level grid (fxx=0 represents analysis hour)
                h = Herbie(
                    dt_hour,
                    model="hrrr",
                    product="prs",
                    fxx=0,
                    save_dir=self.grib_dir
                )
                file_path = h.download()
                if file_path and os.path.exists(file_path):
                    print(f"File cached at: {file_path}")
                    grib_files.append(str(file_path))
                else:
                    print(f"Warning: Download returned empty or path does not exist for hour {hour}.")
            except Exception as e:
                print(f"Error downloading weather grid for hour {hour}: {e}")
                
        if not grib_files:
            raise RuntimeError("Weather download yielded zero files. Simulation aborted.")
            
        print(f"Successfully retrieved {len(grib_files)} weather grid files.")
        return grib_files

    def convert_grib_to_arl(self, grib_files: List[str]):
        """
        Convert weather grids to HYSPLIT ARL format using api2arl_v6.
        Concatenates hourly conversions into a single daily ARL meteorology file.
        
        Args:
            grib_files: List of file paths to raw GRIB2 files.
        """
        print("Converting GRIB2 files to HYSPLIT ARL format using api2arl_v6...")
        if not os.path.exists(self.api2arl_path):
            raise FileNotFoundError(f"HYSPLIT api2arl_v6 executable not found at {self.api2arl_path}")
            
        if os.path.exists(self.met_file_path):
            os.remove(self.met_file_path)

        # Sort files chronologically to maintain ARL record consistency
        for idx, grib_file in enumerate(sorted(grib_files)):
            print(f"Processing grid file {idx+1}/{len(grib_files)}: {os.path.basename(grib_file)}")
            self._convert_one_grib(grib_file)

        if not os.path.exists(self.met_file_path) or os.path.getsize(self.met_file_path) == 0:
            raise RuntimeError("Daily ARL meteorology file is empty or was not created.")

        print(f"Successfully compiled meteorology file: {self.met_file_path}")

    def _convert_one_grib(self, grib_file: str) -> bool:
        """Convert ONE HRRR GRIB2 hour to ARL and append it to the daily met file (self.met_file_path).
        Returns True on success. Used by both the bulk and streaming conversion paths.
        """
        grib_dir = os.path.dirname(grib_file)
        grib_filename = os.path.basename(grib_file)
        local_temp_arl = os.path.join(grib_dir, "DATA.ARL")
        local_cfg_path = os.path.join(grib_dir, "arldata.cfg")
        for tmp in (local_temp_arl, local_cfg_path):
            if os.path.exists(tmp):
                os.remove(tmp)

        cmd = [self.api2arl_path, f"-i{grib_filename}", "-oDATA.ARL", "-z1"]
        run_env = os.environ.copy()
        # Only pin ECCODES_DEFINITION_PATH if our path exists; otherwise leave the system default
        # (CI's apt eccodes) in place rather than pointing api2arl at a missing directory.
        if os.path.isdir(self.eccodes_defs_path):
            run_env["ECCODES_DEFINITION_PATH"] = self.eccodes_defs_path
        try:
            result = subprocess.run(cmd, cwd=grib_dir, env=run_env,
                                    stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, timeout=180)
            if result.returncode != 0:
                print(f"  Error converting {grib_filename}: code {result.returncode}\n  Stderr: {result.stderr[:300]}")
                return False
            if os.path.exists(local_temp_arl):
                with open(self.met_file_path, "ab") as dest, open(local_temp_arl, "rb") as src:
                    shutil.copyfileobj(src, dest)
                os.remove(local_temp_arl)
            else:
                print(f"  Warning: expected {local_temp_arl} not found after conversion.")
                return False
            if os.path.exists(local_cfg_path):
                os.remove(local_cfg_path)
            return True
        except subprocess.TimeoutExpired:
            print(f"  Timeout converting {grib_filename}.")
        except Exception as e:
            print(f"  Unexpected error converting {grib_filename}: {e}")
        return False

    def download_and_convert_streaming(self) -> None:
        """Disk-frugal weather build for CI: for each hour, download the GRIB, convert+append it to the
        daily ARL, then DELETE the GRIB. Peak disk ≈ one ARL (~12 GB) + one GRIB (~0.6 GB) instead of
        ~24 GRIBs (~13 GB) + the ARL at once — so it fits a GitHub Actions runner. Same ARL result as
        download_weather_data()+convert_grib_to_arl().
        """
        print(f"Streaming HRRR download+convert for {self.date_str} (per-hour, deletes GRIBs as it goes)...")
        from herbie import Herbie
        if not os.path.exists(self.api2arl_path):
            raise FileNotFoundError(f"HYSPLIT api2arl_v6 not found at {self.api2arl_path}")
        if os.path.exists(self.met_file_path):
            os.remove(self.met_file_path)

        ok_hours = 0
        for hour in range(24):
            dt_hour = self.date_obj.replace(hour=hour)
            try:
                h = Herbie(dt_hour, model="hrrr", product="prs", fxx=0, save_dir=self.grib_dir)
                fp = h.download()
                if not fp or not os.path.exists(fp):
                    print(f"  Hour {hour:02d}: download returned nothing; skipping.")
                    continue
                fp = str(fp)
                if self._convert_one_grib(fp):
                    ok_hours += 1
                    print(f"  Hour {hour:02d}: converted + appended ({ok_hours} total).")
            except Exception as e:
                print(f"  Hour {hour:02d}: {e}")
            finally:
                # Delete this hour's GRIB immediately to bound disk (whether or not convert succeeded).
                try:
                    if 'fp' in dir() and fp and os.path.exists(fp):
                        os.remove(fp)
                except OSError:
                    pass

        if ok_hours == 0 or not os.path.exists(self.met_file_path) or os.path.getsize(self.met_file_path) == 0:
            raise RuntimeError(f"Streaming weather build produced no usable ARL ({ok_hours} hours converted).")
        print(f"Streaming ARL built: {self.met_file_path} ({ok_hours}/24 hours, {os.path.getsize(self.met_file_path)/1e9:.1f} GB)")

    def _compute_facility_deposition_params(self, facility_name: str) -> dict:
        """
        Compute emission-weighted average dry deposition parameters for a facility.
        
        This method implements the WEIGHTED-AVERAGE DEPOSITION approach described
        in the CHEMICAL_PROPERTIES architecture note. For each facility, it:
        
        1. Retrieves the facility's chemical release list from TRI data
        2. Looks up each chemical's properties in CHEMICAL_PROPERTIES
        3. Computes emission-weighted averages of Vd, molecular weight, and reactivity
        4. Returns these as HYSPLIT CONTROL file deposition parameters
        
        The weights are based on each chemical's total_lbs emission. Chemicals
        emitting more mass have proportionally more influence on the average.
        
        Example: If a facility emits 80% vinyl chloride (Vd=0.003) and 20% HCl (Vd=0.018),
        the weighted Vd = 0.80 * 0.003 + 0.20 * 0.018 = 0.006 m/s.
        
        Returns:
            Dict with keys: 'vd' (m/s), 'mol_wt' (g/mol), 'reactivity' (0-1)
        """
        defaults = CHEMICAL_PROPERTIES.get("_DEFAULT", {"mol_wt": 80.0, "vd": 0.003, "reactivity": 0.0})
        
        tri_data = self.get_facility_releases(facility_name)
        releases = tri_data.get("releases", [])
        
        if not releases:
            print(f"  Deposition: No release data for {facility_name}. Using defaults (Vd={defaults['vd']} m/s).")
            return {"vd": defaults["vd"], "mol_wt": defaults["mol_wt"], "reactivity": defaults["reactivity"]}
        
        # Accumulate emission-weighted sums
        total_weight = 0.0
        weighted_vd = 0.0
        weighted_mol_wt = 0.0
        weighted_reactivity = 0.0
        
        for chem in releases:
            chem_name = chem.get("chemical", "").upper().strip()
            emission_lbs = chem.get("total_lbs", 0.0)
            
            if emission_lbs <= 0:
                continue
            
            # Look up chemical properties; fall back to _DEFAULT for unlisted chemicals
            props = CHEMICAL_PROPERTIES.get(chem_name, defaults)
            
            total_weight += emission_lbs
            weighted_vd += emission_lbs * props["vd"]
            weighted_mol_wt += emission_lbs * props["mol_wt"]
            weighted_reactivity += emission_lbs * props["reactivity"]
        
        if total_weight <= 0:
            print(f"  Deposition: Zero total emissions for {facility_name}. Using defaults.")
            return {"vd": defaults["vd"], "mol_wt": defaults["mol_wt"], "reactivity": defaults["reactivity"]}
        
        result = {
            "vd": round(weighted_vd / total_weight, 6),
            "mol_wt": round(weighted_mol_wt / total_weight, 1),
            "reactivity": round(weighted_reactivity / total_weight, 3),
        }
        
        print(f"  Deposition params for {facility_name}: Vd={result['vd']:.4f} m/s, "
              f"MW={result['mol_wt']:.1f} g/mol, Reactivity={result['reactivity']:.3f} "
              f"(weighted from {len(releases)} chemicals, {total_weight:.0f} total lbs)")
        
        return result

    def write_control_file(self, run_dir: str, facility: Dict[str, Any]):
        """
        Generate a HYSPLIT CONTROL file configured for multi-species dispersion simulation.
        
        Each chemical emitted by the facility becomes its own HYSPLIT pollutant species,
        with per-chemical dry deposition (Vd, mol_wt, reactivity) and wet deposition
        (Henry's Law constant, scavenging coefficients) parameters sourced from
        CHEMICAL_PROPERTIES.
        
        Concentration grid includes level 0 (surface deposition) and level 100m (air
        concentration) so the cdump binary captures both for downstream parsing.
        
        Falls back to a single weighted-average species if no TRI chemical data is available.
        
        Args:
            run_dir: Directory where the CONTROL file should be written.
            facility: Dictionary containing facility release parameters.
        """
        control_path = os.path.join(run_dir, "CONTROL")
        
        # Dates formatted as double digit strings
        yy = self.date_obj.strftime("%y")
        mm = self.date_obj.strftime("%m")
        dd = self.date_obj.strftime("%d")
        
        # Dynamic calculation of grids based on WEATHER_BOX_RADIUS_KM (approx 111 km per degree)
        grid_span = float(WEATHER_BOX_RADIUS_KM) / 111.0
        grid_span_str = f"{grid_span:.3f} {grid_span:.3f}"
        
        # Retrieve per-chemical release data for this facility
        tri_data = self.get_facility_releases(facility["name"])
        releases = tri_data.get("releases", [])
        defaults = CHEMICAL_PROPERTIES.get("_DEFAULT", {"mol_wt": 80.0, "vd": 0.003, "reactivity": 0.0, "henry_const": 1.0})
        
        # Build species list: individual HYSPLIT species ONLY for DEFAULT_ACTIVE_CHEMICALS.
        # All other chemicals are lumped into a single "OTHR" weighted-average species
        # to keep the HYSPLIT run size manageable (10 priority species + 1 aggregate).
        species_list = []
        other_total_emission = 0.0
        other_weighted_vd = 0.0
        other_weighted_mw = 0.0
        other_weighted_react = 0.0
        other_weighted_henry = 0.0
        
        for chem in releases:
            chem_name = chem.get("chemical", "").upper().strip()
            total_lbs = chem.get("total_lbs", 0.0)
            if total_lbs <= 0:
                continue
            
            # Total emission rate in g/hr (stack + fugitive combined for HYSPLIT emission rate)
            emission_g_hr = chem.get("stack_g_hr", 0.0) + chem.get("fugitive_g_hr", 0.0)
            if emission_g_hr <= 0:
                continue
            
            # Look up per-chemical deposition properties
            props = CHEMICAL_PROPERTIES.get(chem_name, defaults)
            
            # Only create individual species for DEFAULT_ACTIVE_CHEMICALS
            if chem_name in DEFAULT_ACTIVE_CHEMICALS:
                # HYSPLIT species label: max 4 characters
                label = ''.join(c for c in chem_name if c.isalnum())[:4].upper()
                if not label:
                    label = "CHEM"
                # Ensure unique labels by appending index if duplicated
                existing_labels = [s["label"] for s in species_list]
                if label in existing_labels:
                    for suffix_idx in range(1, 100):
                        candidate = label[:3] + str(suffix_idx)
                        if candidate not in existing_labels:
                            label = candidate
                            break
                
                species_list.append({
                    "label": label,
                    "chem_name": chem_name,
                    "emission_g_hr": emission_g_hr,
                    "vd": props["vd"],
                    "mol_wt": props["mol_wt"],
                    "reactivity": props["reactivity"],
                    "henry_const": props.get("henry_const", defaults["henry_const"]),
                })
            else:
                # Accumulate for the "OTHR" (other) aggregate species
                other_total_emission += emission_g_hr
                other_weighted_vd += props["vd"] * emission_g_hr
                other_weighted_mw += props["mol_wt"] * emission_g_hr
                other_weighted_react += props["reactivity"] * emission_g_hr
                other_weighted_henry += props.get("henry_const", defaults["henry_const"]) * emission_g_hr
        
        # Add the aggregate "OTHR" species if any non-default chemicals had emissions
        if other_total_emission > 0:
            species_list.append({
                "label": "OTHR",
                "chem_name": "OTHER-AGGREGATE",
                "emission_g_hr": other_total_emission,
                "vd": other_weighted_vd / other_total_emission,
                "mol_wt": other_weighted_mw / other_total_emission,
                "reactivity": other_weighted_react / other_total_emission,
                "henry_const": other_weighted_henry / other_total_emission,
            })
        
        # Fallback: if no per-chemical data at all, use a single weighted-average species
        if not species_list:
            dep_params = self._compute_facility_deposition_params(facility["name"])
            species_list = [{
                "label": "POL",
                "chem_name": "WEIGHTED-AVERAGE",
                "emission_g_hr": 0.0,  # 0.0 means starting locations define rates
                "vd": dep_params["vd"],
                "mol_wt": dep_params["mol_wt"],
                "reactivity": dep_params["reactivity"],
                "henry_const": defaults["henry_const"],
            }]
        
        num_species = len(species_list)
        
        # ── Build CONTROL file lines ──
        lines = [
            f"{yy} {mm} {dd} 01",                             # Start time (YY MM DD HH) - 01 UTC (t00z met unavailable)
            "2",                                              # Number of starting locations (stack and fugitive)
            # Starting location 1: Elevated Stack (Point Source)
            f"{facility['lat']:.4f} {facility['lon']:.4f} 30.0 1.0 0.0",
            # Starting location 2: Ground-Level Fugitive (Area Source)
            f"{facility['lat']:.4f} {facility['lon']:.4f} 2.0 1.0 2500.0",
            "23",                                             # Simulation duration (hours) - 01 through 23 UTC
            "0",                                              # Vertical motion method (0 = use met data vertical velocity)
            "10000.0",                                        # Top of simulation model (m AGL)
            "1",                                              # Number of input meteorology files
            os.path.dirname(self.met_file_path) + "/",       # Directory of meteorology grid (with trailing slash)
            os.path.basename(self.met_file_path),             # Filename of meteorology grid
        ]
        
        # ── Pollutant species definitions (one block per chemical) ──
        lines.append(str(num_species))                        # Number of pollutant species
        for sp in species_list:
            lines.append(sp["label"])                          # Species identifier (max 4 chars)
            lines.append(f"{sp['emission_g_hr']:.4f}")         # Emission rate (g/hr)
            lines.append("23.0")                               # Emission duration (hours)
            lines.append(f"{yy} {mm} {dd} 01 00")              # Release start (YY MM DD HH MM)
        
        # ── Concentration grid definition ──
        lines.extend([
            "1",                                              # Number of concentration grids
            f"{MAP_CENTER[0]:.4f} {MAP_CENTER[1]:.4f}",       # Grid center from global configuration
            "0.02 0.02",                                      # High resolution grid spacing (degrees lat, lon)
            grid_span_str,                                    # Dynamic grid span derived from WEATHER_BOX_RADIUS_KM
            run_dir + "/",                                    # Output directory (with trailing slash)
            "cdump",                                          # Output filename prefix
            "2",                                              # Number of vertical concentration levels
            "0",                                              # Height 1: 0=surface deposition
            "100",                                            # Height 2: 100m=air concentration
            f"{yy} {mm} {dd} 00 00",                          # Dummy start time (bypasses grid calculation)
            f"{yy} {mm} {dd} 00 00",                          # Dummy stop time (bypasses grid calculation)
            "01 00 00",                                       # Averaging period (HH MM SS) - hourly snapshots
        ])
        
        # ── Deposition definition (one block per species) ──
        lines.append(str(num_species))                        # Number of depositing species
        for sp in species_list:
            # Line 1: Particle Characteristics (diameter, density, shape) -> all 0.0 for gas
            lines.append("0.0 0.0 0.0")
            # Line 2: Dry deposition: velocity(m/s), molecular_weight(g/mol), reactivity, diffusivity, effective Henry
            lines.append("0.0 0.0 0.0 0.0 0.0")
            # Line 3: Wet removal: Henry(M/atm), in-cloud_scav(1/s), below-cloud_scav(1/s)
            lines.append("0.0 0.0 0.0")
            # Line 4: Radioactive decay half-life (days)
            lines.append("0.0")
            # Line 5: Pollutant resuspension factor (1/m)
            lines.append("0.0")
        
        with open(control_path, "w") as f:
            f.write("\n".join(lines) + "\n")
        
        # Log summary
        species_summary = ", ".join(f"{sp['label']}({sp['chem_name'][:20]})" for sp in species_list[:5])
        if num_species > 5:
            species_summary += f", ... +{num_species - 5} more"
        print(f"CONTROL file written to: {control_path} ({num_species} species: {species_summary})")

    def write_setup_file(self, run_dir: str, facility: Dict[str, Any]):
        """
        Generate the HYSPLIT SETUP.cfg file to configure particle dumps.
        Scales the number of computational particles (numpar) proportionally
        to the facility's total emissions relative to the maximum emitter,
        enforcing a minimum count of 10 particles for dispersion visualization.
        
        maxpar is scaled up for multi-species runs to ensure enough particles
        are available for all chemical species.
        
        Args:
            run_dir: Directory where SETUP.cfg should be written.
            facility: Dictionary containing facility release parameters.
        """
        setup_path = os.path.join(run_dir, "SETUP.cfg")
        
        # Get total emissions for this facility
        tri_data = self.get_facility_releases(facility["name"])
        releases = tri_data.get("releases", [])
        total_lbs = sum(chem.get("total_lbs", 0.0) for chem in releases)
        
        # Count species with non-zero emissions (matches write_control_file logic)
        num_species = max(1, sum(1 for c in releases if c.get("total_lbs", 0.0) > 0))
        
        # Scale HYSPLIT particles based on PARTICLES_PER_UNIT_EMISSION configuration
        base_numpar = int(PARTICLES_PER_UNIT_EMISSION * 10)
        ratio = total_lbs / self.max_facility_lbs
        numpar_value = int(base_numpar * ratio)
        
        # Enforce floor of 10 particles so even the smallest source produces a visible plume path
        if numpar_value < 10:
            numpar_value = 10
            
        # Make numpar negative to force constant hourly emission rate in HYSPLIT point-source mode
        numpar_value = -numpar_value
        
        # Max particle age converted to hours for HYSPLIT config (khmax)
        khmax_hours = max(1, int(MAX_PARTICLE_AGE_MINUTES / 60))
        
        # Scale maxpar for multi-species: each species needs its own pool of particles
        maxpar_value = max(30000, num_species * 15000)
        
        content = (
            "&SETUP\n"
            "  initd = 0,\n"                            # No particle initialization file at start
            f"  khmax = {khmax_hours},\n"                # Max lifetime of particles (hours) derived from config
            "  ndump = 1,\n"                            # Dump particle positions every 1 hour
            "  ncycl = 1,\n"                            # Particle release cycle interval (hours)
            f"  numpar = {numpar_value},\n"              # Particles released per cycle mapped from config
            f"  maxpar = {maxpar_value},\n"              # Max total active particles (scaled for multi-species)
            "  poutf = 'PARDUMP',\n"                    # Particle dump output file name
            "/\n"
        )
        # HYSPLIT reads the namelist as SETUP.CFG (uppercase). macOS's case-INsensitive filesystem
        # matches our lowercase name, but case-SENSITIVE Linux/CI does not — so hycs_std silently
        # falls back to defaults (ndump=0 → NO PARDUMP → empty particle animation, the CI wind-grid
        # bug). Write BOTH casings so the dump config is honored on every platform.
        for _name in ("SETUP.cfg", "SETUP.CFG"):
            with open(os.path.join(run_dir, _name), "w") as f:
                f.write(content)
        print(f"SETUP.cfg written to: {setup_path} (numpar={numpar_value}, maxpar={maxpar_value}, species={num_species})")

    # ==========================================================================
    # DEPOSITION LAYER PIPELINE (Phase 2A/2B — Native HYSPLIT KML → GeoJSON)
    # ==========================================================================

    def write_deposition_control_file(self, run_dir: str, facility: Dict, chem_name: str,
                                      height: float, emission_g_hr: float, dry_only: bool = False) -> None:
        """Write HYSPLIT CONTROL file for one facility-chemical deposition run.
        Two output levels: 0 (soil deposition g/m²) and 10 (breathing-zone air g/m³).
        HOURLY sampling — averaging line is `type HH MM`: '00 01 00' = type 0 (average),
        1 hour, 0 min. (The earlier '01 00 00' was type 1 / 0-length interval → SIGFPE; that
        was the real cause of the supposed "macOS 12h limit", NOT deposition.)
        dry_only=True zeros wet-scavenging params (fallback if wet params trigger a crash).
        """
        p = CHEMICAL_DEPOSITION[chem_name]
        tag = DEP_CHEMICAL_TAGS[chem_name]
        yy = self.date_obj.strftime("%y")
        mm = self.date_obj.strftime("%m")
        dd = self.date_obj.strftime("%d")
        grid_spacing = DEP_GRID_SPACING
        grid_span = DEP_GRID_SPAN
        H = p["henry_M_atm"]
        in_cloud = 0.0 if dry_only else p["in_cloud_ratio"]
        below_cloud = 0.0 if dry_only else p["below_cloud_s"]
        lines = [
            f"{yy} {mm} {dd} 01",
            "1",
            f"{facility['lat']:.4f} {facility['lon']:.4f} {height:.1f}",
            "23", "0", "10000.0", "1",
            os.path.dirname(self.met_file_path) + "/",
            os.path.basename(self.met_file_path),
            "1", tag,
            f"{emission_g_hr:.4f}", "23.0",
            f"{yy} {mm} {dd} 01 00",
            "1",
            f"{MAP_CENTER[0]:.4f} {MAP_CENTER[1]:.4f}",   # fixed grid center (all chemicals aligned)
            f"{grid_spacing:.3f} {grid_spacing:.3f}",
            f"{grid_span:.3f} {grid_span:.3f}",
            run_dir + "/", "cdump",
            "2", "0", "10",
            "00 00 00 00 00",
            "00 00 00 00 00",
            "00 01 00",
            "1",
            "0.0 0.0 0.0",
            f"{p['dry_vd_ms']:.4f} {p['mol_weight']:.1f} 0.0 0.0 {H:.4f}",
            f"{H:.4f} {in_cloud:.2E} {below_cloud:.2E}",
            f"{p['halflife_days']:.2f}",
            "0.0",
        ]
        with open(os.path.join(run_dir, "CONTROL"), "w") as f:
            f.write("\n".join(lines) + "\n")

    def write_deposition_setup_file(self, run_dir: str) -> None:
        """Write minimal HYSPLIT SETUP.cfg for deposition runs (no PARDUMP needed)."""
        content = (
            "&SETUP\n"
            "  initd = 0,\n"
            "  khmax = 24,\n"
            "  ndump = 0,\n"
            "  ncycl = 1,\n"
            "  numpar = -500,\n"
            "  maxpar = 50000,\n"
            "/\n"
        )
        # Both casings so case-sensitive Linux hycs_std reads it too (see write_setup_file note).
        for _name in ("SETUP.cfg", "SETUP.CFG"):
            with open(os.path.join(run_dir, _name), "w") as f:
                f.write(content)

    def _hysplit_dep_run(self, run_dir: str) -> bool:
        """Execute hycs_std in run_dir; return True if cdump is non-empty."""
        try:
            subprocess.run(
                [self.hycs_std_path], cwd=run_dir,
                stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, timeout=300
            )
        except subprocess.TimeoutExpired:
            return False
        cdump = os.path.join(run_dir, "cdump")
        return os.path.exists(cdump) and os.path.getsize(cdump) > 0

    def run_concplot_kml(self, run_dir: str, layer: str) -> str | None:
        """Run concplot on cdump and return path to renamed KML, or None on failure.
        layer='dep' targets surface deposition (level 0, cumulative).
        layer='air' targets breathing-zone (level 10m, instantaneous).
        """
        if layer == "dep":
            extra = ["-b0", "-t0", "-r2"]   # cumulative soil deposition at level 0
        else:
            extra = ["-b10", "-t10", "-r0"] # per-hour breathing-zone air at level 10m
        cmd = [
            CONCPLOT_PATH,
            "-icdump", "-a3", "-f0", "-g0", "-d1", "-k1",
            "-c1",  # fixed-exponential contour levels: SAME bands across all 23 hourly frames
            "-w2",  # grid-point contour smoothing (rounds off the blocky cell edges)
            "-j" + HYSPLIT_ARLMAP_PATH,
        ] + extra
        try:
            subprocess.run(cmd, cwd=run_dir,
                           stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=300)
        except subprocess.TimeoutExpired:
            return None
        kml = os.path.join(run_dir, "HYSPLIT_ps.kml")
        if os.path.exists(kml) and os.path.getsize(kml) > 200:
            dst = os.path.join(run_dir, f"{layer}.kml")
            os.replace(kml, dst)
            return dst
        return None

    @staticmethod
    def extract_band_values(kml_path: str) -> Dict[int, float]:
        """Read the concplot KML legend → {band_number: contour_value}. concplot's
        '-c1' fixed levels are consistent across frames but DIFFER per chemical, so this must
        be read per file. Legend placemarks look like:
        <name>Contour Level: 1.0E-09 mass/m2</name> ... <styleUrl>#conc5</styleUrl>.
        """
        import re as _re
        out = {}
        try:
            tree = ET.parse(kml_path)
        except ET.ParseError:
            return out
        for pm in tree.getroot().iter("{http://www.opengis.net/kml/2.2}Placemark"):
            name = pm.findtext("{http://www.opengis.net/kml/2.2}name", default="") or ""
            mv = _re.search(r"Contour Level:\s*([0-9.eE+-]+)", name)
            if not mv:
                continue
            style = (pm.findtext("{http://www.opengis.net/kml/2.2}styleUrl", default="") or "").lstrip("#")
            if not style.startswith("conc"):
                continue
            try:
                out[int(style[4:])] = float(mv.group(1))
            except ValueError:
                pass
        return out

    @staticmethod
    def parse_kml_to_features(kml_path: str, layer: str, chem_name: str,
                               fac_name: str, fac_id: int) -> List[Dict]:
        """Parse a concplot KML into GeoJSON-style feature dicts.
        Properties: {layer, hour_frame, band, chem, fac_name, fac_id}.
        hour_frame 0 = first 12h snapshot, 1 = second 12h snapshot.
        """
        NS = {"kml": "http://www.opengis.net/kml/2.2"}
        try:
            tree = ET.parse(kml_path)
        except ET.ParseError:
            return []
        root = tree.getroot()
        doc = root.find("kml:Document", NS)
        if doc is None:
            return []

        features = []
        # concplot KML has 4 boilerplate folders first (Source Locations, Weather, Smoke/Fire,
        # AQI) with no contours; real time-frame folders follow. Count only contour-bearing
        # folders so frames are numbered 0,1,... matching the frontend renderer.
        frame_idx = -1
        for folder in doc.findall("kml:Folder", NS):
            folder_pms = []
            for pm in folder.findall("kml:Placemark", NS):
                style_url = pm.findtext("kml:styleUrl", default="", namespaces=NS).lstrip("#")
                if not style_url.startswith("conc"):
                    continue
                try:
                    band = int(style_url[4:])
                except ValueError:
                    continue
                if band > 0:
                    folder_pms.append((pm, band))
            if not folder_pms:
                continue
            frame_idx += 1

            for pm, band in folder_pms:
                for geom_tag in ("kml:MultiGeometry", "kml:Polygon"):
                    geom = pm.find(geom_tag, NS)
                    if geom is not None:
                        break

                polys = (geom.findall(".//kml:Polygon", NS) if geom is not None
                         else pm.findall(".//kml:Polygon", NS))

                for poly in polys:
                    outer = poly.find(
                        ".//kml:outerBoundaryIs/kml:LinearRing/kml:coordinates", NS)
                    if outer is None or not outer.text:
                        continue
                    coords = []
                    for token in outer.text.split():
                        parts = token.split(",")
                        if len(parts) >= 2:
                            try:
                                coords.append([round(float(parts[0]), 4), round(float(parts[1]), 4)])
                            except ValueError:
                                pass
                    if len(coords) < 3:
                        continue
                    if coords[0] != coords[-1]:
                        coords.append(coords[0])
                    coords = coords[::2] + [coords[-1]]   # keep every 2nd vertex (smoother rings)
                    if len(coords) < 4:
                        continue
                    features.append({
                        "type": "Feature",
                        "geometry": {"type": "Polygon", "coordinates": [coords]},
                        "properties": {
                            "layer": layer,
                            "hour_frame": frame_idx,
                            "band": band,
                            "chem": chem_name,
                            "fac_name": fac_name,
                            "fac_id": fac_id,
                        }
                    })
        return features

    def generate_deposition_outputs(self, run_dir: str, fac_name: str, fac_id: int,
                                    chem_name: str, chem_slug: str,
                                    out_dir: str, out_name: str = None) -> Dict | None:
        """Run concplot twice, parse both KMLs, write one GeoJSON file.
        Returns a manifest entry dict, or None if both layers are empty.
        out_name overrides the output filename (used for combined 2b outputs).
        """
        all_features = []
        layers_present = []
        band_values = {}

        for layer in ("dep", "air"):
            kml_path = self.run_concplot_kml(run_dir, layer)
            if kml_path is None:
                print(f"  concplot produced no KML for {layer} layer")
                continue
            feats = self.parse_kml_to_features(kml_path, layer, chem_name, fac_name, fac_id)
            if feats:
                all_features.extend(feats)
                layers_present.append(layer)
                band_values[layer] = self.extract_band_values(kml_path)
                print(f"  {layer}: {len(feats)} polygon features, bands {band_values[layer]}")
            else:
                print(f"  {layer}: KML empty or unparseable")

        if not all_features:
            return None

        # Hourly frames: frame_idx 0 = simulation hour 2 (first 1h output), k = hour (k+2).
        num_frames = max(f["properties"]["hour_frame"] for f in all_features) + 1
        start_hour = 2

        fac_slug = fac_name.lower().replace(" ", "_").replace(".", "").replace("&", "and")
        filename = out_name or f"{fac_slug}_{chem_slug}.json"
        geojson = {
            "type": "FeatureCollection",
            "features": all_features,
            "metadata": {
                "fac_name": fac_name, "fac_id": fac_id,
                "chem": chem_name, "chem_slug": chem_slug,
                "layers": layers_present,
                "depositor_class": CHEMICAL_DEPOSITION[chem_name]["depositor_class"],
                "num_frames": num_frames,
                "start_hour": start_hour,
                "band_values": band_values,   # {layer: {band: contour value g/m² or g/m³}}
            }
        }
        out_path = os.path.join(out_dir, filename)
        with open(out_path, "w") as f:
            json.dump(geojson, f, separators=(",", ":"))
        print(f"  GeoJSON written: {out_path} ({os.path.getsize(out_path)//1024}KB)")
        return {
            "file": filename,
            "fac_name": fac_name, "fac_id": fac_id,
            "chem": chem_name, "chem_slug": chem_slug,
            "layers": layers_present,
            "depositor_class": CHEMICAL_DEPOSITION[chem_name]["depositor_class"],
        }

    def build_combined_chemical_outputs(self, date_str: str = None) -> List[Dict]:
        """2b: per chemical, SUM the facility cdumps (concadd) → merged fields → concplot → combined footprints.
        We generate three combined footprints per chemical:
        1. combined_stack_{chem_slug}.json (only stack emissions merged)
        2. combined_fugitive_{chem_slug}.json (only fugitive emissions merged)
        3. combined_{chem_slug}.json (both stack + fugitive emissions merged)
        """
        if date_str is None:
            date_str = self.date_obj.strftime("%Y-%m-%d")
        concadd = CONCADD_PATH
        dep_base = os.path.join(self.workspace_dir, "dep_runs", date_str)
        out_dir = os.path.join(self.workspace_dir, "output", "geojson", date_str)
        manifest_path = os.path.join(out_dir, "manifest.json")
        manifest = json.load(open(manifest_path))

        # group per-facility entries by chemical
        by_chem = {}
        for e in manifest["entries"]:
            by_chem.setdefault(e["chem"], []).append(e)

        combined_entries = []
        for chem_name, entries in by_chem.items():
            chem_slug = entries[0]["chem_slug"]
            
            # Setup combination configs: (suffix, entries_to_combine, optional source_type)
            configs = [
                ("", entries, None),
                ("_stack", [e for e in entries if e.get("source_type") == "stack"], "stack"),
                ("_fugitive", [e for e in entries if e.get("source_type") == "fugitive"], "fugitive")
            ]

            for suffix, c_entries, s_type in configs:
                if not c_entries:
                    continue

                cdumps = []
                for e in c_entries:
                    fac_slug = e["fac_name"].lower().replace(" ", "_").replace(".", "").replace("&", "and")
                    src_type = e.get("source_type", "stack")
                    cd = os.path.join(dep_base, f"{fac_slug}_{chem_slug}_{src_type}", "cdump")
                    if os.path.exists(cd):
                        cdumps.append(cd)

                if not cdumps:
                    continue

                crun = os.path.join(dep_base, f"combined_{chem_slug}{suffix}")
                os.makedirs(crun, exist_ok=True)
                combined_cd = os.path.join(crun, "cdump")
                shutil.copy(cdumps[0], combined_cd)
                ok = True
                for extra in cdumps[1:]:
                    tmp = combined_cd + ".tmp"
                    r = subprocess.run([concadd, f"-i{extra}", f"-b{combined_cd}", f"-o{tmp}"],
                                       stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=120)
                    if os.path.exists(tmp) and os.path.getsize(tmp) > 0:
                        os.replace(tmp, combined_cd)
                    else:
                        print(f"  concadd failed for {chem_name} ({suffix}) (+{extra})")
                        ok = False
                        break
                if not ok:
                    continue

                facilities = [e["fac_name"] for e in c_entries]
                entry_name = f"combined_{chem_slug}{suffix}.json"
                entry = self.generate_deposition_outputs(
                    crun, f"Combined ({len(facilities)})", -1, chem_name, chem_slug, out_dir,
                    out_name=entry_name)
                if entry:
                    entry["combined"] = True
                    entry["facilities"] = list(set(facilities))
                    if s_type:
                        entry["source_type"] = s_type
                    combined_entries.append(entry)
                    print(f"  COMBINED {chem_name}{suffix}: {len(facilities)} facilities → {entry['file']}")

        manifest["combined_entries"] = combined_entries
        with open(manifest_path, "w") as f:
            json.dump(manifest, f, indent=2)
        print(f"Combined outputs: {len(combined_entries)} chemicals")
        return combined_entries

    def _execute_single_deposition_run(self, fac: Dict, fac_idx: int, chem_name: str,
                                       source_type: str, emission_g_hr: float, height: float,
                                       dep_base: str, out_dir: str) -> Dict | None:
        """Helper to run a single deposition simulation and output parsing (called in parallel)."""
        try:
            chem_slug = DEP_CHEMICAL_SLUGS[chem_name]
            fac_slug = fac["name"].lower().replace(" ", "_").replace(".", "").replace("&", "and")
            run_dir = os.path.join(dep_base, f"{fac_slug}_{chem_slug}_{source_type}")
            os.makedirs(run_dir, exist_ok=True)

            cdump_path = os.path.join(run_dir, "cdump")
            if os.path.exists(cdump_path) and os.path.getsize(cdump_path) > 0:
                print(f"Skipping HYSPLIT for {fac['name']} / {chem_name} ({source_type}) — cdump already exists.")
                ok = True
            else:
                print(f"Starting: {fac['name']} / {chem_name} ({source_type}: {emission_g_hr:.2f} g/hr at {height:.1f}m)...")
                self.write_deposition_control_file(run_dir, fac, chem_name, height, emission_g_hr)
                self.write_deposition_setup_file(run_dir)
                ok = self._hysplit_dep_run(run_dir)

                if not ok and CHEMICAL_DEPOSITION[chem_name]["in_cloud_ratio"] > 0:
                    print(f"  cdump empty for {fac['name']}/{chem_name} ({source_type}) — retrying with dry-dep-only params")
                    if os.path.exists(os.path.join(run_dir, "cdump")):
                        os.remove(os.path.join(run_dir, "cdump"))
                    self.write_deposition_control_file(
                        run_dir, fac, chem_name, height, emission_g_hr, dry_only=True)
                    ok = self._hysplit_dep_run(run_dir)

            if not ok:
                print(f"HYSPLIT Failed: {fac['name']} / {chem_name} ({source_type})")
                return None

            out_filename = f"{fac_slug}_{chem_slug}_{source_type}.json"
            entry = self.generate_deposition_outputs(
                run_dir, fac["name"], fac_idx, chem_name, chem_slug, out_dir, out_name=out_filename)
            if entry:
                entry["source_type"] = source_type
                print(f"Completed: {fac['name']} / {chem_name} ({source_type})")
                return entry
        except Exception as e:
            print(f"Error in {fac['name']} / {chem_name} ({source_type}): {e}")
        return None

    def run_deposition_pipeline(self) -> List[Dict]:
        """Main Phase 2A/2B entry point. Gather all facility×chemical×source tasks
        and execute them in parallel using concurrent.futures.
        """
        date_str = self.date_obj.strftime("%Y-%m-%d")
        dep_base = os.path.join(self.workspace_dir, "dep_runs", date_str)
        out_dir = os.path.join(self.workspace_dir, "output", "geojson", date_str)
        os.makedirs(dep_base, exist_ok=True)
        os.makedirs(out_dir, exist_ok=True)

        hysplit_bdyfiles = os.path.join(os.path.dirname(self.hysplit_exec_dir), "bdyfiles")
        dep_bdyfiles = os.path.join(dep_base, "bdyfiles")
        if not os.path.exists(dep_bdyfiles) and os.path.isdir(hysplit_bdyfiles):
            os.symlink(hysplit_bdyfiles, dep_bdyfiles)

        # Gather tasks
        tasks = []
        for fac_idx, fac in enumerate(self.facilities):
            fac_name = fac["name"]
            releases = self.get_facility_releases(fac_name).get("releases", [])
            release_by_chem = {r["chemical"].upper(): r for r in releases}

            for chem_name in CHEMICAL_DEPOSITION:
                release = release_by_chem.get(chem_name)
                if not release:
                    continue
                stack_g_hr = release.get("stack_g_hr", 0.0)
                fugitive_g_hr = release.get("fugitive_g_hr", 0.0)

                for source_type, emission_g_hr, height in [("stack", stack_g_hr, fac["height"]), ("fugitive", fugitive_g_hr, 2.0)]:
                    if emission_g_hr <= 0:
                        continue
                    tasks.append((fac, fac_idx, chem_name, source_type, emission_g_hr, height))

        print(f"\nScheduling {len(tasks)} deposition runs in parallel on 2 CPU workers...")

        import concurrent.futures
        manifest_entries = []

        def _meminfo_gb(key):
            try:
                with open("/proc/meminfo") as f:
                    for line in f:
                        if line.startswith(key + ":"):
                            return int(line.split()[1]) / 1024 / 1024
            except Exception:
                return None

        def _mem_avail_mb():
            g = _meminfo_gb("MemAvailable")
            return int(g * 1024) if g is not None else None

        # Auto-scale deposition parallelism to the machine's RAM so NO day (however heavy) can
        # over-subscribe memory and get OOM-killed (exit 143 — what 2025-03-08's wide SE-wind plume
        # did with 2 concurrent concplot renders on the 16 GB CI box). Each concurrent render of a
        # wide plume can use several GB, so budget ~one worker per ~12 GB total RAM: CI's 16 GB → 1
        # (safe on every day); a 32/64 GB dev box → 2/5 (fast). Override with PLUME_DEP_WORKERS.
        _total_gb = _meminfo_gb("MemTotal")
        _auto = max(1, int(_total_gb // 12)) if _total_gb else 1
        max_workers = max(1, int(os.environ.get("PLUME_DEP_WORKERS", str(_auto))))
        print(f"Deposition pipeline: {max_workers} parallel worker(s)"
              + (f" (auto from {_total_gb:.0f} GB RAM)" if _total_gb and 'PLUME_DEP_WORKERS' not in os.environ else ""))

        done = 0
        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = [
                executor.submit(
                    self._execute_single_deposition_run,
                    t[0], t[1], t[2], t[3], t[4], t[5], dep_base, out_dir
                )
                for t in tasks
            ]
            for future in concurrent.futures.as_completed(futures):
                entry = future.result()
                if entry:
                    manifest_entries.append(entry)
                done += 1
                if done % 15 == 0:
                    mf = _mem_avail_mb()
                    if mf is not None:
                        print(f"  [resource] {done}/{len(futures)} dep runs done; MemAvailable {mf} MB")

        manifest = {
            "date": date_str,
            "generated": datetime.datetime.utcnow().isoformat() + "Z",
            "note": "hourly frames: hour_frame k = sim hour (k+2); dep cumulative, air per-hour",
            "entries": manifest_entries,
        }
        with open(os.path.join(out_dir, "manifest.json"), "w") as f:
            json.dump(manifest, f, indent=2)
        print(f"\nManifest: {os.path.join(out_dir, 'manifest.json')} ({len(manifest_entries)} entries)")
        return manifest_entries

    def convert_and_parse_pardumps(self, run_dir: str, facility_idx: int) -> Dict[int, List[Dict[str, Any]]]:
        """
        Convert HYSPLIT binary PARDUMP files to GIS-compatible CSV files, then parse coordinates.
        The single PARDUMP binary contains all hourly particle snapshots. par2asc extracts them
        into a PAR_GIS.txt with a 'time' column that we use to group particles by hour.
        
        Args:
            run_dir: Path to directory containing output files.
            facility_idx: Numeric facility index for labeling particle source.
            
        Returns:
            Dict mapping hour index to lists of particle dictionaries.
        """
        print(f"Extracting particle positions from PARDUMP binaries in: {run_dir}...")
        if not os.path.exists(self.par2asc_path):
            raise FileNotFoundError(f"HYSPLIT par2asc executable not found at {self.par2asc_path}")
        
        # Find the PARDUMP file (single file containing all hourly snapshots)
        pardump_path = os.path.join(run_dir, "PARDUMP")
        if not os.path.exists(pardump_path):
            # Check for numbered variants
            candidates = sorted(glob.glob(os.path.join(run_dir, "PARDUMP.*")))
            if candidates:
                pardump_path = candidates[0]
            else:
                print(f"Warning: No PARDUMP files found in {run_dir}.")
                # DIAGNOSTIC: Linux/CI hycs_std reports success but leaves no findable PARDUMP.
                # Dump exactly what files it DID write (repr shows trailing-space/odd names) and what
                # HYSPLIT logged about the dump — distinguishes "wrong filename" from "never written".
                try:
                    entries = sorted(os.listdir(run_dir))
                    listing = [f"{n!r}({os.path.getsize(os.path.join(run_dir, n))}b)" for n in entries]
                    print(f"  [pardump-diag] run_dir has {len(entries)} files: {listing}")
                    msg = os.path.join(run_dir, "MESSAGE")
                    if os.path.exists(msg):
                        with open(msg, errors="replace") as mf:
                            hits = [l.rstrip() for l in mf if any(
                                k in l.upper() for k in ("NDUMP", "NCYCL", "POUTF", "PARDUMP", "DUMP", "ERROR"))]
                        print(f"  [pardump-diag] MESSAGE dump/err lines: {hits[:12]}")
                except Exception as _e:
                    print(f"  [pardump-diag] inspect failed: {_e}")
                return {}
        
        # Clear pre-existing outputs from past executions
        gis_output = os.path.join(run_dir, "PAR_GIS.txt")
        if os.path.exists(gis_output):
            os.remove(gis_output)
            
        cmd = [
            self.par2asc_path,
            f"-i{pardump_path}",
            "-oPAR_ASC.txt",
            "-a1"  # Generates 1-line-per-particle PAR_GIS.txt file
        ]
        
        try:
            result = subprocess.run(
                cmd,
                cwd=run_dir,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                timeout=60
            )
            
            if result.returncode != 0:
                print(f"Warning: par2asc failed: {result.returncode}")
                print(f"Stderr: {result.stderr}")
                return {}
                
            if os.path.exists(gis_output):
                # Reconstruct species_names list matching write_control_file logic
                facility = self.facilities[facility_idx]
                tri_data = self.get_facility_releases(facility["name"])
                releases = tri_data.get("releases", [])
                defaults = CHEMICAL_PROPERTIES.get("_DEFAULT", {"mol_wt": 80.0, "vd": 0.003, "reactivity": 0.0, "henry_const": 1.0})
                
                species_names = []
                other_total_emission = 0.0
                for chem in releases:
                    chem_name = chem.get("chemical", "").upper().strip()
                    total_lbs = chem.get("total_lbs", 0.0)
                    if total_lbs <= 0:
                        continue
                    emission_g_hr = chem.get("stack_g_hr", 0.0) + chem.get("fugitive_g_hr", 0.0)
                    if emission_g_hr <= 0:
                        continue
                    if chem_name in DEFAULT_ACTIVE_CHEMICALS:
                        species_names.append(chem_name)
                    else:
                        other_total_emission += emission_g_hr
                if other_total_emission > 0:
                    species_names.append("OTHER-AGGREGATE")
                if not species_names:
                    species_names.append("WEIGHTED-AVERAGE")
                
                hourly_particles = self.parse_gis_file_by_hour(gis_output, facility_idx, species_names)
                total = sum(len(v) for v in hourly_particles.values())
                print(f"Parsed {total} total particles across {len(hourly_particles)} hourly snapshots")
                return hourly_particles
            else:
                print(f"Warning: PAR_GIS.txt was not written by par2asc.")
                return {}
        except Exception as e:
            print(f"Error converting PARDUMP file: {e}")
            return {}

    def parse_gis_file_by_hour(self, gis_filepath: str, facility_idx: int, species_names: List[str]) -> Dict[int, List[Dict[str, Any]]]:
        """
        Parse GIS text file containing one-line particle data, grouping by dump hour.
        Filters out particles that drift beyond WEATHER_BOX_RADIUS_KM from MAP_CENTER.
        
        Args:
            gis_filepath: File path to converted PAR_GIS.txt file.
            facility_idx: Numeric facility index for classification.
            species_names: List of chemical names matching PTYP indices.
            
        Returns:
            Dict mapping hour index (1-23) to lists of particle dictionaries.
        """
        hourly_data = {}
        with open(gis_filepath, "r") as f:
            header_line = f.readline().strip()
            if not header_line:
                return {}
                
            # Parse header indices dynamically
            headers = [h.strip().lower() for h in header_line.split(",")]
            header_map = {name: idx for idx, name in enumerate(headers)}
            
            # The 'time' column is always index 0 in PAR_GIS.txt
            time_idx = header_map.get("time", 0)
            lat_idx = header_map.get("latitude") or header_map.get("lat")
            lon_idx = header_map.get("longitude") or header_map.get("lon")
            height_idx = header_map.get("height") or header_map.get("zlvl")
            age_idx = header_map.get("page") or header_map.get("age")
            nsort_idx = header_map.get("nsort") or header_map.get("id")
            ptyp_idx = header_map.get("ptyp")
            
            if lat_idx is None or lon_idx is None:
                print(f"Error parsing headers in {gis_filepath}. Required fields missing.")
                return {}
                
            for line in f:
                line = line.strip()
                if not line:
                    continue
                cols = [c.strip() for c in line.split(",")]
                if len(cols) < len(headers):
                    continue
                    
                try:
                    # Extract hour from time column. par2asc's whitespace/zero-padding differs by
                    # Fortran compiler: macOS emits "M/ D/YY  H: M" (space before minutes) while the
                    # Linux/CI build emits compact "M/DD/YY HH:MM". Take the hour as the token BEFORE
                    # the first colon so both parse correctly. (The old `replace(":","")` turned
                    # "14:00" into 1400 → rejected by the 0..24 filter → empty wind grid on CI.)
                    time_str = cols[time_idx].strip()
                    time_parts = time_str.split()
                    hour = 1  # default
                    for part in time_parts:
                        if ":" in part:
                            hour = int(part.split(":")[0].strip())
                            break
                    if not getattr(self, "_time_fmt_logged", False):
                        # One-line confirmation of par2asc's actual time format + parsed hour, so a
                        # future empty-wind-grid regression is immediately visible in the log.
                        print(f"  [particle parse] time sample {time_str!r} -> hour {hour}")
                        self._time_fmt_logged = True
                    
                    lat = float(cols[lat_idx])
                    lon = float(cols[lon_idx])
                    
                    # Apply physics limits: Filter out particles exceeding WEATHER_BOX_RADIUS_KM from MAP_CENTER
                    if not self._is_within_radius(lat, lon):
                        continue
                        
                    height = float(cols[height_idx]) if height_idx is not None else 0.0
                    age = int(float(cols[age_idx])) if age_idx is not None else 0
                    nsort = int(cols[nsort_idx]) if nsort_idx is not None else 0
                    ptyp = int(cols[ptyp_idx]) if ptyp_idx is not None else 1
                    
                    chem_name = "UNKNOWN"
                    if 0 < ptyp <= len(species_names):
                        chem_name = species_names[ptyp - 1]
                    
                    particle = {
                        "id": nsort,
                        "lat": round(lat, 5),
                        "lon": round(lon, 5),
                        "height": round(height, 1),
                        "age": age,
                        "facility": facility_idx,
                        "chem": chem_name
                    }
                    
                    if hour not in hourly_data:
                        hourly_data[hour] = []
                    hourly_data[hour].append(particle)
                    
                except Exception:
                    continue
                    
        return hourly_data

    def _is_within_radius(self, lat: float, lon: float) -> bool:
        """
        Calculate if coordinate falls within WEATHER_BOX_RADIUS_KM from MAP_CENTER using Haversine formulas.
        """
        lat1, lon1 = MAP_CENTER
        lat2, lon2 = lat, lon
        
        # Radius of Earth in kilometers
        R = 6371.0
        
        dlat = math.radians(lat2 - lat1)
        dlon = math.radians(lon2 - lon1)
        
        a = math.sin(dlat / 2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2)**2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        distance = R * c
        
        return distance <= float(WEATHER_BOX_RADIUS_KM)

    def calculate_facility_deposition(self, parsed_particles: Dict[int, List[Dict[str, Any]]], facility: Dict[str, Any], facility_idx: int) -> Dict[int, List[Dict[str, float]]]:
        """
        Calculate hourly surface deposition grid from particle coordinates for a single facility.
        Replaces the HYSPLIT-native concentration/deposition grid to avoid the Mac SIGFPE crash.
        Calculates cumulative deposition (particles accumulate and stay on the ground).
        """
        grid_span = float(WEATHER_BOX_RADIUS_KM) / 111.0
        lat_min = MAP_CENTER[0] - grid_span
        lat_max = MAP_CENTER[0] + grid_span
        lon_min = MAP_CENTER[1] - grid_span
        lon_max = MAP_CENTER[1] + grid_span
        
        # Calculate emission-weighted Vd * emission_rate for all chemicals
        tri_data = self.get_facility_releases(facility["name"])
        releases = tri_data.get("releases", [])
        defaults = CHEMICAL_PROPERTIES.get("_DEFAULT", {"mol_wt": 80.0, "vd": 0.003, "reactivity": 0.0, "henry_const": 1.0})
        
        total_dep_flux = 0.0
        for chem in releases:
            chem_name = chem.get("chemical", "").upper().strip()
            total_lbs = chem.get("total_lbs", 0.0)
            if total_lbs <= 0:
                continue
            emission_g_hr = chem.get("stack_g_hr", 0.0) + chem.get("fugitive_g_hr", 0.0)
            if emission_g_hr <= 0:
                continue
            
            props = CHEMICAL_PROPERTIES.get(chem_name, defaults)
            total_dep_flux += emission_g_hr * props["vd"]
        
        if total_dep_flux <= 0:
            dep_params = self._compute_facility_deposition_params(facility["name"])
            total_dep_flux = 1000.0 * dep_params["vd"]
            
        facility_deposition = {}
        cumulative_grid = {}  # maps (lat_bin, lon_bin) -> accumulated mass
        
        for hour_idx in sorted(parsed_particles.keys()):
            particles = parsed_particles[hour_idx]
            for p in particles:
                # Accumulate deposition for low-level particles (height <= 100m)
                if p["height"] <= 100.0:
                    lat = p["lat"]
                    lon = p["lon"]
                    
                    # Bin to 0.002 degree grid cells (approx 220m spacing) matching sandbox
                    grid_spacing = 0.002
                    lat_bin = round(round(lat / grid_spacing) * grid_spacing, 4)
                    lon_bin = round(round(lon / grid_spacing) * grid_spacing, 4)
                    
                    if lat_min <= lat_bin <= lat_max and lon_min <= lon_bin <= lon_max:
                        # Linear vertical weighting: max contribution at surface (0m), 10% at 100m
                        weight = 1.0 - 0.9 * (p["height"] / 100.0)
                        key = (lat_bin, lon_bin)
                        cumulative_grid[key] = cumulative_grid.get(key, 0.0) + total_dep_flux * weight
            
            cells_list = []
            for (lat_bin, lon_bin), val in cumulative_grid.items():
                scaled_val = val * 1.5e-6  # slightly reduced scale for cumulative 0.002 binning
                # Filter out extremely small values to prevent JSON bloat
                if scaled_val > 0.0001:
                    cells_list.append({
                        "lat": lat_bin,
                        "lon": lon_bin,
                        "val": round(scaled_val, 6)
                    })
            facility_deposition[hour_idx] = cells_list
            
        total_cells = sum(len(v) for v in facility_deposition.values())
        print(f"  Calculated cumulative deposition grid offline: {total_cells} non-zero cells across {len(facility_deposition)} hours.")
        return facility_deposition

    def run_dispersion_model(self):
        """
        Run HYSPLIT simulation loops independently for each facility.
        
        Returns:
            Tuple of (all_facility_particles, all_deposition_data):
            - all_facility_particles: Dict nested by facility name, then hour index, containing lists of particles.
            - all_deposition_data: Dict mapping hour_index -> list of {lat, lon, val} deposition cells
              aggregated across all facilities.
        """
        print("Executing dispersion model simulations...")
        if not os.path.exists(self.hycs_std_path):
            raise FileNotFoundError(f"HYSPLIT hycs_std executable not found at {self.hycs_std_path}")
        
        # HYSPLIT expects boundary files (ASCDATA.CFG, LANDUSE.ASC, etc.) at ../bdyfiles/
        # relative to each run directory. Create a symlink in the workspace to the HYSPLIT bdyfiles.
        hysplit_bdyfiles = os.path.join(os.path.dirname(self.hysplit_exec_dir), "bdyfiles")
        workspace_bdyfiles = os.path.join(self.workspace_dir, "bdyfiles")
        if os.path.isdir(hysplit_bdyfiles):
            if os.path.exists(workspace_bdyfiles) or os.path.islink(workspace_bdyfiles):
                try:
                    if os.path.islink(workspace_bdyfiles):
                        os.unlink(workspace_bdyfiles)
                    elif os.path.isdir(workspace_bdyfiles):
                        pass
                    else:
                        os.remove(workspace_bdyfiles)
                except Exception as e:
                    print(f"Warning: Could not remove existing link {workspace_bdyfiles}: {e}")
            
            if not os.path.exists(workspace_bdyfiles) and not os.path.islink(workspace_bdyfiles):
                os.symlink(hysplit_bdyfiles, workspace_bdyfiles)
                print(f"Linked boundary files: {workspace_bdyfiles} -> {hysplit_bdyfiles}")
            
        all_facility_particles = {}
        all_deposition_data = {}  # Aggregated deposition across all facilities
        
        for idx, facility in enumerate(self.facilities):
            name = facility["name"]
            print(f"\n========================================\nSource Group: {name}")
            
            # Setup dedicated run directory to prevent file locking issues
            run_dir_name = f"run_{name.lower().replace(' ', '_')}"
            run_dir = os.path.join(self.workspace_dir, run_dir_name)
            os.makedirs(run_dir, exist_ok=True)
            
            self.write_control_file(run_dir, facility)
            self.write_setup_file(run_dir, facility)
            
            print(f"Launching HYSPLIT hycs_std in workspace: {run_dir}...")
            try:
                result = subprocess.run(
                    [self.hycs_std_path],
                    cwd=run_dir,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                    timeout=300
                )
                
                if result.returncode != 0:
                    print(f"Error: HYSPLIT execution failed for {name} (exit code: {result.returncode})")
                    print(f"Stderr: {result.stderr}")
                    continue
                    
                print(f"HYSPLIT run successful. Log output written to HYSPLIT MESSAGE files.")
                
                # Convert and read the binary particle dumps
                parsed_particles = self.convert_and_parse_pardumps(run_dir, idx)
                all_facility_particles[name] = parsed_particles
                
                # Calculate deposition grid from particle coordinates offline
                facility_deposition = self.calculate_facility_deposition(parsed_particles, facility, idx)
                for hour_idx, cells in facility_deposition.items():
                    if hour_idx not in all_deposition_data:
                        all_deposition_data[hour_idx] = []
                    all_deposition_data[hour_idx].extend(cells)
                
            except subprocess.TimeoutExpired:
                print(f"Timeout occurred executing HYSPLIT for {name}.")
            except Exception as e:
                print(f"Unexpected execution failure for {name}: {e}")
        
        # Log deposition summary
        total_dep_cells = sum(len(v) for v in all_deposition_data.values())
        print(f"\nTotal aggregated deposition: {total_dep_cells} cells across {len(all_deposition_data)} hours from all facilities.")
                
        return all_facility_particles, all_deposition_data

    def process_ambient_monitors(self) -> Dict[str, Any]:
        """
        Process the EPA monitoring CSV files in chunks.
        Extract units of measure dynamically and filter for target state and counties on target date.
        """
        import pandas as pd
        import numpy as np

        regional_monitor_data = {}

        # Build CSV paths for the ACTIVE date's year (hourly_<code>_<year>.csv). Fall back to a 2025
        # file if the year-specific one is absent (so existing dev data still resolves).
        _year = self.date_obj.year
        for pollutant, info in EPA_MONITOR_CONFIG.items():
            csv_path = os.path.join(BASE_DATA_DIR, f"hourly_{info['code']}_{_year}.csv")
            if not os.path.exists(csv_path):
                _fallback = os.path.join(BASE_DATA_DIR, f"hourly_{info['code']}_2025.csv")
                if os.path.exists(_fallback):
                    csv_path = _fallback
            if not os.path.exists(csv_path):
                print(f"Warning: CSV file for {pollutant} not found at {csv_path}. Skipping.")
                regional_monitor_data[pollutant] = {
                    "unit": "N/A",
                    "good": info["good"],
                    "mod": info["mod"],
                    "unhealthy": info["unhealthy"],
                    "stations": {}
                }
                continue

            unit = None
            stations_data = {}  # station_id -> {county, lat, lon, parameter_name, hourly_values: [[] for _ in range(24)]}

            print(f"Processing EPA monitor data for {pollutant} from {os.path.basename(csv_path)}...")
            try:
                # Optimized line-by-line reading with pre-filtering
                with open(csv_path, "r", encoding="utf-8") as f:
                    header_line = f.readline()
                    if not header_line:
                        continue
                    
                    # Parse header to find column indices
                    reader = csv.reader([header_line])
                    headers = next(reader)
                    
                    try:
                        idx_state_name = headers.index('State Name')
                        idx_county_name = headers.index('County Name')
                        idx_date_local = headers.index('Date Local')
                        idx_units = headers.index('Units of Measure')
                        idx_state_code = headers.index('State Code')
                        idx_county_code = headers.index('County Code')
                        idx_site_num = headers.index('Site Num')
                        idx_lat = headers.index('Latitude')
                        idx_lon = headers.index('Longitude')
                        idx_param_name = headers.index('Parameter Name')
                        idx_time_local = headers.index('Time Local')
                        idx_sample_meas = headers.index('Sample Measurement')
                    except ValueError as ve:
                        print(f"Warning: Missing required columns in {csv_path}: {ve}. Skipping.")
                        continue
                    
                    target_counties_set = set(TARGET_COUNTIES)
                    
                    # Fast search loop to identify matching lines as raw strings
                    matching_lines = []
                    for line in f:
                        if TARGET_STATE in line and self.date_str in line:
                            matching_lines.append(line)
                            
                if matching_lines:
                    reader = csv.reader(matching_lines)
                    for row in reader:
                        if len(row) <= max(idx_state_name, idx_county_name, idx_date_local):
                            continue
                        if row[idx_state_name] != TARGET_STATE:
                            continue
                        if row[idx_county_name] not in target_counties_set:
                            continue
                        if row[idx_date_local] != self.date_str:
                            continue
                            
                        # Extract units dynamically from first matched row
                        if unit is None:
                            unit_val = row[idx_units].strip()
                            if unit_val:
                                unit = unit_val
                                
                        state_code = row[idx_state_code].strip().zfill(2)
                        county_code = row[idx_county_code].strip().zfill(3)
                        site_num = row[idx_site_num].strip().zfill(4)
                        station_id = f"{state_code}-{county_code}-{site_num}"
                        
                        lat = float(row[idx_lat])
                        lon = float(row[idx_lon])
                        county = row[idx_county_name].strip()
                        param_name = row[idx_param_name].strip()
                        
                        time_str = row[idx_time_local].strip()
                        try:
                            hour = int(time_str.split(':')[0])
                        except Exception:
                            continue
                            
                        if not (0 <= hour <= 23):
                            continue
                            
                        val_str = row[idx_sample_meas]
                        if not val_str or val_str.strip() == "":
                            val = None
                        else:
                            try:
                                val = float(val_str)
                            except ValueError:
                                val = None
                                
                        if station_id not in stations_data:
                            stations_data[station_id] = {
                                "county": county,
                                "lat": lat,
                                "lon": lon,
                                "parameter_name": param_name,
                                "hourly_values": [[] for _ in range(24)]
                            }
                            
                        if val is not None:
                            stations_data[station_id]["hourly_values"][hour].append(val)

                # After chunking, finalize station values (average multiple measurements for the same hour)
                formatted_stations = {}
                for sid, sinfo in stations_data.items():
                    hourly_data = [None] * 24
                    for h in range(24):
                        vals = sinfo["hourly_values"][h]
                        if vals:
                            hourly_data[h] = float(np.mean(vals))

                    formatted_stations[sid] = {
                        "county": sinfo["county"],
                        "lat": sinfo["lat"],
                        "lon": sinfo["lon"],
                        "parameter_name": sinfo["parameter_name"],
                        "hourly_data": hourly_data
                    }

                # Store compiled data
                regional_monitor_data[pollutant] = {
                    "unit": unit if unit is not None else "N/A",
                    "good": info["good"],
                    "mod": info["mod"],
                    "unhealthy": info["unhealthy"],
                    "stations": formatted_stations
                }

                # Print summary
                num_stations = len(formatted_stations)
                print(f"  Pollutant {pollutant}: unit='{unit}', found {num_stations} stations in target counties.")

            except Exception as e:
                print(f"Error processing CSV for {pollutant}: {e}")
                regional_monitor_data[pollutant] = {
                    "unit": "N/A",
                    "good": info["good"],
                    "mod": info["mod"],
                    "unhealthy": info["unhealthy"],
                    "stations": {}
                }

        # --- PARSE LOCAL CALVERT CITY DAILY VOC EXCEL DATA ---
        excel_path = os.path.join(self.original_workspace_dir, "CalvertDailyVOCS_DateEnding6.30.2025.xlsx")
        if os.path.exists(excel_path):
            print(f"Processing local Calvert City VOC data from {os.path.basename(excel_path)}...")
            try:
                # Read the excel file
                df_voc = pd.read_excel(excel_path)
                df_voc['Date Local'] = pd.to_datetime(df_voc['Date Local'])
                
                # Find all unique dates in the Excel file
                available_dates = df_voc['Date Local'].dropna().unique()
                
                if len(available_dates) > 0:
                    target_date = pd.to_datetime(self.date_str)
                    
                    # Find the next available sample date on or after the target date,
                    # since canisters accumulate air in the days leading up to the sample date.
                    future_dates = [d for d in available_dates if pd.to_datetime(d) >= target_date]
                    if future_dates:
                        closest_date = min(future_dates)
                    else:
                        closest_date = max(available_dates) # Fallback to the latest available past date
                        
                    closest_date_str = pd.to_datetime(closest_date).strftime('%Y-%m-%d')
                    days_diff = int(abs((pd.to_datetime(closest_date) - target_date).days))
                    
                    # Filter dataset for the closest date
                    df_date = df_voc[df_voc['Date Local'] == closest_date]
                    
                    if not df_date.empty:
                        # Make sure the "VOCs" parameter group exists and has proper units
                        if "VOCs" in regional_monitor_data:
                            if regional_monitor_data["VOCs"].get("unit") in (None, "N/A", "None", "None"):
                                regional_monitor_data["VOCs"]["unit"] = "ppbC"
                        else:
                            regional_monitor_data["VOCs"] = {
                                "unit": "ppbC",
                                "good": 50.0,
                                "mod": 150.0,
                                "unhealthy": 300.0,
                                "stations": {}
                            }
                        
                        # Group by station to sum all compounds and extract detailed lists
                        for (site_num, site_name), station_df in df_date.groupby(['Site Num', 'Local Site Name']):
                            lat = float(station_df.iloc[0].get('Latitude', 0.0))
                            lon = float(station_df.iloc[0].get('Longitude', 0.0))
                            county = station_df.iloc[0].get('County Name', 'Marshall')
                            
                            # Sum all non-null daily average values to calculate Total VOCs
                            mean_vals = station_df['Arithmetic Mean'].dropna()
                            total_sum = float(mean_vals.sum()) if not mean_vals.empty else None
                            
                            # Replicate daily measurement across all 24 hours
                            hourly_data = [total_sum] * 24 if total_sum is not None else [None] * 24
                            
                            # Gather sorted dictionary of individual chemical measurements
                            voc_details = {}
                            for _, row in station_df.iterrows():
                                p_name = row.get('Parameter Name')
                                m_val = row.get('Arithmetic Mean')
                                if not pd.isna(m_val) and p_name:
                                    voc_details[p_name] = float(m_val)
                            
                            # Sort chemical details descending by concentration
                            sorted_vocs = sorted(voc_details.items(), key=lambda x: x[1] if x[1] is not None else 0.0, reverse=True)
                            voc_details_dict = {k: v for k, v in sorted_vocs}
                            
                            station_id = f"CC_{int(site_num)} - {site_name}"
                            regional_monitor_data["VOCs"]["stations"][station_id] = {
                                "county": county,
                                "lat": lat,
                                "lon": lon,
                                "parameter_name": "Total VOCs",
                                "hourly_data": hourly_data,
                                "voc_details": voc_details_dict,
                                "sample_date": closest_date_str,
                                "is_interpolated": days_diff > 0,
                                "days_diff": days_diff
                            }
                        
                        print(f"  Successfully loaded {df_date['Parameter Name'].nunique()} local VOC compounds from sample date {closest_date_str} for target date {self.date_str} (diff: {days_diff}d).")
                    else:
                        print(f"  No local VOC data found in Excel for closest date {closest_date_str}.")
                else:
                    print("  No dates found in Excel.")
            except Exception as e:
                print(f"Error parsing Calvert VOC Excel file: {e}")

        return regional_monitor_data

    def build_embedded_facilities(self) -> List[Dict[str, Any]]:
        """Build the facility objects embedded in the page.

        Only chemicals in DEFAULT_ACTIVE_CHEMICALS (the HYSPLIT-modeled set) are embedded — the
        other TRI compounds are modeled only by the old particle method and are dropped so they
        can't be toggled on and flood the UI. A facility that emits none of the modeled chemicals
        is omitted entirely (removed from the map + point-source list). Kept facilities are
        re-indexed to a dense 0..M-1 range and `self.orig_to_new_fac_id` records
        {original_fac_id: new_id} so build_deposition_archive() can remap the deposition manifest's
        fac_id to match.

        NOTHING is deleted from the source config/TRI data — the full FACILITIES dict and TRI CSV
        stay intact. To re-enable a chemical or facility later, add its chemical name to
        DEFAULT_ACTIVE_CHEMICALS (and rerun); this filter picks it up automatically.

        Used by BOTH the full-pipeline compile path and the --regen-html fast path so the embedded
        facilities (and therefore the fac_id mapping) are always identical.
        """
        default_set = {c.strip().upper() for c in DEFAULT_ACTIVE_CHEMICALS}
        compiled = []
        orig_to_new = {}
        for fac in self.facilities:
            tri_data = self.get_facility_releases(fac["name"])
            releases = tri_data.get("releases", [])
            modeled = [c for c in releases if c.get("chemical", "").strip().upper() in default_set]
            if not modeled:
                continue  # no modeled chemicals → drop this facility from the map + list
            new_id = len(compiled)
            orig_to_new[fac["id"]] = new_id
            compiled.append({
                "id": new_id,
                "name": fac["name"],
                "lat": fac["lat"],
                "lon": fac["lon"],
                "height": fac["height"],
                "color": fac["color"],
                "tri_id": fac["tri_id"],
                "tri_name": tri_data.get("fac_name", fac["name"]),
                "chemicals": modeled,
                # total_lbs stays the facility's FULL TRI total (all chemicals), not just the
                # modeled subset: it's the facility's real emission figure AND the frontend's
                # particle-density scaling reference (maxFacLbs). Using the modeled-only sum here
                # would shrink maxFacLbs and inflate spawn counts, changing the particle density.
                "total_lbs": sum(c.get("total_lbs", 0.0) for c in releases),
                "schedule": fac.get("schedule", "continuous"),
            })
        self.orig_to_new_fac_id = orig_to_new
        dropped = len(self.facilities) - len(compiled)
        print(f"Embedded facilities: {len(compiled)} kept, {dropped} dropped (no modeled chemicals).")
        return compiled

    def compile_data_for_json(self, raw_particles: Dict[str, Dict[int, List[Dict[str, Any]]]], deposition_data: Dict[int, List[Dict[str, float]]] = None) -> Dict[str, Any]:
        """
        Compile facilities list and hourly simulation timelines into a JavaScript-friendly structure.
        
        Args:
            raw_particles: Output coordinates from dispersion runs.
            deposition_data: Aggregated hourly deposition grid data from run_dispersion_model().
                Dict mapping hour_index -> list of {lat, lon, val} records.
            
        Returns:
            Dict containing formatted facility objects, simulation timelines, and deposition grids.
        """
        if deposition_data is None:
            deposition_data = {}
        print("\nCompiling trajectory coordinates and EPA data for web layout...")
        self.regional_monitor_data = self.process_ambient_monitors()

        
        # Compile facility variables (modeled-chemicals-only, dropped-empties, re-indexed).
        compiled_facilities = self.build_embedded_facilities()

        # Build internal timeline (used only for wind vector extraction, not serialized)
        timeline = [[] for _ in range(25)]
        
        for fac in self.facilities:
            fac_name = fac["name"]
            fac_data = raw_particles.get(fac_name, {})
            
            for hour_idx, particles in fac_data.items():
                if 0 <= hour_idx <= 24:
                    timeline[hour_idx].extend(particles)
                    
        # Extract per-hour wind grids from particle displacements
        # Each grid is a 2D array of size GRID_SIZE x GRID_SIZE.
        # Each cell stores median displacement (dLat/dLon) AND IQR-based spread (sLat/sLon)
        # so the JS sandbox can fan particles out to match real HYSPLIT dispersion width.
        GRID_SIZE = 20
        grid_span = float(WEATHER_BOX_RADIUS_KM) / 111.0
        lat_min = MAP_CENTER[0] - grid_span
        lat_max = MAP_CENTER[0] + grid_span
        lon_min = MAP_CENTER[1] - grid_span
        lon_max = MAP_CENTER[1] + grid_span

        lat_span = lat_max - lat_min
        lon_span = lon_max - lon_min

        def _iqr_half(vals_sorted):
            """Half the interquartile range as a spread estimate."""
            n = len(vals_sorted)
            if n < 4:
                return 0.0
            return (vals_sorted[3 * n // 4] - vals_sorted[n // 4]) / 2.0

        def build_wind_grid_for_filter(height_filter_fn, label: str) -> list:
            grid_list = []
            for hour_idx in range(24):
                curr = [p for p in timeline[hour_idx] if height_filter_fn(p["height"])]
                nxt = timeline[hour_idx + 1] if hour_idx + 1 <= 24 else []
                # To keep trajectory references consistent, match target particles in the next hour
                nxt_filtered = [p for p in nxt if height_filter_fn(p["height"])]

                # Compute global median displacement and IQR spread for this hour as a fallback
                global_dlat = 0.0
                global_dlon = 0.0
                global_slat = 0.0
                global_slon = 0.0
                next_map = {}
                if curr and nxt_filtered:
                    next_map = {(p["facility"], p["id"]): p for p in nxt_filtered}
                    all_dlats = []
                    all_dlons = []
                    for p in curr:
                        key = (p["facility"], p["id"])
                        if key in next_map:
                            pn = next_map[key]
                            dl = pn["lat"] - p["lat"]
                            do_ = pn["lon"] - p["lon"]
                            if abs(dl) < 0.5 and abs(do_) < 0.5:
                                all_dlats.append(dl)
                                all_dlons.append(do_)
                    if all_dlats:
                        all_dlats.sort()
                        all_dlons.sort()
                        n = len(all_dlats)
                        global_dlat = all_dlats[n // 2]
                        global_dlon = all_dlons[n // 2]
                        global_slat = _iqr_half(all_dlats)
                        global_slon = _iqr_half(all_dlons)

                # Initialize empty grid with global median + spread fallback
                hour_grid = [[{
                    "dLat": round(global_dlat, 6), "dLon": round(global_dlon, 6),
                    "sLat": round(global_slat, 6), "sLon": round(global_slon, 6)
                } for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]

                # Group displacements by cell
                cell_displacements = {} # (r, c) -> {"dlats": [], "dlons": []}
                if curr and nxt_filtered:
                    for p in curr:
                        key = (p["facility"], p["id"])
                        if key in next_map:
                            pn = next_map[key]
                            dl = pn["lat"] - p["lat"]
                            do_ = pn["lon"] - p["lon"]
                            if abs(dl) < 0.5 and abs(do_) < 0.5:
                                # Map coordinate to cell index
                                r = int(((p["lat"] - lat_min) / lat_span) * GRID_SIZE)
                                c = int(((p["lon"] - lon_min) / lon_span) * GRID_SIZE)
                                # Clamp indices to grid boundaries
                                r = max(0, min(GRID_SIZE - 1, r))
                                c = max(0, min(GRID_SIZE - 1, c))

                                cell_key = (r, c)
                                if cell_key not in cell_displacements:
                                    cell_displacements[cell_key] = {"dlats": [], "dlons": []}
                                cell_displacements[cell_key]["dlats"].append(dl)
                                cell_displacements[cell_key]["dlons"].append(do_)

                # Compute median + IQR spread for each populated cell
                for (r, c), data in cell_displacements.items():
                    dlats = sorted(data["dlats"])
                    dlons = sorted(data["dlons"])
                    n = len(dlats)
                    local_dlat = dlats[n // 2]
                    local_dlon = dlons[n // 2]
                    local_slat = _iqr_half(dlats) if n >= 4 else global_slat
                    local_slon = _iqr_half(dlons) if n >= 4 else global_slon
                    hour_grid[r][c] = {
                        "dLat": round(local_dlat, 6), "dLon": round(local_dlon, 6),
                        "sLat": round(local_slat, 6), "sLon": round(local_slon, 6),
                    }

                # Run IDW interpolation for unpopulated cells (median + spread)
                smoothed_grid = [[{
                    "dLat": hour_grid[r][c]["dLat"], "dLon": hour_grid[r][c]["dLon"],
                    "sLat": hour_grid[r][c]["sLat"], "sLon": hour_grid[r][c]["sLon"],
                } for c in range(GRID_SIZE)] for r in range(GRID_SIZE)]
                for r in range(GRID_SIZE):
                    for c in range(GRID_SIZE):
                        if (r, c) not in cell_displacements:
                            # Find distance-weighted average from cells with particles
                            weights_sum = 0.0
                            dlat_sum = 0.0
                            dlon_sum = 0.0
                            slat_sum = 0.0
                            slon_sum = 0.0
                            for (pr, pc), pdata in cell_displacements.items():
                                dist = math.sqrt((r - pr)**2 + (c - pc)**2)
                                if dist == 0:
                                    continue
                                w = 1.0 / (dist**2)
                                weights_sum += w
                                p_dlats = sorted(pdata["dlats"])
                                p_dlons = sorted(pdata["dlons"])
                                pn = len(p_dlats)
                                dlat_sum += p_dlats[pn // 2] * w
                                dlon_sum += p_dlons[pn // 2] * w
                                slat_sum += (_iqr_half(p_dlats) if pn >= 4 else global_slat) * w
                                slon_sum += (_iqr_half(p_dlons) if pn >= 4 else global_slon) * w

                            if weights_sum > 0:
                                smoothed_grid[r][c] = {
                                    "dLat": round(dlat_sum / weights_sum, 6),
                                    "dLon": round(dlon_sum / weights_sum, 6),
                                    "sLat": round(slat_sum / weights_sum, 6),
                                    "sLon": round(slon_sum / weights_sum, 6),
                                }

                num_cells_filled = len(cell_displacements)
                print(f"  [{label}] Hour {hour_idx:2d}→{hour_idx+1:2d}: global dLat={global_dlat:+.5f}° dLon={global_dlon:+.5f}°, {num_cells_filled}/{GRID_SIZE*GRID_SIZE} cells populated.")
                grid_list.append(smoothed_grid)
            return grid_list

        print("Compiling elevated stack wind grid...")
        wind_grid_stack = build_wind_grid_for_filter(lambda h: h >= 15.0, "Stack")
        
        print("Compiling surface fugitive wind grid...")
        wind_grid_fugitive = build_wind_grid_for_filter(lambda h: h < 15.0, "Fugitive")

        # Defense-in-depth: this grid was silently empty on CI once (par2asc time-format parse bug).
        # Fail LOUD if it ever happens again instead of shipping a dead particle animation.
        _nz = sum(1 for wg in (wind_grid_stack, wind_grid_fugitive)
                  for h in wg for row in h for c in row
                  if abs(c["dLat"]) > 1e-9 or abs(c["dLon"]) > 1e-9)
        if _nz == 0:
            print("  ⚠️  WARNING: wind grid is EMPTY (0 populated cells) — particle animation will be "
                  "dead. Likely no PARDUMP particles parsed (check the [particle parse] line + par2asc).")
        else:
            print(f"  Wind grid OK: {_nz} nonzero cells across stack+fugitive.")

        grid_info = {
            "grid_size": GRID_SIZE,
            "lat_min": round(lat_min, 6),
            "lat_max": round(lat_max, 6),
            "lon_min": round(lon_min, 6),
            "lon_max": round(lon_max, 6)
        }
        
        # Compile deposition grid for heatmap visualization
        # Structure: {"hours": [{"cells": [{lat, lon, val}, ...]}, ...], "max_val": float}
        dep_hours = []
        global_max_dep = 0.0
        for hour_idx in range(24):
            cells = deposition_data.get(hour_idx, [])
            if cells:
                hour_max = max(c["val"] for c in cells)
                global_max_dep = max(global_max_dep, hour_max)
            dep_hours.append({"cells": cells})
        
        deposition_grid = {
            "hours": dep_hours,
            "max_val": global_max_dep,
            "grid_spacing": 0.002  # matches the high-fidelity grid spacing in degrees
        }
        
        total_dep_cells = sum(len(h["cells"]) for h in dep_hours)
        print(f"Deposition grid compiled: {total_dep_cells} total cells, max={global_max_dep:.6e}")
        
        # Build serializable chemical properties for frontend display
        # (includes Vd, mol_wt, henry_const for tooltip/sidebar info)
        chem_props_for_json = {}
        for chem_name, props in CHEMICAL_PROPERTIES.items():
            if chem_name == "_DEFAULT":
                continue
            chem_props_for_json[chem_name] = {
                "mol_wt": props["mol_wt"],
                "vd": props["vd"],
                "reactivity": props["reactivity"],
                "henry_const": props["henry_const"]
            }
        
        # Downsample and serialize HYSPLIT particles
        hysplit_particles = {}
        for fac_name, fac_data in raw_particles.items():
            max_count = 0
            for hour_idx, plist in fac_data.items():
                max_count = max(max_count, len(plist))
            
            # Target max ~300 particles per hour per facility
            target_max = 300
            n_factor = max(1, max_count // target_max)
            
            fac_particles = {}
            for hour_idx, plist in fac_data.items():
                filtered_list = []
                for p in plist:
                    if p["id"] % n_factor == 0:
                        filtered_list.append([
                            p["id"],
                            p["lat"],
                            p["lon"],
                            p["height"],
                            p["age"],
                            p.get("chem", "UNKNOWN"),
                            p.get("facility", 0)
                        ])
                fac_particles[hour_idx] = filtered_list
            hysplit_particles[fac_name] = fac_particles
        
        return {
            "facilities": compiled_facilities,
            "wind_grid_stack": wind_grid_stack,
            "wind_grid_fugitive": wind_grid_fugitive,
            "grid_info": grid_info,
            "deposition_grid": deposition_grid,
            "chemical_properties": chem_props_for_json,
            "particles": hysplit_particles
        }

    def build_deposition_archive(self, dates: List[str]) -> Dict[str, Any]:
        """Read the per-date deposition GeoJSON + manifest from disk and bundle them for inline
        embedding in index.html. Returns {date: {manifest, files:{fname: geojson}}}.
        Empty/missing dates are simply omitted (graceful). Inline embedding is required because the
        page is opened via file:// where fetch() of local files is blocked by the browser.
        """
        archive = {}
        base = os.path.join(self.workspace_dir, "output", "geojson")
        for date_str in dates:
            date_dir = os.path.join(base, date_str)
            manifest_path = os.path.join(date_dir, "manifest.json")
            if not os.path.exists(manifest_path):
                continue
            try:
                with open(manifest_path) as f:
                    manifest = json.load(f)
            except Exception:
                continue

            # ── Slim the embed: drop the per-facility footprint files (biggest size lever) ──
            # The per-facility footprints are ~55% of the deposition data. They're used ONLY for (a)
            # particle gating — which falls back to the COMBINED footprints automatically — and (b) the
            # per-facility % attribution in the deposition hover readout. Dropping them shrinks the file
            # a lot; the only loss is that hover-% breakdown (the combined value, the clinic popups, and
            # the drawn footprints all come from the combined entries and are unaffected). We also clear
            # manifest["entries"] so airBandAtPoint doesn't find a dangling per-facility key (which would
            # make it return null instead of falling through to combined). Set to False to restore.
            if EMBED_PER_FACILITY_FOOTPRINTS:
                remap = getattr(self, "orig_to_new_fac_id", {}) or {}
                if remap:
                    for entry in manifest.get("entries", []):
                        if entry.get("fac_id") in remap:
                            entry["fac_id"] = remap[entry["fac_id"]]
                file_entries = manifest.get("entries", []) + manifest.get("combined_entries", [])
            else:
                manifest["entries"] = []
                file_entries = manifest.get("combined_entries", [])

            files = {}
            for entry in file_entries:
                fpath = os.path.join(date_dir, entry["file"])
                if os.path.exists(fpath):
                    try:
                        with open(fpath) as f:
                            files[entry["file"]] = self._slim_geojson(json.load(f))
                    except Exception:
                        pass
            if files:
                archive[date_str] = {"manifest": manifest, "files": files}
        total = sum(len(v["files"]) for v in archive.values())
        print(f"Deposition archive: {len(archive)} date(s), {total} facility-chemical file(s) embedded")
        return archive

    @staticmethod
    def _slim_geojson(fc: Dict[str, Any]) -> Dict[str, Any]:
        """Shrink an embedded deposition FeatureCollection to cut index.html size (no re-run needed):
        round coordinates to 3 dp (~111 m — finer than the ~3 km grid, so no visible change) and
        decimate long polygon rings (drop every other vertex, keeping first/last, above 8 points).
        Contours are already smoothed; point-in-polygon (clinic popups, gating) is unaffected at
        this scale. Typically ~35-45% smaller.
        """
        for feat in fc.get("features", []):
            geom = feat.get("geometry") or {}
            coords = geom.get("coordinates")
            if not coords:
                continue
            new_rings = []
            for ring in coords:  # Polygon: list of rings
                pts = [[round(pt[0], 3), round(pt[1], 3)] for pt in ring]
                if len(pts) > 8:
                    pts = [pts[i] for i in range(0, len(pts), 2)]
                    if pts[-1] != ring[-1][:2] and len(ring) > 1:
                        pts.append([round(ring[-1][0], 3), round(ring[-1][1], 3)])
                new_rings.append(pts)
            geom["coordinates"] = new_rings
        return fc

    # ── Per-date bundle output (fetch-based site) ──
    SITE_DIR = "site"  # workspace-relative root of the deployable fetch-based site

    def write_date_bundle(self, date_str: str, plumes: Dict[str, Any], monitors: Dict[str, Any]) -> str:
        """Write one day's data as `site/data/dates/{date}.json` for the fetch-based frontend.

        Bundle shape (mirrors the old embedded structures, one date each):
          {"date", "plumes": {...}, "monitors": {...}, "dep": {"manifest":..., "files":...}}
        `plumes` is stripped of the embed-only heavy/dead fields (particles, deposition_grid) exactly
        like generate_web_visualization did. `dep` reuses build_deposition_archive (combined-only per
        EMBED_PER_FACILITY_FOOTPRINTS, coords slimmed) — that reads output/geojson/{date}/ from disk.
        Replaces the old extract-from-index.html merging: each day is a standalone file.
        """
        # build_deposition_archive needs the fac_id remap map (set as a side effect); harmless if the
        # per-facility entries are dropped (combined-only) — facilities are date-independent.
        self.build_embedded_facilities()

        plumes = dict(plumes)
        plumes.pop("particles", None)
        plumes.pop("deposition_grid", None)

        dep = self.build_deposition_archive([date_str]).get(date_str, {"manifest": {}, "files": {}})

        bundle = {"date": date_str, "plumes": plumes, "monitors": monitors or {}, "dep": dep}
        out_dir = os.path.join(self.workspace_dir, self.SITE_DIR, "data", "dates")
        os.makedirs(out_dir, exist_ok=True)
        out_path = os.path.join(out_dir, f"{date_str}.json")
        with open(out_path, "w") as f:
            json.dump(bundle, f, separators=(",", ":"))
        print(f"  Wrote date bundle: {out_path} ({os.path.getsize(out_path)/1e6:.2f} MB)")
        return out_path

    def cleanup_transient(self, date_str: str) -> None:
        """Delete a date's multi-GB scratch files after its bundle is written (for CI/cron disk limits).
        Removes: MET_<date>.ARL, dep_runs/<date>/, and that date's HRRR GRIB cache. The per-date JSON
        bundle (the only artifact that ships) is already saved before this runs.
        """
        import shutil
        yyyymmdd = date_str.replace("-", "")
        targets = [
            os.path.join(self.workspace_dir, f"MET_{yyyymmdd}.ARL"),
            os.path.join(self.workspace_dir, "dep_runs", date_str),
            os.path.join(self.grib_dir, "hrrr", yyyymmdd),
        ]
        freed = 0
        for t in targets:
            try:
                if os.path.isdir(t):
                    freed += sum(os.path.getsize(os.path.join(dp, f)) for dp, _, fs in os.walk(t) for f in fs)
                    shutil.rmtree(t, ignore_errors=True)
                elif os.path.isfile(t):
                    freed += os.path.getsize(t)
                    os.remove(t)
            except OSError as e:
                print(f"  cleanup: could not remove {t}: {e}")
        print(f"  Cleanup for {date_str}: freed ~{freed/1e9:.1f} GB of transient weather/run data.")

    def generate_web_visualization(self, manifest: Dict[str, Any]):
        """
        Render the fetch-based site shell: writes site/index.html + site/app.js. The page embeds only
        the small manifest (dates + labels); per-date data is fetched from data/dates/<date>.json.

        Args:
            manifest: {"generated_at", "dates": [{"date", "label"?}, ...]} — from build_site().
        """
        # Small manifest embedded in the page (dates + labels); everything else is fetched at runtime.
        manifest_json = json.dumps(manifest, separators=(',', ':'))

        # Particle-density anchor: max facility total over ALL facilities (facility-independent of date),
        # so the frontend spawn ratio (chem_lbs / maxFacLbs) stays stable. build_embedded_facilities()
        # sets self.max_facility_lbs; ensure it's populated.
        self.build_embedded_facilities()
        max_fac_lbs_ref = round(float(getattr(self, "max_facility_lbs", 0.0) or 0.0), 4)

        # Landmark locations (veterinary clinics) embedded inline (tiny).
        vet_clinics_json = json.dumps(VET_CLINICS, separators=(',', ':'))
        # Chemical-filter checkbox list, derived from the modeled set so it can't drift.
        dep_chem_names_json = json.dumps(DEFAULT_ACTIVE_CHEMICALS, separators=(',', ':'))
        dep_chem_labels_json = json.dumps(
            {c: CHEMICAL_DISPLAY_NAMES.get(c, c.title()) for c in DEFAULT_ACTIVE_CHEMICALS},
            separators=(',', ':'))

        html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Calvert City Industrial Dispersion Prototype</title>
    
    <!-- Google Fonts -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Outfit:wght@400;600;800&display=swap" rel="stylesheet">
    
    <!-- Leaflet.js Mapping Engine -->
    <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" integrity="sha256-p4NxAoJBhIIN+hmNHrzRCf9tD/miZyoHS5obTRR9BMY=" crossorigin=""/>
    <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js" integrity="sha256-20nQCchB9co0qIjJZRGuk2/Z9VM+kNiyxNV1lvTlZBo=" crossorigin=""></script>
    <!-- Leaflet.heat plugin for smooth gaussian heatmaps -->
    <script src="https://unpkg.com/leaflet.heat@0.2.0/dist/leaflet-heat.js"></script>
    
    <style>
        :root {{
            --bg-dark: #0f0f12;
            --panel-bg: rgba(20, 20, 25, 0.72);
            --panel-border: rgba(255, 255, 255, 0.09);
            --text-main: #f9fafb;
            --text-muted: #9ca3af;
            --primary-accent: #3b82f6;
            --primary-accent-glow: rgba(59, 130, 246, 0.35);
            --font-family: 'Inter', system-ui, sans-serif;
            --header-font: 'Outfit', sans-serif;
        }}

        * {{
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }}

        body, html {{
            width: 100%;
            height: 100%;
            overflow: hidden;
            background-color: var(--bg-dark);
            font-family: var(--font-family);
            color: var(--text-main);
        }}

        #map-viewport {{
            position: relative;
            width: 100vw;
            height: 100vh;
            z-index: 1;
        }}

        #map {{
            width: 100%;
            height: 100%;
            background-color: var(--bg-dark);
        }}

        #particle-canvas {{
            position: absolute;
            pointer-events: none;
        }}

        /* Dark theme Leaflet Popups (removes white border and tip) */
        .leaflet-popup-content-wrapper {{
            background: #121214 !important;
            color: #f3f4f6 !important;
            padding: 0 !important;
            border-radius: 12px !important;
            border: 1px solid rgba(255, 255, 255, 0.12) !important;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.6) !important;
        }}

        .leaflet-popup-content {{
            margin: 0 !important;
            padding: 0 !important;
        }}

        .leaflet-popup-tip {{
            background: #121214 !important;
            border-left: 1px solid rgba(255, 255, 255, 0.12) !important;
            border-top: 1px solid rgba(255, 255, 255, 0.12) !important;
            box-shadow: none !important;
        }}

        .leaflet-popup-close-button {{
            color: #9ca3af !important;
            padding: 8px 8px 0 0 !important;
        }}

        .leaflet-popup-close-button:hover {{
            color: #fff !important;
            background: transparent !important;
        }}

        /* Glassmorphic Panel Design System */
        .glass-panel {{
            background: var(--panel-bg);
            border: 1px solid var(--panel-border);
            backdrop-filter: blur(16px);
            -webkit-backdrop-filter: blur(16px);
            border-radius: 16px;
            box-shadow: 0 12px 40px rgba(0, 0, 0, 0.65),
                        inset 0 1px 0 rgba(255, 255, 255, 0.05);
            color: var(--text-main);
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        }}

        /* ── Collapsible Panel System ── */
        .panel-topbar {{
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin-bottom: 4px;
        }}

        .panel-collapse-btn {{
            background: rgba(255, 255, 255, 0.06);
            border: 1px solid rgba(255, 255, 255, 0.1);
            color: var(--text-muted);
            border-radius: 6px;
            width: 28px;
            height: 28px;
            display: flex;
            align-items: center;
            justify-content: center;
            cursor: pointer;
            font-size: 14px;
            line-height: 1;
            transition: all 0.2s ease;
            outline: none;
            flex-shrink: 0;
        }}

        .panel-collapse-btn:hover {{
            background: rgba(255, 255, 255, 0.14);
            border-color: rgba(255, 255, 255, 0.25);
            color: #fff;
            transform: scale(1.1);
        }}

        .panel-body {{
            overflow: hidden;
            transition: max-height 0.35s cubic-bezier(0.4, 0, 0.2, 1),
                        opacity 0.25s ease,
                        padding 0.3s ease;
            max-height: 2000px;
            opacity: 1;
        }}

        .panel-body.collapsed {{
            max-height: 0;
            opacity: 0;
            padding-top: 0;
            padding-bottom: 0;
        }}

        /* Floating restore pills — visible when parent panel is collapsed */
        .panel-restore-pill {{
            position: absolute;
            z-index: 1100;
            display: none;
            align-items: center;
            gap: 6px;
            padding: 8px 14px;
            border-radius: 20px;
            cursor: pointer;
            font-family: var(--font-family);
            font-size: 11px;
            font-weight: 700;
            letter-spacing: 0.04em;
            text-transform: uppercase;
            transition: all 0.25s ease;
        }}

        .panel-restore-pill.visible {{
            display: flex;
        }}

        .panel-restore-pill:hover {{
            transform: scale(1.06);
        }}

        #restore-header {{
            top: 24px;
            left: 24px;
            background: var(--panel-bg);
            border: 1px solid var(--panel-border);
            backdrop-filter: blur(16px);
            -webkit-backdrop-filter: blur(16px);
            color: #a5b4fc;
            box-shadow: 0 8px 24px rgba(0, 0, 0, 0.5);
        }}

        #restore-header:hover {{
            background: rgba(30, 30, 38, 0.85);
            box-shadow: 0 8px 28px rgba(59, 130, 246, 0.15);
        }}

        #restore-legend {{
            top: 24px;
            right: 24px;
            background: var(--panel-bg);
            border: 1px solid var(--panel-border);
            backdrop-filter: blur(16px);
            -webkit-backdrop-filter: blur(16px);
            color: #a5b4fc;
            box-shadow: 0 8px 24px rgba(0, 0, 0, 0.5);
        }}

        #restore-legend:hover {{
            background: rgba(30, 30, 38, 0.85);
            box-shadow: 0 8px 28px rgba(59, 130, 246, 0.15);
        }}

        /* Header Panel */
        .hud-header {{
            position: absolute;
            top: 24px;
            left: 24px;
            z-index: 1100;
            padding: 20px 24px;
            width: 380px;
        }}

        .hud-header.panel-hidden {{
            display: none;
        }}

        .hud-header h1 {{
            font-family: var(--header-font);
            font-size: 20px;
            font-weight: 700;
            letter-spacing: -0.02em;
            margin-bottom: 6px;
            background: linear-gradient(135deg, #ffffff 30%, #a5b4fc 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }}

        .hud-header .subtitle {{
            font-size: 12px;
            color: var(--text-muted);
            line-height: 1.4;
        }}

        .hud-header .divider {{
            height: 1px;
            background: rgba(255, 255, 255, 0.08);
            margin: 12px 0;
        }}

        .hud-header .meta-row {{
            display: flex;
            justify-content: space-between;
            font-size: 11px;
        }}

        .hud-header .meta-val {{
            font-weight: 600;
            color: #a5b4fc;
        }}

        /* Bottom Controls HUD */
        .hud-controls {{
            position: absolute;
            bottom: 36px;
            left: 50%;
            transform: translateX(-50%);
            z-index: 1100;
            width: 680px;
            padding: 20px 28px;
            display: flex;
            flex-direction: column;
            gap: 16px;
        }}

        .controls-row {{
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 20px;
        }}

        .time-readout {{
            display: flex;
            align-items: center;
            gap: 8px;
            min-width: 140px;
        }}

        .time-meta {{ display: flex; flex-direction: column; line-height: 1.25; }}
        .time-date {{ font-size: 9px; color: var(--text-muted); letter-spacing: 0.02em; text-transform: none; }}

        .time-val {{
            font-family: var(--header-font);
            font-size: 26px;
            font-weight: 600;
            color: #fff;
            font-variant-numeric: tabular-nums;
        }}

        .time-label {{
            font-size: 11px;
            color: var(--text-muted);
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }}

        .playback-actions {{
            display: flex;
            align-items: center;
            gap: 14px;
        }}

        .btn {{
            background: rgba(255, 255, 255, 0.07);
            border: 1px solid rgba(255, 255, 255, 0.1);
            color: var(--text-main);
            border-radius: 50%;
            width: 44px;
            height: 44px;
            display: flex;
            align-items: center;
            justify-content: center;
            cursor: pointer;
            transition: all 0.2s ease;
            outline: none;
        }}

        .btn:hover {{
            background: rgba(255, 255, 255, 0.15);
            border-color: rgba(255, 255, 255, 0.25);
            box-shadow: 0 0 10px rgba(255, 255, 255, 0.1);
            transform: scale(1.05);
        }}

        .btn:active {{
            transform: scale(0.95);
        }}

        .slider-container {{
            flex-grow: 1;
            display: flex;
            align-items: center;
            gap: 12px;
        }}

        .slider {{
            -webkit-appearance: none;
            width: 100%;
            height: 6px;
            border-radius: 3px;
            background: rgba(255, 255, 255, 0.12);
            outline: none;
            cursor: pointer;
            transition: background 0.15s ease;
        }}

        .slider::-webkit-slider-thumb {{
            -webkit-appearance: none;
            appearance: none;
            width: 16px;
            height: 16px;
            border-radius: 50%;
            background: #fff;
            cursor: pointer;
            box-shadow: 0 0 8px rgba(0,0,0,0.5);
            transition: transform 0.1s ease;
        }}

        .slider::-webkit-slider-thumb:hover {{
            transform: scale(1.25);
            background: #a5b4fc;
        }}

        /* Speed slider specifics */
        .speed-control {{
            display: flex;
            align-items: center;
            gap: 8px;
            font-size: 11px;
            color: var(--text-muted);
            min-width: 140px;
        }}

        .speed-control select {{
            background: rgba(20, 20, 25, 0.85);
            border: 1px solid var(--panel-border);
            color: var(--text-main);
            padding: 4px 8px;
            border-radius: 6px;
            outline: none;
            cursor: pointer;
            font-family: var(--font-family);
            font-size: 11px;
        }}

        /* Legend Panel */
        .hud-legend {{
            position: absolute;
            top: 24px;
            right: 24px;
            z-index: 1100;
            width: 360px;
            padding: 20px;
            max-height: calc(100vh - 120px);
            display: flex;
            flex-direction: column;
        }}

        .hud-legend.panel-hidden {{
            display: none;
        }}

        #legend-panel-body {{
            display: flex;
            flex-direction: column;
            min-height: 0;
            flex: 1;
        }}

        .legend-title {{
            font-family: var(--header-font);
            font-size: 15px;
            font-weight: 600;
            margin-bottom: 14px;
            letter-spacing: -0.01em;
            color: #fff;
        }}

        .facility-list {{
            display: flex;
            flex-direction: column;
            gap: 12px;
            overflow-y: auto;
            padding-right: 4px;
            flex: 1;
            min-height: 0;
        }}

        .facility-item {{
            border-radius: 10px;
            padding: 10px 12px;
            background: rgba(255, 255, 255, 0.02);
            border: 1px solid rgba(255, 255, 255, 0.03);
            cursor: pointer;
            transition: all 0.2s ease;
        }}

        .facility-item:hover {{
            background: rgba(255, 255, 255, 0.05);
            border-color: rgba(255, 255, 255, 0.08);
        }}

        .facility-item.disabled {{
            opacity: 0.35;
        }}

        .facility-header {{
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin-bottom: 6px;
        }}

        .facility-name-row {{
            display: flex;
            align-items: center;
            gap: 8px;
        }}

        .facility-badge {{
            width: 10px;
            height: 10px;
            border-radius: 50%;
            box-shadow: 0 0 8px currentColor;
        }}

        .facility-name {{
            font-weight: 600;
            font-size: 13px;
            color: #fff;
        }}

        .toggle-icon {{
            font-size: 10px;
            color: var(--text-muted);
            text-transform: uppercase;
            font-weight: 700;
            letter-spacing: 0.05em;
        }}

        .chem-list {{
            display: flex;
            flex-direction: column;
            gap: 4px;
            padding-left: 18px;
            font-size: 11px;
            color: var(--text-muted);
            border-left: 1px solid rgba(255, 255, 255, 0.06);
            margin-top: 4px;
        }}

        .chem-item {{
            display: flex;
            justify-content: space-between;
        }}

        .chem-val {{
            font-weight: 500;
            color: var(--text-main);
        }}

        /* Tooltip style */
        .particle-tooltip {{
            position: absolute;
            z-index: 1200;
            background: rgba(12, 12, 16, 0.92);
            border: 1px solid rgba(255, 255, 255, 0.15);
            border-radius: 8px;
            padding: 10px 14px;
            color: var(--text-main);
            font-size: 11px;
            pointer-events: none;
            box-shadow: 0 8px 24px rgba(0,0,0,0.6);
            display: none;
            line-height: 1.5;
            backdrop-filter: blur(8px);
        }}

        .tooltip-header {{
            font-weight: 700;
            margin-bottom: 4px;
            border-bottom: 1px solid rgba(255,255,255,0.1);
            padding-bottom: 2px;
            font-family: var(--header-font);
        }}

        /* Map Attribution adjustments */
        .leaflet-control-attribution {{
            background: rgba(0,0,0,0.85) !important;
            color: var(--text-muted) !important;
            font-size: 9px !important;
        }}

        /* Custom Facility Marker DivIcon Overrides */
        .custom-facility-divicon {{
            background: transparent !important;
            border: none !important;
            box-shadow: none !important;
        }}

        /* Enable Text Selection inside Leaflet Popups */
        .leaflet-popup-content, .leaflet-popup-content * {{
            -webkit-user-select: text !important;
            -moz-user-select: text !important;
            -ms-user-select: text !important;
            user-select: text !important;
        }}

        #pollutant-select, #date-picker, #display-mode-select, #deposition-source-select {{
            width: 100%;
            background: rgba(18, 18, 20, 0.6);
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 8px;
            color: #fff;
            font-family: 'Inter', sans-serif;
            font-size: 12px;
            padding: 8px 12px;
            outline: none;
            cursor: pointer;
            transition: all 0.2s ease;
            backdrop-filter: blur(4px);
        }}
        
        #pollutant-select:hover, #date-picker:hover, #display-mode-select:hover, #deposition-source-select:hover {{
            background: rgba(255, 255, 255, 0.08);
            border-color: rgba(255, 255, 255, 0.2);
        }}
        
        #pollutant-select option, #display-mode-select option, #deposition-source-select option {{
            background: #121214;
            color: #fff;
        }}

        #date-picker::-webkit-calendar-picker-indicator {{
            filter: invert(1);
            cursor: pointer;
        }}

        /* ── Simulation Sandbox Panel ── */
        .sandbox-section {{
            margin-top: 14px;
        }}

        .sandbox-toggle-btn {{
            display: flex;
            align-items: center;
            justify-content: space-between;
            width: 100%;
            background: rgba(59, 130, 246, 0.08);
            border: 1px solid rgba(59, 130, 246, 0.18);
            border-radius: 8px;
            padding: 8px 12px;
            cursor: pointer;
            color: #a5b4fc;
            font-family: var(--font-family);
            font-size: 11px;
            font-weight: 700;
            letter-spacing: 0.06em;
            text-transform: uppercase;
            transition: all 0.25s ease;
        }}

        .sandbox-toggle-btn:hover {{
            background: rgba(59, 130, 246, 0.15);
            border-color: rgba(59, 130, 246, 0.35);
            box-shadow: 0 0 12px rgba(59, 130, 246, 0.15);
        }}

        .sandbox-toggle-arrow {{
            transition: transform 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            font-size: 10px;
        }}

        .sandbox-toggle-arrow.expanded {{
            transform: rotate(180deg);
        }}

        .sandbox-body {{
            display: none;
            flex-direction: column;
            gap: 10px;
            margin-top: 10px;
            padding: 12px;
            background: rgba(10, 10, 14, 0.5);
            border: 1px solid rgba(255, 255, 255, 0.04);
            border-radius: 10px;
        }}

        .sandbox-body.open {{
            display: flex;
        }}

        .sandbox-group {{
            display: flex;
            flex-direction: column;
            gap: 4px;
        }}

        .sandbox-label {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            font-size: 10px;
            color: var(--text-muted);
            font-weight: 600;
            letter-spacing: 0.04em;
        }}

        .sandbox-val {{
            font-weight: 700;
            color: #a5b4fc;
            font-variant-numeric: tabular-nums;
            min-width: 56px;
            text-align: right;
        }}

        .sandbox-slider {{
            -webkit-appearance: none;
            width: 100%;
            height: 5px;
            border-radius: 3px;
            background: rgba(255, 255, 255, 0.1);
            outline: none;
            cursor: pointer;
            transition: background 0.15s ease;
        }}

        .sandbox-slider::-webkit-slider-thumb {{
            -webkit-appearance: none;
            appearance: none;
            width: 14px;
            height: 14px;
            border-radius: 50%;
            background: linear-gradient(135deg, #818cf8, #6366f1);
            cursor: pointer;
            box-shadow: 0 0 6px rgba(99, 102, 241, 0.5);
            transition: transform 0.12s ease, box-shadow 0.12s ease;
        }}

        .sandbox-slider::-webkit-slider-thumb:hover {{
            transform: scale(1.3);
            box-shadow: 0 0 12px rgba(99, 102, 241, 0.7);
        }}

        .sandbox-slider::-moz-range-thumb {{
            width: 14px;
            height: 14px;
            border-radius: 50%;
            background: linear-gradient(135deg, #818cf8, #6366f1);
            cursor: pointer;
            border: none;
            box-shadow: 0 0 6px rgba(99, 102, 241, 0.5);
        }}

        .sandbox-divider {{
            height: 1px;
            background: rgba(255, 255, 255, 0.05);
            margin: 2px 0;
        }}
        /* ── Deposition / Air-Layer toggles ── */
        .dep-toggle {{ position:relative; display:inline-block; width:30px; height:16px; flex-shrink:0; }}
        .dep-toggle input {{ display:none; }}
        .dep-toggle-slider {{ position:absolute; top:0; left:0; right:0; bottom:0; background:#333; border-radius:16px; cursor:pointer; transition:.2s; }}
        .dep-toggle-slider::before {{ content:""; position:absolute; width:12px; height:12px; left:2px; bottom:2px; background:#555; border-radius:50%; transition:.2s; }}
        .dep-toggle input:checked + .dep-toggle-slider {{ background:#2a7a4f; }}
        .dep-toggle input:checked + .dep-toggle-slider::before {{ background:#fff; transform:translateX(14px); }}
        .dep-info-btn {{ position:relative; cursor:help; font-size:10px; color:var(--text-muted); border:1px solid rgba(255,255,255,.25); border-radius:50%; width:14px; height:14px; display:inline-flex; align-items:center; justify-content:center; flex-shrink:0; }}
        /* Custom instant-hover tooltip (native title= has a ~3-4s browser delay).
           Reparented to <body> + position:fixed via JS so the panel's overflow:hidden
           (collapse animation) can't clip it; JS sets left/top on hover. */
        .info-pop {{ display:none; position:fixed; z-index:10000; width:270px; padding:10px 12px; background:#121214; color:#e5e7eb; border:1px solid rgba(255,255,255,.15); border-radius:8px; font-size:10px; line-height:1.55; font-weight:400; letter-spacing:normal; text-align:left; box-shadow:0 10px 28px rgba(0,0,0,.55); white-space:normal; pointer-events:none; }}
        .info-pop b {{ color:#fff; font-weight:600; }}
        .info-pop .ip-sep {{ display:block; height:6px; }}
        /* Related-tool link — Odor Forecast (external, opens new tab) */
        .odor-link {{ display:flex; flex-direction:column; gap:2px; margin-top:14px; padding:10px 12px; border-radius:10px; text-decoration:none; background:rgba(59,130,246,.14); border:1px solid rgba(59,130,246,.42); transition:background .15s ease, border-color .15s ease, transform .08s ease; }}
        .odor-link:hover {{ background:rgba(59,130,246,.24); border-color:rgba(59,130,246,.75); }}
        .odor-link:active {{ transform:translateY(1px); }}
        .odor-link-main {{ font-family:var(--header-font); font-size:12.5px; font-weight:600; color:var(--text-main); display:flex; align-items:center; gap:6px; }}
        .odor-link-arrow {{ color:var(--primary-accent); font-size:13px; font-weight:700; }}
        .odor-link-hint {{ font-size:9px; color:var(--text-muted); letter-spacing:.03em; }}
        /* LOCATIONS collapsible section */
        .loc-toggle-btn {{ display:flex; align-items:center; justify-content:space-between; width:100%; background:none; border:none; padding:0; cursor:pointer; color:var(--text-muted); font-size:10px; font-weight:600; letter-spacing:.05em; }}
        .loc-toggle-btn:hover {{ color:var(--text-primary); }}
        .loc-arrow {{ font-size:8px; transition:transform .2s; transform:rotate(-90deg); }}
        .loc-arrow.expanded {{ transform:rotate(0deg); }}
        .loc-body {{ overflow:hidden; max-height:0; opacity:0; transition:max-height .3s ease, opacity .25s ease; }}
        .loc-body.open {{ max-height:300px; opacity:1; }}
        .loc-swatch {{ width:11px; height:11px; border-radius:50%; flex-shrink:0; display:inline-block; }}
        .loc-swatch-vet {{ background:#0d9488; border:1.5px solid #fff; box-shadow:0 0 3px rgba(0,0,0,.4); }}
        /* Vet clinic marker (SVG divIcon has no box; keep pointer cursor) */
        .vet-clinic-divicon {{ cursor:pointer; }}
        .vet-clinic-divicon svg {{ display:block; filter:drop-shadow(0 2px 3px rgba(0,0,0,.45)); }}
        .vet-pop {{ font-size:12px; color:#f3f4f6; min-width:210px; max-width:250px; padding:11px 15px 12px 15px; box-sizing:border-box; }}
        .vet-pop .vp-title {{ font-weight:600; font-size:13px; color:#fff; margin-bottom:3px; padding-right:16px; line-height:1.35; }}
        .vet-pop .vp-addr {{ color:#9ca3af; font-size:11px; margin-bottom:8px; line-height:1.4; }}
        .vet-pop .vp-dep {{ font-size:11px; line-height:1.55; border-top:1px solid rgba(255,255,255,.12); padding-top:7px; }}
        .vet-pop .vp-more {{ color:#93c5fd; cursor:pointer; text-decoration:underline; text-decoration-style:dotted; white-space:nowrap; }}
        .vet-pop .vp-more:hover {{ color:#bfdbfe; }}
        .vet-pop .vp-arrow {{ font-size:9px; text-decoration:none; display:inline-block; }}
        .vet-pop .vp-chemlist {{ margin-top:6px; border-top:1px dashed rgba(255,255,255,.12); padding-top:5px; }}
        .vet-pop .vp-chemrow {{ display:flex; justify-content:space-between; gap:12px; padding:1px 0; color:rgba(255,255,255,.8); font-size:10.5px; }}
        .vet-pop .vp-chemrow span:first-child {{ text-transform:capitalize; }}
        .dep-chem-pill {{ display:flex; align-items:center; gap:3px; font-size:9px; color:var(--text-muted); cursor:pointer; background:rgba(255,255,255,.04); border:1px solid rgba(255,255,255,.08); border-radius:10px; padding:2px 6px; white-space:nowrap; }}
        .dep-chem-pill input {{ cursor:pointer; margin:0; }}
        .dep-chem-pill:has(input:checked) {{ border-color:rgba(255,255,255,.25); color:rgba(255,255,255,.8); }}
        /* ── Hover concentration readout ── */
        #dep-readout {{ position:absolute; z-index:9999; pointer-events:none; display:none;
            background:rgba(10,12,20,.93); border:1px solid rgba(255,255,255,.15); border-radius:8px;
            padding:8px 10px; font-size:11px; color:#e8e8ef; max-width:260px;
            box-shadow:0 4px 16px rgba(0,0,0,.45); backdrop-filter:blur(6px); }}
        #dep-readout .dr-title {{ font-size:9px; color:var(--text-muted); margin-bottom:5px; letter-spacing:.05em; }}
        #dep-readout .dr-chem {{ font-weight:600; margin-top:4px; }}
        #dep-readout .dr-row {{ display:flex; justify-content:space-between; gap:14px; color:rgba(255,255,255,.75); }}
    </style>
</head>
<body>

    <div id="map-viewport">
        <!-- Leaflet Map Div -->
        <div id="map"></div>

        <!-- Overhead Particle Rendering Canvas -->
        <canvas id="particle-canvas"></canvas>

        <!-- Hover concentration readout -->
        <div id="dep-readout"></div>

        <!-- Floating Restore Pills (visible when panels are collapsed) -->
        <div class="panel-restore-pill" id="restore-header">
            <span>☰</span><span>Controls</span>
        </div>
        <div class="panel-restore-pill" id="restore-legend">
            <span>☰</span><span>Sources</span>
        </div>

        <!-- HUD Header -->
        <div class="hud-header glass-panel" id="hud-header-panel">
            <div class="panel-topbar">
                <h1 style="margin-bottom:0">Calvert City Plume Analysis</h1>
                <button class="panel-collapse-btn" id="collapse-header" title="Minimize Panel">−</button>
            </div>
            <div class="panel-body" id="header-panel-body">
                <div class="subtitle" style="margin-top:4px">Multi-date batch chemical dispersion simulation using hourly NOAA HRRR boundary conditions.</div>
                <div class="divider"></div>
                <div class="meta-row">
                    <div style="display: flex; align-items: center; gap: 4px;">STATE: <span class="meta-val">KENTUCKY</span></div>
                    <div style="display: flex; align-items: center; gap: 4px;">WEATHER: <span class="meta-val">HRRR GRIB2</span></div>
                </div>
                <div class="divider"></div>
                <div style="margin-top: 12px;">
                    <label for="date-picker" style="font-size: 10px; color: var(--text-muted); font-weight: 600; display: block; margin-bottom: 6px; letter-spacing: 0.05em;">SIMULATION DATE</label>
                    <select id="date-picker"></select>
                </div>
                <div style="margin-top: 12px;">
                    <label for="pollutant-select" style="font-size: 10px; color: var(--text-muted); font-weight: 600; display: block; margin-bottom: 6px; letter-spacing: 0.05em;">EPA AIR QUALITY PARAMETER</label>
                    <select id="pollutant-select">
                        <!-- Javascript populated -->
                    </select>
                </div>
                <div style="margin-top: 12px;">
                    <label for="display-mode-select" style="font-size: 10px; color: var(--text-muted); font-weight: 600; display: block; margin-bottom: 6px; letter-spacing: 0.05em;">PLUME DISPLAY MODE</label>
                    <select id="display-mode-select">
                        <option value="combined" selected>Combined Total Air</option>
                        <option value="stack">Stacks Only</option>
                        <option value="fugitive">Fugitive Only</option>
                    </select>
                </div>

                <div style="margin-top: 12px;">
                    <div style="display:flex;align-items:center;gap:5px;margin-bottom:6px;">
                        <span style="font-size:10px;color:var(--text-muted);font-weight:600;letter-spacing:.05em;">CHEMICAL FILTERS</span>
                    </div>
                    <div id="dep-chem-list" style="display:flex;flex-wrap:wrap;gap:3px;max-height:96px;overflow-y:auto;"></div>
                </div>

                <!-- ══ Layers ══ -->
                <div class="divider"></div>
                <div style="margin-top:12px;">
                    <div style="display:flex;align-items:center;gap:5px;margin-bottom:8px;">
                        <span style="font-size:10px;color:var(--text-muted);font-weight:600;letter-spacing:.05em;">LAYERS</span>
                        <span class="dep-info-btn">ⓘ<span class="info-pop">Three independent views of the same release:<span class="ip-sep"></span><b>Soil Deposition (g/m²)</b> — mass that physically settles onto the ground, accumulating over the day. Chlorine &amp; ammonia deposit meaningfully; VOCs barely deposit (tiny footprints — honest).<span class="ip-sep"></span><b>Ground-Level Air (g/m³)</b> — breathing-zone concentration at ~10&nbsp;m, shown per hour. This is what you'd actually inhale; every chemical has a footprint here.<span class="ip-sep"></span><b>Particle Simulation</b> — animated tracers streamed from each facility (colored by source), advected on the HYSPLIT hourly wind. They show <b>how</b> the plume moves and mixes in real time; the footprints show <b>where</b> concentration and deposit end up.<span class="ip-sep"></span>Footprints are straight from HYSPLIT contours (23 hourly frames, sim hours 2–24): deposition accumulates, air is per-hour, particles animate continuously.</span></span>
                    </div>
                    <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:5px;">
                        <span style="font-size:11px;color:var(--text-primary);">Soil Deposition <span style="color:var(--text-muted);font-size:9px;">(g/m²)</span></span>
                        <label class="dep-toggle"><input type="checkbox" id="dep-layer-toggle" checked><span class="dep-toggle-slider"></span></label>
                    </div>
                    <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:5px;">
                        <span style="font-size:11px;color:var(--text-primary);">Ground-Level Air <span style="color:var(--text-muted);font-size:9px;">(g/m³)</span></span>
                        <label class="dep-toggle"><input type="checkbox" id="air-layer-toggle" checked><span class="dep-toggle-slider"></span></label>
                    </div>
                    <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:8px;">
                        <span style="font-size:11px;color:var(--text-primary);">Particle Simulation <span style="color:var(--text-muted);font-size:9px;">(animated)</span></span>
                        <label class="dep-toggle"><input type="checkbox" id="particles-toggle" checked><span class="dep-toggle-slider"></span></label>
                    </div>
                </div>

                <!-- ══ Locations (landmark layers) ══ -->
                <div class="divider"></div>
                <div style="margin-top:12px;">
                    <button class="loc-toggle-btn" id="locations-toggle" type="button">
                        <span>LOCATIONS</span>
                        <span class="loc-arrow expanded" id="locations-arrow">▼</span>
                    </button>
                    <div class="loc-body open" id="locations-body">
                        <div style="display:flex;align-items:center;justify-content:space-between;margin-top:8px;">
                            <span style="font-size:11px;color:var(--text-primary);display:flex;align-items:center;gap:6px;">
                                <span class="loc-swatch loc-swatch-vet"></span>Veterinary Clinics
                                <span style="color:var(--text-muted);font-size:9px;" id="vet-count"></span>
                            </span>
                            <label class="dep-toggle"><input type="checkbox" id="vet-clinics-toggle" checked><span class="dep-toggle-slider"></span></label>
                        </div>
                    </div>
                </div>

                <!-- ══ Related tool: Odor Forecast (external, opens in a new tab) ══ -->
                <a href="https://nwright083.github.io/weather-variable-analysis/" target="_blank" rel="noopener noreferrer" class="odor-link" title="Opens the Odor Forecast tool in a new browser tab">
                    <span class="odor-link-main">View Odor Forecast <span class="odor-link-arrow">↗</span></span>
                    <span class="odor-link-hint">opens in a new tab</span>
                </a>

                <!-- Simulation Sandbox removed: particle motion/appearance are fixed so viewers
                     can't alter the model. Defaults live in the getSandbox*() getters + the
                     footprintOpacity constant. -->
            </div>
        </div>

        <!-- Legend and Toggles -->
        <div class="hud-legend glass-panel" id="hud-legend-panel">
            <div class="panel-topbar">
                <div class="legend-title" style="margin-bottom:0">Industrial Point Sources</div>
                <button class="panel-collapse-btn" id="collapse-legend" title="Minimize Panel">−</button>
            </div>
            <div class="panel-body" id="legend-panel-body">
                <div class="facility-list" id="facility-legend">
                    <!-- Javascript populated -->
                </div>
            </div>
        </div>

        <!-- Controls HUD -->
        <div class="hud-controls glass-panel">
            <div class="controls-row">
                <div class="time-readout">
                    <span class="time-val" id="time-display">12:00</span>
                    <span class="time-meta">
                        <span class="time-label" id="ampm-display">AM</span>
                        <span class="time-date" id="time-date-display"></span>
                    </span>
                    <span class="dep-info-btn" style="align-self:center; margin-left:2px;">ⓘ<span class="info-pop"><b>Times are shown in Calvert City local time (Central — CST/CDT).</b><span class="ip-sep"></span>The model runs on the day's UTC weather (NOAA HRRR) and the clock converts each hour to local time. Because a UTC day spans two local dates, the timeline starts the prior evening (~7&nbsp;PM) and ends the next evening — the small date under the clock is the actual local date at each moment (it rolls over at local midnight).</span></span>
                </div>
                
                <div class="slider-container">
                    <span style="font-size:10px; color:var(--text-muted)">00:00</span>
                    <input type="range" min="0.0" max="24.0" step="0.01" value="0.0" class="slider" id="time-slider">
                    <span style="font-size:10px; color:var(--text-muted)">24:00</span>
                </div>
            </div>
            
            <div class="controls-row" style="margin-top: 4px;">
                <div class="playback-actions">
                    <button class="btn" id="play-btn" title="Play/Pause">
                        <!-- Play Icon -->
                        <svg id="play-icon" width="14" height="16" viewBox="0 0 14 16" fill="none" style="display:none;">
                            <path d="M13 8L1 1V15L13 8Z" fill="white" stroke="white" stroke-width="2" stroke-linejoin="round"/>
                        </svg>
                        <!-- Pause Icon -->
                        <svg id="pause-icon" width="12" height="16" viewBox="0 0 12 16" fill="none">
                            <path d="M1 1V15M11 1V15" stroke="white" stroke-width="3" stroke-linecap="round"/>
                        </svg>
                    </button>
                    <button class="btn" id="restart-btn" title="Restart Simulation">
                        <!-- Restart SVG -->
                        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                            <path d="M21 12a9 9 0 1 1-9-9c2.52 0 4.93 1 6.74 2.74L21 8"/>
                            <path d="M21 3v5h-5"/>
                        </svg>
                    </button>
                </div>
                
                <div class="speed-control">
                    <span>PLAYBACK SPEED:</span>
                    <select id="speed-select">
                        <option value="1">1 Hour/Min</option>
                        <option value="2" selected>5 Hours/Min</option>
                        <option value="3">10 Hours/Min</option>
                        <option value="4">30 Hours/Min</option>
                        <option value="5">60 Hours/Min</option>
                    </select>
                </div>
                
                <div style="font-size: 11px; color: var(--text-muted)">
                    ACTIVE PARTICLES: <span id="active-count" style="font-weight:600; color:#fff">0</span>
                </div>
            </div>
        </div>
        
        <!-- Interactive Tooltip Overlay -->
        <div class="particle-tooltip" id="tooltip">
            <div class="tooltip-header" id="tooltip-title">Facility</div>
            <div id="tooltip-body">Coords</div>
        </div>
    </div>

    <!-- Data Injection Block -->
    <script>
        // ── Fetch-based loading ── these start empty and are filled from data/dates/<date>.json.
        // (A month of embedded days would exceed GitHub's 100 MB/file limit, so each day is fetched.)
        let historicalSimulationArchive = {{}};
        let depositionArchive = {{}};
        let activeDate = null, PLUME_DATA = null, regionalMonitorData = null;
        const VET_CLINICS = {vet_clinics_json};
        const PLUME_MANIFEST = {manifest_json};   // {{ generated_at, dates:[{{date,label}}] }}

        // Friendly fatal-error card (opened via file://, or a pruned/missing date).
        function pd_showFatal(msg) {{
            let el = document.getElementById('pd-fatal');
            if (!el) {{
                el = document.createElement('div'); el.id = 'pd-fatal';
                el.style.cssText = 'position:fixed;inset:0;z-index:99999;display:flex;align-items:center;justify-content:center;background:#0b0d12;color:#e5e7eb;font-family:Inter,system-ui,sans-serif;padding:24px;text-align:center';
                (document.body || document.documentElement).appendChild(el);
            }}
            el.innerHTML = '<div style="max-width:520px"><div style="font-size:38px;margin-bottom:10px">&#128062;</div>'
                + '<div style="font-size:17px;font-weight:600;margin-bottom:8px">Calvert City Plume Analysis</div>'
                + '<div style="font-size:13px;line-height:1.6;color:#9ca3af">' + msg + '</div></div>';
        }}
        // Fetch one day's bundle into the archives (cached after first load).
        async function pd_fetchDate(dateStr) {{
            if (historicalSimulationArchive[dateStr]) return;
            const resp = await fetch('data/dates/' + dateStr + '.json', {{ cache: 'default' }});
            if (!resp.ok) throw new Error('HTTP ' + resp.status);
            const b = await resp.json();
            historicalSimulationArchive[dateStr] = {{ plumes: b.plumes, monitors: b.monitors }};
            depositionArchive[dateStr] = b.dep;
        }}
        // Boot: pick date (?date= or newest), fetch it, then load the app (app.js).
        (async function pd_boot() {{
            const all = (PLUME_MANIFEST.dates || []).map(function (d) {{ return d.date; }});
            const params = new URLSearchParams(location.search);
            let target = params.get('date');
            if (all.indexOf(target) < 0) target = all.length ? all[all.length - 1] : null;
            if (!target) {{ pd_showFatal('No simulation days are available yet. Check back after the next nightly update.'); return; }}
            try {{ await pd_fetchDate(target); }}
            catch (e) {{
                pd_showFatal(location.protocol === 'file:'
                    ? 'This page loads its data over the network, which browsers block for files opened directly. Use the included <b>View&nbsp;Locally</b> script to preview it.'
                    : 'Could not load data for ' + target + ' (' + e.message + '). Please refresh.');
                return;
            }}
            window.__ACTIVE_DATE = target;
            const s = document.createElement('script'); s.src = 'app.js';
            document.body.appendChild(s);
        }})();
    </script>

    <!-- UI and Rendering Engine Script -->
    <script>
        // Active date + data (globals declared in the bootstrap above; assigned here from the bundle)
        activeDate = window.__ACTIVE_DATE;
        PLUME_DATA = historicalSimulationArchive[activeDate].plumes;
        regionalMonitorData = historicalSimulationArchive[activeDate].monitors;
        // Declared early (before the map) so drawParticles()/updateTooltip(), which Leaflet may
        // fire during map init, never hit a temporal-dead-zone ReferenceError. Default visible;
        // overwritten below from the toggle elements IF they exist (some builds omit them).
        let showParticles = true;
        let showDeposition = true;

        // Save the original pre-calculated HYSPLIT deposition grids so they aren't lost
        Object.keys(historicalSimulationArchive).forEach(dateStr => {{
            const plumes = historicalSimulationArchive[dateStr].plumes;
            if (plumes.deposition_grid && !plumes.hysplit_deposition_grid) {{
                plumes.hysplit_deposition_grid = JSON.parse(JSON.stringify(plumes.deposition_grid));
            }}
        }});

        // Leaflet Map Initialization
        // zoomAnimation:false — the animated zoom was leaving SVG vector layers (deposition contours,
        // air-monitor circles) mid-transform after a zoom (off-center until a pan re-computed them).
        // Markers reposition individually so they were fine. Instant zoom keeps every layer aligned.
        const map = L.map('map', {{
            zoomControl: false,
            maxZoom: 16,
            minZoom: 7,
            zoomAnimation: false
        }}).setView([{MAP_CENTER[0]}, {MAP_CENTER[1]}], {MAP_ZOOM_LEVEL});
        
        // CartoDB Voyager tile layer (detailed streets, rivers, labels — readable under footprints)
        L.tileLayer('https://{{s}}.basemaps.cartocdn.com/rastertiles/voyager/{{z}}/{{x}}/{{y}}{{r}}.png', {{
            attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>',
            subdomains: 'abcd',
            maxZoom: 20
        }}).addTo(map);
        
        // Custom control layout placement
        L.control.zoom({{
            position: 'bottomright'
        }}).addTo(map);

        // Stop propagation of mouse wheel and clicks on HUD overlays to prevent map zoom/drag
        ['hud-header-panel', 'hud-legend-panel'].forEach(id => {{
            const el = document.getElementById(id);
            if (el) {{
                L.DomEvent.disableScrollPropagation(el);
                L.DomEvent.disableClickPropagation(el);
            }}
        }});
        const ctrlEl = document.querySelector('.hud-controls');
        if (ctrlEl) {{
            L.DomEvent.disableScrollPropagation(ctrlEl);
            L.DomEvent.disableClickPropagation(ctrlEl);
        }}

        // Stop propagation of mousedown and touchstart inside Leaflet popups
        // to prevent Leaflet from intercepting drag events and disabling selection.
        document.addEventListener('mousedown', function(e) {{
            if (e.target.closest('.leaflet-popup')) {{
                e.stopPropagation();
            }}
        }}, true);
        document.addEventListener('touchstart', function(e) {{
            if (e.target.closest('.leaflet-popup')) {{
                e.stopPropagation();
            }}
        }}, true);

        // --- EPA MONITORING LAYERS ---
        const activeMonitorLayer = L.layerGroup().addTo(map);

        // ── Deposition / Ground-Level Air footprint layers ──
        // Two custom panes BELOW the particle canvas (overlayPane=400) so particles float on top,
        // but ABOVE the basemap tiles (tilePane=200) so the map shows through. Each layer gets its
        // OWN pane and the master transparency is applied to the WHOLE pane (CSS opacity) — a pane
        // composites as one group, so stacked chemicals/bands no longer COMPOUND into opacity.
        map.createPane('airPane');
        map.getPane('airPane').style.zIndex = 245;
        map.getPane('airPane').style.pointerEvents = 'none';
        map.createPane('depPane');
        map.getPane('depPane').style.zIndex = 250;
        map.getPane('depPane').style.pointerEvents = 'none';
        const depositionLayer    = L.layerGroup().addTo(map);
        const airConcentrationLayer = L.layerGroup().addTo(map);

        // Derived from the engine's DEFAULT_ACTIVE_CHEMICALS so the filter list always matches the
        // modeled set (adding a chemical there auto-adds its checkbox — no JS edit needed).
        const DEP_CHEM_NAMES = {dep_chem_names_json};
        const DEP_CHEM_LABELS = {dep_chem_labels_json};
        // band 1 = HIGHEST concentration (smallest, near source) → band N = lowest (largest, outer).
        // Ramps go intense → faint so the core reads strong and the edge fades. Saturated for the
        // light Voyager basemap.
        const DEP_COLORS = ["#800026","#bd0026","#f03b20","#fd8d3c","#feb24c"]; // deep red → amber (soil)
        const AIR_COLORS = ["#084594","#2171b5","#4292c6","#6baed6","#9ecae1"]; // deep → light blue (air)
        // Show only contour bands within ~1.5 decades of each footprint's PEAK concentration. This
        // keys on the absolute value (band_values), not the band number, so it's robust to concplot's
        // per-field auto-scaled levels (e.g. combined ammonia got 2-decade steps). The faint far
        // trails (>1.5 decades below peak) are what clipped into the grid "square" — hiding them keeps
        // the footprint inside the grid and shows only meaningful deposition.
        const VISIBLE_DECADE_RATIO = 32;  // keep bands with value >= peakValue / 32
        // SOIL DEPOSITION uses the SAME 32 threshold. (A looser 100 was tried to push the footprint
        // toward the clinics, but per-chemical band structure varies — e.g. tetrachloroethylene's
        // 2-decade band reaches ~232 km, past the ~220 km grid half-span → the "square" clip returns.
        // Instead we pick simulation days whose HIGH-concentration deposition genuinely blows over the
        // clinics, and the clinic popups report the true all-band value at each location.)
        const DEP_VISIBLE_DECADE_RATIO = 32;

        let depManifest = null;
        let depGeoJsonCache = {{}};
        let depActiveChem = new Set(DEP_CHEM_NAMES);
        let footprintOpacity = 0.45;   // master pane transparency (tunable via sandbox slider)

        (function() {{
            const list = document.getElementById('dep-chem-list');
            DEP_CHEM_NAMES.forEach(chem => {{
                const lbl = document.createElement('label');
                lbl.className = 'dep-chem-pill';
                lbl.innerHTML = `<input type="checkbox" class="dep-chem-chk" data-chem="${{chem}}" checked> ${{DEP_CHEM_LABELS[chem]}}`;
                list.appendChild(lbl);
            }});
        }})();

        document.querySelectorAll('.dep-chem-chk').forEach(chk => {{
            chk.addEventListener('change', () => {{
                const chem = chk.dataset.chem;
                const isChecked = chk.checked;
                
                // Update global active set
                depActiveChem = new Set([...document.querySelectorAll('.dep-chem-chk:checked')].map(c => c.dataset.chem));
                
                // Update all facilities' chemical active state for this chemical
                PLUME_DATA.facilities.forEach(fac => {{
                    if (activeChemicals[fac.id] && activeChemicals[fac.id][chem] !== undefined) {{
                        activeChemicals[fac.id][chem] = isChecked;
                        // Update checkbox in UI
                        const facChk = document.querySelector(`.chem-chk[data-fac="${{fac.id}}"][data-chem="${{chem}}"]`);
                        if (facChk) {{
                            facChk.checked = isChecked;
                        }}
                        // Filter out existing particles of this chemical from map immediately
                        if (!isChecked) {{
                            particles = particles.filter(p => p.fac !== fac.id || p.chem !== chem);
                        }}
                        // Recalculate facility totals
                        let active_total = 0;
                        fac.chemicals.forEach(c => {{
                            if (activeChemicals[fac.id][c.chemical]) {{
                                active_total += c.total_lbs || 0;
                            }}
                        }});
                        const totalLbsLabel = document.getElementById('total-lbs-' + fac.id);
                        if (totalLbsLabel) {{
                            totalLbsLabel.textContent = active_total === 0 ? '0.0 lbs' : active_total.toLocaleString(undefined, {{maximumFractionDigits: 1}}) + ' lbs/yr';
                        }}
                        updateFacilityPopup(fac.id);
                    }}
                }});
                
                refreshDepLayers();
                drawParticles();
            }});
        }});
        document.getElementById('dep-layer-toggle').addEventListener('change', refreshDepLayers);
        document.getElementById('air-layer-toggle').addEventListener('change', refreshDepLayers);
        // Particle Simulation general on/off (mirrors the dep/air layer toggles).
        {{
            const _partTog = document.getElementById('particles-toggle');
            if (_partTog) {{
                showParticles = _partTog.checked;
                _partTog.addEventListener('change', (e) => {{ showParticles = e.target.checked; drawParticles(); }});
            }}
        }}

        // ── Custom info tooltips ──
        // Reparent each .info-pop to <body> so the panel's overflow:hidden (collapse animation)
        // can't clip it, then position it as a fixed, viewport-clamped popup on hover. (The native
        // title= attribute we replaced had a ~3-4s browser delay; this shows instantly.)
        document.querySelectorAll('.dep-info-btn').forEach((btn) => {{
            const pop = btn.querySelector('.info-pop');
            if (!pop) return;
            document.body.appendChild(pop);  // escape ancestor overflow clipping
            const place = () => {{
                pop.style.display = 'block';
                const r = btn.getBoundingClientRect();
                const pw = pop.offsetWidth, ph = pop.offsetHeight;
                let left = r.left;
                let top = r.bottom + 6;
                if (left + pw > window.innerWidth - 8) left = window.innerWidth - pw - 8;
                if (left < 8) left = 8;
                if (top + ph > window.innerHeight - 8) top = r.top - ph - 6;  // flip above if no room
                if (top < 8) top = 8;
                pop.style.left = left + 'px';
                pop.style.top = top + 'px';
            }};
            btn.addEventListener('mouseenter', place);
            btn.addEventListener('mouseleave', () => {{ pop.style.display = 'none'; }});
        }});

        // ── Footprint gating lookup: (facName|chem|srcType) → file key ──
        // Built once when the deposition manifest loads. Used by airBandAtPoint() to
        // gate particle lifetime/opacity against the HYSPLIT air-concentration contours.
        let airFootprintLookup = {{}};

        function loadDepManifest(dateStr) {{
            // Data is embedded inline (depositionArchive) — no fetch (file:// blocks it).
            const entry = (typeof depositionArchive !== 'undefined') ? depositionArchive[dateStr] : null;
            depManifest = entry ? entry.manifest : null;
            depGeoJsonCache = entry ? entry.files : {{}};

            // Build footprint lookup from per-facility entries
            airFootprintLookup = {{}};
            if (depManifest) {{
                // Per-facility entries (tagged with fac_name, chem, source_type)
                (depManifest.entries || []).forEach(e => {{
                    const key = (e.fac_name || '') + '|' + (e.chem || '') + '|' + (e.source_type || '');
                    airFootprintLookup[key] = e.file;
                }});
                // Combined entries (keyed as "combined|chem|srcType")
                (depManifest.combined_entries || []).forEach(e => {{
                    const st = e.source_type || '';
                    const key = 'combined|' + (e.chem || '') + '|' + st;
                    airFootprintLookup[key] = e.file;
                }});
            }}

            refreshDepLayers();
        }}

        function loadAndRefreshDepLayers() {{ refreshDepLayers(); }}

        // ── Footprint gating: test if a lat/lon is inside a HYSPLIT air contour ──
        // Returns the lowest band number containing the point (highest concentration),
        // or null if outside all bands. Used to gate particle lifetime and opacity.
        function airBandAtPoint(facName, chem, srcType, lat, lon) {{
            // Determine which footprint file to query
            let fileKey = airFootprintLookup[facName + '|' + chem + '|' + srcType];
            // Fallback: try combined entry (for display mode 'combined')
            if (!fileKey) fileKey = airFootprintLookup['combined|' + chem + '|'];
            // Fallback: try combined with source type
            if (!fileKey) fileKey = airFootprintLookup['combined|' + chem + '|' + srcType];
            if (!fileKey) return null;

            const fc = depGeoJsonCache[fileKey];
            if (!fc || !fc.features) return null;

            const md = fc.metadata || {{}};
            const N = md.num_frames || 1;
            const S = (md.start_hour != null) ? md.start_hour : 2;
            const currentFrame = Math.max(0, Math.min(N - 1, Math.floor(playbackTime - S)));

            // Filter features for air layer at current frame
            let bestBand = null;
            for (let i = 0; i < fc.features.length; i++) {{
                const f = fc.features[i];
                const props = f.properties;
                if (props.layer !== 'air' || props.hour_frame !== currentFrame) continue;
                const ring = f.geometry.coordinates[0];
                if (ring && depPointInRing(lat, lon, ring)) {{
                    const band = props.band || 99;
                    if (bestBand === null || band < bestBand) bestBand = band;
                }}
            }}
            return bestBand;
        }}

        // Map contour band number to brightness/opacity target.
        // Band 1 (near source, highest conc) → ~1.0; Band N (edge) → ~0.15
        function bandToBrightness(band, numBands) {{
            if (numBands <= 1) return 1.0;
            return 1.0 - 0.85 * ((band - 1) / (numBands - 1));
        }}

        // Animate the real hourly frames keyed to the timeline. Each file carries
        // metadata.num_frames (N) and start_hour (S): frame k = sim hour (k+S).
        // Cross-fade between consecutive hourly frames (per-polygon) for smoothness; the master
        // transparency + the 0→2h fade-in are applied at the PANE level so nothing compounds.
        // Hit-test index of currently-shown footprint polygons (rebuilt each refresh) for hover readout
        let depHitIndex = [];
        // 2b: per-facility hit-test index (not drawn, used for hover attribution %)
        let perFacHitIndex = [];

        function refreshDepLayers() {{
            const displayMode = document.getElementById('display-mode-select').value;
            depositionLayer.clearLayers();
            airConcentrationLayer.clearLayers();
            depHitIndex = [];
            perFacHitIndex = [];
            if (!depManifest) return;
            const showDep = document.getElementById('dep-layer-toggle').checked;
            const showAir = document.getElementById('air-layer-toggle').checked;

            const hour = (typeof playbackTime === 'number')
                ? playbackTime
                : (parseFloat(document.getElementById('time-slider').value) || 0);

            // Master pane transparency × soft fade-in over the first 2 hours
            const globalIntensity = Math.max(0, Math.min(1, hour / 2));
            const paneOpacity = footprintOpacity * globalIntensity;
            map.getPane('depPane').style.opacity = (showDep ? paneOpacity : 0);
            map.getPane('airPane').style.opacity = (showAir ? paneOpacity : 0);
            if ((!showDep && !showAir) || hour <= 0) return;

            // Draw combined contours based on displayMode
            let activeCombinedEntries = (depManifest.combined_entries || []).filter(entry => {{
                if (displayMode === 'combined') {{
                    return entry.source_type === undefined || entry.source_type === null;
                }} else {{
                    return entry.source_type === displayMode;
                }}
            }});

            activeCombinedEntries.forEach(entry => {{
                if (!depActiveChem.has(entry.chem)) return;
                const fc = depGeoJsonCache[entry.file];
                if (!fc) return;
                const md = fc.metadata || {{}};
                const N = md.num_frames || 1;
                const S = (md.start_hour != null) ? md.start_hour : 2;

                const fp  = Math.max(0, Math.min(N - 1, hour - S));         // frame position
                const fLow = Math.floor(fp);
                const fHigh = Math.min(N - 1, fLow + 1);
                const frac = fp - fLow;

                const renderLayer = (layerName, layerGroup, paneName, colors, baseAlpha) => {{
                    // Keep only bands within ~1.5 decades of the peak concentration (value-based, not
                    // band number) — hides the faint far trails that clip the grid into a "square".
                    const bandVals = (md.band_values || {{}})[layerName] || {{}};
                    let peakVal = 0;
                    for (const b in bandVals) if (bandVals[b] > peakVal) peakVal = bandVals[b];
                    const visFloor = peakVal / (layerName === 'dep' ? DEP_VISIBLE_DECADE_RATIO : VISIBLE_DECADE_RATIO);
                    const draw = (frameIdx, factor) => {{
                        if (factor <= 0.002) return;
                        const feats = fc.features.filter(f =>
                            f.properties.layer === layerName && f.properties.hour_frame === frameIdx
                            && bandVals[f.properties.band] >= visFloor);
                        if (!feats.length) return;
                        L.geoJSON({{type:'FeatureCollection', features:feats}}, {{
                            pane: paneName,
                            interactive: false,
                            style: f => ({{
                                fillColor: colors[Math.min((f.properties.band||1)-1, colors.length-1)],
                                fillOpacity: baseAlpha * factor,   // cross-fade only; master is pane-level
                                stroke: false, weight: 0
                            }})
                        }}).addTo(layerGroup);
                        if (frameIdx === fLow) {{
                            for (const f of feats) depHitIndex.push({{
                                chem: entry.chem, fac: md.fac_name, layer: layerName,
                                band: f.properties.band, value: bandVals[f.properties.band],
                                ring: f.geometry.coordinates[0]
                            }});
                        }}
                    }};
                    draw(fLow, 1 - frac);
                    if (fHigh !== fLow) draw(fHigh, frac);
                }};

                if (showDep && entry.layers.includes('dep')) renderLayer('dep', depositionLayer, 'depPane', DEP_COLORS, 0.6);
                if (showAir && entry.layers.includes('air')) renderLayer('air', airConcentrationLayer, 'airPane', AIR_COLORS, 0.5);
            }});

            // 2b: build per-facility hit-test index for hover attribution %
            // (uses the per-facility entries that are embedded but NOT drawn)
            const activePerFacEntries = (depManifest.entries || []).filter(entry => {{
                if (displayMode === 'combined') {{
                    return true; 
                }} else {{
                    return entry.source_type === displayMode;
                }}
            }});

            activePerFacEntries.forEach(entry => {{
                if (!depActiveChem.has(entry.chem)) return;
                if (activeFacilities[entry.fac_id] === false) return;
                if (activeChemicals[entry.fac_id] && activeChemicals[entry.fac_id][entry.chem] === false) return;
                const fc = depGeoJsonCache[entry.file];
                if (!fc) return;
                const md = fc.metadata || {{}};
                const N = md.num_frames || 1;
                const S = (md.start_hour != null) ? md.start_hour : 2;
                const fp = Math.max(0, Math.min(N - 1, hour - S));
                const fLow = Math.floor(fp);
                for (const layerName of ['dep', 'air']) {{
                    if (layerName === 'dep' && !showDep) continue;
                    if (layerName === 'air' && !showAir) continue;
                    const bandVals = (md.band_values || {{}})[layerName] || {{}};
                    let peakVal = 0;
                    for (const b in bandVals) if (bandVals[b] > peakVal) peakVal = bandVals[b];
                    const visFloor = peakVal / (layerName === 'dep' ? DEP_VISIBLE_DECADE_RATIO : VISIBLE_DECADE_RATIO);
                    const feats = fc.features.filter(f =>
                        f.properties.layer === layerName && f.properties.hour_frame === fLow
                        && bandVals[f.properties.band] >= visFloor);
                    for (const f of feats) perFacHitIndex.push({{
                        chem: entry.chem, fac: md.fac_name, layer: layerName,
                        band: f.properties.band, value: bandVals[f.properties.band],
                        ring: f.geometry.coordinates[0]
                    }});
                }}
            }});
        }}

        // Throttled animation tick (called from the main playback loop)
        let _lastDepHour = -999;
        let _lastDepMs = 0;
        function maybeAnimateDep() {{
            const hour = (typeof playbackTime === 'number') ? playbackTime : 0;
            // refreshDepLayers() rebuilds hundreds of footprint SVG polygons — expensive. Throttle it
            // to a real-time floor (~150ms = ~6/sec) AND a sim-hour step, so the cross-fade stays
            // smooth without churning the DOM 12×/sec. Big DOM/paint/heat saving.
            const now = (typeof performance !== 'undefined') ? performance.now() : Date.now();
            if (Math.abs(hour - _lastDepHour) >= 0.08 && (now - _lastDepMs) >= 150) {{
                _lastDepHour = hour;
                _lastDepMs = now;
                refreshDepLayers();
            }}
        }}

        // ── Hover concentration readout ──
        // On mouse move, point-in-polygon test the cursor against the currently-shown footprints;
        // the lowest band number containing the point = highest contour level there ("≥ value").
        function depPointInRing(lat, lng, ring) {{
            let inside = false;
            for (let i = 0, j = ring.length - 1; i < ring.length; j = i++) {{
                const xi = ring[i][0], yi = ring[i][1], xj = ring[j][0], yj = ring[j][1];
                if (((yi > lat) !== (yj > lat)) && (lng < (xj - xi) * (lat - yi) / (yj - yi) + xi))
                    inside = !inside;
            }}
            return inside;
        }}
        function fmtConc(v, unit) {{
            // Contour bands are decades; the true value sits between this level and the next (×10).
            // Show that range so it's clear these are binned, not a single round "filler" number.
            const f = x => x >= 1 ? x.toPrecision(3) : (x >= 0.001 ? x.toPrecision(2) : x.toExponential(1));
            return f(v * 1e6) + '–' + f(v * 1e7) + ' µg/' + unit;
        }}
        const depReadoutEl = document.getElementById('dep-readout');
        let _depHoverT = 0;
        map.on('mousemove', (e) => {{
            const now = performance.now();
            if (now - _depHoverT < 45) return;
            _depHoverT = now;
            if (!depHitIndex.length && !perFacHitIndex.length) {{ depReadoutEl.style.display = 'none'; return; }}
            const lat = e.latlng.lat, lng = e.latlng.lng;

            // 2b: combined value from depHitIndex (drawn combined footprints)
            // chem -> {{dep: value, air: value}} — the true merged concentration
            const combAgg = {{}};
            for (const h of depHitIndex) {{
                if (h.value == null) continue;
                if (!depPointInRing(lat, lng, h.ring)) continue;
                const a = combAgg[h.chem] || (combAgg[h.chem] = {{ dep: null, air: null }});
                if (a[h.layer] == null || h.value > a[h.layer]) a[h.layer] = h.value;
            }}

            // 2b: per-facility attribution from perFacHitIndex (not drawn)
            // chem -> {{dep: {{fac: value}}, air: {{fac: value}}}}
            const facAgg = {{}};
            for (const h of perFacHitIndex) {{
                if (h.value == null) continue;
                if (!depPointInRing(lat, lng, h.ring)) continue;
                const a = facAgg[h.chem] || (facAgg[h.chem] = {{ dep: {{}}, air: {{}} }});
                const lm = a[h.layer];
                if (lm[h.fac] == null || h.value > lm[h.fac]) lm[h.fac] = h.value;
            }}

            const chems = Object.keys(combAgg).sort();
            if (!chems.length) {{ depReadoutEl.style.display = 'none'; return; }}
            let html = '<div class="dr-title">AT CURSOR &nbsp;' + lat.toFixed(3) + ', ' + lng.toFixed(3) + '</div>';
            for (const c of chems) {{
                html += '<div class="dr-chem">' + (DEP_CHEM_LABELS[c] || c) + '</div>';
                for (const ld of [['dep', 'soil', 'm²'], ['air', 'air', 'm³']]) {{
                    const combVal = combAgg[c][ld[0]];
                    if (combVal == null) continue;
                    html += '<div class="dr-row"><span>' + ld[1] + '</span><span>' + fmtConc(combVal, ld[2]) + '</span></div>';
                    // Per-facility attribution breakdown
                    const facs = (facAgg[c] || {{ dep: {{}}, air: {{}} }})[ld[0]];
                    const names = Object.keys(facs);
                    if (names.length > 1) {{
                        let total = 0; for (const n of names) total += facs[n];
                        names.sort((a, b) => facs[b] - facs[a]);
                        for (const n of names) {{
                            const pct = Math.round(100 * facs[n] / total);
                            html += '<div class="dr-row" style="font-size:10px;opacity:.65;padding-left:10px"><span>' + n + '</span><span>' + pct + '%</span></div>';
                        }}
                    }}
                }}
            }}
            depReadoutEl.innerHTML = html;
            depReadoutEl.style.display = 'block';
            const cp = e.containerPoint;
            const vp = document.getElementById('map-viewport').getBoundingClientRect();
            let x = cp.x + 16, y = cp.y + 16;
            if (x + 270 > vp.width) x = cp.x - 270;
            depReadoutEl.style.left = x + 'px';
            depReadoutEl.style.top = y + 'px';
        }});
        map.on('mouseout', () => {{ depReadoutEl.style.display = 'none'; }});

        const monitorMarkers = [];

        // Populate monitor markers for all unique stations across all dates
        const uniqueStations = {{}};
        Object.keys(historicalSimulationArchive).forEach(dateStr => {{
            const dayMonitors = historicalSimulationArchive[dateStr].monitors;
            Object.keys(dayMonitors).forEach(pollutant => {{
                const pData = dayMonitors[pollutant];
                const stations = pData.stations || {{}};
                
                Object.keys(stations).forEach(stationId => {{
                    const station = stations[stationId];
                    const key = pollutant + "_" + stationId;
                    if (!uniqueStations[key]) {{
                        uniqueStations[key] = {{
                            pollutant: pollutant,
                            stationId: stationId,
                            lat: station.lat,
                            lon: station.lon,
                            unit: pData.unit
                        }};
                    }}
                }});
            }});
        }});

        // Build leaflet markers from the unique stations list
        Object.keys(uniqueStations).forEach(key => {{
            const info = uniqueStations[key];
            const marker = L.circleMarker([info.lat, info.lon], {{
                radius: 8,
                fillColor: '#808080',
                color: '#ffffff',
                weight: 2,
                opacity: 0.9,
                fillOpacity: 0.8
            }});

            marker.bindPopup('', {{
                className: 'custom-leaflet-popup'
            }});

            monitorMarkers.push({{
                marker: marker,
                pollutant: info.pollutant,
                stationId: info.stationId,
                unit: info.unit
            }});
        }});

        // Populate pollutant select dropdown
        const pollutantSelect = document.getElementById('pollutant-select');
        Object.keys(regionalMonitorData).forEach(pollutant => {{
            const opt = document.createElement('option');
            opt.value = pollutant;
            opt.textContent = pollutant;
            pollutantSelect.appendChild(opt);
        }});

        // Configure Date Picker
        const datePicker = document.getElementById('date-picker');
        // Populate the dropdown from whatever dates are embedded (one <option> per available day),
        // so switching between simulation days works regardless of how many are bundled.
        (function initDatePicker() {{
            const entries = (typeof PLUME_MANIFEST !== 'undefined' && PLUME_MANIFEST.dates) ? PLUME_MANIFEST.dates.slice() : [];
            // Newest date at the TOP of the dropdown (descending). ISO YYYY-MM-DD sorts lexically =
            // chronologically, so this puts the most recent day first; the older pinned showcase days
            // (still labeled) fall to the bottom. Native <select> scrolls automatically once the list
            // grows (e.g. the full 30-day rolling window + pinned).
            entries.sort((a, b) => (a.date < b.date ? 1 : (a.date > b.date ? -1 : 0)));
            datePicker.innerHTML = '';
            entries.forEach(entry => {{
                const d = entry.date;
                const opt = document.createElement('option');
                opt.value = d;
                const dt = new Date(d + 'T00:00:00');
                let txt = dt.toLocaleDateString('en-US', {{ month: 'short', day: 'numeric', year: 'numeric' }});
                if (entry.label) txt += ' — ' + entry.label;   // pinned curated days show their label
                opt.textContent = txt;
                datePicker.appendChild(opt);
            }});
            datePicker.value = activeDate;
        }})();

        function syncActiveMonitorLayer(selectedPollutant) {{
            activeMonitorLayer.clearLayers();
            monitorMarkers.forEach(m => {{
                if (m.pollutant === selectedPollutant) {{
                    m.marker.addTo(activeMonitorLayer);
                }}
            }});
        }}

        // Initialize with default pollutant
        const defaultPollutant = regionalMonitorData['VOCs'] ? 'VOCs' : (Object.keys(regionalMonitorData)[0] || 'PM2.5');
        pollutantSelect.value = defaultPollutant;
        syncActiveMonitorLayer(defaultPollutant);

        pollutantSelect.addEventListener('change', (e) => {{
            const selected = e.target.value;
            syncActiveMonitorLayer(selected);
            let currentHourInt = Math.floor(playbackTime);
            if (currentHourInt < 0) currentHourInt = 0;
            if (currentHourInt > 23) currentHourInt = 23;
            updateMonitorPopups(currentHourInt);
        }});

        // Date Picker Change Event Listener — fetch the day's bundle on demand, then hot-swap.
        datePicker.addEventListener('change', async (e) => {{
            const selectedDate = e.target.value;
            try {{ await pd_fetchDate(selectedDate); }}
            catch (err) {{
                alert('Could not load ' + selectedDate + ' (' + err.message + '). It may have aged out; try refreshing.');
                datePicker.value = activeDate;   // revert selection
                return;
            }}
            const activeDayData = historicalSimulationArchive[selectedDate];
            if (!activeDayData) return;

            // Pause playback
            isPlaying = false;
            document.getElementById('play-icon').style.display = 'block';
            document.getElementById('pause-icon').style.display = 'none';

            // Hot-swap data layers
            activeDate = selectedDate;
            PLUME_DATA = activeDayData.plumes;
            regionalMonitorData = activeDayData.monitors;

            // Reset simulation timeline
            playbackTime = 0.0;
            prevPlaybackTime = 0.0;
            particles = [];
            nextSandboxId = 0;
            lastSpawnTime = -999;

            // Update UI components
            updateHUD();
            PLUME_DATA.facilities.forEach(fac => {{
                updateFacilityPopup(fac.id);
            }});
            updateDepositionSourceSelect();
            recalculateDeposition();
            drawParticles();
            loadDepManifest(selectedDate);
        }});

        function getMonitorColorAndStatus(val, thresholds) {{
            if (val === null || val === undefined) {{
                return {{ color: '#808080', status: 'No Data' }};
            }}
            if (val <= thresholds.good) {{
                return {{ color: '#10B981', status: 'Good' }};
            }} else if (val <= thresholds.mod) {{
                return {{ color: '#F59E0B', status: 'Moderate' }};
            }} else if (val <= thresholds.unhealthy) {{
                return {{ color: '#EF4444', status: 'Unhealthy' }};
            }} else {{
                return {{ color: '#8B5CF6', status: 'Very Unhealthy' }};
            }}
        }}

        // If the nearest available sample is more than this many days from the shown date, the
        // monitor is drawn grayed-out (not colored by AQI) so it never looks like current measured
        // data. Recent days legitimately have no published AQS/VOC data yet (months of lag).
        const STALE_MONITOR_DAYS = 14;

        function updateMonitorPopups(currentHourInt) {{
            const selected = document.getElementById('pollutant-select').value;
            monitorMarkers.forEach(m => {{
                if (m.pollutant !== selected) return;

                const thresholds = {{
                    good: regionalMonitorData[m.pollutant].good,
                    mod: regionalMonitorData[m.pollutant].mod,
                    unhealthy: regionalMonitorData[m.pollutant].unhealthy
                }};
                
                const station = regionalMonitorData[m.pollutant].stations[m.stationId];
                if (!station) {{
                    m.marker.setStyle({{
                        fillColor: '#808080'
                    }});
                    m.marker.setPopupContent('<div style="font-family:Inter,sans-serif;font-size:11px;color:#fff;padding:6px;">No data for this station on this day.</div>');
                    return;
                }}

                const val = station.hourly_data[currentHourInt];
                const {{ color, status }} = getMonitorColorAndStatus(val, thresholds);
                const isStale = station.is_interpolated && station.days_diff > STALE_MONITOR_DAYS;

                if (isStale) {{
                    // Data is a far-off nearest sample (e.g. recent dates before AQS/VOC publishes):
                    // gray + dim + dashed so it reads as "location only, not current data".
                    m.marker.setStyle({{
                        fillColor: '#6b7280', color: '#9ca3af', fillOpacity: 0.3,
                        opacity: 0.55, weight: 1, dashArray: '2,3'
                    }});
                }} else {{
                    m.marker.setStyle({{
                        fillColor: color, color: '#ffffff', fillOpacity: 0.8,
                        opacity: 0.9, weight: 2, dashArray: null
                    }});
                }}

                const valStr = (val !== null && val !== undefined) ? (val.toFixed(2) + ' ' + m.unit) : 'No Data';

                let sampleDateRow = '';
                let measuredVocHeader = 'Measured VOC Compounds (' + m.unit + '):';
                if (station.sample_date) {{
                    const statusText = station.is_interpolated ? ` (${{station.days_diff}}d nearest)` : ' (Actual)';
                    const colorStyle = station.is_interpolated ? 'color: #F59E0B;' : 'color: #10B981;';
                    sampleDateRow = 
                        '<tr style="border-bottom: 1px solid rgba(255,255,255,0.05);">' +
                            '<td style="padding: 4px 0; color: #9ca3af;">Sample Date:</td>' +
                            '<td style="padding: 4px 0; font-weight: 600; text-align: right; ' + colorStyle + '">' + station.sample_date + statusText + '</td>' +
                        '</tr>';
                    
                    if (station.is_interpolated) {{
                        measuredVocHeader = 'Measured VOC Compounds (' + m.unit + ' - Sampled ' + station.sample_date + '):';
                    }}
                }}

                const popupContent = 
                    '<div style="font-family: Inter, sans-serif; font-size: 12px; color: #f3f4f6; width: 260px; background: #121214; padding: 10px; border-radius: 8px; border: 1px solid rgba(255,255,255,0.1);">' +
                        '<strong style="color: #a5b4fc; font-size: 14px; font-family: Outfit, sans-serif;">EPA Ambient Monitor</strong>' +
                        '<div style="height: 1px; background: rgba(255,255,255,0.08); margin: 8px 0;"></div>' +
                        '<table style="width: 100%; border-collapse: collapse; font-size: 11px; color: #d1d5db;">' +
                            '<tr style="border-bottom: 1px solid rgba(255,255,255,0.05);">' +
                                '<td style="padding: 4px 0; color: #9ca3af;">Station ID:</td>' +
                                '<td style="padding: 4px 0; font-weight: 600; text-align: right; color: #fff;">' + m.stationId + '</td>' +
                            '</tr>' +
                            '<tr style="border-bottom: 1px solid rgba(255,255,255,0.05);">' +
                                '<td style="padding: 4px 0; color: #9ca3af;">County:</td>' +
                                '<td style="padding: 4px 0; font-weight: 600; text-align: right; color: #fff;">' + station.county + '</td>' +
                            '</tr>' +
                            '<tr style="border-bottom: 1px solid rgba(255,255,255,0.05);">' +
                                '<td style="padding: 4px 0; color: #9ca3af;">Coordinates:</td>' +
                                '<td style="padding: 4px 0; font-weight: 600; text-align: right; color: #fff;">' + station.lat.toFixed(4) + ', ' + station.lon.toFixed(4) + '</td>' +
                            '</tr>' +
                            '<tr style="border-bottom: 1px solid rgba(255,255,255,0.05);">' +
                                '<td style="padding: 4px 0; color: #9ca3af;">Parameter:</td>' +
                                '<td style="padding: 4px 0; font-weight: 600; text-align: right; color: #fff; max-width: 150px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;" title="' + station.parameter_name + '">' + station.parameter_name + '</td>' +
                            '</tr>' +
                            sampleDateRow +
                            '<tr style="border-bottom: 1px solid rgba(255,255,255,0.05);">' +
                                '<td style="padding: 4px 0; color: #9ca3af;">Active Hour:</td>' +
                                '<td style="padding: 4px 0; font-weight: 600; text-align: right; color: #fff;">' + String(currentHourInt).padStart(2, '0') + ':00</td>' +
                            '</tr>' +
                            '<tr style="border-bottom: 1px solid rgba(255,255,255,0.05);">' +
                                '<td style="padding: 4px 0; color: #9ca3af;">Value:</td>' +
                                '<td style="padding: 4px 0; font-weight: 600; text-align: right; color: #fff;">' + valStr + '</td>' +
                            '</tr>' +
                            '<tr' + (station.voc_details ? ' style="border-bottom: 1px solid rgba(255,255,255,0.05);"' : '') + '>' +
                                '<td style="padding: 4px 0; color: #9ca3af;">Classification:</td>' +
                                '<td style="padding: 4px 0; font-weight: 700; text-align: right; color: ' + color + ';">' + status + '</td>' +
                            '</tr>' +
                        '</table>' +
                        (station.voc_details ? 
                            ('<div style="margin-top: 8px; border-top: 1px dashed rgba(255,255,255,0.15); padding-top: 8px;">' +
                                '<strong style="color: #a5b4fc; font-size: 11px; display: block; margin-bottom: 6px;">' + measuredVocHeader + '</strong>' +
                                '<div style="max-height: 120px; overflow-y: auto; font-size: 10px; padding-right: 4px;">' +
                                Object.keys(station.voc_details).map(compound => {{
                                    const cVal = station.voc_details[compound];
                                    const cValStr = cVal !== null ? cVal.toFixed(3) : 'N/A';
                                    return '<div style="display: flex; justify-content: space-between; margin-bottom: 3px; border-bottom: 1px solid rgba(255,255,255,0.02); padding-bottom: 1px;">' +
                                               '<span style="color: #9ca3af; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; max-width: 170px;" title="' + compound + '">' + compound + ':</span>' +
                                               '<span style="font-weight: 600; color: #fff;">' + cValStr + '</span>' +
                                           '</div>';
                                }}).join('') +
                                '</div>' +
                            '</div>') : '') +
                    '</div>';

                m.marker.setPopupContent(popupContent);

                if (m.marker.isPopupOpen()) {{
                    m.marker.getPopup().setContent(popupContent);
                }}
            }});
        }}

        // State variables
        let isPlaying = true;
        let playbackTime = 0.0; // simulation hour index (0.0 to 24.0)
        let activeFacilities = new Array(PLUME_DATA.facilities.length).fill(true); // boolean array for toggles
        let activeChemicals = {{}}; // nested object for chemical checkbox toggles
        
        // Canvas Setup
        const canvas = document.getElementById('particle-canvas');
        const ctx = canvas.getContext('2d');
        
        // Canvas lives in overlayPane so Leaflet manages its stacking (above depPane/airPane,
        // below markerPane/popupPane).
        map.getPanes().overlayPane.appendChild(canvas);
        canvas.style.position = 'absolute';
        canvas.style.left = '0';
        canvas.style.top = '0';

        // Position the canvas the SAME way Leaflet positions its own layers: via a translate3d
        // transform (L.DomUtil.setPosition), NOT via left/top. The overlayPane is moved by a GPU
        // transform; if we moved the canvas with left/top instead, the two would composite on
        // different timelines during zoom/pan and the particles would drift off the map (and stay
        // offset until the next repaint). Using a transform keeps the canvas locked to the pane on
        // the compositor. Canvas top-left is pinned to container [0,0], so a container point maps
        // directly to a canvas pixel in drawParticles().
        function resizeCanvas() {{
            const size = map.getSize();
            if (canvas.width !== size.x) canvas.width = size.x;
            if (canvas.height !== size.y) canvas.height = size.y;
            L.DomUtil.setPosition(canvas, map.containerPointToLayerPoint([0, 0]));
        }}
        resizeCanvas();
        
        // Helper formatting functions
        function formatSimulationTime(decHours) {{
            // The simulation runs on UTC hours. Display them in Calvert City's LOCAL time
            // (America/Chicago = Central, DST-aware: CDT in summer, CST in winter) so residents
            // read the plume's timing in their own clock, not UTC.
            const totalMinutes = Math.floor(decHours * 60);
            const h = Math.floor(totalMinutes / 60);
            const m = totalMinutes % 60;
            const base = (typeof activeDate === 'string' && activeDate) ? activeDate : '2000-01-01';
            const dt = new Date(base + 'T00:00:00Z');
            dt.setUTCHours(h, m, 0, 0);
            try {{
                const parts = new Intl.DateTimeFormat('en-US', {{
                    timeZone: 'America/Chicago', month: 'short', day: 'numeric',
                    hour: 'numeric', minute: '2-digit', hour12: true, timeZoneName: 'short'
                }}).formatToParts(dt);
                let hh = '', mm = '', ap = '', tz = 'CT', mon = '', day = '';
                for (const p of parts) {{
                    if (p.type === 'hour') hh = p.value;
                    else if (p.type === 'minute') mm = p.value;
                    else if (p.type === 'dayPeriod') ap = p.value.toUpperCase();
                    else if (p.type === 'timeZoneName') tz = p.value;
                    else if (p.type === 'month') mon = p.value;
                    else if (p.type === 'day') day = p.value;
                }}
                // date = the LOCAL (Central) calendar date for this frame. Because a UTC sim-day maps to
                // two Central dates, this makes the ~8 PM-prev-evening → ~6 PM start/end explicit.
                return {{ time: String(hh).padStart(2, '0') + ':' + mm, ampm: ap + ' ' + tz, date: mon + ' ' + day }};
            }} catch (e) {{
                const hours12 = h % 12 === 0 ? 12 : h % 12;
                const ampm = h >= 12 ? 'PM' : 'AM';
                return {{ time: String(hours12).padStart(2, '0') + ':' + String(m).padStart(2, '0'), ampm: ampm + ' UTC', date: '' }};
            }}
        }}
        
        function hexToRgbA(hex, opacity) {{
            if (!hex || hex.indexOf('#') !== 0) return 'rgba(255,255,255,' + opacity + ')';
            let c = hex.substring(1);
            if (c.length === 3) {{
                c = c.split('').map(x => x + x).join('');
            }}
            if (c.length === 6) {{
                const r = parseInt(c.substring(0, 2), 16);
                const g = parseInt(c.substring(2, 4), 16);
                const b = parseInt(c.substring(4, 6), 16);
                return 'rgba(' + r + ',' + g + ',' + b + ',' + opacity + ')';
            }}
            return 'rgba(255,255,255,' + opacity + ')';
        }}

        // Draw static facilities markers and setup facilityMarkers global dictionary
        const facilityMarkers = {{}};

        function updateFacilityPopup(facId) {{
            const fac = PLUME_DATA.facilities.find(f => f.id === facId);
            const marker = facilityMarkers[facId];
            if (!fac || !marker) return;
            
            let active_stack_total = 0;
            let active_fugitive_total = 0;
            let active_total = 0;
            
            let chemHtml = '';
            fac.chemicals.forEach(c => {{
                const isActive = activeChemicals[facId][c.chemical];
                const props = (PLUME_DATA.chemical_properties && PLUME_DATA.chemical_properties[c.chemical]) || {{ vd: 0, mol_wt: 0, henry_const: 0 }};
                const depInfo = `Vd: ${{props.vd.toFixed(4)}} m/s, MW: ${{props.mol_wt.toFixed(1)}} g/mol, H: ${{props.henry_const !== undefined ? props.henry_const.toExponential(1) : 'N/A'}} M/atm`;
                if (isActive) {{
                    active_stack_total += c.stack_lbs || 0;
                    active_fugitive_total += c.fugitive_lbs || 0;
                    active_total += c.total_lbs || 0;
                    
                    chemHtml += `<div style="display:flex; justify-content:space-between; gap:10px; margin-top:2px;" title="${{depInfo}}">
                        <span style="color:#9ca3af; border-bottom: 1px dotted rgba(255,255,255,0.25);">${{c.chemical}}:</span>
                        <span style="font-weight:600; color:#fff">${{c.total_lbs.toLocaleString()}} lbs/yr</span>
                    </div>`;
                }} else {{
                    chemHtml += `<div style="display:flex; justify-content:space-between; gap:10px; margin-top:2px; opacity:0.4;" title="${{depInfo}}">
                        <span style="color:#9ca3af; text-decoration: line-through;">${{c.chemical}}:</span>
                        <span style="font-weight:600; color:#9ca3af">0.0 lbs</span>
                    </div>`;
                }}
            }});
            
            const totalText = active_total === 0 ? '0.0 lbs' : active_total.toLocaleString(undefined, {{maximumFractionDigits: 1}}) + ' lbs/yr';
            const stackText = active_stack_total === 0 ? '0.0 lbs' : active_stack_total.toLocaleString(undefined, {{maximumFractionDigits: 1}}) + ' lbs/yr';
            const fugitiveText = active_fugitive_total === 0 ? '0.0 lbs' : active_fugitive_total.toLocaleString(undefined, {{maximumFractionDigits: 1}}) + ' lbs/yr';
            
            const popupContent = `
                <div style="font-family:'Inter',sans-serif; font-size:12px; color:#f3f4f6; width:240px; background:#121214; padding:6px; border-radius:8px;">
                    <strong style="color:${{fac.color}}; font-size:13px;">${{fac.name}}</strong><br/>
                    <span style="font-size:11px; color:#9b9b9b;">TRI ID: ${{fac.tri_id}}</span>
                    <div style="height:1px; background:#2e2e2e; margin:6px 0;"></div>
                    <div style="font-weight:600; color:#a5b4fc; margin-bottom:4px;">Active Source Strength:</div>
                    <div style="display:flex; justify-content:space-between; font-size:11px; margin-bottom:2px;">
                        <span style="color:#9ca3af">Active Stack:</span>
                        <span style="font-weight:600; color:#fff">${{stackText}}</span>
                    </div>
                    <div style="display:flex; justify-content:space-between; font-size:11px; margin-bottom:4px;">
                        <span style="color:#9ca3af">Active Fugitive:</span>
                        <span style="font-weight:600; color:#fff">${{fugitiveText}}</span>
                    </div>
                    <div style="display:flex; justify-content:space-between; font-size:11px; font-weight:700; border-top:1px dashed #2e2e2e; padding-top:4px; margin-bottom:6px;">
                        <span style="color:#a5b4fc">Active Combined:</span>
                        <span style="color:#a5b4fc">${{totalText}}</span>
                    </div>
                    <div style="height:1px; background:#2e2e2e; margin:6px 0;"></div>
                    <span style="font-weight:500; font-size:11px; color:#a5b4fc;">Annual Chemical Releases:</span>
                    ${{chemHtml}}
                </div>
            `;
            
            marker.bindPopup(popupContent, {{
                className: 'custom-leaflet-popup'
            }});
            
            if (marker.isPopupOpen()) {{
                marker.getPopup().setContent(popupContent);
            }}
        }}

        PLUME_DATA.facilities.forEach(fac => {{
            const squareIcon = L.divIcon({{
                className: 'custom-facility-divicon',
                html: `<div style="background-color: ${{fac.color}}; border: 1.5px solid #ffffff; width: 10px; height: 10px; box-shadow: 0 0 4px rgba(0,0,0,0.5);"></div>`,
                iconSize: [13, 13],
                iconAnchor: [6.5, 6.5]
            }});
            const marker = L.marker([fac.lat, fac.lon], {{
                icon: squareIcon
            }}).addTo(map);
            
            facilityMarkers[fac.id] = marker;
        }});

        // ── Veterinary clinic landmarks (LOCATIONS layer) ──
        // Anchored Leaflet markers (markerPane) → no zoom/pan drift. Toggleable as a group.
        // Custom teal pin + white paw + red medical cross SVG (an original take on the vet paw icon).
        const VET_CLINIC_SVG =
            '<svg width="28" height="36" viewBox="0 0 28 36" xmlns="http://www.w3.org/2000/svg">' +
            '<path d="M14 35 C14 35 25.5 20.5 25.5 13 A11.5 11.5 0 1 0 2.5 13 C2.5 20.5 14 35 14 35 Z" fill="#0d9488" stroke="#ffffff" stroke-width="1.6"/>' +
            '<ellipse cx="14" cy="15.6" rx="4.3" ry="3.5" fill="#ffffff"/>' +
            '<circle cx="8.6" cy="10.8" r="1.7" fill="#ffffff"/>' +
            '<circle cx="12.1" cy="8.4" r="1.7" fill="#ffffff"/>' +
            '<circle cx="15.9" cy="8.4" r="1.7" fill="#ffffff"/>' +
            '<circle cx="19.4" cy="10.8" r="1.7" fill="#ffffff"/>' +
            '<rect x="13.2" y="13.6" width="1.6" height="4.2" rx="0.4" fill="#e11d48"/>' +
            '<rect x="11.9" y="14.9" width="4.2" height="1.6" rx="0.4" fill="#e11d48"/>' +
            '</svg>';
        const vetIcon = L.divIcon({{
            className: 'vet-clinic-divicon',
            html: VET_CLINIC_SVG,
            iconSize: [28, 36],
            iconAnchor: [14, 35],     // pin tip sits on the coordinate
            popupAnchor: [0, -30]
        }});

        // Soil deposition at a point, from the currently-drawn combined soil footprints (depHitIndex).
        // Returns {{maxVal, minBand, chem}} or null if the point is outside every dep contour this hour.
        // TRUE soil deposition at a point: queries the combined SOIL footprints directly across ALL
        // bands (not just the drawn/visible ones), so a clinic gets its real value even where the
        // drawn footprint doesn't reach. Matches the current display mode + active chemicals + frame.
        function soilDepAtPoint(lat, lon) {{
            if (typeof depManifest === 'undefined' || !depManifest) return null;
            const modeEl = document.getElementById('display-mode-select');
            const wantSrc = (modeEl && modeEl.value !== 'combined') ? modeEl.value : '';
            const hour = (typeof playbackTime === 'number') ? playbackTime : 24;
            const perChem = {{}};   // chem -> highest soil-dep value covering this point
            (depManifest.combined_entries || []).forEach(entry => {{
                if ((entry.source_type || '') !== wantSrc) return;
                if (typeof depActiveChem !== 'undefined' && depActiveChem.size && !depActiveChem.has(entry.chem)) return;
                const fc = depGeoJsonCache[entry.file];
                if (!fc || !fc.features) return;
                const md = fc.metadata || {{}};
                const N = md.num_frames || 1;
                const S = (md.start_hour != null) ? md.start_hour : 2;
                const fp = Math.max(0, Math.min(N - 1, Math.floor(hour - S)));
                const bv = (md.band_values || {{}}).dep || {{}};
                for (const f of fc.features) {{
                    if (f.properties.layer !== 'dep' || f.properties.hour_frame !== fp) continue;
                    if (!depPointInRing(lat, lon, f.geometry.coordinates[0])) continue;
                    const v = bv[f.properties.band] || 0;
                    if (!(entry.chem in perChem) || v > perChem[entry.chem]) perChem[entry.chem] = v;
                }}
            }});
            const list = Object.keys(perChem).map(c => ({{ chem: c, val: perChem[c] }}))
                                             .sort((a, b) => b.val - a.val);
            return list.length ? {{ list: list }} : null;
        }}

        function depRisk(v) {{
            if (v >= 1e-4) return {{ label: 'Elevated', color: '#ef4444' }};
            if (v >= 1e-6) return {{ label: 'Moderate', color: '#f59e0b' }};
            if (v >= 1e-8) return {{ label: 'Low',      color: '#22c55e' }};
            return {{ label: 'Trace', color: '#9ca3af' }};
        }}

        // Expand/collapse the "+N more" per-chemical deposition list inside a clinic popup.
        function toggleVetChems(el) {{
            const list = el.parentElement.querySelector('.vp-chemlist');
            if (!list) return;
            const show = (list.style.display === 'none' || !list.style.display);
            list.style.display = show ? 'block' : 'none';
            const arrow = el.querySelector('.vp-arrow');
            if (arrow) arrow.textContent = show ? '▴' : '▾';
        }}

        function vetPopupHtml(cl) {{
            const dep = soilDepAtPoint(cl.lat, cl.lon);
            let depHtml;
            if (dep && dep.list.length) {{
                const top = dep.list[0];
                const r = depRisk(top.val);
                depHtml = 'Soil deposition here: <strong>' + fmtConc(top.val, 'm²') + '</strong><br/>'
                        + 'Level: <strong style="color:' + r.color + '">' + r.label + '</strong>'
                        + ' <span style="color:#9ca3af">(' + top.chem.toLowerCase() + ')</span>';
                if (dep.list.length > 1) {{
                    const extra = dep.list.length - 1;
                    depHtml += ' <span class="vp-more" onclick="toggleVetChems(this)">+' + extra
                             + ' more <span class="vp-arrow">▾</span></span>';
                    // Full per-chemical breakdown with concentrations (hidden until clicked)
                    let rows = '';
                    dep.list.forEach(c => {{
                        const cr = depRisk(c.val);
                        rows += '<div class="vp-chemrow"><span>' + c.chem.toLowerCase() + '</span>'
                              + '<span><span style="color:' + cr.color + '">' + fmtConc(c.val, 'm²')
                              + '</span></span></div>';
                    }});
                    depHtml += '<div class="vp-chemlist" style="display:none">' + rows + '</div>';
                }}
            }} else {{
                depHtml = '<span style="color:#9ca3af">No modeled soil deposition reaches here at this hour.</span>';
            }}
            return '<div class="vet-pop">'
                 + '<div class="vp-title">🐾 ' + cl.name + '</div>'
                 + '<div class="vp-addr">' + cl.address + '</div>'
                 + '<div class="vp-dep">' + depHtml + '</div>'
                 + '</div>';
        }}

        const vetClinicLayer = L.layerGroup();
        (typeof VET_CLINICS !== 'undefined' ? VET_CLINICS : []).forEach(cl => {{
            const m = L.marker([cl.lat, cl.lon], {{ icon: vetIcon, title: cl.name }});
            m.bindPopup(() => vetPopupHtml(cl), {{ maxWidth: 260, className: 'vet-popup' }});
            vetClinicLayer.addLayer(m);
        }});
        vetClinicLayer.addTo(map);   // shown by default; toggleable
        {{ const _vc = document.getElementById('vet-count'); if (_vc) _vc.textContent = '(' + ((typeof VET_CLINICS !== 'undefined') ? VET_CLINICS.length : 0) + ')'; }}

        // LOCATIONS section wiring: Veterinary Clinics on/off + collapsible dropdown
        {{
            const vt = document.getElementById('vet-clinics-toggle');
            if (vt) vt.addEventListener('change', e => {{
                if (e.target.checked) vetClinicLayer.addTo(map); else map.removeLayer(vetClinicLayer);
            }});
            const lt = document.getElementById('locations-toggle');
            const lb = document.getElementById('locations-body');
            const la = document.getElementById('locations-arrow');
            if (lt && lb && la) lt.addEventListener('click', () => {{
                const open = lb.classList.toggle('open');
                la.classList.toggle('expanded', open);
            }});
        }}

        // Legend construction with collapsible dropdowns and total lbs display
        const legendContainer = document.getElementById('facility-legend');
        PLUME_DATA.facilities.forEach(fac => {{
            // Initialize active chemical states for this facility based on defaultActive
            activeChemicals[fac.id] = {{}};
            fac.chemicals.forEach(c => {{
                activeChemicals[fac.id][c.chemical] = c.defaultActive;
            }});

            const item = document.createElement('div');
            item.className = 'facility-item';
            item.dataset.id = fac.id;
            
            let chemHtml = '';
            fac.chemicals.forEach(c => {{
                const isChecked = c.defaultActive ? 'checked' : '';
                const props = (PLUME_DATA.chemical_properties && PLUME_DATA.chemical_properties[c.chemical]) || {{ vd: 0, mol_wt: 0, henry_const: 0 }};
                const depInfo = `Vd: ${{props.vd.toFixed(4)}} m/s, MW: ${{props.mol_wt.toFixed(1)}} g/mol, H: ${{props.henry_const !== undefined ? props.henry_const.toExponential(1) : 'N/A'}} M/atm`;
                chemHtml += `
                    <div class="chem-item" style="margin-bottom: 4px; display: flex; align-items: center; justify-content: space-between; gap: 8px;" title="${{depInfo}}">
                        <label style="display: flex; align-items: center; gap: 6px; cursor: pointer; font-size: 11px; color: #d1d5db; user-select: none; min-width: 0; flex: 1;">
                            <input type="checkbox" ${{isChecked}} class="chem-chk" data-fac="${{fac.id}}" data-chem="${{c.chemical}}" style="accent-color: ${{fac.color}}; cursor: pointer; flex-shrink: 0;" />
                            <span style="overflow: hidden; text-overflow: ellipsis; white-space: nowrap; border-bottom: 1px dotted rgba(255,255,255,0.15);">${{c.chemical}}</span>
                        </label>
                        <span class="chem-val" style="white-space: nowrap; margin-left: 10px; font-size: 11px; color: var(--text-muted);">${{c.total_lbs.toLocaleString()}} lbs/yr</span>
                    </div>`;
            }});
            
            const totalLbsFormatted = fac.total_lbs ? fac.total_lbs.toLocaleString(undefined, {{maximumFractionDigits: 1}}) : "0";
            
            item.innerHTML = `
                <div class="facility-header" style="display: flex; align-items: center; justify-content: space-between; gap: 8px;">
                    <div class="facility-left-section" style="display: flex; align-items: center; gap: 8px; flex: 1; min-width: 0;">
                        <span class="facility-badge" style="color:${{fac.color}}; background-color:${{fac.color}}; flex-shrink: 0;"></span>
                        <div class="facility-info" style="min-width: 0; display: flex; flex-direction: column;">
                            <span class="facility-name" style="white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">${{fac.name}}</span>
                            <span class="facility-total-lbs" id="total-lbs-${{fac.id}}" style="font-size: 11px; color: var(--text-muted); font-weight: 500; margin-top: 1px;">
                                ${{totalLbsFormatted}} lbs/yr
                            </span>
                        </div>
                    </div>
                    <div class="facility-actions" style="display: flex; align-items: center; gap: 8px; flex-shrink: 0;">
                        <span class="toggle-icon" id="toggle-lbl-${{fac.id}}" style="padding: 4px 6px; border-radius: 4px; font-size: 9px; cursor: pointer; transition: all 0.2s; color: #10B981; background: rgba(16, 185, 129, 0.1); font-weight: 700; letter-spacing: 0.05em;">VISIBLE</span>
                        <span class="dropdown-arrow" id="arrow-${{fac.id}}" style="font-size: 11px; transition: transform 0.2s; padding: 4px; cursor: pointer; color: var(--text-muted);">▼</span>
                    </div>
                </div>
                <div class="chem-list" id="chem-list-${{fac.id}}" style="display: none; flex-direction: column; margin-top: 10px; border-top: 1px solid rgba(255, 255, 255, 0.05); padding-top: 8px;">
                    ${{chemHtml}}
                </div>
            `;
            
            const toggleBtn = item.querySelector(`#toggle-lbl-${{fac.id}}`);
            const chemList = item.querySelector(`#chem-list-${{fac.id}}`);
            const arrow = item.querySelector(`#arrow-${{fac.id}}`);
            
            // Particle visibility toggle
            toggleBtn.addEventListener('click', (e) => {{
                e.stopPropagation(); // Prevent dropdown expansion
                activeFacilities[fac.id] = !activeFacilities[fac.id];
                if (activeFacilities[fac.id]) {{
                    item.classList.remove('disabled');
                    toggleBtn.textContent = 'VISIBLE';
                    toggleBtn.style.color = '#10B981';
                    toggleBtn.style.background = 'rgba(16, 185, 129, 0.1)';
                }} else {{
                    item.classList.add('disabled');
                    toggleBtn.textContent = 'HIDDEN';
                    toggleBtn.style.color = 'var(--text-muted)';
                    toggleBtn.style.background = 'rgba(255, 255, 255, 0.05)';
                }}
                // Sync map marker visibility
                const marker = facilityMarkers[fac.id];
                if (marker) {{
                    if (activeFacilities[fac.id]) {{
                        marker.addTo(map);
                    }} else {{
                        marker.remove();
                    }}
                }}
                drawParticles();
                refreshDepLayers();
            }});

            // Chemical checkbox toggles
            item.querySelectorAll('.chem-chk').forEach(chk => {{
                chk.addEventListener('change', (e) => {{
                    const facId = parseInt(chk.dataset.fac);
                    const chemName = chk.dataset.chem;
                    activeChemicals[facId][chemName] = chk.checked;
                    
                    // If checked and global pill is unchecked, check it
                    if (chk.checked && !depActiveChem.has(chemName)) {{
                        const globalChk = document.querySelector(`.dep-chem-chk[data-chem="${{chemName}}"]`);
                        if (globalChk) {{
                            globalChk.checked = true;
                            depActiveChem.add(chemName);
                        }}
                    }}
                    
                    // Filter out existing particles of this chemical from map immediately
                    if (!chk.checked) {{
                        particles = particles.filter(p => p.fac !== facId || p.chem !== chemName);
                    }}
                    
                    // Recalculate totals
                    const facObj = PLUME_DATA.facilities.find(f => f.id === facId);
                    let active_total = 0;
                    facObj.chemicals.forEach(c => {{
                        if (activeChemicals[facId][c.chemical]) {{
                            active_total += c.total_lbs || 0;
                        }}
                    }});
                    
                    // Update sidebar total
                    const totalLbsLabel = document.getElementById('total-lbs-' + facId);
                    if (totalLbsLabel) {{
                        totalLbsLabel.textContent = active_total === 0 ? '0.0 lbs' : active_total.toLocaleString(undefined, {{maximumFractionDigits: 1}}) + ' lbs/yr';
                    }}
                    
                    // Update Leaflet popup content
                    updateFacilityPopup(facId);
                    
                    // [Particle rework: always sandbox mode now]
                    // Particles are always wind-advected + footprint-gated; no HYSPLIT replay.
                    drawParticles();
                    refreshDepLayers();
                    lastDepositionHour = -1;
                    lastDepUpdateTime = -999;
                    if (depositionHeatLayer) {{ map.removeLayer(depositionHeatLayer); depositionHeatLayer = null; }}
                    renderDepositionHeatmap(playbackTime);
                    drawParticles();
                    refreshDepLayers();
                }});
                chk.addEventListener('click', (e) => {{
                    e.stopPropagation(); // Prevent dropdown collapse/expand
                }});
            }});
            
            // Chemical dropdown toggle
            item.addEventListener('click', () => {{
                const isExpanded = chemList.style.display !== 'none';
                if (isExpanded) {{
                    chemList.style.display = 'none';
                    arrow.style.transform = 'rotate(0deg)';
                }} else {{
                    chemList.style.display = 'flex';
                    arrow.style.transform = 'rotate(180deg)';
                }}
            }});
            
            legendContainer.appendChild(item);
            
            // Initialize popups and sidebar labels
            updateFacilityPopup(fac.id);
            
            let initial_active_total = 0;
            fac.chemicals.forEach(c => {{
                if (activeChemicals[fac.id][c.chemical]) {{
                    initial_active_total += c.total_lbs || 0;
                }}
            }});
            const totalLbsLabel = document.getElementById('total-lbs-' + fac.id);
            if (totalLbsLabel) {{
                totalLbsLabel.textContent = initial_active_total === 0 ? '0.0 lbs' : initial_active_total.toLocaleString(undefined, {{maximumFractionDigits: 1}}) + ' lbs/yr';
            }}
        }});


        // Plume Display Mode select event listener
        document.getElementById('display-mode-select').addEventListener('change', () => {{
            const displayMode = document.getElementById('display-mode-select').value;
            if (displayMode === 'stack') {{
                particles = particles.filter(p => p.type === 'stack');
            }} else if (displayMode === 'fugitive') {{
                particles = particles.filter(p => p.type === 'fugitive');
            }}
            recalculateDeposition();
            lastDepositionHour = -1;
            lastDepUpdateTime = -999;
            if (depositionHeatLayer) {{ map.removeLayer(depositionHeatLayer); depositionHeatLayer = null; }}
            renderDepositionHeatmap(playbackTime);
            drawParticles();
            refreshDepLayers();
        }});

        // ================================================================
        // CLIENT-SIDE CONTINUOUS PARTICLE SYSTEM
        // ================================================================
        
        // Physics constants for emergent particle lifespan (mass-based deposition)
        const DEP_MASS_FLOOR = 0.05;   // particle vanishes when remaining mass fraction drops to this
        const SAFETY_MAX_AGE = 1440;   // backstop (minutes = 24h): early-released particles must live the
                                       // full day to ride the HYSPLIT wind out to the far footprint edge
                                       // (the day-24 footprint is an accumulated envelope of all-day transport)
        const DEP_GAMMA = 0.5;         // sqrt lifts faint distant cells

        // Sandbox slider live-read helpers (replace hardcoded constants)
        function getSandboxSize() {{
            const el = document.getElementById('sizeSlider');
            return el ? parseFloat(el.value) : {BASE_PARTICLE_RADIUS_PIXELS};
        }}
        function getSandboxDensity() {{
            const el = document.getElementById('densitySlider');
            return el ? parseFloat(el.value) : 1.0;
        }}
        function getSandboxStackOpacity() {{
            const el = document.getElementById('stackOpacitySlider');
            return el ? parseFloat(el.value) : 0.70;
        }}
        function getSandboxFugitiveOpacity() {{
            const el = document.getElementById('fugitiveOpacitySlider');
            return el ? parseFloat(el.value) : 0.70;
        }}

        const MAX_ACTIVE = 8000;                // Global particle cap (raised for plume fill)
        const SPAWN_INTERVAL = 1.0 / 30.0;     // Spawn every 2 sim-minutes
        const BASE_SPAWN_COUNT = 12;            // Particles per spawn for biggest emitter (raised for plume fill)
        const TURB_BASE = 0.0025;               // Base turbulent diffusion (deg/hr)
        const TURB_GROWTH = 0.0026;             // Extra diffusion per hour of age. Kept modest so WIND
                                                // advection clearly leads and the plume reads as directional
                                                // rather than radiating in all directions (turbulent spread
                                                // is real, but was previously tuned high to fill the footprint).
        const TURB_MAX = 0.025;                 // Cap ~halved: aged particles still spread but stay a minority
                                                // of the wind magnitude. The deposition footprint LAYER (a
                                                // separate HYSPLIT product) still shows the full plume extent.
        const MAX_WIND_PER_HR = 0.18;           // Raised from 0.10 to allow real HYSPLIT transport distances
        
        // Find max emissions for proportional spawning
        // Density anchor is the max facility total over ALL facilities (including any dropped for
        // having no modeled chemicals) — embedded from Python so spawn density is stable regardless
        // of which facilities are shown. Falls back to the max over embedded facilities.
        const maxFacLbs = Math.max({max_fac_lbs_ref}, ...PLUME_DATA.facilities.map(f => f.total_lbs || 1), 1);
        
        let particles = [];           // Sandbox simulation particles
        let nextSandboxId = 0;        // Stable unique ID generator for sandbox particles
        let hysplitParticles = [];     // Interpolated HYSPLIT particles (from Python-exported data)
        let particleSource = 'sandbox'; // always 'sandbox' — HYSPLIT PARDUMP replay removed in particle rework
        let lastSpawnTime = -999;
        let prevPlaybackTime = playbackTime;

        // ── HYSPLIT Particle Interpolation Engine ──
        // [COMMENTED OUT — particle rework: PARDUMP replay removed, replaced by
        //  footprint-gated wind-advected particles. Kept as reference.]
        /*
        // Reads pre-computed HYSPLIT particle trajectories from PLUME_DATA.particles
        // and linearly interpolates between hourly snapshots to produce smooth playback.
        // This is the performance-friendly, high-accuracy alternative to the sandbox.
        function updateHysplitParticles(time) {{
            if (!PLUME_DATA.particles) {{ hysplitParticles = []; return; }}
            
            const H_cur = Math.max(0, Math.min(23, Math.floor(time)));
            const H_next = Math.min(23, H_cur + 1);
            const frac = time - Math.floor(time); // always 0.0→1.0 within the hour

            const displayMode = document.getElementById('display-mode-select').value;
            const newParticles = [];

            // Iterate over each facility's HYSPLIT particles
            const facNameMap = {{}};
            PLUME_DATA.facilities.forEach((f, idx) => {{ facNameMap[f.name] = idx; }});

            for (const [facName, hourlyData] of Object.entries(PLUME_DATA.particles)) {{
                const facIdx = facNameMap[facName];
                if (facIdx === undefined) continue;
                if (!activeFacilities[facIdx]) continue;

                const fac = PLUME_DATA.facilities[facIdx];
                const curList = hourlyData[H_cur] || hourlyData[String(H_cur)] || [];
                const nxtList = hourlyData[H_next] || hourlyData[String(H_next)] || [];

                // Build lookup by particle ID for next-hour snapshot
                const nxtMap = new Map();
                for (const pn of nxtList) {{
                    nxtMap.set(pn[0], pn); // key: id
                }}

                for (const pc of curList) {{
                    const [id, lat, lon, height, age, chem, fac_i] = pc;

                    // Respect chemical toggles
                    if (activeChemicals[facIdx] && !activeChemicals[facIdx][chem]) continue;

                    // Classify type
                    const type = (height >= 15.0) ? 'stack' : 'fugitive';

                    // Respect display mode filter
                    if (displayMode === 'stack' && type !== 'stack') continue;
                    if (displayMode === 'fugitive' && type !== 'fugitive') continue;

                    let finalLat = lat, finalLon = lon, finalHt = height, finalAge = age;
                    let fadeMod = 1.0;

                    const pn = nxtMap.get(id);
                    const isSameParticle = pn && (pn[4] > age);
                    if (isSameParticle && H_cur !== H_next) {{
                        finalLat = lat + (pn[1] - lat) * frac;
                        finalLon = lon + (pn[2] - lon) * frac;
                        finalHt  = Math.max(0, height + (pn[3] - height) * frac);
                        finalAge = age + (pn[4] - age) * frac;
                    }} else if (pn && !isSameParticle) {{
                        if (frac > 0.5) continue;
                        fadeMod = 1.0 - frac * 2.0;
                    }}

                    newParticles.push({{
                        id,
                        lat: finalLat,
                        lon: finalLon,
                        ht: finalHt,
                        age: finalAge,
                        fac: facIdx,
                        chem,
                        col: fac.color,
                        type,
                        birth: time - (finalAge / 60.0),
                        fadeMod
                    }});
                }}
            }}
            hysplitParticles = newParticles;
        }}
        */

        // ── Sandbox UI removed ── particle motion/size/opacity + footprint opacity are now fixed
        // (viewers can't alter the model). The getSandbox*() getters return their built-in defaults
        // when the sliders are absent, and footprintOpacity stays at its initial 0.45.

        // ── Collapsible Panel Toggle System ──
        (function initPanelToggles() {{
            // Left Controls panel
            const headerPanel = document.getElementById('hud-header-panel');
            const headerBody = document.getElementById('header-panel-body');
            const collapseHeader = document.getElementById('collapse-header');
            const restoreHeader = document.getElementById('restore-header');

            collapseHeader.addEventListener('click', () => {{
                headerPanel.classList.add('panel-hidden');
                restoreHeader.classList.add('visible');
            }});
            restoreHeader.addEventListener('click', () => {{
                headerPanel.classList.remove('panel-hidden');
                restoreHeader.classList.remove('visible');
            }});

            // Right Legend/Sources panel
            const legendPanel = document.getElementById('hud-legend-panel');
            const legendBody = document.getElementById('legend-panel-body');
            const collapseLegend = document.getElementById('collapse-legend');
            const restoreLegend = document.getElementById('restore-legend');

            collapseLegend.addEventListener('click', () => {{
                legendPanel.classList.add('panel-hidden');
                restoreLegend.classList.add('visible');
            }});
            restoreLegend.addEventListener('click', () => {{
                legendPanel.classList.remove('panel-hidden');
                restoreLegend.classList.remove('visible');
            }});
        }})();
        
        // ── Wind vector interpolation ──
        const gridInfo = PLUME_DATA.grid_info;
        const GRID_SIZE = gridInfo.grid_size;
        const latMin = gridInfo.lat_min;
        const latMax = gridInfo.lat_max;
        const lonMin = gridInfo.lon_min;
        const lonMax = gridInfo.lon_max;
        const latSpan = latMax - latMin;
        const lonSpan = lonMax - lonMin;

        function interpolateGrid(grid, lat, lon) {{
            // Derive dimensions from the ACTUAL grid slice rather than trusting GRID_SIZE.
            // Embedded wind grids can be jagged / differently-sized than GRID_SIZE
            // (stale data, per-hour variation); using real dims prevents out-of-range
            // index access (grid[y][x] === undefined → crash) that would silently kill
            // every advect() call via tick()'s try/catch.
            const rows = grid.length;
            const cols = (grid[0] && grid[0].length) || 1;
            const ZERO = {{ dLat: 0, dLon: 0, sLat: 0, sLon: 0 }};

            let clampedLat = Math.max(latMin, Math.min(latMax, lat));
            let clampedLon = Math.max(lonMin, Math.min(lonMax, lon));

            const x = ((clampedLon - lonMin) / lonSpan) * (cols - 1);
            const y = ((clampedLat - latMin) / latSpan) * (rows - 1);

            // Robust floor mapping with explicit boundary clamping to prevent index thrashing
            const x0 = Math.max(0, Math.min(cols - 2, Math.floor(x)));
            const x1 = x0 + 1;
            const y0 = Math.max(0, Math.min(rows - 2, Math.floor(y)));
            const y1 = y0 + 1;

            const tx = Math.max(0, Math.min(1.0, x - x0));
            const ty = Math.max(0, Math.min(1.0, y - y0));

            // Per-row fallback to ZERO guards against jagged rows of unequal length.
            const row0 = grid[y0] || [];
            const row1 = grid[y1] || [];
            const v00 = row0[x0] || ZERO;
            const v10 = row0[x1] || ZERO;
            const v01 = row1[x0] || ZERO;
            const v11 = row1[x1] || ZERO;

            const dLat = (1 - ty) * ((1 - tx) * v00.dLat + tx * v10.dLat) +
                          ty  * ((1 - tx) * v01.dLat + tx * v11.dLat);
            const dLon = (1 - ty) * ((1 - tx) * v00.dLon + tx * v10.dLon) +
                          ty  * ((1 - tx) * v01.dLon + tx * v11.dLon);
            // IQR-based spread from HYSPLIT particle statistics
            const sLat = (1 - ty) * ((1 - tx) * (v00.sLat||0) + tx * (v10.sLat||0)) +
                          ty  * ((1 - tx) * (v01.sLat||0) + tx * (v11.sLat||0));
            const sLon = (1 - ty) * ((1 - tx) * (v00.sLon||0) + tx * (v10.sLon||0)) +
                          ty  * ((1 - tx) * (v01.sLon||0) + tx * (v11.sLon||0));

            return {{ dLat, dLon, sLat, sLon }};
        }}

        // Returns true when every cell in wind grid slice idx is zero (day-edge artifact hours 0,1,23).
        // Results are cached on the grid array object to avoid repeated scanning.
        function windHourIsZero(wg, idx) {{
            if (!wg._zeroCache) wg._zeroCache = {{}};
            if (wg._zeroCache[idx] !== undefined) return wg._zeroCache[idx];
            const grid = wg[idx];
            let nonzero = false;
            outer: for (let r = 0; r < grid.length; r++)
                for (let c = 0; c < grid[r].length; c++)
                    if (grid[r][c].dLat !== 0 || grid[r][c].dLon !== 0) {{ nonzero = true; break outer; }}
            wg._zeroCache[idx] = !nonzero;
            return wg._zeroCache[idx];
        }}

        // Returns the nearest hourly index (forward or backward) whose wind slice is non-zero.
        function nearestNonZeroHour(wg, idx) {{
            if (!windHourIsZero(wg, idx)) return idx;
            for (let d = 1; d < wg.length; d++) {{
                if (idx - d >= 0 && !windHourIsZero(wg, idx - d)) return idx - d;
                if (idx + d < wg.length && !windHourIsZero(wg, idx + d)) return idx + d;
            }}
            return idx;
        }}

        function getWind(time, lat, lon, type) {{
            let wg = (type === 'fugitive') ? PLUME_DATA.wind_grid_fugitive : PLUME_DATA.wind_grid_stack;
            if (!wg) {{
                wg = PLUME_DATA.wind_grid; // fallback for backwards compatibility
            }}
            if (!wg || wg.length === 0) return {{dLat: 0, dLon: 0, sLat: 0, sLon: 0}};

            const h  = Math.max(0, Math.min(wg.length - 2, Math.floor(time)));
            const hn = Math.min(wg.length - 1, h + 1);
            const t = time - Math.floor(time);
            const s = t * t * (3 - 2 * t); // smoothstep

            // Borrow nearest populated hour for day-edge slices that are fully zero
            const w1 = interpolateGrid(wg[nearestNonZeroHour(wg, h)],  lat, lon);
            const w2 = interpolateGrid(wg[nearestNonZeroHour(wg, hn)], lat, lon);

            let dLat = w1.dLat + s * (w2.dLat - w1.dLat);
            let dLon = w1.dLon + s * (w2.dLon - w1.dLon);
            // Blend HYSPLIT-derived spread (IQR half-range) alongside median displacement
            const sLat = w1.sLat + s * (w2.sLat - w1.sLat);
            const sLon = w1.sLon + s * (w2.sLon - w1.sLon);
            // Clamp magnitude to suppress anomalous spikes while preserving direction
            const mag = Math.hypot(dLat, dLon);
            if (mag > MAX_WIND_PER_HR) {{ const k = MAX_WIND_PER_HR / mag; dLat *= k; dLon *= k; }}
            return {{ dLat, dLon, sLat, sLon }};
        }}
        
        // ── Spawn particles at all active facilities ──
        // Density slider multiplies the base spawn count in real-time.
        function spawnBatch(dtHours) {{
            if (particles.length >= MAX_ACTIVE) return;

            const displayMode = document.getElementById('display-mode-select').value;
            const densityMult = getSandboxDensity();  // live density slider
            // Scale spawn count to elapsed sim-time so rate is continuous, not bursty
            const rateScale = (dtHours !== undefined) ? dtHours / SPAWN_INTERVAL : 1.0;
            // No lifespanScale: lifespan is now emergent from mass depletion; MAX_ACTIVE caps steady-state count
            
            PLUME_DATA.facilities.forEach((fac, idx) => {{
                if (!activeFacilities[idx]) return;
                
                // Enforce operating hours schedule if configured
                if (fac.schedule && fac.schedule !== 'continuous') {{
                    const currentHour = playbackTime;
                    if (fac.schedule.type === 'shift') {{
                        if (currentHour < fac.schedule.start_hour || currentHour > fac.schedule.end_hour) {{
                            return;
                        }}
                    }}
                }}
                
                fac.chemicals.forEach(c => {{
                    if (!activeChemicals[idx] || !activeChemicals[idx][c.chemical]) return;
                    
                    // Stack Spawning
                    if (displayMode === 'combined' || displayMode === 'stack') {{
                        const stackLbs = c.stack_lbs || 0;
                        if (stackLbs > 0) {{
                            const ratio = stackLbs / maxFacLbs;
                            const countFloat = ratio * BASE_SPAWN_COUNT * 1.5 * densityMult * rateScale;
                            let count = Math.floor(countFloat);
                            if (Math.random() < (countFloat - count)) count += 1;

                            for (let i = 0; i < count; i++) {{
                                particles.push({{
                                    id: nextSandboxId++,
                                    lat: fac.lat + (Math.random() - 0.5) * 0.0008,
                                    lon: fac.lon + (Math.random() - 0.5) * 0.0008,
                                    ht: fac.height || 15.0,
                                    birth: playbackTime,
                                    fac: idx,
                                    chem: c.chemical,
                                    col: fac.color,
                                    type: 'stack',
                                    mass: 1.0,
                                    tLat: (Math.random() - 0.5) * 2,
                                    tLon: (Math.random() - 0.5) * 2
                                }});
                            }}
                        }}
                    }}

                    // Fugitive Spawning
                    if (displayMode === 'combined' || displayMode === 'fugitive') {{
                        const fugitiveLbs = c.fugitive_lbs || 0;
                        if (fugitiveLbs > 0) {{
                            const ratio = fugitiveLbs / maxFacLbs;
                            const countFloat = ratio * BASE_SPAWN_COUNT * 1.5 * densityMult * rateScale;
                            let count = Math.floor(countFloat);
                            if (Math.random() < (countFloat - count)) count += 1;

                            for (let i = 0; i < count; i++) {{
                                particles.push({{
                                    id: nextSandboxId++,
                                    lat: fac.lat + (Math.random() - 0.5) * 0.0012,
                                    lon: fac.lon + (Math.random() - 0.5) * 0.0012,
                                    ht: 2.0, // lower fugitive release height
                                    birth: playbackTime,
                                    fac: idx,
                                    chem: c.chemical,
                                    col: fac.color,
                                    type: 'fugitive',
                                    mass: 1.0,
                                    tLat: (Math.random() - 0.5) * 3,
                                    tLon: (Math.random() - 0.5) * 3
                                }});
                            }}
                        }}
                    }}
                }});
            }});
        }}
        // [COMMENTED OUT — particle rework: batch deposition precompute removed.
        //  Deposition is now driven by footprint-gated particles + liveDepGrid. Kept as reference.]
        /*
        function recalculateDeposition() {{
            const sourceSelect = document.getElementById('deposition-source-select');
            const source = sourceSelect ? sourceSelect.value : 'sandbox';
            if (source === 'hysplit' && PLUME_DATA.hysplit_deposition_grid) {{
                PLUME_DATA.deposition_grid = PLUME_DATA.hysplit_deposition_grid;
                return;
            }}
            const hourlyDepGrid = Array.from({{length: 24}}, () => new Map());
            let simParticles = [];
            const dt = 0.1;
            const stepsPerHour = 10;
            const liveLifespan = SAFETY_MAX_AGE;
            const displayMode = document.getElementById('display-mode-select').value;
            
            let seed = 42;
            function random() {{
                const x = Math.sin(seed++) * 10000;
                return x - Math.floor(x);
            }}
            
            for (let hour = 0; hour < 24; hour++) {{
                for (let step = 0; step < stepsPerHour; step++) {{
                    const time = hour + step * dt;
                    
                    PLUME_DATA.facilities.forEach((fac, idx) => {{
                        if (!activeFacilities[idx]) return;
                        
                        if (fac.schedule && fac.schedule !== 'continuous') {{
                            if (fac.schedule.type === 'shift') {{
                                if (time < fac.schedule.start_hour || time > fac.schedule.end_hour) {{
                                    return;
                                }}
                            }}
                        }}
                        
                        fac.chemicals.forEach(c => {{
                            if (!activeChemicals[idx] || !activeChemicals[idx][c.chemical]) return;
                            
                            if (displayMode === 'combined' || displayMode === 'stack') {{
                                const stackLbs = c.stack_lbs || 0;
                                if (stackLbs > 0) {{
                                    const ratio = stackLbs / maxFacLbs;
                                    const countFloat = ratio * BASE_SPAWN_COUNT * 1.5 * dt;
                                    let count = Math.floor(countFloat);
                                    if (random() < (countFloat - count)) count += 1;
                                    
                                    for (let i = 0; i < count; i++) {{
                                        simParticles.push({{
                                            lat: fac.lat + (random() - 0.5) * 0.0008,
                                            lon: fac.lon + (random() - 0.5) * 0.0008,
                                            ht: fac.height || 15.0,
                                            birth: time,
                                            fac: idx,
                                            chem: c.chemical,
                                            type: 'stack',
                                            mass: 1.0,
                                            tLat: (random() - 0.5) * 2,
                                            tLon: (random() - 0.5) * 2
                                        }});
                                    }}
                                }}
                            }}
                            
                            if (displayMode === 'combined' || displayMode === 'fugitive') {{
                                const fugitiveLbs = c.fugitive_lbs || 0;
                                if (fugitiveLbs > 0) {{
                                    const ratio = fugitiveLbs / maxFacLbs;
                                    const countFloat = ratio * BASE_SPAWN_COUNT * 1.5 * dt;
                                    let count = Math.floor(countFloat);
                                    if (random() < (countFloat - count)) count += 1;
                                    
                                    for (let i = 0; i < count; i++) {{
                                        simParticles.push({{
                                            lat: fac.lat + (random() - 0.5) * 0.0012,
                                            lon: fac.lon + (random() - 0.5) * 0.0012,
                                            ht: 2.0,
                                            birth: time,
                                            fac: idx,
                                            chem: c.chemical,
                                            type: 'fugitive',
                                            mass: 1.0,
                                            tLat: (random() - 0.5) * 3,
                                            tLon: (random() - 0.5) * 3
                                        }});
                                    }}
                                }}
                            }}
                        }});
                    }});
                    
                    simParticles = simParticles.filter(p => {{
                        const ageMin = (time - p.birth) * 60;
                        const inBounds = p.lat >= latMin && p.lat <= latMax && p.lon >= lonMin && p.lon <= lonMax;
                        return ageMin >= 0 && ageMin < liveLifespan && inBounds;
                    }});
                    
                    for (let i = 0; i < simParticles.length; i++) {{
                        const p = simParticles[i];
                        const ageH = time - p.birth;
                        const baseTurb   = p.type === 'fugitive' ? TURB_BASE   * 1.5 : TURB_BASE;
                        const turbGrowth = p.type === 'fugitive' ? TURB_GROWTH * 1.5 : TURB_GROWTH;
                        const turbMax    = p.type === 'fugitive' ? TURB_MAX    * 1.5 : TURB_MAX;
                        const ageTurb = Math.min(turbMax, baseTurb + turbGrowth * ageH);

                        if (p.lat < latMin || p.lat > latMax || p.lon < lonMin || p.lon > lonMax) continue;

                        const wind = getWind(time, p.lat, p.lon, p.type);
                        const SPREAD_KICK = 1.2;
                        const spreadLat = Math.max(ageTurb, (wind.sLat || 0) * SPREAD_KICK);
                        const spreadLon = Math.max(ageTurb, (wind.sLon || 0) * SPREAD_KICK);
                        
                        const windMag = Math.hypot(wind.dLat, wind.dLon);
                        const noiseScale = Math.min(1.0, ageH * 4.0) * Math.min(1.0, windMag / 0.01);
                        p.lat += (wind.dLat + p.tLat * spreadLat + (random() - 0.5) * spreadLat * 0.4 * noiseScale) * dt;
                        p.lon += (wind.dLon + p.tLon * spreadLon + (random() - 0.5) * spreadLon * 0.4 * noiseScale) * dt;
                        
                        if (p.type === 'fugitive') {{
                            p.ht = Math.max(0, Math.min(10, p.ht + (random() - 0.5) * 1 * dt));
                        }} else {{
                            p.ht = Math.max(0, p.ht + (random() - 0.5) * 3 * dt);
                        }}
                        
                        if (p.ht < 30.0) {{
                            const chemKey = p.chem.toUpperCase();
                            const chemProp = PLUME_DATA.chemical_properties[chemKey] || {{vd: 0.003, henry: 0.01, reactivity: 0.5}};
                            const vd = chemProp.vd || 0.003;
                            
                            const dtSec = dt * 3600.0;
                            const fraction = Math.min(0.2, (vd * dtSec) / 30.0);
                            const dDep = p.mass * fraction;
                            p.mass -= dDep;
                            
                            const grid_spacing = 0.002;
                            const cellLat = Math.round(p.lat / grid_spacing) * grid_spacing;
                            const cellLon = Math.round(p.lon / grid_spacing) * grid_spacing;
                            const cellKey = `${{cellLat.toFixed(4)}},${{cellLon.toFixed(4)}}`;
                            
                            const currentGrid = hourlyDepGrid[hour];
                            const currentVal = currentGrid.get(cellKey) || 0.0;
                            currentGrid.set(cellKey, currentVal + dDep);
                        }}
                    }}
                }}
            }}
            
            const accumulatedGrid = Array.from({{length: 24}}, () => new Map());
            for (let hour = 0; hour < 24; hour++) {{
                for (let prevHour = 0; prevHour <= hour; prevHour++) {{
                    for (const [key, val] of hourlyDepGrid[prevHour]) {{
                        accumulatedGrid[hour].set(key, (accumulatedGrid[hour].get(key) || 0.0) + val);
                    }}
                }}
            }}
            
            let globalMaxVal = 0.0;
            const hoursData = [];
            
            for (let hour = 0; hour < 24; hour++) {{
                const cells = [];
                for (const [key, val] of accumulatedGrid[hour]) {{
                    const [latStr, lonStr] = key.split(",");
                    const lat = parseFloat(latStr);
                    const lon = parseFloat(lonStr);
                    
                    if (val > 0.0001) {{
                        cells.push({{ lat, lon, val }});
                        if (val > globalMaxVal) globalMaxVal = val;
                    }}
                }}
                hoursData.push({{ cells }});
            }}
            
            PLUME_DATA.deposition_grid = {{
                hours: hoursData,
                max_val: globalMaxVal,
                grid_spacing: 0.002
            }};
        }}
        */
        // Stub so existing callers don't throw
        function recalculateDeposition() {{ }}

        // ── Advect all particles forward by dtHours ──
        // PARTICLE REWORK: particles are footprint-gated by the HYSPLIT Ground-Level Air contour.
        // Inside the plume → mass lerps toward band brightness (dense near source, faint at edge).
        // Outside the plume → mass decays rapidly and particle dies.
        // SAFETY_MAX_AGE backstop prevents calm-air particles from accumulating indefinitely.
        function advect(dtHours) {{
            const displayMode = document.getElementById('display-mode-select').value;
            const dtSec = dtHours * 3600.0;
            const grid_spacing = 0.002;
            // Frame-rate-independent turbulence. The random-walk jitter is a diffusion process: a plain
            // "* dtHours" step makes it diffuse MORE and jump HARDER per frame at lower fps (that's why
            // 30fps looked shaky and over-spread). Scaling the random step by this factor keeps its
            // diffusion matched to the reference 120fps look at ANY frame rate. Deterministic advection
            // (wind + directional fan-out) still uses the full dtHours. Computed once per call.
            const _hourRate = getSpeedMultiplier();
            const randCorr = (dtHours > 0) ? Math.sqrt(_hourRate / (120.0 * dtHours)) : 1.0;
            let writeIdx = 0;
            for (let i = 0; i < particles.length; i++) {{
                const p = particles[i];
                const age = (playbackTime - p.birth) * 60; // minutes
                const matchesMode = (displayMode === 'combined') || (displayMode === p.type);
                // Cull: must be active, not past safety cap, and still have mass
                if (!(age >= 0 && age < SAFETY_MAX_AGE && activeFacilities[p.fac] && activeChemicals[p.fac][p.chem] && matchesMode)) continue;
                if (p.mass !== undefined && p.mass <= DEP_MASS_FLOOR) continue;

                // Active Grid Boundary Truncation & Proximity Fade
                const borderLat = 0.005;
                const borderLon = 0.005;
                let fade = 1.0;
                if (p.lat < latMin + borderLat) fade = Math.min(fade, (p.lat - latMin) / borderLat);
                if (p.lat > latMax - borderLat) fade = Math.min(fade, (latMax - p.lat) / borderLat);
                if (p.lon < lonMin + borderLon) fade = Math.min(fade, (p.lon - lonMin) / borderLon);
                if (p.lon > lonMax - borderLon) fade = Math.min(fade, (lonMax - p.lon) / borderLon);
                p.boundaryFade = Math.max(0.0, Math.min(1.0, fade));

                if (p.lat < latMin || p.lat > latMax || p.lon < lonMin || p.lon > lonMax) continue;

                const ageH = playbackTime - p.birth;
                const baseTurb   = p.type === 'fugitive' ? TURB_BASE   * 1.5 : TURB_BASE;
                const turbGrowth = p.type === 'fugitive' ? TURB_GROWTH * 1.5 : TURB_GROWTH;
                const turbMax    = p.type === 'fugitive' ? TURB_MAX    * 1.5 : TURB_MAX;
                const ageTurb = Math.min(turbMax, baseTurb + turbGrowth * ageH);
                const wind = getWind(playbackTime, p.lat, p.lon, p.type);
                // HYSPLIT IQR spread drives fan-out; age-based turbulence is a floor for calm areas
                const SPREAD_KICK = 2.5;
                const spreadLat = Math.max(ageTurb, (wind.sLat || 0) * SPREAD_KICK);
                const spreadLon = Math.max(ageTurb, (wind.sLon || 0) * SPREAD_KICK);
                
                // Balance random-walk dispersion near source clusters and at low velocities
                const windMag = Math.hypot(wind.dLat, wind.dLon);
                const noiseScale = Math.min(1.0, ageH * 4.0) * Math.min(1.0, windMag / 0.01);
                // Deterministic advection (wind + directional fan-out) × dtHours; random-walk jitter
                // × dtHours × randCorr so its diffusion is frame-rate-independent (no shakiness).
                p.lat += (wind.dLat + p.tLat * spreadLat) * dtHours + (Math.random() - 0.5) * spreadLat * 0.4 * noiseScale * dtHours * randCorr;
                p.lon += (wind.dLon + p.tLon * spreadLon) * dtHours + (Math.random() - 0.5) * spreadLon * 0.4 * noiseScale * dtHours * randCorr;
                if (p.type === 'fugitive') {{
                    p.ht = Math.max(0, Math.min(10, p.ht + (Math.random() - 0.5) * 1 * dtHours));
                }} else {{
                    p.ht = Math.max(0, p.ht + (Math.random() - 0.5) * 3 * dtHours);
                }}

                // ── FOOTPRINT GATING: lifetime + opacity from HYSPLIT air contour ──
                // Query the HYSPLIT Ground-Level Air footprint for this particle's
                // facility, chemical, and source type. If inside, lerp mass toward
                // the band brightness; if outside, rapid fade to death.
                const facName = PLUME_DATA.facilities[p.fac].name;
                const gateType = (displayMode === 'combined') ? p.type : displayMode;
                const b = airBandAtPoint(facName, p.chem, gateType, p.lat, p.lon);

                if (b === null) {{
                    // Outside all air contour bands → fading out. TIME-BASED (frame-rate
                    // independent): ~0.55h e-folding → ~1.5h to the death floor. Survives a
                    // brief excursion so it can re-enter the hour-to-hour shifting plume,
                    // instead of dying the instant it clips a contour edge (the old per-call
                    // *0.85 killed particles in a fraction of a sim-hour at 60fps).
                    p.mass *= Math.exp(-dtHours / 0.55);
                }} else {{
                    // Inside plume → ease mass toward the band brightness (dense/bright near
                    // source, faint at the edge). Time-based convergence (~0.25h) so the look
                    // is identical regardless of frame rate.
                    const target = bandToBrightness(b, 5);
                    const k = 1.0 - Math.exp(-dtHours / 0.25);
                    p.mass = p.mass + k * (target - p.mass);
                }}

                // [Removed: the per-particle liveDepGrid accumulation. It ran string-key + Map ops
                //  for every particle every frame but only fed renderDepositionHeatmap(), which is
                //  disabled — pure dead-weight CPU/heat. Deposition is shown via the HYSPLIT footprint
                //  contours (depositionArchive), not this grid.]

                /* [COMMENTED OUT — old vd-based mass drain, replaced by footprint gating above]
                // Dry deposition: near-surface particles lose mass proportional to Vd (m/s)
                if (p.mass !== undefined && p.ht < 30.0) {{
                    const chemKey = p.chem.toUpperCase();
                    const chemProp = PLUME_DATA.chemical_properties[chemKey] || {{vd: 0.003}};
                    const vd = chemProp.vd || 0.003;
                    const fraction = Math.min(0.15, (vd * dtSec) / 30.0);
                    const dDep = p.mass * fraction;
                    p.mass -= dDep;

                    // Accumulate deposited mass into the live grid
                    const cellLat = Math.round(p.lat / grid_spacing) * grid_spacing;
                    const cellLon = Math.round(p.lon / grid_spacing) * grid_spacing;
                    const cellKey = cellLat.toFixed(4) + ',' + cellLon.toFixed(4);
                    let cell = liveDepGrid.get(cellKey);
                    if (!cell) {{
                        cell = {{ lat: cellLat, lon: cellLon, val: 0.0 }};
                        liveDepGrid.set(cellKey, cell);
                    }}
                    cell.val += dDep;
                    if (cell.val > liveDepMax) liveDepMax = cell.val;
                }}
                */

                particles[writeIdx++] = p;
            }}
            particles.length = writeIdx;
        }}
        
        // ── Deterministic jitter to de-cluster co-located dots ──
        function jHash(a, b) {{
            const s = a * 2654435761 + b * 340573321;
            return ((s >>> 0) % 1000) / 1000.0;
        }}

        // Hex color cache — facility colors are static, parse once
        const _hexRgbCache = {{}};
        function getHexRgb(hex) {{
            if (_hexRgbCache[hex]) return _hexRgbCache[hex];
            const r = parseInt(hex.slice(1,3), 16);
            const g = parseInt(hex.slice(3,5), 16);
            const b = parseInt(hex.slice(5,7), 16);
            return (_hexRgbCache[hex] = {{r, g, b}});
        }}

        // Persistent per-opacity-bucket arrays — reset length each frame, never reallocated
        const _renderBuckets = new Map();

        // ── Draw all active particles ──
        // Optimized: 3 Leaflet projections per frame (was ~4000), zero LatLng allocs,
        // batched fills grouped by color+opacity bucket, in-place viewport cull.
        function drawParticles() {{
            resizeCanvas();  // pins canvas top-left to container [0,0] via transform
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            if (!showParticles) return;

            const liveSize = getSandboxSize();
            const stackOpacity = getSandboxStackOpacity();
            const fugitiveOpacity = getSandboxFugitiveOpacity();

            // Numeric viewport bounds — no LatLng alloc per particle
            const bounds = map.getBounds();
            const margin = 0.05;
            const bS = bounds.getSouth() - margin, bN = bounds.getNorth() + margin;
            const bW = bounds.getWest()  - margin, bE = bounds.getEast()  + margin;

            const activeList = particles;  // always sandbox mode
            document.getElementById('active-count').textContent = activeList.length;

            // ── Particle draw loop ──
            // Each particle is projected exactly with map.latLngToContainerPoint — the same
            // projection Leaflet uses for its (never-drifting) footprints/markers — so particles
            // stay locked to the map at every zoom/pan. Canvas top-left = container [0,0] (set via
            // transform in resizeCanvas), so a container point IS a canvas pixel.
            const baseR = Math.max(1.0, liveSize);
            for (let i = 0; i < activeList.length; i++) {{
                const p = activeList[i];

                // Fast numeric viewport cull
                if (p.lat < bS || p.lat > bN || p.lon < bW || p.lon > bE) continue;

                // Fade: mass-based (footprint-gated)
                const ageFade = (p.mass !== undefined)
                    ? Math.max(0, (p.mass - DEP_MASS_FLOOR) / (1.0 - DEP_MASS_FLOOR)) : 1.0;
                if (ageFade <= 0.01) continue;

                const typeOpacityCap = (p.type === 'fugitive') ? fugitiveOpacity : stackOpacity;
                const boundaryFade = (p.boundaryFade !== undefined) ? p.boundaryFade : 1.0;
                const opacity = ageFade * typeOpacityCap * (p.fadeMod !== undefined ? p.fadeMod : 1.0) * boundaryFade;
                if (opacity <= 0.01) continue;

                const hBonus = Math.min(1.2, p.ht / 250.0);
                const radius = Math.max(0.8, Math.min(liveSize * 2.5, baseR * (1.0 + hBonus)));

                // Exact per-particle projection (container point = canvas pixel), + small jitter
                const jx = (jHash(i, p.fac) - 0.5) * 2.5;
                const jy = (jHash(i + 7919, p.fac) - 0.5) * 2.5;
                const cp = map.latLngToContainerPoint(L.latLng(p.lat, p.lon));
                const px = cp.x + jx;
                const py = cp.y + jy;

                // Dark contrast halo under each particle so light facility colors
                // (cyan/yellow/lime) stay visible on the light Voyager basemap.
                ctx.beginPath();
                ctx.arc(px, py, radius * 1.6, 0, 6.2832);
                ctx.fillStyle = 'rgba(15,18,28,' + (opacity * 0.40) + ')';
                ctx.fill();

                // Colored particle dot (facility color)
                const rgb = getHexRgb(p.col);
                ctx.beginPath();
                ctx.arc(px, py, radius, 0, 6.2832);
                ctx.fillStyle = 'rgba(' + rgb.r + ',' + rgb.g + ',' + rgb.b + ',' + opacity + ')';
                ctx.fill();
            }}
        }}

        // Playback speed mapping
        function getSpeedMultiplier() {{
            const selectVal = parseInt(document.getElementById('speed-select').value);
            switch(selectVal) {{
                case 1: return 1.0 / 60.0;
                case 2: return 5.0 / 60.0;
                case 3: return 10.0 / 60.0;
                case 4: return 30.0 / 60.0;
                case 5: return 60.0 / 60.0;
                default: return 5.0 / 60.0;
            }}
        }}

        // HUD State update
        const timeSlider = document.getElementById('time-slider');
        const timeValDisplay = document.getElementById('time-display');
        const ampmDisplay = document.getElementById('ampm-display');
        const timeDateDisplay = document.getElementById('time-date-display');

        function updateHUD() {{
            timeSlider.value = playbackTime.toFixed(2);
            const {{ time, ampm, date }} = formatSimulationTime(playbackTime);
            timeValDisplay.textContent = time;
            ampmDisplay.textContent = ampm;
            if (timeDateDisplay) timeDateDisplay.textContent = date || '';

            let currentHourInt = Math.floor(playbackTime);
            if (currentHourInt < 0) currentHourInt = 0;
            if (currentHourInt > 23) currentHourInt = 23;
            updateMonitorPopups(currentHourInt);
        }}

        // Slider scrub
        timeSlider.addEventListener('input', (e) => {{
            const newTime = parseFloat(e.target.value);
            if (Math.abs(newTime - playbackTime) > 0.3) {{
                particles = [];
                nextSandboxId = 0;
                lastSpawnTime = -999;
            }}
            playbackTime = newTime;
            prevPlaybackTime = playbackTime;
            // Refresh HYSPLIT particles on scrub
            // [Particle rework: always sandbox mode, no HYSPLIT replay on scrub]
            updateHUD();
            drawParticles();
            refreshDepLayers();
        }});

        // Tooltip hover
        const tooltip = document.getElementById('tooltip');
        const tooltipTitle = document.getElementById('tooltip-title');
        const tooltipBody = document.getElementById('tooltip-body');
        
        let lastMouseEvt = null;
        function updateTooltip(e) {{
            if (!e) return;
            const mp = e.containerPoint;
            let hit = null;
            
            // Query the active particle list (HYSPLIT or sandbox)
            const queryList = particles;  // always sandbox mode
            for (let i = 0; i < queryList.length; i++) {{
                const p = queryList[i];
                const pt = map.latLngToContainerPoint(L.latLng(p.lat, p.lon));
                if (Math.hypot(pt.x - mp.x, pt.y - mp.y) < 8) {{
                    hit = p;
                    break;
                }}
            }}
            
            if (hit) {{
                const fac = PLUME_DATA.facilities[hit.fac];
                tooltipTitle.textContent = fac.name;
                tooltipTitle.style.color = fac.color;
                // For HYSPLIT particles, age comes directly from the field; for sandbox, calculate from birth
                const ageMin = ((playbackTime - hit.birth) * 60).toFixed(0);
                const sourceLabel = '⛗️ HYSPLIT-Gated';
                tooltipBody.innerHTML = `
                    <span style="font-size:10px;color:#6b7280;">` + sourceLabel + `</span><br/>
                    Chemical: <strong>` + hit.chem + `</strong><br/>
                    Type: <strong>` + hit.type.toUpperCase() + `</strong><br/>
                    Lat/Lon: <strong>` + hit.lat.toFixed(4) + `, ` + hit.lon.toFixed(4) + `</strong><br/>
                    Release height: <strong>` + hit.ht.toFixed(0) + ` m AGL</strong><br/>
                    Age: <strong>` + ageMin + ` min</strong>
                `;
                tooltip.style.left = (mp.x + 15) + "px";
                tooltip.style.top = (mp.y + 15) + "px";
                tooltip.style.display = 'block';
                // Hide the deposition readout popup to prevent double-popup overlap
                depReadoutEl.style.display = 'none';
            }} else {{
                // [Particle rework: old liveDepGrid "Surface Deposition" tooltip removed —
                //  dep-readout (#dep-readout) is the sole deposition hover (per-facility % attribution).
                //  Old HYSPLIT deposition grid tooltip path also removed below:]
                // [Particle rework: HYSPLIT deposition grid tooltip path removed —
                //  live deposition tooltip above covers the sandbox/footprint-gated path]
                /*
                    const depGrid = PLUME_DATA.deposition_grid;
                    if (depGrid && depGrid.hours && depGrid.max_val > 0) {{
                        const hi = Math.max(0, Math.min(depGrid.hours.length - 1, Math.floor(playbackTime)));
                        const hourData = depGrid.hours[hi];
                        if (hourData && hourData.cells && hourData.cells.length > 0) {{
                            const mouseLat = e.latlng.lat;
                            const mouseLon = e.latlng.lng;
                            let closestCell = null;
                            let minDist = 0.0015;
                            for (let c = 0; c < hourData.cells.length; c++) {{
                                const cell = hourData.cells[c];
                                const dist = Math.hypot(cell.lat - mouseLat, cell.lon - mouseLon);
                                if (dist < minDist) {{ minDist = dist; closestCell = cell; }}
                            }}
                            if (closestCell) {{
                                tooltipTitle.textContent = "🌡️ Surface Deposition";
                                tooltipTitle.style.color = "#f59e0b";
                                const intensity = closestCell.val / depGrid.max_val;
                                let risk = "Low"; let riskColor = "#22c55e";
                                if (intensity >= 0.5) {{ risk = "High"; riskColor = "#ef4444"; }}
                                else if (intensity >= 0.15) {{ risk = "Moderate"; riskColor = "#f59e0b"; }}
                                const displayVal = closestCell.val >= 0.01 ? closestCell.val.toFixed(4) : closestCell.val.toExponential(3);
                                tooltipBody.innerHTML = `
                                    Lat/Lon: <strong>` + closestCell.lat.toFixed(4) + `, ` + closestCell.lon.toFixed(4) + `</strong><br/>
                                    Accumulated Mass: <strong>` + displayVal + ` g/m²</strong><br/>
                                    Deposition Level: <strong style="color: ` + riskColor + `;">` + risk + `</strong>
                                `;
                                tooltip.style.left = (mp.x + 15) + "px";
                                tooltip.style.top = (mp.y + 15) + "px";
                                tooltip.style.display = 'block';
                                return;
                            }}
                        }}
                    }}
                */
                tooltip.style.display = 'none';
            }}
        }}

        map.on('mousemove', (e) => {{
            lastMouseEvt = e;
            updateTooltip(e);
        }});
        
        map.on('mouseout', () => {{
            tooltip.style.display = 'none';
            lastMouseEvt = null;
        }});

        // Play/Pause
        const playBtn = document.getElementById('play-btn');
        const playIcon = document.getElementById('play-icon');
        const pauseIcon = document.getElementById('pause-icon');
        
        playBtn.addEventListener('click', () => {{
            isPlaying = !isPlaying;
            if (isPlaying) {{
                playIcon.style.display = 'none';
                pauseIcon.style.display = 'block';
            }} else {{
                playIcon.style.display = 'block';
                pauseIcon.style.display = 'none';
            }}
        }});

        document.getElementById('restart-btn').addEventListener('click', () => {{
            playbackTime = 0.0;
            prevPlaybackTime = 0.0;
            particles = [];
            nextSandboxId = 0;
            lastSpawnTime = -999;
            liveDepGrid = new Map();
            liveDepMax = 0;
            if (depositionHeatLayer) {{ map.removeLayer(depositionHeatLayer); depositionHeatLayer = null; }}
            updateHUD();
            drawParticles();
            refreshDepLayers();
        }});

        // Map redraws
        map.on('move', drawParticles);
        map.on('move', () => {{
            if (showDeposition && depositionHeatLayer && depositionHeatLayer._reset)
                depositionHeatLayer._reset();
        }});
        map.on('zoom', drawParticles);
        map.on('zoomend', () => {{
            // Canvas is transform-positioned + particles are projected exactly, so a plain redraw
            // stays aligned. (The tick loop also redraws every frame; this keeps paused pans crisp.)
            resizeCanvas();
            drawParticles();
            if (showDeposition) {{
                if (depositionHeatLayer) {{ map.removeLayer(depositionHeatLayer); depositionHeatLayer = null; }}
                lastDepUpdateTime = -999;
                renderDepositionHeatmap(playbackTime);
            }}
        }});
        map.on('resize', () => {{
            resizeCanvas();
            drawParticles();
        }});

        // ── Deposition Heatmap Layer ──
        // Renders HYSPLIT surface deposition (level 0) as colored grid cells.
        // Toggle on/off via the checkbox. Color scale: yellow → orange → red → deep red.
        let depositionHeatLayer = null;
        {{ const _pTog = document.getElementById('particles-toggle'); if (_pTog) showParticles = _pTog.checked; }}
        {{ const _dTog = document.getElementById('deposition-toggle'); if (_dTog) showDeposition = _dTog.checked; }}
        let lastDepositionHour = -1;
        let lastDepUpdateTime = -999; // throttle sub-hour deposition updates
        let lastDepRenderMs = 0; // real-time throttle for deposition re-render
        let liveDepGrid = new Map(); // cellKey -> accumulated deposited mass (grows as particles deposit)
        let liveDepMax = 0;          // current max value for normalization
        
        // Custom warm gradient for the heatmap canvas
        // Creates a smooth yellow → orange → red → deep red gradient
        const depositionGradient = {{
            0.0: 'rgba(255, 255, 100, 0)',
            0.15: 'rgba(255, 255, 50, 0.4)',
            0.35: 'rgba(255, 200, 0, 0.55)',
            0.5: 'rgba(255, 150, 0, 0.65)',
            0.7: 'rgba(255, 80, 0, 0.75)',
            0.85: 'rgba(220, 30, 0, 0.85)',
            1.0: 'rgba(160, 0, 0, 0.95)'
        }};
        
        function getHeatmapOptionsForZoom(zoom) {{
            // Adjust radius and blur dynamically with zoom to ensure smooth overlap
            if (zoom <= 10) return {{ radius: 12, blur: 10 }};
            if (zoom === 11) return {{ radius: 15, blur: 12 }};
            if (zoom === 12) return {{ radius: 22, blur: 16 }};
            if (zoom === 13) return {{ radius: 32, blur: 22 }};
            if (zoom === 14) return {{ radius: 48, blur: 30 }};
            if (zoom === 15) return {{ radius: 72, blur: 45 }};
            if (zoom === 16) return {{ radius: 110, blur: 65 }};
            return {{ radius: 160, blur: 90 }};
        }}

        function renderDepositionHeatmap(fracTime) {{
            // DISABLED: the leaflet.heat heatmap uses a fixed PIXEL radius, so it visually drifts off
            // the point sources when zooming out, and it duplicates the geo-anchored GeoJSON contour
            // footprints (depPane/airPane via refreshDepLayers), which are the canonical deposition
            // layer and stay correctly aligned at every zoom. Re-enable/rework in the particle pass.
            if (depositionHeatLayer) {{ map.removeLayer(depositionHeatLayer); depositionHeatLayer = null; }}
            return;
            // eslint-disable-next-line no-unreachable
            if (!showDeposition) {{
                if (depositionHeatLayer) {{ map.removeLayer(depositionHeatLayer); depositionHeatLayer = null; }}
                return;
            }}

            const heatPoints = [];

            // [Particle rework: always sandbox mode — live dep path always active]
            if (true) {{
                // ── Live sandbox path: build heatmap directly from running deposition accumulator ──
                if (liveDepMax <= 0) {{
                    if (depositionHeatLayer) {{ map.removeLayer(depositionHeatLayer); depositionHeatLayer = null; }}
                    return;
                }}
                const depGrid = PLUME_DATA.deposition_grid;
                const maxVal = (depGrid && depGrid.max_val > 0) ? depGrid.max_val : liveDepMax;
                for (const cell of liveDepGrid.values()) {{
                    const rel = cell.val / maxVal;
                    const intensity = Math.min(1.0, rel); // Linear scale!
                    if (intensity >= 0.003) {{
                        heatPoints.push([cell.lat, cell.lon, intensity]);
                    }}
                }}
            }} else {{
                // ── HYSPLIT reference path: render current hour precomputed snapshot directly ──
                // Bypasses interpolation to eliminate thousands of string allocations and Map lookups per second
                const depGrid = PLUME_DATA.deposition_grid;
                if (!depGrid || !depGrid.hours || depGrid.max_val <= 0) return;

                const h0 = Math.max(0, Math.min(depGrid.hours.length - 1, Math.floor(fracTime)));
                const hourData = depGrid.hours[h0];
                if (hourData && hourData.cells) {{
                    const maxVal = depGrid.max_val;
                    for (let i = 0; i < hourData.cells.length; i++) {{
                        const cell = hourData.cells[i];
                        const intensity = cell.val / maxVal;
                        if (intensity >= 0.005) {{
                            heatPoints.push([cell.lat, cell.lon, intensity]);
                        }}
                    }}
                }}
            }}

            if (heatPoints.length === 0) {{
                if (depositionHeatLayer) {{ map.removeLayer(depositionHeatLayer); depositionHeatLayer = null; }}
                return;
            }}

            const zoomOpts = getHeatmapOptionsForZoom(map.getZoom());
            if (!depositionHeatLayer) {{
                depositionHeatLayer = L.heatLayer(heatPoints, {{
                    radius: zoomOpts.radius,
                    blur: zoomOpts.blur,
                    maxZoom: 17,
                    max: 1.0,
                    minOpacity: 0.08,
                    gradient: depositionGradient
                }}).addTo(map);
            }} else {{
                depositionHeatLayer.setLatLngs(heatPoints);
                depositionHeatLayer.redraw();
            }}
        }}
        
        // Particles toggle event handler (element may be absent in some builds)
        {{ const _pTog2 = document.getElementById('particles-toggle');
           if (_pTog2) _pTog2.addEventListener('change', (e) => {{ showParticles = e.target.checked; }}); }}

        // Deposition toggle event handler (element may be absent in some builds)
        {{ const _dTog2 = document.getElementById('deposition-toggle');
           if (_dTog2) _dTog2.addEventListener('change', (e) => {{
            showDeposition = e.target.checked;
            const _legend = document.getElementById('deposition-legend');
            if (_legend) _legend.style.display = showDeposition ? 'block' : 'none';

            const depSourceContainer = document.getElementById('deposition-source-container');
            if (depSourceContainer) {{
                depSourceContainer.style.display = showDeposition ? 'block' : 'none';
            }}

            lastDepositionHour = -1;  // kept for compat
            lastDepUpdateTime = -999;
            if (depositionHeatLayer) {{ map.removeLayer(depositionHeatLayer); depositionHeatLayer = null; }}
            renderDepositionHeatmap(playbackTime);
        }}); }}

        function updateDepositionSourceSelect() {{
            const selectEl = document.getElementById('deposition-source-select');
            if (!selectEl) return;
            
            // Save currently selected value
            const currentVal = selectEl.value;
            
            // Clear current options
            selectEl.innerHTML = '';
            
            // HYSPLIT option
            const hasHysplit = !!(PLUME_DATA && PLUME_DATA.hysplit_deposition_grid);
            const hysplitOpt = document.createElement('option');
            hysplitOpt.value = 'hysplit';
            hysplitOpt.textContent = 'HYSPLIT Residence Footprint (Reference)';
            if (!hasHysplit) {{
                hysplitOpt.disabled = true;
                hysplitOpt.textContent += ' - Not Available';
            }}
            selectEl.appendChild(hysplitOpt);

            // Sandbox option
            const sandboxOpt = document.createElement('option');
            sandboxOpt.value = 'sandbox';
            sandboxOpt.textContent = 'Live Deposition (Physics)';
            selectEl.appendChild(sandboxOpt);
            
            // Default to sandbox for smooth continuous emission from point sources.
            // HYSPLIT option remains available for exact trajectory playback.
            if (currentVal && currentVal !== '') {{
                selectEl.value = currentVal; // preserve user's previous choice
            }} else {{
                selectEl.value = 'sandbox';
            }}
        }}

        // [COMMENTED OUT — particle rework: deposition source toggle removed.
        //  Particle system is always footprint-gated wind-advected. Kept as reference.]
        /*
        // Listen for deposition source changes
        // Also switch particle source to match deposition source for visual consistency
        const _depSrcSel = document.getElementById('deposition-source-select');
        if (_depSrcSel) _depSrcSel.addEventListener('change', () => {{
            const srcVal = _depSrcSel.value;
            if (srcVal === 'hysplit') {{
                particleSource = 'hysplit';
                particles = []; // clear sandbox particles
                nextSandboxId = 0;
                updateHysplitParticles(playbackTime);
                recalculateDeposition();
            }} else {{
                particleSource = 'sandbox';
                hysplitParticles = []; // clear HYSPLIT particles
                particles = [];
                nextSandboxId = 0;
                liveDepGrid = new Map();
                liveDepMax = 0;
                recalculateDeposition();
            }}
            lastDepositionHour = -1;
            lastDepUpdateTime = -999;
            if (depositionHeatLayer) {{ map.removeLayer(depositionHeatLayer); depositionHeatLayer = null; }}
            renderDepositionHeatmap(playbackTime);
        }});
        */

        // Main animation loop
        let lastTimestamp = null;
        let lastFrameMs = -1;
        const FRAME_MIN_MS = 1000 / 60;   // cap the sim+render to ~60fps (halves 120Hz ProMotion load
                                          // while keeping motion smooth — 30fps made the per-frame
                                          // turbulence jitter step too large, so particles looked shaky
                                          // and over-diffused late in the day)

        // Reset the frame clock when the tab becomes visible again so we don't take one huge
        // time-step after being backgrounded.
        document.addEventListener('visibilitychange', () => {{ if (!document.hidden) {{ lastTimestamp = null; lastFrameMs = -1; }} }});

        function tick(timestamp) {{
            requestAnimationFrame(tick);   // always keep the loop alive

            // ── Power/heat saver #1: do nothing while the tab is hidden ──
            // Skip the sim + canvas repaint entirely when backgrounded so the page doesn't peg the
            // GPU/CPU in a tab nobody is looking at (browsers throttle rAF here, so this is cheap).
            if (document.hidden) {{ lastTimestamp = timestamp; return; }}

            // ── Power/heat saver #3: frame-rate cap (~30fps) ──
            // rAF fires at the display refresh (60Hz, or 120Hz on ProMotion Macs). Advecting ~1500
            // particles + footprint gating + canvas repaint 120×/sec is what makes the laptop hot.
            // Processing at ~30fps looks smooth for this animation and cuts the work 2–4×. Playback
            // speed is unaffected — dtHours scales with real elapsed time.
            if (lastFrameMs >= 0 && (timestamp - lastFrameMs) < FRAME_MIN_MS - 1) return;
            lastFrameMs = timestamp;

            if (!lastTimestamp) lastTimestamp = timestamp;
            const deltaSec = (timestamp - lastTimestamp) / 1000;
            lastTimestamp = timestamp;

            if (isPlaying) {{
                const hourRate = getSpeedMultiplier();
                const dtHours = deltaSec * hourRate;
                playbackTime += dtHours;

                if (playbackTime > 24.0) {{
                    playbackTime = 0.0;
                    particles = [];
                    nextSandboxId = 0;
                    hysplitParticles = [];
                    lastSpawnTime = -999;
                    liveDepGrid = new Map();
                    liveDepMax = 0;
                }}

                // Crash-proof: a throw in particle/dep code must NEVER freeze the animation loop.
                try {{
                    // Particle rework: always spawn+advect (footprint-gated), no HYSPLIT branch
                    spawnBatch(dtHours);
                    advect(dtHours);
                }} catch (e) {{ if (!window._partErr) {{ console.error('particle update error:', e); window._partErr = true; }} }}

                prevPlaybackTime = playbackTime;

                updateHUD();
                try {{ maybeAnimateDep(); }} catch (e) {{ if (!window._depErr) {{ console.error('dep animate error:', e); window._depErr = true; }} }}

                // ── Power/heat saver #2: only repaint the particle canvas WHILE PLAYING ──
                // When paused the scene is static, so there's nothing to redraw each frame. Every
                // interaction that changes what's on screen (pan, zoom, layer/date/chemical toggles)
                // already calls drawParticles() from its own handler, so the canvas still updates on
                // demand — we just stop repainting 60×/sec at idle. Big CPU/GPU/battery/heat win.
                try {{ drawParticles(); }} catch (e) {{ if (!window._drawErr) {{ console.error('drawParticles error:', e); window._drawErr = true; }} }}
                if (lastMouseEvt && tooltip.style.display === 'block') {{
                    try {{ updateTooltip(lastMouseEvt); }} catch (e) {{}}
                }}
            }}
        }}

        // Boot
        requestAnimationFrame(tick);
        loadDepManifest(activeDate);
    </script>
</body>
</html>
"""
        
        # ── Split the app logic into app.js so it loads AFTER the fetch bootstrap AND stays in global
        #    scope (inline onclick handlers like the vet popup's toggleVetChems rely on globals) ──
        site_dir = os.path.join(self.workspace_dir, self.SITE_DIR)
        os.makedirs(os.path.join(site_dir, "data", "dates"), exist_ok=True)
        marker = "<!-- UI and Rendering Engine Script -->"
        head, _sep, tail = html_content.partition(marker)
        _so = tail.index("<script>") + len("<script>")
        _sc = tail.index("</script>", _so)
        app_js = tail[_so:_sc]
        page_tail = tail[_sc + len("</script>"):]   # closing </body></html>
        index_html = head + page_tail  # marker + app <script> removed; bootstrap (in head) appends app.js

        index_path = os.path.join(site_dir, "index.html")
        app_path = os.path.join(site_dir, "app.js")
        with open(index_path, "w") as f:
            f.write(index_html)
        with open(app_path, "w") as f:
            f.write(app_js)
        print(f"Fetch site written: {index_path} ({len(index_html)/1e3:.0f} KB) + app.js ({len(app_js)/1e6:.2f} MB)")

    def build_site(self):
        """Assemble the deployable fetch-based site from the per-date bundles on disk.

        Scans site/data/dates/*.json, applies retention (newest ROLLING_WINDOW_DAYS daily dates PLUS
        the pinned curated days), prunes bundles outside that set, writes site/data/manifest.json,
        and renders site/index.html + site/app.js. Safe to run any time (no simulation).
        """
        import glob, datetime as _dt
        dates_dir = os.path.join(self.workspace_dir, self.SITE_DIR, "data", "dates")
        os.makedirs(dates_dir, exist_ok=True)
        present = sorted(os.path.basename(p)[:-5] for p in glob.glob(os.path.join(dates_dir, "*.json")))

        # Retention: keep newest N daily dates + all pinned dates that exist on disk.
        rolling = [d for d in present if d not in PINNED_DATES]
        keep_rolling = set(rolling[-ROLLING_WINDOW_DAYS:])
        keep = {d for d in present if d in PINNED_DATES or d in keep_rolling}
        for d in present:
            if d not in keep:
                try:
                    os.remove(os.path.join(dates_dir, f"{d}.json"))
                    print(f"  Pruned old date bundle: {d}")
                except OSError:
                    pass

        # Manifest: pinned days first (labeled), then rolling days ascending; picker defaults to newest.
        kept = sorted(keep)
        entries = []
        for d in kept:
            e = {"date": d}
            if d in PINNED_DATES:
                e["label"] = PINNED_DATES[d]
                e["pinned"] = True
            entries.append(e)
        # Order: rolling dates ascending, pinned appended at the end so "newest" (last) is a real day.
        rolling_entries = [e for e in entries if not e.get("pinned")]
        pinned_entries = [e for e in entries if e.get("pinned")]
        ordered = rolling_entries + pinned_entries
        newest_daily = rolling_entries[-1]["date"] if rolling_entries else (kept[-1] if kept else None)
        manifest = {
            "generated_at": _dt.datetime.utcnow().replace(microsecond=0).isoformat() + "Z",
            "newest": newest_daily,
            "dates": ordered,
        }
        with open(os.path.join(self.workspace_dir, self.SITE_DIR, "data", "manifest.json"), "w") as f:
            json.dump(manifest, f, separators=(",", ":"))
        print(f"Site manifest: {len(ordered)} date(s) ({len(pinned_entries)} pinned), newest={newest_daily}")
        self.generate_web_visualization(manifest)
        return manifest

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Calvert City Plume Dispersion Simulation Pipeline")
    parser.add_argument(
        "--workspace",
        default=os.path.dirname(os.path.abspath(__file__)),
        help="Workspace directory containing calculations and web assets"
    )
    parser.add_argument(
        "--skip-weather",
        action="store_true",
        help="Skip weather downloading and conversion if MET file is already created"
    )
    parser.add_argument(
        "--stream-weather", action="store_true",
        help="Disk-frugal weather build (download each HRRR hour, convert, delete it) — keeps peak disk "
             "to ~one ARL + one GRIB. For CI runners with limited disk. Implies no GRIB cache is kept."
    )
    parser.add_argument(
        "--regen-html",
        action="store_true",
        help="Skip ALL simulation steps and only regenerate the HTML visualization "
             "using data already embedded in the existing index.html"
    )
    parser.add_argument(
        "--date", action="append", default=None, metavar="YYYY-MM-DD",
        help="Target date(s) to simulate, overriding START_DATE/END_DATE. Repeatable, or comma-separated. "
             "Each date is simulated then written as a per-date bundle under site/data/dates/."
    )
    parser.add_argument(
        "--cleanup", action="store_true",
        help="After a date's outputs are written, delete its transient weather + run files "
             "(MET_<date>.ARL, dep_runs/<date>/, and the HRRR GRIB cache) to bound disk use. For CI/cron."
    )
    parser.add_argument(
        "--build-site", action="store_true",
        help="Skip simulation; (re)build the fetch-based site from existing per-date bundles: "
             "write site/data/manifest.json and the small site/index.html (retention applied)."
    )
    parser.add_argument(
        "--no-build-site", action="store_true",
        help="With --date, write the per-date bundle(s) but do NOT rebuild the site afterward "
             "(the orchestrator rebuilds once at the end)."
    )

    args = parser.parse_args()

    # Normalize --date: allow repeated flags and/or comma-separated values.
    _cli_dates = None
    if args.date:
        _cli_dates = []
        for _d in args.date:
            _cli_dates.extend([x.strip() for x in _d.split(",") if x.strip()])

    # Run the full pipeline orchestration
    try:
        pipeline = CalvertCityPlumeEngine(
            workspace_dir=args.workspace
        )

        # Step 1: Programmatically generate the list of dates between START_DATE and END_DATE
        start_dt = datetime.datetime.strptime(START_DATE, "%Y-%m-%d")
        end_dt = datetime.datetime.strptime(END_DATE, "%Y-%m-%d")
        delta = datetime.timedelta(days=1)

        date_list = []
        curr_dt = start_dt
        while curr_dt <= end_dt:
            date_list.append(curr_dt.strftime("%Y-%m-%d"))
            curr_dt += delta

        # --date overrides the START_DATE..END_DATE range.
        if _cli_dates:
            date_list = _cli_dates

        # ── Site-only modes (no simulation): assemble the fetch site from existing bundles ──
        if args.build_site or args.regen_html:
            what = "--build-site" if args.build_site else "--regen-html"
            print(f"\n{what}: assembling the fetch-based site from existing per-date bundles (no simulation).")
            pipeline.build_site()
            print("\nSite build complete.")
            sys.exit(0)

        # ── Full pipeline per target date → one per-date bundle each ──
        for d_str in date_list:
            print(f"\n========================================================")
            print(f" PROCESSING SIMULATION FOR DATE: {d_str}")
            print(f"========================================================\n")
            pipeline.set_active_date(d_str)

            # Step 1: NOAA HRRR retrieval (skip download+conversion if a complete daily ARL already exists)
            grib_files = []
            if os.path.exists(pipeline.met_file_path) and os.path.getsize(pipeline.met_file_path) >= 10 * 1024 * 1024 * 1024:
                print(f"Existing complete ARL meteorology file found for {d_str}. Skipping weather download and conversion.")
            elif args.stream_weather:
                pipeline.download_and_convert_streaming()   # CI disk-frugal path
            else:
                if args.skip_weather:
                    date_folder_str = pipeline.date_obj.strftime("%Y%m%d")
                    grib_pattern = os.path.join(pipeline.grib_dir, "hrrr", date_folder_str, "**", "*.grib2")
                    grib_files = sorted(glob.glob(grib_pattern, recursive=True))
                    if not grib_files:
                        grib_files = sorted(glob.glob(os.path.join(pipeline.grib_dir, f"*{date_folder_str}*.grib2")))
                    if grib_files:
                        print(f"Skipping weather download. Found {len(grib_files)} existing GRIB files for {d_str}.")
                    else:
                        print(f"No cached GRIB/ARL for {d_str}. Running download...")
                        grib_files = pipeline.download_weather_data()
                else:
                    grib_files = pipeline.download_weather_data()
                pipeline.convert_grib_to_arl(grib_files)

            # Step 2-3.5: HYSPLIT particles + compile + deposition footprints
            raw_output, deposition_data = pipeline.run_dispersion_model()
            compiled_json = pipeline.compile_data_for_json(raw_output, deposition_data)
            print("\n========================================\nRunning Deposition Pipeline")
            pipeline.run_deposition_pipeline()
            pipeline.build_combined_chemical_outputs()

            # Step 4: write this day's fetch bundle (site/data/dates/<date>.json)
            pipeline.write_date_bundle(d_str, compiled_json, pipeline.regional_monitor_data)

            # Step 5: optional cleanup of this date's multi-GB transients (for CI/cron disk limits)
            if args.cleanup:
                pipeline.cleanup_transient(d_str)

        # Step 6: rebuild the site (manifest + index.html + app.js), unless the orchestrator defers it.
        if not args.no_build_site:
            pipeline.build_site()

        print("\nPipeline execution completed successfully!")
        print(f"Site: {os.path.join(pipeline.workspace_dir, pipeline.SITE_DIR, 'index.html')}  "
              f"(preview via the 'View Locally' script; deploy the site/ folder)")

    except Exception as err:
        print(f"\nPipeline failure: {err}", file=sys.stderr)
        sys.exit(1)


