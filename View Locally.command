#!/bin/bash
# ── Preview the Calvert City plume site on your own Mac ──
# Double-click this file. Browsers block the site's data fetches when a page is opened directly
# (file://), so this starts a tiny local web server and opens it in your browser. Close this
# Terminal window (or press Ctrl+C) when you're done.
cd "$(dirname "$0")/site" 2>/dev/null || { echo "Could not find the site/ folder next to this script."; read -r; exit 1; }
PORT=8123
echo "Serving the plume site at:  http://localhost:${PORT}/"
echo "(Close this window or press Ctrl+C to stop.)"
python3 -c "import webbrowser,time; time.sleep(1); webbrowser.open('http://localhost:${PORT}/')" &
python3 -m http.server "$PORT"
