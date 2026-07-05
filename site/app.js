
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
        Object.keys(historicalSimulationArchive).forEach(dateStr => {
            const plumes = historicalSimulationArchive[dateStr].plumes;
            if (plumes.deposition_grid && !plumes.hysplit_deposition_grid) {
                plumes.hysplit_deposition_grid = JSON.parse(JSON.stringify(plumes.deposition_grid));
            }
        });

        // Leaflet Map Initialization
        // zoomAnimation:false — the animated zoom was leaving SVG vector layers (deposition contours,
        // air-monitor circles) mid-transform after a zoom (off-center until a pan re-computed them).
        // Markers reposition individually so they were fine. Instant zoom keeps every layer aligned.
        const map = L.map('map', {
            zoomControl: false,
            maxZoom: 16,
            minZoom: 7,
            zoomAnimation: false
        }).setView([37.0317, -88.3542], 12);
        
        // CartoDB Voyager tile layer (detailed streets, rivers, labels — readable under footprints)
        L.tileLayer('https://{s}.basemaps.cartocdn.com/rastertiles/voyager/{z}/{x}/{y}{r}.png', {
            attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>',
            subdomains: 'abcd',
            maxZoom: 20
        }).addTo(map);
        
        // Custom control layout placement
        L.control.zoom({
            position: 'bottomright'
        }).addTo(map);

        // Stop propagation of mouse wheel and clicks on HUD overlays to prevent map zoom/drag
        ['hud-header-panel', 'hud-legend-panel'].forEach(id => {
            const el = document.getElementById(id);
            if (el) {
                L.DomEvent.disableScrollPropagation(el);
                L.DomEvent.disableClickPropagation(el);
            }
        });
        const ctrlEl = document.querySelector('.hud-controls');
        if (ctrlEl) {
            L.DomEvent.disableScrollPropagation(ctrlEl);
            L.DomEvent.disableClickPropagation(ctrlEl);
        }

        // Stop propagation of mousedown and touchstart inside Leaflet popups
        // to prevent Leaflet from intercepting drag events and disabling selection.
        document.addEventListener('mousedown', function(e) {
            if (e.target.closest('.leaflet-popup')) {
                e.stopPropagation();
            }
        }, true);
        document.addEventListener('touchstart', function(e) {
            if (e.target.closest('.leaflet-popup')) {
                e.stopPropagation();
            }
        }, true);

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

        const DEP_CHEM_NAMES = [
            "VINYL CHLORIDE","1,2-DICHLOROETHANE","BENZENE","1,3-BUTADIENE",
            "XYLENE (MIXED ISOMERS)","TETRACHLOROETHYLENE","1,2,4-TRICHLOROBENZENE",
            "CHLORINE","AMMONIA"
        ];
        const DEP_CHEM_LABELS = {
            "VINYL CHLORIDE":"Vinyl Chloride","1,2-DICHLOROETHANE":"Ethylene Dichloride",
            "BENZENE":"Benzene","1,3-BUTADIENE":"1,3-Butadiene",
            "XYLENE (MIXED ISOMERS)":"Xylenes","TETRACHLOROETHYLENE":"Tetrachloroethylene",
            "1,2,4-TRICHLOROBENZENE":"1,2,4-TCB","CHLORINE":"Chlorine","AMMONIA":"Ammonia"
        };
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
        let depGeoJsonCache = {};
        let depActiveChem = new Set(DEP_CHEM_NAMES);
        let footprintOpacity = 0.45;   // master pane transparency (tunable via sandbox slider)

        (function() {
            const list = document.getElementById('dep-chem-list');
            DEP_CHEM_NAMES.forEach(chem => {
                const lbl = document.createElement('label');
                lbl.className = 'dep-chem-pill';
                lbl.innerHTML = `<input type="checkbox" class="dep-chem-chk" data-chem="${chem}" checked> ${DEP_CHEM_LABELS[chem]}`;
                list.appendChild(lbl);
            });
        })();

        document.querySelectorAll('.dep-chem-chk').forEach(chk => {
            chk.addEventListener('change', () => {
                const chem = chk.dataset.chem;
                const isChecked = chk.checked;
                
                // Update global active set
                depActiveChem = new Set([...document.querySelectorAll('.dep-chem-chk:checked')].map(c => c.dataset.chem));
                
                // Update all facilities' chemical active state for this chemical
                PLUME_DATA.facilities.forEach(fac => {
                    if (activeChemicals[fac.id] && activeChemicals[fac.id][chem] !== undefined) {
                        activeChemicals[fac.id][chem] = isChecked;
                        // Update checkbox in UI
                        const facChk = document.querySelector(`.chem-chk[data-fac="${fac.id}"][data-chem="${chem}"]`);
                        if (facChk) {
                            facChk.checked = isChecked;
                        }
                        // Filter out existing particles of this chemical from map immediately
                        if (!isChecked) {
                            particles = particles.filter(p => p.fac !== fac.id || p.chem !== chem);
                        }
                        // Recalculate facility totals
                        let active_total = 0;
                        fac.chemicals.forEach(c => {
                            if (activeChemicals[fac.id][c.chemical]) {
                                active_total += c.total_lbs || 0;
                            }
                        });
                        const totalLbsLabel = document.getElementById('total-lbs-' + fac.id);
                        if (totalLbsLabel) {
                            totalLbsLabel.textContent = active_total === 0 ? '0.0 lbs' : active_total.toLocaleString(undefined, {maximumFractionDigits: 1}) + ' lbs/yr';
                        }
                        updateFacilityPopup(fac.id);
                    }
                });
                
                refreshDepLayers();
                drawParticles();
            });
        });
        document.getElementById('dep-layer-toggle').addEventListener('change', refreshDepLayers);
        document.getElementById('air-layer-toggle').addEventListener('change', refreshDepLayers);
        // Particle Simulation general on/off (mirrors the dep/air layer toggles).
        {
            const _partTog = document.getElementById('particles-toggle');
            if (_partTog) {
                showParticles = _partTog.checked;
                _partTog.addEventListener('change', (e) => { showParticles = e.target.checked; drawParticles(); });
            }
        }

        // ── Custom info tooltips ──
        // Reparent each .info-pop to <body> so the panel's overflow:hidden (collapse animation)
        // can't clip it, then position it as a fixed, viewport-clamped popup on hover. (The native
        // title= attribute we replaced had a ~3-4s browser delay; this shows instantly.)
        document.querySelectorAll('.dep-info-btn').forEach((btn) => {
            const pop = btn.querySelector('.info-pop');
            if (!pop) return;
            document.body.appendChild(pop);  // escape ancestor overflow clipping
            const place = () => {
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
            };
            btn.addEventListener('mouseenter', place);
            btn.addEventListener('mouseleave', () => { pop.style.display = 'none'; });
        });

        // ── Footprint gating lookup: (facName|chem|srcType) → file key ──
        // Built once when the deposition manifest loads. Used by airBandAtPoint() to
        // gate particle lifetime/opacity against the HYSPLIT air-concentration contours.
        let airFootprintLookup = {};

        function loadDepManifest(dateStr) {
            // Data is embedded inline (depositionArchive) — no fetch (file:// blocks it).
            const entry = (typeof depositionArchive !== 'undefined') ? depositionArchive[dateStr] : null;
            depManifest = entry ? entry.manifest : null;
            depGeoJsonCache = entry ? entry.files : {};

            // Build footprint lookup from per-facility entries
            airFootprintLookup = {};
            if (depManifest) {
                // Per-facility entries (tagged with fac_name, chem, source_type)
                (depManifest.entries || []).forEach(e => {
                    const key = (e.fac_name || '') + '|' + (e.chem || '') + '|' + (e.source_type || '');
                    airFootprintLookup[key] = e.file;
                });
                // Combined entries (keyed as "combined|chem|srcType")
                (depManifest.combined_entries || []).forEach(e => {
                    const st = e.source_type || '';
                    const key = 'combined|' + (e.chem || '') + '|' + st;
                    airFootprintLookup[key] = e.file;
                });
            }

            refreshDepLayers();
        }

        function loadAndRefreshDepLayers() { refreshDepLayers(); }

        // ── Footprint gating: test if a lat/lon is inside a HYSPLIT air contour ──
        // Returns the lowest band number containing the point (highest concentration),
        // or null if outside all bands. Used to gate particle lifetime and opacity.
        function airBandAtPoint(facName, chem, srcType, lat, lon) {
            // Determine which footprint file to query
            let fileKey = airFootprintLookup[facName + '|' + chem + '|' + srcType];
            // Fallback: try combined entry (for display mode 'combined')
            if (!fileKey) fileKey = airFootprintLookup['combined|' + chem + '|'];
            // Fallback: try combined with source type
            if (!fileKey) fileKey = airFootprintLookup['combined|' + chem + '|' + srcType];
            if (!fileKey) return null;

            const fc = depGeoJsonCache[fileKey];
            if (!fc || !fc.features) return null;

            const md = fc.metadata || {};
            const N = md.num_frames || 1;
            const S = (md.start_hour != null) ? md.start_hour : 2;
            const currentFrame = Math.max(0, Math.min(N - 1, Math.floor(playbackTime - S)));

            // Filter features for air layer at current frame
            let bestBand = null;
            for (let i = 0; i < fc.features.length; i++) {
                const f = fc.features[i];
                const props = f.properties;
                if (props.layer !== 'air' || props.hour_frame !== currentFrame) continue;
                const ring = f.geometry.coordinates[0];
                if (ring && depPointInRing(lat, lon, ring)) {
                    const band = props.band || 99;
                    if (bestBand === null || band < bestBand) bestBand = band;
                }
            }
            return bestBand;
        }

        // Map contour band number to brightness/opacity target.
        // Band 1 (near source, highest conc) → ~1.0; Band N (edge) → ~0.15
        function bandToBrightness(band, numBands) {
            if (numBands <= 1) return 1.0;
            return 1.0 - 0.85 * ((band - 1) / (numBands - 1));
        }

        // Animate the real hourly frames keyed to the timeline. Each file carries
        // metadata.num_frames (N) and start_hour (S): frame k = sim hour (k+S).
        // Cross-fade between consecutive hourly frames (per-polygon) for smoothness; the master
        // transparency + the 0→2h fade-in are applied at the PANE level so nothing compounds.
        // Hit-test index of currently-shown footprint polygons (rebuilt each refresh) for hover readout
        let depHitIndex = [];
        // 2b: per-facility hit-test index (not drawn, used for hover attribution %)
        let perFacHitIndex = [];

        function refreshDepLayers() {
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
            let activeCombinedEntries = (depManifest.combined_entries || []).filter(entry => {
                if (displayMode === 'combined') {
                    return entry.source_type === undefined || entry.source_type === null;
                } else {
                    return entry.source_type === displayMode;
                }
            });

            activeCombinedEntries.forEach(entry => {
                if (!depActiveChem.has(entry.chem)) return;
                const fc = depGeoJsonCache[entry.file];
                if (!fc) return;
                const md = fc.metadata || {};
                const N = md.num_frames || 1;
                const S = (md.start_hour != null) ? md.start_hour : 2;

                const fp  = Math.max(0, Math.min(N - 1, hour - S));         // frame position
                const fLow = Math.floor(fp);
                const fHigh = Math.min(N - 1, fLow + 1);
                const frac = fp - fLow;

                const renderLayer = (layerName, layerGroup, paneName, colors, baseAlpha) => {
                    // Keep only bands within ~1.5 decades of the peak concentration (value-based, not
                    // band number) — hides the faint far trails that clip the grid into a "square".
                    const bandVals = (md.band_values || {})[layerName] || {};
                    let peakVal = 0;
                    for (const b in bandVals) if (bandVals[b] > peakVal) peakVal = bandVals[b];
                    const visFloor = peakVal / (layerName === 'dep' ? DEP_VISIBLE_DECADE_RATIO : VISIBLE_DECADE_RATIO);
                    const draw = (frameIdx, factor) => {
                        if (factor <= 0.002) return;
                        const feats = fc.features.filter(f =>
                            f.properties.layer === layerName && f.properties.hour_frame === frameIdx
                            && bandVals[f.properties.band] >= visFloor);
                        if (!feats.length) return;
                        L.geoJSON({type:'FeatureCollection', features:feats}, {
                            pane: paneName,
                            interactive: false,
                            style: f => ({
                                fillColor: colors[Math.min((f.properties.band||1)-1, colors.length-1)],
                                fillOpacity: baseAlpha * factor,   // cross-fade only; master is pane-level
                                stroke: false, weight: 0
                            })
                        }).addTo(layerGroup);
                        if (frameIdx === fLow) {
                            for (const f of feats) depHitIndex.push({
                                chem: entry.chem, fac: md.fac_name, layer: layerName,
                                band: f.properties.band, value: bandVals[f.properties.band],
                                ring: f.geometry.coordinates[0]
                            });
                        }
                    };
                    draw(fLow, 1 - frac);
                    if (fHigh !== fLow) draw(fHigh, frac);
                };

                if (showDep && entry.layers.includes('dep')) renderLayer('dep', depositionLayer, 'depPane', DEP_COLORS, 0.6);
                if (showAir && entry.layers.includes('air')) renderLayer('air', airConcentrationLayer, 'airPane', AIR_COLORS, 0.5);
            });

            // 2b: build per-facility hit-test index for hover attribution %
            // (uses the per-facility entries that are embedded but NOT drawn)
            const activePerFacEntries = (depManifest.entries || []).filter(entry => {
                if (displayMode === 'combined') {
                    return true; 
                } else {
                    return entry.source_type === displayMode;
                }
            });

            activePerFacEntries.forEach(entry => {
                if (!depActiveChem.has(entry.chem)) return;
                if (activeFacilities[entry.fac_id] === false) return;
                if (activeChemicals[entry.fac_id] && activeChemicals[entry.fac_id][entry.chem] === false) return;
                const fc = depGeoJsonCache[entry.file];
                if (!fc) return;
                const md = fc.metadata || {};
                const N = md.num_frames || 1;
                const S = (md.start_hour != null) ? md.start_hour : 2;
                const fp = Math.max(0, Math.min(N - 1, hour - S));
                const fLow = Math.floor(fp);
                for (const layerName of ['dep', 'air']) {
                    if (layerName === 'dep' && !showDep) continue;
                    if (layerName === 'air' && !showAir) continue;
                    const bandVals = (md.band_values || {})[layerName] || {};
                    let peakVal = 0;
                    for (const b in bandVals) if (bandVals[b] > peakVal) peakVal = bandVals[b];
                    const visFloor = peakVal / (layerName === 'dep' ? DEP_VISIBLE_DECADE_RATIO : VISIBLE_DECADE_RATIO);
                    const feats = fc.features.filter(f =>
                        f.properties.layer === layerName && f.properties.hour_frame === fLow
                        && bandVals[f.properties.band] >= visFloor);
                    for (const f of feats) perFacHitIndex.push({
                        chem: entry.chem, fac: md.fac_name, layer: layerName,
                        band: f.properties.band, value: bandVals[f.properties.band],
                        ring: f.geometry.coordinates[0]
                    });
                }
            });
        }

        // Throttled animation tick (called from the main playback loop)
        let _lastDepHour = -999;
        let _lastDepMs = 0;
        function maybeAnimateDep() {
            const hour = (typeof playbackTime === 'number') ? playbackTime : 0;
            // refreshDepLayers() rebuilds hundreds of footprint SVG polygons — expensive. Throttle it
            // to a real-time floor (~150ms = ~6/sec) AND a sim-hour step, so the cross-fade stays
            // smooth without churning the DOM 12×/sec. Big DOM/paint/heat saving.
            const now = (typeof performance !== 'undefined') ? performance.now() : Date.now();
            if (Math.abs(hour - _lastDepHour) >= 0.08 && (now - _lastDepMs) >= 150) {
                _lastDepHour = hour;
                _lastDepMs = now;
                refreshDepLayers();
            }
        }

        // ── Hover concentration readout ──
        // On mouse move, point-in-polygon test the cursor against the currently-shown footprints;
        // the lowest band number containing the point = highest contour level there ("≥ value").
        function depPointInRing(lat, lng, ring) {
            let inside = false;
            for (let i = 0, j = ring.length - 1; i < ring.length; j = i++) {
                const xi = ring[i][0], yi = ring[i][1], xj = ring[j][0], yj = ring[j][1];
                if (((yi > lat) !== (yj > lat)) && (lng < (xj - xi) * (lat - yi) / (yj - yi) + xi))
                    inside = !inside;
            }
            return inside;
        }
        function fmtConc(v, unit) {
            // Contour bands are decades; the true value sits between this level and the next (×10).
            // Show that range so it's clear these are binned, not a single round "filler" number.
            const f = x => x >= 1 ? x.toPrecision(3) : (x >= 0.001 ? x.toPrecision(2) : x.toExponential(1));
            return f(v * 1e6) + '–' + f(v * 1e7) + ' µg/' + unit;
        }
        const depReadoutEl = document.getElementById('dep-readout');
        let _depHoverT = 0;
        map.on('mousemove', (e) => {
            const now = performance.now();
            if (now - _depHoverT < 45) return;
            _depHoverT = now;
            if (!depHitIndex.length && !perFacHitIndex.length) { depReadoutEl.style.display = 'none'; return; }
            const lat = e.latlng.lat, lng = e.latlng.lng;

            // 2b: combined value from depHitIndex (drawn combined footprints)
            // chem -> {dep: value, air: value} — the true merged concentration
            const combAgg = {};
            for (const h of depHitIndex) {
                if (h.value == null) continue;
                if (!depPointInRing(lat, lng, h.ring)) continue;
                const a = combAgg[h.chem] || (combAgg[h.chem] = { dep: null, air: null });
                if (a[h.layer] == null || h.value > a[h.layer]) a[h.layer] = h.value;
            }

            // 2b: per-facility attribution from perFacHitIndex (not drawn)
            // chem -> {dep: {fac: value}, air: {fac: value}}
            const facAgg = {};
            for (const h of perFacHitIndex) {
                if (h.value == null) continue;
                if (!depPointInRing(lat, lng, h.ring)) continue;
                const a = facAgg[h.chem] || (facAgg[h.chem] = { dep: {}, air: {} });
                const lm = a[h.layer];
                if (lm[h.fac] == null || h.value > lm[h.fac]) lm[h.fac] = h.value;
            }

            const chems = Object.keys(combAgg).sort();
            if (!chems.length) { depReadoutEl.style.display = 'none'; return; }
            let html = '<div class="dr-title">AT CURSOR &nbsp;' + lat.toFixed(3) + ', ' + lng.toFixed(3) + '</div>';
            for (const c of chems) {
                html += '<div class="dr-chem">' + (DEP_CHEM_LABELS[c] || c) + '</div>';
                for (const ld of [['dep', 'soil', 'm²'], ['air', 'air', 'm³']]) {
                    const combVal = combAgg[c][ld[0]];
                    if (combVal == null) continue;
                    html += '<div class="dr-row"><span>' + ld[1] + '</span><span>' + fmtConc(combVal, ld[2]) + '</span></div>';
                    // Per-facility attribution breakdown
                    const facs = (facAgg[c] || { dep: {}, air: {} })[ld[0]];
                    const names = Object.keys(facs);
                    if (names.length > 1) {
                        let total = 0; for (const n of names) total += facs[n];
                        names.sort((a, b) => facs[b] - facs[a]);
                        for (const n of names) {
                            const pct = Math.round(100 * facs[n] / total);
                            html += '<div class="dr-row" style="font-size:10px;opacity:.65;padding-left:10px"><span>' + n + '</span><span>' + pct + '%</span></div>';
                        }
                    }
                }
            }
            depReadoutEl.innerHTML = html;
            depReadoutEl.style.display = 'block';
            const cp = e.containerPoint;
            const vp = document.getElementById('map-viewport').getBoundingClientRect();
            let x = cp.x + 16, y = cp.y + 16;
            if (x + 270 > vp.width) x = cp.x - 270;
            depReadoutEl.style.left = x + 'px';
            depReadoutEl.style.top = y + 'px';
        });
        map.on('mouseout', () => { depReadoutEl.style.display = 'none'; });

        const monitorMarkers = [];

        // Populate monitor markers for all unique stations across all dates
        const uniqueStations = {};
        Object.keys(historicalSimulationArchive).forEach(dateStr => {
            const dayMonitors = historicalSimulationArchive[dateStr].monitors;
            Object.keys(dayMonitors).forEach(pollutant => {
                const pData = dayMonitors[pollutant];
                const stations = pData.stations || {};
                
                Object.keys(stations).forEach(stationId => {
                    const station = stations[stationId];
                    const key = pollutant + "_" + stationId;
                    if (!uniqueStations[key]) {
                        uniqueStations[key] = {
                            pollutant: pollutant,
                            stationId: stationId,
                            lat: station.lat,
                            lon: station.lon,
                            unit: pData.unit
                        };
                    }
                });
            });
        });

        // Build leaflet markers from the unique stations list
        Object.keys(uniqueStations).forEach(key => {
            const info = uniqueStations[key];
            const marker = L.circleMarker([info.lat, info.lon], {
                radius: 8,
                fillColor: '#808080',
                color: '#ffffff',
                weight: 2,
                opacity: 0.9,
                fillOpacity: 0.8
            });

            marker.bindPopup('', {
                className: 'custom-leaflet-popup'
            });

            monitorMarkers.push({
                marker: marker,
                pollutant: info.pollutant,
                stationId: info.stationId,
                unit: info.unit
            });
        });

        // Populate pollutant select dropdown
        const pollutantSelect = document.getElementById('pollutant-select');
        Object.keys(regionalMonitorData).forEach(pollutant => {
            const opt = document.createElement('option');
            opt.value = pollutant;
            opt.textContent = pollutant;
            pollutantSelect.appendChild(opt);
        });

        // Configure Date Picker
        const datePicker = document.getElementById('date-picker');
        // Populate the dropdown from whatever dates are embedded (one <option> per available day),
        // so switching between simulation days works regardless of how many are bundled.
        (function initDatePicker() {
            const entries = (typeof PLUME_MANIFEST !== 'undefined' && PLUME_MANIFEST.dates) ? PLUME_MANIFEST.dates : [];
            datePicker.innerHTML = '';
            entries.forEach(entry => {
                const d = entry.date;
                const opt = document.createElement('option');
                opt.value = d;
                const dt = new Date(d + 'T00:00:00');
                let txt = dt.toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' });
                if (entry.label) txt += ' — ' + entry.label;   // pinned curated days show their label
                opt.textContent = txt;
                datePicker.appendChild(opt);
            });
            datePicker.value = activeDate;
        })();

        function syncActiveMonitorLayer(selectedPollutant) {
            activeMonitorLayer.clearLayers();
            monitorMarkers.forEach(m => {
                if (m.pollutant === selectedPollutant) {
                    m.marker.addTo(activeMonitorLayer);
                }
            });
        }

        // Initialize with default pollutant
        const defaultPollutant = regionalMonitorData['VOCs'] ? 'VOCs' : (Object.keys(regionalMonitorData)[0] || 'PM2.5');
        pollutantSelect.value = defaultPollutant;
        syncActiveMonitorLayer(defaultPollutant);

        pollutantSelect.addEventListener('change', (e) => {
            const selected = e.target.value;
            syncActiveMonitorLayer(selected);
            let currentHourInt = Math.floor(playbackTime);
            if (currentHourInt < 0) currentHourInt = 0;
            if (currentHourInt > 23) currentHourInt = 23;
            updateMonitorPopups(currentHourInt);
        });

        // Date Picker Change Event Listener — fetch the day's bundle on demand, then hot-swap.
        datePicker.addEventListener('change', async (e) => {
            const selectedDate = e.target.value;
            try { await pd_fetchDate(selectedDate); }
            catch (err) {
                alert('Could not load ' + selectedDate + ' (' + err.message + '). It may have aged out; try refreshing.');
                datePicker.value = activeDate;   // revert selection
                return;
            }
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
            PLUME_DATA.facilities.forEach(fac => {
                updateFacilityPopup(fac.id);
            });
            updateDepositionSourceSelect();
            recalculateDeposition();
            drawParticles();
            loadDepManifest(selectedDate);
        });

        function getMonitorColorAndStatus(val, thresholds) {
            if (val === null || val === undefined) {
                return { color: '#808080', status: 'No Data' };
            }
            if (val <= thresholds.good) {
                return { color: '#10B981', status: 'Good' };
            } else if (val <= thresholds.mod) {
                return { color: '#F59E0B', status: 'Moderate' };
            } else if (val <= thresholds.unhealthy) {
                return { color: '#EF4444', status: 'Unhealthy' };
            } else {
                return { color: '#8B5CF6', status: 'Very Unhealthy' };
            }
        }

        function updateMonitorPopups(currentHourInt) {
            const selected = document.getElementById('pollutant-select').value;
            monitorMarkers.forEach(m => {
                if (m.pollutant !== selected) return;

                const thresholds = {
                    good: regionalMonitorData[m.pollutant].good,
                    mod: regionalMonitorData[m.pollutant].mod,
                    unhealthy: regionalMonitorData[m.pollutant].unhealthy
                };
                
                const station = regionalMonitorData[m.pollutant].stations[m.stationId];
                if (!station) {
                    m.marker.setStyle({
                        fillColor: '#808080'
                    });
                    m.marker.setPopupContent('<div style="font-family:Inter,sans-serif;font-size:11px;color:#fff;padding:6px;">No data for this station on this day.</div>');
                    return;
                }

                const val = station.hourly_data[currentHourInt];
                const { color, status } = getMonitorColorAndStatus(val, thresholds);
                
                m.marker.setStyle({
                    fillColor: color
                });

                const valStr = (val !== null && val !== undefined) ? (val.toFixed(2) + ' ' + m.unit) : 'No Data';

                let sampleDateRow = '';
                let measuredVocHeader = 'Measured VOC Compounds (' + m.unit + '):';
                if (station.sample_date) {
                    const statusText = station.is_interpolated ? ` (${station.days_diff}d nearest)` : ' (Actual)';
                    const colorStyle = station.is_interpolated ? 'color: #F59E0B;' : 'color: #10B981;';
                    sampleDateRow = 
                        '<tr style="border-bottom: 1px solid rgba(255,255,255,0.05);">' +
                            '<td style="padding: 4px 0; color: #9ca3af;">Sample Date:</td>' +
                            '<td style="padding: 4px 0; font-weight: 600; text-align: right; ' + colorStyle + '">' + station.sample_date + statusText + '</td>' +
                        '</tr>';
                    
                    if (station.is_interpolated) {
                        measuredVocHeader = 'Measured VOC Compounds (' + m.unit + ' - Sampled ' + station.sample_date + '):';
                    }
                }

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
                                Object.keys(station.voc_details).map(compound => {
                                    const cVal = station.voc_details[compound];
                                    const cValStr = cVal !== null ? cVal.toFixed(3) : 'N/A';
                                    return '<div style="display: flex; justify-content: space-between; margin-bottom: 3px; border-bottom: 1px solid rgba(255,255,255,0.02); padding-bottom: 1px;">' +
                                               '<span style="color: #9ca3af; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; max-width: 170px;" title="' + compound + '">' + compound + ':</span>' +
                                               '<span style="font-weight: 600; color: #fff;">' + cValStr + '</span>' +
                                           '</div>';
                                }).join('') +
                                '</div>' +
                            '</div>') : '') +
                    '</div>';

                m.marker.setPopupContent(popupContent);

                if (m.marker.isPopupOpen()) {
                    m.marker.getPopup().setContent(popupContent);
                }
            });
        }

        // State variables
        let isPlaying = true;
        let playbackTime = 0.0; // simulation hour index (0.0 to 24.0)
        let activeFacilities = new Array(PLUME_DATA.facilities.length).fill(true); // boolean array for toggles
        let activeChemicals = {}; // nested object for chemical checkbox toggles
        
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
        function resizeCanvas() {
            const size = map.getSize();
            if (canvas.width !== size.x) canvas.width = size.x;
            if (canvas.height !== size.y) canvas.height = size.y;
            L.DomUtil.setPosition(canvas, map.containerPointToLayerPoint([0, 0]));
        }
        resizeCanvas();
        
        // Helper formatting functions
        function formatSimulationTime(decHours) {
            const totalMinutes = Math.floor(decHours * 60);
            const hours24 = Math.floor(totalMinutes / 60);
            const minutes = totalMinutes % 60;
            
            const hours12 = hours24 % 12 === 0 ? 12 : hours24 % 12;
            const ampm = hours24 >= 12 ? 'PM' : 'AM';
            
            const timeStr = `${String(hours12).padStart(2, '0')}:${String(minutes).padStart(2, '0')}`;
            return { time: timeStr, ampm: ampm };
        }
        
        function hexToRgbA(hex, opacity) {
            if (!hex || hex.indexOf('#') !== 0) return 'rgba(255,255,255,' + opacity + ')';
            let c = hex.substring(1);
            if (c.length === 3) {
                c = c.split('').map(x => x + x).join('');
            }
            if (c.length === 6) {
                const r = parseInt(c.substring(0, 2), 16);
                const g = parseInt(c.substring(2, 4), 16);
                const b = parseInt(c.substring(4, 6), 16);
                return 'rgba(' + r + ',' + g + ',' + b + ',' + opacity + ')';
            }
            return 'rgba(255,255,255,' + opacity + ')';
        }

        // Draw static facilities markers and setup facilityMarkers global dictionary
        const facilityMarkers = {};

        function updateFacilityPopup(facId) {
            const fac = PLUME_DATA.facilities.find(f => f.id === facId);
            const marker = facilityMarkers[facId];
            if (!fac || !marker) return;
            
            let active_stack_total = 0;
            let active_fugitive_total = 0;
            let active_total = 0;
            
            let chemHtml = '';
            fac.chemicals.forEach(c => {
                const isActive = activeChemicals[facId][c.chemical];
                const props = (PLUME_DATA.chemical_properties && PLUME_DATA.chemical_properties[c.chemical]) || { vd: 0, mol_wt: 0, henry_const: 0 };
                const depInfo = `Vd: ${props.vd.toFixed(4)} m/s, MW: ${props.mol_wt.toFixed(1)} g/mol, H: ${props.henry_const !== undefined ? props.henry_const.toExponential(1) : 'N/A'} M/atm`;
                if (isActive) {
                    active_stack_total += c.stack_lbs || 0;
                    active_fugitive_total += c.fugitive_lbs || 0;
                    active_total += c.total_lbs || 0;
                    
                    chemHtml += `<div style="display:flex; justify-content:space-between; gap:10px; margin-top:2px;" title="${depInfo}">
                        <span style="color:#9ca3af; border-bottom: 1px dotted rgba(255,255,255,0.25);">${c.chemical}:</span>
                        <span style="font-weight:600; color:#fff">${c.total_lbs.toLocaleString()} lbs/yr</span>
                    </div>`;
                } else {
                    chemHtml += `<div style="display:flex; justify-content:space-between; gap:10px; margin-top:2px; opacity:0.4;" title="${depInfo}">
                        <span style="color:#9ca3af; text-decoration: line-through;">${c.chemical}:</span>
                        <span style="font-weight:600; color:#9ca3af">0.0 lbs</span>
                    </div>`;
                }
            });
            
            const totalText = active_total === 0 ? '0.0 lbs' : active_total.toLocaleString(undefined, {maximumFractionDigits: 1}) + ' lbs/yr';
            const stackText = active_stack_total === 0 ? '0.0 lbs' : active_stack_total.toLocaleString(undefined, {maximumFractionDigits: 1}) + ' lbs/yr';
            const fugitiveText = active_fugitive_total === 0 ? '0.0 lbs' : active_fugitive_total.toLocaleString(undefined, {maximumFractionDigits: 1}) + ' lbs/yr';
            
            const popupContent = `
                <div style="font-family:'Inter',sans-serif; font-size:12px; color:#f3f4f6; width:240px; background:#121214; padding:6px; border-radius:8px;">
                    <strong style="color:${fac.color}; font-size:13px;">${fac.name}</strong><br/>
                    <span style="font-size:11px; color:#9b9b9b;">TRI ID: ${fac.tri_id}</span>
                    <div style="height:1px; background:#2e2e2e; margin:6px 0;"></div>
                    <div style="font-weight:600; color:#a5b4fc; margin-bottom:4px;">Active Source Strength:</div>
                    <div style="display:flex; justify-content:space-between; font-size:11px; margin-bottom:2px;">
                        <span style="color:#9ca3af">Active Stack:</span>
                        <span style="font-weight:600; color:#fff">${stackText}</span>
                    </div>
                    <div style="display:flex; justify-content:space-between; font-size:11px; margin-bottom:4px;">
                        <span style="color:#9ca3af">Active Fugitive:</span>
                        <span style="font-weight:600; color:#fff">${fugitiveText}</span>
                    </div>
                    <div style="display:flex; justify-content:space-between; font-size:11px; font-weight:700; border-top:1px dashed #2e2e2e; padding-top:4px; margin-bottom:6px;">
                        <span style="color:#a5b4fc">Active Combined:</span>
                        <span style="color:#a5b4fc">${totalText}</span>
                    </div>
                    <div style="height:1px; background:#2e2e2e; margin:6px 0;"></div>
                    <span style="font-weight:500; font-size:11px; color:#a5b4fc;">Annual Chemical Releases:</span>
                    ${chemHtml}
                </div>
            `;
            
            marker.bindPopup(popupContent, {
                className: 'custom-leaflet-popup'
            });
            
            if (marker.isPopupOpen()) {
                marker.getPopup().setContent(popupContent);
            }
        }

        PLUME_DATA.facilities.forEach(fac => {
            const squareIcon = L.divIcon({
                className: 'custom-facility-divicon',
                html: `<div style="background-color: ${fac.color}; border: 1.5px solid #ffffff; width: 10px; height: 10px; box-shadow: 0 0 4px rgba(0,0,0,0.5);"></div>`,
                iconSize: [13, 13],
                iconAnchor: [6.5, 6.5]
            });
            const marker = L.marker([fac.lat, fac.lon], {
                icon: squareIcon
            }).addTo(map);
            
            facilityMarkers[fac.id] = marker;
        });

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
        const vetIcon = L.divIcon({
            className: 'vet-clinic-divicon',
            html: VET_CLINIC_SVG,
            iconSize: [28, 36],
            iconAnchor: [14, 35],     // pin tip sits on the coordinate
            popupAnchor: [0, -30]
        });

        // Soil deposition at a point, from the currently-drawn combined soil footprints (depHitIndex).
        // Returns {maxVal, minBand, chem} or null if the point is outside every dep contour this hour.
        // TRUE soil deposition at a point: queries the combined SOIL footprints directly across ALL
        // bands (not just the drawn/visible ones), so a clinic gets its real value even where the
        // drawn footprint doesn't reach. Matches the current display mode + active chemicals + frame.
        function soilDepAtPoint(lat, lon) {
            if (typeof depManifest === 'undefined' || !depManifest) return null;
            const modeEl = document.getElementById('display-mode-select');
            const wantSrc = (modeEl && modeEl.value !== 'combined') ? modeEl.value : '';
            const hour = (typeof playbackTime === 'number') ? playbackTime : 24;
            const perChem = {};   // chem -> highest soil-dep value covering this point
            (depManifest.combined_entries || []).forEach(entry => {
                if ((entry.source_type || '') !== wantSrc) return;
                if (typeof depActiveChem !== 'undefined' && depActiveChem.size && !depActiveChem.has(entry.chem)) return;
                const fc = depGeoJsonCache[entry.file];
                if (!fc || !fc.features) return;
                const md = fc.metadata || {};
                const N = md.num_frames || 1;
                const S = (md.start_hour != null) ? md.start_hour : 2;
                const fp = Math.max(0, Math.min(N - 1, Math.floor(hour - S)));
                const bv = (md.band_values || {}).dep || {};
                for (const f of fc.features) {
                    if (f.properties.layer !== 'dep' || f.properties.hour_frame !== fp) continue;
                    if (!depPointInRing(lat, lon, f.geometry.coordinates[0])) continue;
                    const v = bv[f.properties.band] || 0;
                    if (!(entry.chem in perChem) || v > perChem[entry.chem]) perChem[entry.chem] = v;
                }
            });
            const list = Object.keys(perChem).map(c => ({ chem: c, val: perChem[c] }))
                                             .sort((a, b) => b.val - a.val);
            return list.length ? { list: list } : null;
        }

        function depRisk(v) {
            if (v >= 1e-4) return { label: 'Elevated', color: '#ef4444' };
            if (v >= 1e-6) return { label: 'Moderate', color: '#f59e0b' };
            if (v >= 1e-8) return { label: 'Low',      color: '#22c55e' };
            return { label: 'Trace', color: '#9ca3af' };
        }

        // Expand/collapse the "+N more" per-chemical deposition list inside a clinic popup.
        function toggleVetChems(el) {
            const list = el.parentElement.querySelector('.vp-chemlist');
            if (!list) return;
            const show = (list.style.display === 'none' || !list.style.display);
            list.style.display = show ? 'block' : 'none';
            const arrow = el.querySelector('.vp-arrow');
            if (arrow) arrow.textContent = show ? '▴' : '▾';
        }

        function vetPopupHtml(cl) {
            const dep = soilDepAtPoint(cl.lat, cl.lon);
            let depHtml;
            if (dep && dep.list.length) {
                const top = dep.list[0];
                const r = depRisk(top.val);
                depHtml = 'Soil deposition here: <strong>' + fmtConc(top.val, 'm²') + '</strong><br/>'
                        + 'Level: <strong style="color:' + r.color + '">' + r.label + '</strong>'
                        + ' <span style="color:#9ca3af">(' + top.chem.toLowerCase() + ')</span>';
                if (dep.list.length > 1) {
                    const extra = dep.list.length - 1;
                    depHtml += ' <span class="vp-more" onclick="toggleVetChems(this)">+' + extra
                             + ' more <span class="vp-arrow">▾</span></span>';
                    // Full per-chemical breakdown with concentrations (hidden until clicked)
                    let rows = '';
                    dep.list.forEach(c => {
                        const cr = depRisk(c.val);
                        rows += '<div class="vp-chemrow"><span>' + c.chem.toLowerCase() + '</span>'
                              + '<span><span style="color:' + cr.color + '">' + fmtConc(c.val, 'm²')
                              + '</span></span></div>';
                    });
                    depHtml += '<div class="vp-chemlist" style="display:none">' + rows + '</div>';
                }
            } else {
                depHtml = '<span style="color:#9ca3af">No modeled soil deposition reaches here at this hour.</span>';
            }
            return '<div class="vet-pop">'
                 + '<div class="vp-title">🐾 ' + cl.name + '</div>'
                 + '<div class="vp-addr">' + cl.address + '</div>'
                 + '<div class="vp-dep">' + depHtml + '</div>'
                 + '</div>';
        }

        const vetClinicLayer = L.layerGroup();
        (typeof VET_CLINICS !== 'undefined' ? VET_CLINICS : []).forEach(cl => {
            const m = L.marker([cl.lat, cl.lon], { icon: vetIcon, title: cl.name });
            m.bindPopup(() => vetPopupHtml(cl), { maxWidth: 260, className: 'vet-popup' });
            vetClinicLayer.addLayer(m);
        });
        vetClinicLayer.addTo(map);   // shown by default; toggleable
        { const _vc = document.getElementById('vet-count'); if (_vc) _vc.textContent = '(' + ((typeof VET_CLINICS !== 'undefined') ? VET_CLINICS.length : 0) + ')'; }

        // LOCATIONS section wiring: Veterinary Clinics on/off + collapsible dropdown
        {
            const vt = document.getElementById('vet-clinics-toggle');
            if (vt) vt.addEventListener('change', e => {
                if (e.target.checked) vetClinicLayer.addTo(map); else map.removeLayer(vetClinicLayer);
            });
            const lt = document.getElementById('locations-toggle');
            const lb = document.getElementById('locations-body');
            const la = document.getElementById('locations-arrow');
            if (lt && lb && la) lt.addEventListener('click', () => {
                const open = lb.classList.toggle('open');
                la.classList.toggle('expanded', open);
            });
        }

        // Legend construction with collapsible dropdowns and total lbs display
        const legendContainer = document.getElementById('facility-legend');
        PLUME_DATA.facilities.forEach(fac => {
            // Initialize active chemical states for this facility based on defaultActive
            activeChemicals[fac.id] = {};
            fac.chemicals.forEach(c => {
                activeChemicals[fac.id][c.chemical] = c.defaultActive;
            });

            const item = document.createElement('div');
            item.className = 'facility-item';
            item.dataset.id = fac.id;
            
            let chemHtml = '';
            fac.chemicals.forEach(c => {
                const isChecked = c.defaultActive ? 'checked' : '';
                const props = (PLUME_DATA.chemical_properties && PLUME_DATA.chemical_properties[c.chemical]) || { vd: 0, mol_wt: 0, henry_const: 0 };
                const depInfo = `Vd: ${props.vd.toFixed(4)} m/s, MW: ${props.mol_wt.toFixed(1)} g/mol, H: ${props.henry_const !== undefined ? props.henry_const.toExponential(1) : 'N/A'} M/atm`;
                chemHtml += `
                    <div class="chem-item" style="margin-bottom: 4px; display: flex; align-items: center; justify-content: space-between; gap: 8px;" title="${depInfo}">
                        <label style="display: flex; align-items: center; gap: 6px; cursor: pointer; font-size: 11px; color: #d1d5db; user-select: none; min-width: 0; flex: 1;">
                            <input type="checkbox" ${isChecked} class="chem-chk" data-fac="${fac.id}" data-chem="${c.chemical}" style="accent-color: ${fac.color}; cursor: pointer; flex-shrink: 0;" />
                            <span style="overflow: hidden; text-overflow: ellipsis; white-space: nowrap; border-bottom: 1px dotted rgba(255,255,255,0.15);">${c.chemical}</span>
                        </label>
                        <span class="chem-val" style="white-space: nowrap; margin-left: 10px; font-size: 11px; color: var(--text-muted);">${c.total_lbs.toLocaleString()} lbs/yr</span>
                    </div>`;
            });
            
            const totalLbsFormatted = fac.total_lbs ? fac.total_lbs.toLocaleString(undefined, {maximumFractionDigits: 1}) : "0";
            
            item.innerHTML = `
                <div class="facility-header" style="display: flex; align-items: center; justify-content: space-between; gap: 8px;">
                    <div class="facility-left-section" style="display: flex; align-items: center; gap: 8px; flex: 1; min-width: 0;">
                        <span class="facility-badge" style="color:${fac.color}; background-color:${fac.color}; flex-shrink: 0;"></span>
                        <div class="facility-info" style="min-width: 0; display: flex; flex-direction: column;">
                            <span class="facility-name" style="white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">${fac.name}</span>
                            <span class="facility-total-lbs" id="total-lbs-${fac.id}" style="font-size: 11px; color: var(--text-muted); font-weight: 500; margin-top: 1px;">
                                ${totalLbsFormatted} lbs/yr
                            </span>
                        </div>
                    </div>
                    <div class="facility-actions" style="display: flex; align-items: center; gap: 8px; flex-shrink: 0;">
                        <span class="toggle-icon" id="toggle-lbl-${fac.id}" style="padding: 4px 6px; border-radius: 4px; font-size: 9px; cursor: pointer; transition: all 0.2s; color: #10B981; background: rgba(16, 185, 129, 0.1); font-weight: 700; letter-spacing: 0.05em;">VISIBLE</span>
                        <span class="dropdown-arrow" id="arrow-${fac.id}" style="font-size: 11px; transition: transform 0.2s; padding: 4px; cursor: pointer; color: var(--text-muted);">▼</span>
                    </div>
                </div>
                <div class="chem-list" id="chem-list-${fac.id}" style="display: none; flex-direction: column; margin-top: 10px; border-top: 1px solid rgba(255, 255, 255, 0.05); padding-top: 8px;">
                    ${chemHtml}
                </div>
            `;
            
            const toggleBtn = item.querySelector(`#toggle-lbl-${fac.id}`);
            const chemList = item.querySelector(`#chem-list-${fac.id}`);
            const arrow = item.querySelector(`#arrow-${fac.id}`);
            
            // Particle visibility toggle
            toggleBtn.addEventListener('click', (e) => {
                e.stopPropagation(); // Prevent dropdown expansion
                activeFacilities[fac.id] = !activeFacilities[fac.id];
                if (activeFacilities[fac.id]) {
                    item.classList.remove('disabled');
                    toggleBtn.textContent = 'VISIBLE';
                    toggleBtn.style.color = '#10B981';
                    toggleBtn.style.background = 'rgba(16, 185, 129, 0.1)';
                } else {
                    item.classList.add('disabled');
                    toggleBtn.textContent = 'HIDDEN';
                    toggleBtn.style.color = 'var(--text-muted)';
                    toggleBtn.style.background = 'rgba(255, 255, 255, 0.05)';
                }
                // Sync map marker visibility
                const marker = facilityMarkers[fac.id];
                if (marker) {
                    if (activeFacilities[fac.id]) {
                        marker.addTo(map);
                    } else {
                        marker.remove();
                    }
                }
                drawParticles();
                refreshDepLayers();
            });

            // Chemical checkbox toggles
            item.querySelectorAll('.chem-chk').forEach(chk => {
                chk.addEventListener('change', (e) => {
                    const facId = parseInt(chk.dataset.fac);
                    const chemName = chk.dataset.chem;
                    activeChemicals[facId][chemName] = chk.checked;
                    
                    // If checked and global pill is unchecked, check it
                    if (chk.checked && !depActiveChem.has(chemName)) {
                        const globalChk = document.querySelector(`.dep-chem-chk[data-chem="${chemName}"]`);
                        if (globalChk) {
                            globalChk.checked = true;
                            depActiveChem.add(chemName);
                        }
                    }
                    
                    // Filter out existing particles of this chemical from map immediately
                    if (!chk.checked) {
                        particles = particles.filter(p => p.fac !== facId || p.chem !== chemName);
                    }
                    
                    // Recalculate totals
                    const facObj = PLUME_DATA.facilities.find(f => f.id === facId);
                    let active_total = 0;
                    facObj.chemicals.forEach(c => {
                        if (activeChemicals[facId][c.chemical]) {
                            active_total += c.total_lbs || 0;
                        }
                    });
                    
                    // Update sidebar total
                    const totalLbsLabel = document.getElementById('total-lbs-' + facId);
                    if (totalLbsLabel) {
                        totalLbsLabel.textContent = active_total === 0 ? '0.0 lbs' : active_total.toLocaleString(undefined, {maximumFractionDigits: 1}) + ' lbs/yr';
                    }
                    
                    // Update Leaflet popup content
                    updateFacilityPopup(facId);
                    
                    // [Particle rework: always sandbox mode now]
                    // Particles are always wind-advected + footprint-gated; no HYSPLIT replay.
                    drawParticles();
                    refreshDepLayers();
                    lastDepositionHour = -1;
                    lastDepUpdateTime = -999;
                    if (depositionHeatLayer) { map.removeLayer(depositionHeatLayer); depositionHeatLayer = null; }
                    renderDepositionHeatmap(playbackTime);
                    drawParticles();
                    refreshDepLayers();
                });
                chk.addEventListener('click', (e) => {
                    e.stopPropagation(); // Prevent dropdown collapse/expand
                });
            });
            
            // Chemical dropdown toggle
            item.addEventListener('click', () => {
                const isExpanded = chemList.style.display !== 'none';
                if (isExpanded) {
                    chemList.style.display = 'none';
                    arrow.style.transform = 'rotate(0deg)';
                } else {
                    chemList.style.display = 'flex';
                    arrow.style.transform = 'rotate(180deg)';
                }
            });
            
            legendContainer.appendChild(item);
            
            // Initialize popups and sidebar labels
            updateFacilityPopup(fac.id);
            
            let initial_active_total = 0;
            fac.chemicals.forEach(c => {
                if (activeChemicals[fac.id][c.chemical]) {
                    initial_active_total += c.total_lbs || 0;
                }
            });
            const totalLbsLabel = document.getElementById('total-lbs-' + fac.id);
            if (totalLbsLabel) {
                totalLbsLabel.textContent = initial_active_total === 0 ? '0.0 lbs' : initial_active_total.toLocaleString(undefined, {maximumFractionDigits: 1}) + ' lbs/yr';
            }
        });


        // Plume Display Mode select event listener
        document.getElementById('display-mode-select').addEventListener('change', () => {
            const displayMode = document.getElementById('display-mode-select').value;
            if (displayMode === 'stack') {
                particles = particles.filter(p => p.type === 'stack');
            } else if (displayMode === 'fugitive') {
                particles = particles.filter(p => p.type === 'fugitive');
            }
            recalculateDeposition();
            lastDepositionHour = -1;
            lastDepUpdateTime = -999;
            if (depositionHeatLayer) { map.removeLayer(depositionHeatLayer); depositionHeatLayer = null; }
            renderDepositionHeatmap(playbackTime);
            drawParticles();
            refreshDepLayers();
        });

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
        function getSandboxSize() {
            const el = document.getElementById('sizeSlider');
            return el ? parseFloat(el.value) : 2.5;
        }
        function getSandboxDensity() {
            const el = document.getElementById('densitySlider');
            return el ? parseFloat(el.value) : 1.0;
        }
        function getSandboxStackOpacity() {
            const el = document.getElementById('stackOpacitySlider');
            return el ? parseFloat(el.value) : 0.70;
        }
        function getSandboxFugitiveOpacity() {
            const el = document.getElementById('fugitiveOpacitySlider');
            return el ? parseFloat(el.value) : 0.70;
        }

        const MAX_ACTIVE = 8000;                // Global particle cap (raised for plume fill)
        const SPAWN_INTERVAL = 1.0 / 30.0;     // Spawn every 2 sim-minutes
        const BASE_SPAWN_COUNT = 12;            // Particles per spawn for biggest emitter (raised for plume fill)
        const TURB_BASE = 0.0035;               // Base turbulent diffusion (deg/hr)
        const TURB_GROWTH = 0.0040;             // Extra diffusion per hour of age — lets the population
                                                // fan out to FILL the HYSPLIT footprint (the footprint
                                                // edge is HYSPLIT's dispersive leading tail, not median wind)
        const TURB_MAX = 0.050;                 // Cap raised ~4x: aged particles disperse to the footprint
                                                // edge (~1deg over a day); gating clips them to plume shape
        const MAX_WIND_PER_HR = 0.18;           // Raised from 0.10 to allow real HYSPLIT transport distances
        
        // Find max emissions for proportional spawning
        // Density anchor is the max facility total over ALL facilities (including any dropped for
        // having no modeled chemicals) — embedded from Python so spawn density is stable regardless
        // of which facilities are shown. Falls back to the max over embedded facilities.
        const maxFacLbs = Math.max(720080.0, ...PLUME_DATA.facilities.map(f => f.total_lbs || 1), 1);
        
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
        function updateHysplitParticles(time) {
            if (!PLUME_DATA.particles) { hysplitParticles = []; return; }
            
            const H_cur = Math.max(0, Math.min(23, Math.floor(time)));
            const H_next = Math.min(23, H_cur + 1);
            const frac = time - Math.floor(time); // always 0.0→1.0 within the hour

            const displayMode = document.getElementById('display-mode-select').value;
            const newParticles = [];

            // Iterate over each facility's HYSPLIT particles
            const facNameMap = {};
            PLUME_DATA.facilities.forEach((f, idx) => { facNameMap[f.name] = idx; });

            for (const [facName, hourlyData] of Object.entries(PLUME_DATA.particles)) {
                const facIdx = facNameMap[facName];
                if (facIdx === undefined) continue;
                if (!activeFacilities[facIdx]) continue;

                const fac = PLUME_DATA.facilities[facIdx];
                const curList = hourlyData[H_cur] || hourlyData[String(H_cur)] || [];
                const nxtList = hourlyData[H_next] || hourlyData[String(H_next)] || [];

                // Build lookup by particle ID for next-hour snapshot
                const nxtMap = new Map();
                for (const pn of nxtList) {
                    nxtMap.set(pn[0], pn); // key: id
                }

                for (const pc of curList) {
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
                    if (isSameParticle && H_cur !== H_next) {
                        finalLat = lat + (pn[1] - lat) * frac;
                        finalLon = lon + (pn[2] - lon) * frac;
                        finalHt  = Math.max(0, height + (pn[3] - height) * frac);
                        finalAge = age + (pn[4] - age) * frac;
                    } else if (pn && !isSameParticle) {
                        if (frac > 0.5) continue;
                        fadeMod = 1.0 - frac * 2.0;
                    }

                    newParticles.push({
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
                    });
                }
            }
            hysplitParticles = newParticles;
        }
        */

        // ── Sandbox UI removed ── particle motion/size/opacity + footprint opacity are now fixed
        // (viewers can't alter the model). The getSandbox*() getters return their built-in defaults
        // when the sliders are absent, and footprintOpacity stays at its initial 0.45.

        // ── Collapsible Panel Toggle System ──
        (function initPanelToggles() {
            // Left Controls panel
            const headerPanel = document.getElementById('hud-header-panel');
            const headerBody = document.getElementById('header-panel-body');
            const collapseHeader = document.getElementById('collapse-header');
            const restoreHeader = document.getElementById('restore-header');

            collapseHeader.addEventListener('click', () => {
                headerPanel.classList.add('panel-hidden');
                restoreHeader.classList.add('visible');
            });
            restoreHeader.addEventListener('click', () => {
                headerPanel.classList.remove('panel-hidden');
                restoreHeader.classList.remove('visible');
            });

            // Right Legend/Sources panel
            const legendPanel = document.getElementById('hud-legend-panel');
            const legendBody = document.getElementById('legend-panel-body');
            const collapseLegend = document.getElementById('collapse-legend');
            const restoreLegend = document.getElementById('restore-legend');

            collapseLegend.addEventListener('click', () => {
                legendPanel.classList.add('panel-hidden');
                restoreLegend.classList.add('visible');
            });
            restoreLegend.addEventListener('click', () => {
                legendPanel.classList.remove('panel-hidden');
                restoreLegend.classList.remove('visible');
            });
        })();
        
        // ── Wind vector interpolation ──
        const gridInfo = PLUME_DATA.grid_info;
        const GRID_SIZE = gridInfo.grid_size;
        const latMin = gridInfo.lat_min;
        const latMax = gridInfo.lat_max;
        const lonMin = gridInfo.lon_min;
        const lonMax = gridInfo.lon_max;
        const latSpan = latMax - latMin;
        const lonSpan = lonMax - lonMin;

        function interpolateGrid(grid, lat, lon) {
            // Derive dimensions from the ACTUAL grid slice rather than trusting GRID_SIZE.
            // Embedded wind grids can be jagged / differently-sized than GRID_SIZE
            // (stale data, per-hour variation); using real dims prevents out-of-range
            // index access (grid[y][x] === undefined → crash) that would silently kill
            // every advect() call via tick()'s try/catch.
            const rows = grid.length;
            const cols = (grid[0] && grid[0].length) || 1;
            const ZERO = { dLat: 0, dLon: 0, sLat: 0, sLon: 0 };

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

            return { dLat, dLon, sLat, sLon };
        }

        // Returns true when every cell in wind grid slice idx is zero (day-edge artifact hours 0,1,23).
        // Results are cached on the grid array object to avoid repeated scanning.
        function windHourIsZero(wg, idx) {
            if (!wg._zeroCache) wg._zeroCache = {};
            if (wg._zeroCache[idx] !== undefined) return wg._zeroCache[idx];
            const grid = wg[idx];
            let nonzero = false;
            outer: for (let r = 0; r < grid.length; r++)
                for (let c = 0; c < grid[r].length; c++)
                    if (grid[r][c].dLat !== 0 || grid[r][c].dLon !== 0) { nonzero = true; break outer; }
            wg._zeroCache[idx] = !nonzero;
            return wg._zeroCache[idx];
        }

        // Returns the nearest hourly index (forward or backward) whose wind slice is non-zero.
        function nearestNonZeroHour(wg, idx) {
            if (!windHourIsZero(wg, idx)) return idx;
            for (let d = 1; d < wg.length; d++) {
                if (idx - d >= 0 && !windHourIsZero(wg, idx - d)) return idx - d;
                if (idx + d < wg.length && !windHourIsZero(wg, idx + d)) return idx + d;
            }
            return idx;
        }

        function getWind(time, lat, lon, type) {
            let wg = (type === 'fugitive') ? PLUME_DATA.wind_grid_fugitive : PLUME_DATA.wind_grid_stack;
            if (!wg) {
                wg = PLUME_DATA.wind_grid; // fallback for backwards compatibility
            }
            if (!wg || wg.length === 0) return {dLat: 0, dLon: 0, sLat: 0, sLon: 0};

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
            if (mag > MAX_WIND_PER_HR) { const k = MAX_WIND_PER_HR / mag; dLat *= k; dLon *= k; }
            return { dLat, dLon, sLat, sLon };
        }
        
        // ── Spawn particles at all active facilities ──
        // Density slider multiplies the base spawn count in real-time.
        function spawnBatch(dtHours) {
            if (particles.length >= MAX_ACTIVE) return;

            const displayMode = document.getElementById('display-mode-select').value;
            const densityMult = getSandboxDensity();  // live density slider
            // Scale spawn count to elapsed sim-time so rate is continuous, not bursty
            const rateScale = (dtHours !== undefined) ? dtHours / SPAWN_INTERVAL : 1.0;
            // No lifespanScale: lifespan is now emergent from mass depletion; MAX_ACTIVE caps steady-state count
            
            PLUME_DATA.facilities.forEach((fac, idx) => {
                if (!activeFacilities[idx]) return;
                
                // Enforce operating hours schedule if configured
                if (fac.schedule && fac.schedule !== 'continuous') {
                    const currentHour = playbackTime;
                    if (fac.schedule.type === 'shift') {
                        if (currentHour < fac.schedule.start_hour || currentHour > fac.schedule.end_hour) {
                            return;
                        }
                    }
                }
                
                fac.chemicals.forEach(c => {
                    if (!activeChemicals[idx] || !activeChemicals[idx][c.chemical]) return;
                    
                    // Stack Spawning
                    if (displayMode === 'combined' || displayMode === 'stack') {
                        const stackLbs = c.stack_lbs || 0;
                        if (stackLbs > 0) {
                            const ratio = stackLbs / maxFacLbs;
                            const countFloat = ratio * BASE_SPAWN_COUNT * 1.5 * densityMult * rateScale;
                            let count = Math.floor(countFloat);
                            if (Math.random() < (countFloat - count)) count += 1;

                            for (let i = 0; i < count; i++) {
                                particles.push({
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
                                });
                            }
                        }
                    }

                    // Fugitive Spawning
                    if (displayMode === 'combined' || displayMode === 'fugitive') {
                        const fugitiveLbs = c.fugitive_lbs || 0;
                        if (fugitiveLbs > 0) {
                            const ratio = fugitiveLbs / maxFacLbs;
                            const countFloat = ratio * BASE_SPAWN_COUNT * 1.5 * densityMult * rateScale;
                            let count = Math.floor(countFloat);
                            if (Math.random() < (countFloat - count)) count += 1;

                            for (let i = 0; i < count; i++) {
                                particles.push({
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
                                });
                            }
                        }
                    }
                });
            });
        }
        // [COMMENTED OUT — particle rework: batch deposition precompute removed.
        //  Deposition is now driven by footprint-gated particles + liveDepGrid. Kept as reference.]
        /*
        function recalculateDeposition() {
            const sourceSelect = document.getElementById('deposition-source-select');
            const source = sourceSelect ? sourceSelect.value : 'sandbox';
            if (source === 'hysplit' && PLUME_DATA.hysplit_deposition_grid) {
                PLUME_DATA.deposition_grid = PLUME_DATA.hysplit_deposition_grid;
                return;
            }
            const hourlyDepGrid = Array.from({length: 24}, () => new Map());
            let simParticles = [];
            const dt = 0.1;
            const stepsPerHour = 10;
            const liveLifespan = SAFETY_MAX_AGE;
            const displayMode = document.getElementById('display-mode-select').value;
            
            let seed = 42;
            function random() {
                const x = Math.sin(seed++) * 10000;
                return x - Math.floor(x);
            }
            
            for (let hour = 0; hour < 24; hour++) {
                for (let step = 0; step < stepsPerHour; step++) {
                    const time = hour + step * dt;
                    
                    PLUME_DATA.facilities.forEach((fac, idx) => {
                        if (!activeFacilities[idx]) return;
                        
                        if (fac.schedule && fac.schedule !== 'continuous') {
                            if (fac.schedule.type === 'shift') {
                                if (time < fac.schedule.start_hour || time > fac.schedule.end_hour) {
                                    return;
                                }
                            }
                        }
                        
                        fac.chemicals.forEach(c => {
                            if (!activeChemicals[idx] || !activeChemicals[idx][c.chemical]) return;
                            
                            if (displayMode === 'combined' || displayMode === 'stack') {
                                const stackLbs = c.stack_lbs || 0;
                                if (stackLbs > 0) {
                                    const ratio = stackLbs / maxFacLbs;
                                    const countFloat = ratio * BASE_SPAWN_COUNT * 1.5 * dt;
                                    let count = Math.floor(countFloat);
                                    if (random() < (countFloat - count)) count += 1;
                                    
                                    for (let i = 0; i < count; i++) {
                                        simParticles.push({
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
                                        });
                                    }
                                }
                            }
                            
                            if (displayMode === 'combined' || displayMode === 'fugitive') {
                                const fugitiveLbs = c.fugitive_lbs || 0;
                                if (fugitiveLbs > 0) {
                                    const ratio = fugitiveLbs / maxFacLbs;
                                    const countFloat = ratio * BASE_SPAWN_COUNT * 1.5 * dt;
                                    let count = Math.floor(countFloat);
                                    if (random() < (countFloat - count)) count += 1;
                                    
                                    for (let i = 0; i < count; i++) {
                                        simParticles.push({
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
                                        });
                                    }
                                }
                            }
                        });
                    });
                    
                    simParticles = simParticles.filter(p => {
                        const ageMin = (time - p.birth) * 60;
                        const inBounds = p.lat >= latMin && p.lat <= latMax && p.lon >= lonMin && p.lon <= lonMax;
                        return ageMin >= 0 && ageMin < liveLifespan && inBounds;
                    });
                    
                    for (let i = 0; i < simParticles.length; i++) {
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
                        
                        if (p.type === 'fugitive') {
                            p.ht = Math.max(0, Math.min(10, p.ht + (random() - 0.5) * 1 * dt));
                        } else {
                            p.ht = Math.max(0, p.ht + (random() - 0.5) * 3 * dt);
                        }
                        
                        if (p.ht < 30.0) {
                            const chemKey = p.chem.toUpperCase();
                            const chemProp = PLUME_DATA.chemical_properties[chemKey] || {vd: 0.003, henry: 0.01, reactivity: 0.5};
                            const vd = chemProp.vd || 0.003;
                            
                            const dtSec = dt * 3600.0;
                            const fraction = Math.min(0.2, (vd * dtSec) / 30.0);
                            const dDep = p.mass * fraction;
                            p.mass -= dDep;
                            
                            const grid_spacing = 0.002;
                            const cellLat = Math.round(p.lat / grid_spacing) * grid_spacing;
                            const cellLon = Math.round(p.lon / grid_spacing) * grid_spacing;
                            const cellKey = `${cellLat.toFixed(4)},${cellLon.toFixed(4)}`;
                            
                            const currentGrid = hourlyDepGrid[hour];
                            const currentVal = currentGrid.get(cellKey) || 0.0;
                            currentGrid.set(cellKey, currentVal + dDep);
                        }
                    }
                }
            }
            
            const accumulatedGrid = Array.from({length: 24}, () => new Map());
            for (let hour = 0; hour < 24; hour++) {
                for (let prevHour = 0; prevHour <= hour; prevHour++) {
                    for (const [key, val] of hourlyDepGrid[prevHour]) {
                        accumulatedGrid[hour].set(key, (accumulatedGrid[hour].get(key) || 0.0) + val);
                    }
                }
            }
            
            let globalMaxVal = 0.0;
            const hoursData = [];
            
            for (let hour = 0; hour < 24; hour++) {
                const cells = [];
                for (const [key, val] of accumulatedGrid[hour]) {
                    const [latStr, lonStr] = key.split(",");
                    const lat = parseFloat(latStr);
                    const lon = parseFloat(lonStr);
                    
                    if (val > 0.0001) {
                        cells.push({ lat, lon, val });
                        if (val > globalMaxVal) globalMaxVal = val;
                    }
                }
                hoursData.push({ cells });
            }
            
            PLUME_DATA.deposition_grid = {
                hours: hoursData,
                max_val: globalMaxVal,
                grid_spacing: 0.002
            };
        }
        */
        // Stub so existing callers don't throw
        function recalculateDeposition() { }

        // ── Advect all particles forward by dtHours ──
        // PARTICLE REWORK: particles are footprint-gated by the HYSPLIT Ground-Level Air contour.
        // Inside the plume → mass lerps toward band brightness (dense near source, faint at edge).
        // Outside the plume → mass decays rapidly and particle dies.
        // SAFETY_MAX_AGE backstop prevents calm-air particles from accumulating indefinitely.
        function advect(dtHours) {
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
            for (let i = 0; i < particles.length; i++) {
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
                if (p.type === 'fugitive') {
                    p.ht = Math.max(0, Math.min(10, p.ht + (Math.random() - 0.5) * 1 * dtHours));
                } else {
                    p.ht = Math.max(0, p.ht + (Math.random() - 0.5) * 3 * dtHours);
                }

                // ── FOOTPRINT GATING: lifetime + opacity from HYSPLIT air contour ──
                // Query the HYSPLIT Ground-Level Air footprint for this particle's
                // facility, chemical, and source type. If inside, lerp mass toward
                // the band brightness; if outside, rapid fade to death.
                const facName = PLUME_DATA.facilities[p.fac].name;
                const gateType = (displayMode === 'combined') ? p.type : displayMode;
                const b = airBandAtPoint(facName, p.chem, gateType, p.lat, p.lon);

                if (b === null) {
                    // Outside all air contour bands → fading out. TIME-BASED (frame-rate
                    // independent): ~0.55h e-folding → ~1.5h to the death floor. Survives a
                    // brief excursion so it can re-enter the hour-to-hour shifting plume,
                    // instead of dying the instant it clips a contour edge (the old per-call
                    // *0.85 killed particles in a fraction of a sim-hour at 60fps).
                    p.mass *= Math.exp(-dtHours / 0.55);
                } else {
                    // Inside plume → ease mass toward the band brightness (dense/bright near
                    // source, faint at the edge). Time-based convergence (~0.25h) so the look
                    // is identical regardless of frame rate.
                    const target = bandToBrightness(b, 5);
                    const k = 1.0 - Math.exp(-dtHours / 0.25);
                    p.mass = p.mass + k * (target - p.mass);
                }

                // [Removed: the per-particle liveDepGrid accumulation. It ran string-key + Map ops
                //  for every particle every frame but only fed renderDepositionHeatmap(), which is
                //  disabled — pure dead-weight CPU/heat. Deposition is shown via the HYSPLIT footprint
                //  contours (depositionArchive), not this grid.]

                /* [COMMENTED OUT — old vd-based mass drain, replaced by footprint gating above]
                // Dry deposition: near-surface particles lose mass proportional to Vd (m/s)
                if (p.mass !== undefined && p.ht < 30.0) {
                    const chemKey = p.chem.toUpperCase();
                    const chemProp = PLUME_DATA.chemical_properties[chemKey] || {vd: 0.003};
                    const vd = chemProp.vd || 0.003;
                    const fraction = Math.min(0.15, (vd * dtSec) / 30.0);
                    const dDep = p.mass * fraction;
                    p.mass -= dDep;

                    // Accumulate deposited mass into the live grid
                    const cellLat = Math.round(p.lat / grid_spacing) * grid_spacing;
                    const cellLon = Math.round(p.lon / grid_spacing) * grid_spacing;
                    const cellKey = cellLat.toFixed(4) + ',' + cellLon.toFixed(4);
                    let cell = liveDepGrid.get(cellKey);
                    if (!cell) {
                        cell = { lat: cellLat, lon: cellLon, val: 0.0 };
                        liveDepGrid.set(cellKey, cell);
                    }
                    cell.val += dDep;
                    if (cell.val > liveDepMax) liveDepMax = cell.val;
                }
                */

                particles[writeIdx++] = p;
            }
            particles.length = writeIdx;
        }
        
        // ── Deterministic jitter to de-cluster co-located dots ──
        function jHash(a, b) {
            const s = a * 2654435761 + b * 340573321;
            return ((s >>> 0) % 1000) / 1000.0;
        }

        // Hex color cache — facility colors are static, parse once
        const _hexRgbCache = {};
        function getHexRgb(hex) {
            if (_hexRgbCache[hex]) return _hexRgbCache[hex];
            const r = parseInt(hex.slice(1,3), 16);
            const g = parseInt(hex.slice(3,5), 16);
            const b = parseInt(hex.slice(5,7), 16);
            return (_hexRgbCache[hex] = {r, g, b});
        }

        // Persistent per-opacity-bucket arrays — reset length each frame, never reallocated
        const _renderBuckets = new Map();

        // ── Draw all active particles ──
        // Optimized: 3 Leaflet projections per frame (was ~4000), zero LatLng allocs,
        // batched fills grouped by color+opacity bucket, in-place viewport cull.
        function drawParticles() {
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
            for (let i = 0; i < activeList.length; i++) {
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
            }
        }

        // Playback speed mapping
        function getSpeedMultiplier() {
            const selectVal = parseInt(document.getElementById('speed-select').value);
            switch(selectVal) {
                case 1: return 1.0 / 60.0;
                case 2: return 5.0 / 60.0;
                case 3: return 10.0 / 60.0;
                case 4: return 30.0 / 60.0;
                case 5: return 60.0 / 60.0;
                default: return 5.0 / 60.0;
            }
        }

        // HUD State update
        const timeSlider = document.getElementById('time-slider');
        const timeValDisplay = document.getElementById('time-display');
        const ampmDisplay = document.getElementById('ampm-display');
        
        function updateHUD() {
            timeSlider.value = playbackTime.toFixed(2);
            const { time, ampm } = formatSimulationTime(playbackTime);
            timeValDisplay.textContent = time;
            ampmDisplay.textContent = ampm;

            let currentHourInt = Math.floor(playbackTime);
            if (currentHourInt < 0) currentHourInt = 0;
            if (currentHourInt > 23) currentHourInt = 23;
            updateMonitorPopups(currentHourInt);
        }

        // Slider scrub
        timeSlider.addEventListener('input', (e) => {
            const newTime = parseFloat(e.target.value);
            if (Math.abs(newTime - playbackTime) > 0.3) {
                particles = [];
                nextSandboxId = 0;
                lastSpawnTime = -999;
            }
            playbackTime = newTime;
            prevPlaybackTime = playbackTime;
            // Refresh HYSPLIT particles on scrub
            // [Particle rework: always sandbox mode, no HYSPLIT replay on scrub]
            updateHUD();
            drawParticles();
            refreshDepLayers();
        });

        // Tooltip hover
        const tooltip = document.getElementById('tooltip');
        const tooltipTitle = document.getElementById('tooltip-title');
        const tooltipBody = document.getElementById('tooltip-body');
        
        let lastMouseEvt = null;
        function updateTooltip(e) {
            if (!e) return;
            const mp = e.containerPoint;
            let hit = null;
            
            // Query the active particle list (HYSPLIT or sandbox)
            const queryList = particles;  // always sandbox mode
            for (let i = 0; i < queryList.length; i++) {
                const p = queryList[i];
                const pt = map.latLngToContainerPoint(L.latLng(p.lat, p.lon));
                if (Math.hypot(pt.x - mp.x, pt.y - mp.y) < 8) {
                    hit = p;
                    break;
                }
            }
            
            if (hit) {
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
                    Height: <strong>` + hit.ht.toFixed(0) + ` m AGL</strong><br/>
                    Age: <strong>` + ageMin + ` min</strong>
                `;
                tooltip.style.left = (mp.x + 15) + "px";
                tooltip.style.top = (mp.y + 15) + "px";
                tooltip.style.display = 'block';
                // Hide the deposition readout popup to prevent double-popup overlap
                depReadoutEl.style.display = 'none';
            } else {
                // [Particle rework: old liveDepGrid "Surface Deposition" tooltip removed —
                //  dep-readout (#dep-readout) is the sole deposition hover (per-facility % attribution).
                //  Old HYSPLIT deposition grid tooltip path also removed below:]
                // [Particle rework: HYSPLIT deposition grid tooltip path removed —
                //  live deposition tooltip above covers the sandbox/footprint-gated path]
                /*
                    const depGrid = PLUME_DATA.deposition_grid;
                    if (depGrid && depGrid.hours && depGrid.max_val > 0) {
                        const hi = Math.max(0, Math.min(depGrid.hours.length - 1, Math.floor(playbackTime)));
                        const hourData = depGrid.hours[hi];
                        if (hourData && hourData.cells && hourData.cells.length > 0) {
                            const mouseLat = e.latlng.lat;
                            const mouseLon = e.latlng.lng;
                            let closestCell = null;
                            let minDist = 0.0015;
                            for (let c = 0; c < hourData.cells.length; c++) {
                                const cell = hourData.cells[c];
                                const dist = Math.hypot(cell.lat - mouseLat, cell.lon - mouseLon);
                                if (dist < minDist) { minDist = dist; closestCell = cell; }
                            }
                            if (closestCell) {
                                tooltipTitle.textContent = "🌡️ Surface Deposition";
                                tooltipTitle.style.color = "#f59e0b";
                                const intensity = closestCell.val / depGrid.max_val;
                                let risk = "Low"; let riskColor = "#22c55e";
                                if (intensity >= 0.5) { risk = "High"; riskColor = "#ef4444"; }
                                else if (intensity >= 0.15) { risk = "Moderate"; riskColor = "#f59e0b"; }
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
                            }
                        }
                    }
                */
                tooltip.style.display = 'none';
            }
        }

        map.on('mousemove', (e) => {
            lastMouseEvt = e;
            updateTooltip(e);
        });
        
        map.on('mouseout', () => {
            tooltip.style.display = 'none';
            lastMouseEvt = null;
        });

        // Play/Pause
        const playBtn = document.getElementById('play-btn');
        const playIcon = document.getElementById('play-icon');
        const pauseIcon = document.getElementById('pause-icon');
        
        playBtn.addEventListener('click', () => {
            isPlaying = !isPlaying;
            if (isPlaying) {
                playIcon.style.display = 'none';
                pauseIcon.style.display = 'block';
            } else {
                playIcon.style.display = 'block';
                pauseIcon.style.display = 'none';
            }
        });

        document.getElementById('restart-btn').addEventListener('click', () => {
            playbackTime = 0.0;
            prevPlaybackTime = 0.0;
            particles = [];
            nextSandboxId = 0;
            lastSpawnTime = -999;
            liveDepGrid = new Map();
            liveDepMax = 0;
            if (depositionHeatLayer) { map.removeLayer(depositionHeatLayer); depositionHeatLayer = null; }
            updateHUD();
            drawParticles();
            refreshDepLayers();
        });

        // Map redraws
        map.on('move', drawParticles);
        map.on('move', () => {
            if (showDeposition && depositionHeatLayer && depositionHeatLayer._reset)
                depositionHeatLayer._reset();
        });
        map.on('zoom', drawParticles);
        map.on('zoomend', () => {
            // Canvas is transform-positioned + particles are projected exactly, so a plain redraw
            // stays aligned. (The tick loop also redraws every frame; this keeps paused pans crisp.)
            resizeCanvas();
            drawParticles();
            if (showDeposition) {
                if (depositionHeatLayer) { map.removeLayer(depositionHeatLayer); depositionHeatLayer = null; }
                lastDepUpdateTime = -999;
                renderDepositionHeatmap(playbackTime);
            }
        });
        map.on('resize', () => {
            resizeCanvas();
            drawParticles();
        });

        // ── Deposition Heatmap Layer ──
        // Renders HYSPLIT surface deposition (level 0) as colored grid cells.
        // Toggle on/off via the checkbox. Color scale: yellow → orange → red → deep red.
        let depositionHeatLayer = null;
        { const _pTog = document.getElementById('particles-toggle'); if (_pTog) showParticles = _pTog.checked; }
        { const _dTog = document.getElementById('deposition-toggle'); if (_dTog) showDeposition = _dTog.checked; }
        let lastDepositionHour = -1;
        let lastDepUpdateTime = -999; // throttle sub-hour deposition updates
        let lastDepRenderMs = 0; // real-time throttle for deposition re-render
        let liveDepGrid = new Map(); // cellKey -> accumulated deposited mass (grows as particles deposit)
        let liveDepMax = 0;          // current max value for normalization
        
        // Custom warm gradient for the heatmap canvas
        // Creates a smooth yellow → orange → red → deep red gradient
        const depositionGradient = {
            0.0: 'rgba(255, 255, 100, 0)',
            0.15: 'rgba(255, 255, 50, 0.4)',
            0.35: 'rgba(255, 200, 0, 0.55)',
            0.5: 'rgba(255, 150, 0, 0.65)',
            0.7: 'rgba(255, 80, 0, 0.75)',
            0.85: 'rgba(220, 30, 0, 0.85)',
            1.0: 'rgba(160, 0, 0, 0.95)'
        };
        
        function getHeatmapOptionsForZoom(zoom) {
            // Adjust radius and blur dynamically with zoom to ensure smooth overlap
            if (zoom <= 10) return { radius: 12, blur: 10 };
            if (zoom === 11) return { radius: 15, blur: 12 };
            if (zoom === 12) return { radius: 22, blur: 16 };
            if (zoom === 13) return { radius: 32, blur: 22 };
            if (zoom === 14) return { radius: 48, blur: 30 };
            if (zoom === 15) return { radius: 72, blur: 45 };
            if (zoom === 16) return { radius: 110, blur: 65 };
            return { radius: 160, blur: 90 };
        }

        function renderDepositionHeatmap(fracTime) {
            // DISABLED: the leaflet.heat heatmap uses a fixed PIXEL radius, so it visually drifts off
            // the point sources when zooming out, and it duplicates the geo-anchored GeoJSON contour
            // footprints (depPane/airPane via refreshDepLayers), which are the canonical deposition
            // layer and stay correctly aligned at every zoom. Re-enable/rework in the particle pass.
            if (depositionHeatLayer) { map.removeLayer(depositionHeatLayer); depositionHeatLayer = null; }
            return;
            // eslint-disable-next-line no-unreachable
            if (!showDeposition) {
                if (depositionHeatLayer) { map.removeLayer(depositionHeatLayer); depositionHeatLayer = null; }
                return;
            }

            const heatPoints = [];

            // [Particle rework: always sandbox mode — live dep path always active]
            if (true) {
                // ── Live sandbox path: build heatmap directly from running deposition accumulator ──
                if (liveDepMax <= 0) {
                    if (depositionHeatLayer) { map.removeLayer(depositionHeatLayer); depositionHeatLayer = null; }
                    return;
                }
                const depGrid = PLUME_DATA.deposition_grid;
                const maxVal = (depGrid && depGrid.max_val > 0) ? depGrid.max_val : liveDepMax;
                for (const cell of liveDepGrid.values()) {
                    const rel = cell.val / maxVal;
                    const intensity = Math.min(1.0, rel); // Linear scale!
                    if (intensity >= 0.003) {
                        heatPoints.push([cell.lat, cell.lon, intensity]);
                    }
                }
            } else {
                // ── HYSPLIT reference path: render current hour precomputed snapshot directly ──
                // Bypasses interpolation to eliminate thousands of string allocations and Map lookups per second
                const depGrid = PLUME_DATA.deposition_grid;
                if (!depGrid || !depGrid.hours || depGrid.max_val <= 0) return;

                const h0 = Math.max(0, Math.min(depGrid.hours.length - 1, Math.floor(fracTime)));
                const hourData = depGrid.hours[h0];
                if (hourData && hourData.cells) {
                    const maxVal = depGrid.max_val;
                    for (let i = 0; i < hourData.cells.length; i++) {
                        const cell = hourData.cells[i];
                        const intensity = cell.val / maxVal;
                        if (intensity >= 0.005) {
                            heatPoints.push([cell.lat, cell.lon, intensity]);
                        }
                    }
                }
            }

            if (heatPoints.length === 0) {
                if (depositionHeatLayer) { map.removeLayer(depositionHeatLayer); depositionHeatLayer = null; }
                return;
            }

            const zoomOpts = getHeatmapOptionsForZoom(map.getZoom());
            if (!depositionHeatLayer) {
                depositionHeatLayer = L.heatLayer(heatPoints, {
                    radius: zoomOpts.radius,
                    blur: zoomOpts.blur,
                    maxZoom: 17,
                    max: 1.0,
                    minOpacity: 0.08,
                    gradient: depositionGradient
                }).addTo(map);
            } else {
                depositionHeatLayer.setLatLngs(heatPoints);
                depositionHeatLayer.redraw();
            }
        }
        
        // Particles toggle event handler (element may be absent in some builds)
        { const _pTog2 = document.getElementById('particles-toggle');
           if (_pTog2) _pTog2.addEventListener('change', (e) => { showParticles = e.target.checked; }); }

        // Deposition toggle event handler (element may be absent in some builds)
        { const _dTog2 = document.getElementById('deposition-toggle');
           if (_dTog2) _dTog2.addEventListener('change', (e) => {
            showDeposition = e.target.checked;
            const _legend = document.getElementById('deposition-legend');
            if (_legend) _legend.style.display = showDeposition ? 'block' : 'none';

            const depSourceContainer = document.getElementById('deposition-source-container');
            if (depSourceContainer) {
                depSourceContainer.style.display = showDeposition ? 'block' : 'none';
            }

            lastDepositionHour = -1;  // kept for compat
            lastDepUpdateTime = -999;
            if (depositionHeatLayer) { map.removeLayer(depositionHeatLayer); depositionHeatLayer = null; }
            renderDepositionHeatmap(playbackTime);
        }); }

        function updateDepositionSourceSelect() {
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
            if (!hasHysplit) {
                hysplitOpt.disabled = true;
                hysplitOpt.textContent += ' - Not Available';
            }
            selectEl.appendChild(hysplitOpt);

            // Sandbox option
            const sandboxOpt = document.createElement('option');
            sandboxOpt.value = 'sandbox';
            sandboxOpt.textContent = 'Live Deposition (Physics)';
            selectEl.appendChild(sandboxOpt);
            
            // Default to sandbox for smooth continuous emission from point sources.
            // HYSPLIT option remains available for exact trajectory playback.
            if (currentVal && currentVal !== '') {
                selectEl.value = currentVal; // preserve user's previous choice
            } else {
                selectEl.value = 'sandbox';
            }
        }

        // [COMMENTED OUT — particle rework: deposition source toggle removed.
        //  Particle system is always footprint-gated wind-advected. Kept as reference.]
        /*
        // Listen for deposition source changes
        // Also switch particle source to match deposition source for visual consistency
        const _depSrcSel = document.getElementById('deposition-source-select');
        if (_depSrcSel) _depSrcSel.addEventListener('change', () => {
            const srcVal = _depSrcSel.value;
            if (srcVal === 'hysplit') {
                particleSource = 'hysplit';
                particles = []; // clear sandbox particles
                nextSandboxId = 0;
                updateHysplitParticles(playbackTime);
                recalculateDeposition();
            } else {
                particleSource = 'sandbox';
                hysplitParticles = []; // clear HYSPLIT particles
                particles = [];
                nextSandboxId = 0;
                liveDepGrid = new Map();
                liveDepMax = 0;
                recalculateDeposition();
            }
            lastDepositionHour = -1;
            lastDepUpdateTime = -999;
            if (depositionHeatLayer) { map.removeLayer(depositionHeatLayer); depositionHeatLayer = null; }
            renderDepositionHeatmap(playbackTime);
        });
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
        document.addEventListener('visibilitychange', () => { if (!document.hidden) { lastTimestamp = null; lastFrameMs = -1; } });

        function tick(timestamp) {
            requestAnimationFrame(tick);   // always keep the loop alive

            // ── Power/heat saver #1: do nothing while the tab is hidden ──
            // Skip the sim + canvas repaint entirely when backgrounded so the page doesn't peg the
            // GPU/CPU in a tab nobody is looking at (browsers throttle rAF here, so this is cheap).
            if (document.hidden) { lastTimestamp = timestamp; return; }

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

            if (isPlaying) {
                const hourRate = getSpeedMultiplier();
                const dtHours = deltaSec * hourRate;
                playbackTime += dtHours;

                if (playbackTime > 24.0) {
                    playbackTime = 0.0;
                    particles = [];
                    nextSandboxId = 0;
                    hysplitParticles = [];
                    lastSpawnTime = -999;
                    liveDepGrid = new Map();
                    liveDepMax = 0;
                }

                // Crash-proof: a throw in particle/dep code must NEVER freeze the animation loop.
                try {
                    // Particle rework: always spawn+advect (footprint-gated), no HYSPLIT branch
                    spawnBatch(dtHours);
                    advect(dtHours);
                } catch (e) { if (!window._partErr) { console.error('particle update error:', e); window._partErr = true; } }

                prevPlaybackTime = playbackTime;

                updateHUD();
                try { maybeAnimateDep(); } catch (e) { if (!window._depErr) { console.error('dep animate error:', e); window._depErr = true; } }

                // ── Power/heat saver #2: only repaint the particle canvas WHILE PLAYING ──
                // When paused the scene is static, so there's nothing to redraw each frame. Every
                // interaction that changes what's on screen (pan, zoom, layer/date/chemical toggles)
                // already calls drawParticles() from its own handler, so the canvas still updates on
                // demand — we just stop repainting 60×/sec at idle. Big CPU/GPU/battery/heat win.
                try { drawParticles(); } catch (e) { if (!window._drawErr) { console.error('drawParticles error:', e); window._drawErr = true; } }
                if (lastMouseEvt && tooltip.style.display === 'block') {
                    try { updateTooltip(lastMouseEvt); } catch (e) {}
                }
            }
        }

        // Boot
        requestAnimationFrame(tick);
        loadDepManifest(activeDate);
    