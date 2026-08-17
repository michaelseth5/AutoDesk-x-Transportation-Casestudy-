"""
LA Connect — Sepulveda + C Line Network
Generates an interactive Folium map showing a five-phase "car-free LA" concept that
connects two REAL Metro projects — the existing C Line (I-105 corridor) and the
approved, underground Sepulveda Transit Corridor (I-405 corridor) — with one new rail
connector at LAX, a bus feeder layer, station-area density zones, and a future
regional link. Phase 0 (the two real lines) is not proposed by this project; only
Phase 2 (the connector) is genuinely new.

Run: python3 generate_map.py
Output: output/la_405_transit_concept.html
"""

import os

import folium

# ---------------------------------------------------------------------------
# Palette + phase styling
# ---------------------------------------------------------------------------
# Phase 0 (existing/approved): solid, thick, muted gray — no new funding needed.
# Phase 1 (bus feeders): dashed, thin, orange.
# Phase 2 (the one new rail segment): solid, thick, green.
# Phase 3 (density zones): translucent gold radius circles, not a line.
# Phase 4 (future/planned regional links): dotted, thin, light blue.

PHASE0_COLOR = "#8A8D91"  # muted gray — existing / approved, not a new proposal
PHASE1_COLOR = "#E8720C"  # orange — bus feeders
PHASE2_COLOR = "#1F9D6B"  # green — the one new rail connector
PHASE3_COLOR = "#F2B705"  # gold — station-area density zones
PHASE4_COLOR = "#5B9BD9"  # light blue — future / planned regional links

RAIL_WEIGHT = 6
BUS_WEIGHT = 3.5

PHASE0_STYLE = dict(color=PHASE0_COLOR, weight=RAIL_WEIGHT, opacity=0.9)
PHASE1_STYLE = dict(color=PHASE1_COLOR, weight=BUS_WEIGHT, opacity=0.85, dash_array="8,6")
PHASE2_STYLE = dict(color=PHASE2_COLOR, weight=RAIL_WEIGHT, opacity=0.95)
PHASE4_STYLE = dict(color=PHASE4_COLOR, weight=2.5, opacity=0.85, dash_array="2,8")

# ---------------------------------------------------------------------------
# Data — Phase 0: existing / approved Metro infrastructure (NOT proposed here)
# ---------------------------------------------------------------------------

C_LINE_STATIONS = [
    {"name": "LAX / Metro Transit Center", "coords": (33.9382, -118.4076)},
    {"name": "Aviation / Century", "coords": (33.9434, -118.3928)},
    {"name": "Hawthorne / Lennox", "coords": (33.9247, -118.3562)},
    {"name": "Crenshaw", "coords": (33.9252, -118.3265)},
    {"name": "Vermont / Athens", "coords": (33.9252, -118.2917)},
    {"name": "Harbor Freeway", "coords": (33.9256, -118.2775)},
    {"name": "Willowbrook / Rosa Parks", "coords": (33.9271, -118.2489)},
    {"name": "Long Beach Blvd", "coords": (33.9271, -118.2251)},
    {"name": "Lakewood Blvd", "coords": (33.9271, -118.1554)},
    {"name": "Norwalk", "coords": (33.9188, -118.1156)},
]

SEPULVEDA_CORRIDOR_STATIONS = [
    {"name": "Sherman Oaks / Van Nuys", "coords": (34.1510, -118.4480)},
    {"name": "Sepulveda Pass / UCLA", "coords": (34.0736, -118.4390)},
    {"name": "Culver City / Palms", "coords": (34.0211, -118.3965)},
    {"name": "LAX / Westchester", "coords": (33.9416, -118.4085)},
]

ALL_PHASE0_STATIONS = C_LINE_STATIONS + SEPULVEDA_CORRIDOR_STATIONS

PHASE0_POPUP = "Existing / Approved Metro Infrastructure.<br>{note} This project connects to it — it does not propose or fund it."

# ---------------------------------------------------------------------------
# Data — Phase 1: bus feeders off the Sepulveda Corridor (pre-2028 Games readiness)
# ---------------------------------------------------------------------------

BUS_FEEDERS = [
    {"from": "LAX / Westchester", "to": "Westchester", "coords": (33.9597, -118.3965)},
    {"from": "LAX / Westchester", "to": "Playa Vista", "coords": (33.9760, -118.4180)},
    {"from": "Culver City / Palms", "to": "Palms", "coords": (34.0203, -118.4140)},
    {"from": "Culver City / Palms", "to": "Mar Vista", "coords": (34.0037, -118.4300)},
    {"from": "Sepulveda Pass / UCLA", "to": "UCLA / Westwood", "coords": (34.0689, -118.4452)},
    {"from": "Sepulveda Pass / UCLA", "to": "Brentwood", "coords": (34.0522, -118.4695)},
    {"from": "Sherman Oaks / Van Nuys", "to": "Sherman Oaks", "coords": (34.1511, -118.4490)},
    {"from": "Sherman Oaks / Van Nuys", "to": "Van Nuys", "coords": (34.1867, -118.4489)},
]

# ---------------------------------------------------------------------------
# Data — Phase 2: the ONE new rail segment this project proposes
# ---------------------------------------------------------------------------

LEGACY_CONNECTOR = [
    (33.9416, -118.4085),  # LAX / Westchester — Sepulveda Corridor terminus
    (33.9382, -118.4076),  # LAX / Metro Transit Center — C Line terminus
]
LEGACY_FARE = 4.25  # flat fare, USD
LEGACY_SPEED_MPH = 40  # standard urban rail assumption

LEGACY_POPUP = (
    "New Connector — Post-Games Legacy Rail.<br>"
    "The one new rail segment this project proposes: a short link joining the "
    "Sepulveda Transit Corridor to Metro's C Line at LAX.<br>"
    f"Flat fare: ${LEGACY_FARE:.2f}"
)

# Downtown LA Connector — a second new Phase 2 segment, branching off the existing
# Culver City / Palms station and following the real E Line alignment northeast
# through Exposition Park / USC into Downtown LA.
DOWNTOWN_CONNECTOR_STATIONS = [
    {"name": "La Cienega / Jefferson", "coords": (34.0217, -118.3776)},
    {"name": "Expo / Crenshaw", "coords": (34.0227, -118.3382)},
    {"name": "Expo Park / USC", "coords": (34.0181, -118.2868)},
    {"name": "7th St / Metro Center", "coords": (34.0489, -118.2588)},
    {"name": "Downtown LA / Union Station", "coords": (34.0561, -118.2365)},
]
CULVER_CITY_PALMS_COORD = next(
    s["coords"] for s in SEPULVEDA_CORRIDOR_STATIONS if s["name"] == "Culver City / Palms"
)
DOWNTOWN_CONNECTOR_PATH = [CULVER_CITY_PALMS_COORD] + [s["coords"] for s in DOWNTOWN_CONNECTOR_STATIONS]

DOWNTOWN_CONNECTOR_POPUP = (
    "New Rail Connector — Downtown LA Branch.<br>"
    "Part of the new rail connector this project proposes, linking the Sepulveda "
    "Corridor into Downtown LA via Culver City / Palms.<br>"
    f"Flat fare: ${LEGACY_FARE:.2f}"
)

# ---------------------------------------------------------------------------
# Data — Phase 4: future / planned regional links (not funded, shown for context)
# ---------------------------------------------------------------------------

FUTURE_K_LINE_EXTENSION = [
    (33.8497, -118.3887),  # Redondo Beach
    (33.8358, -118.3406),  # Torrance Transit Center
]

# ---------------------------------------------------------------------------
# Map setup
# ---------------------------------------------------------------------------

center_lat = sum(s["coords"][0] for s in ALL_PHASE0_STATIONS) / len(ALL_PHASE0_STATIONS)
center_lon = sum(s["coords"][1] for s in ALL_PHASE0_STATIONS) / len(ALL_PHASE0_STATIONS)

m = folium.Map(
    location=[center_lat, center_lon],
    zoom_start=10,
    tiles="cartodbpositron",
)

# Title banner
title_html = """
<div style="
    position: fixed;
    top: 10px; left: 50%; transform: translateX(-50%);
    z-index: 9999;
    background: white;
    padding: 10px 22px;
    border: 1px solid #999;
    border-radius: 6px;
    box-shadow: 0 2px 6px rgba(0,0,0,0.25);
    font-family: Arial, sans-serif;
    font-size: 18px;
    font-weight: bold;
    color: #0B3C6B;
    text-align: center;
">
LA Connect — Sepulveda + C Line Network
<div style="font-size:12px; font-weight:normal; color:#666; margin-top:2px;">
Built on LA's real rail network — connecting what exists to what's next.
</div>
</div>
"""
m.get_root().html.add_child(folium.Element(title_html))

# ---------------------------------------------------------------------------
# Phase 0: Metro C Line (existing, real, in service today)
# ---------------------------------------------------------------------------

c_line_coords = [s["coords"] for s in C_LINE_STATIONS]
folium.PolyLine(
    c_line_coords,
    tooltip="Metro C Line (I-105 corridor) — existing light rail, in service today",
    **PHASE0_STYLE,
).add_to(m)

for station in C_LINE_STATIONS:
    folium.CircleMarker(
        location=station["coords"],
        radius=7,
        color=PHASE0_COLOR,
        fill=True,
        fill_color=PHASE0_COLOR,
        fill_opacity=0.95,
        weight=2,
        popup=folium.Popup(
            f"<b>{station['name']}</b><br>" + PHASE0_POPUP.format(note="Metro C Line — real, in service today."),
            max_width=280,
        ),
        tooltip=f"{station['name']} — Existing Metro C Line",
    ).add_to(m)

# ---------------------------------------------------------------------------
# Phase 0: Sepulveda Transit Corridor (Metro-approved, funded, underground)
# ---------------------------------------------------------------------------

sepulveda_coords = [s["coords"] for s in SEPULVEDA_CORRIDOR_STATIONS]
folium.PolyLine(
    sepulveda_coords,
    tooltip="Sepulveda Transit Corridor (I-405 corridor) — Metro-approved, underground, funded",
    **PHASE0_STYLE,
).add_to(m)

for station in SEPULVEDA_CORRIDOR_STATIONS:
    folium.CircleMarker(
        location=station["coords"],
        radius=7,
        color=PHASE0_COLOR,
        fill=True,
        fill_color=PHASE0_COLOR,
        fill_opacity=0.95,
        weight=2,
        popup=folium.Popup(
            f"<b>{station['name']}</b><br>"
            + PHASE0_POPUP.format(note="Sepulveda Transit Corridor — Metro-approved and funded, underground."),
            max_width=280,
        ),
        tooltip=f"{station['name']} — Approved Sepulveda Transit Corridor",
    ).add_to(m)

# ---------------------------------------------------------------------------
# Phase 1: bus feeders off the Sepulveda Corridor
# ---------------------------------------------------------------------------

station_lookup = {s["name"]: s["coords"] for s in SEPULVEDA_CORRIDOR_STATIONS}

for feeder in BUS_FEEDERS:
    start = station_lookup[feeder["from"]]
    end = feeder["coords"]

    folium.PolyLine(
        [start, end],
        tooltip=f"Express bus feeder: {feeder['from']} to {feeder['to']}",
        **PHASE1_STYLE,
    ).add_to(m)

    folium.CircleMarker(
        location=end,
        radius=8,
        color=PHASE1_COLOR,
        fill=True,
        fill_color=PHASE1_COLOR,
        fill_opacity=0.9,
        popup=folium.Popup(
            f"<b>{feeder['to']}</b><br>Bus Feeder Stop / Local Business District<br>"
            f"<i>Food perk redemptions available for riders</i>",
            max_width=260,
        ),
        tooltip=f"{feeder['to']} — Bus Feeder Stop / Local Business District",
    ).add_to(m)

# ---------------------------------------------------------------------------
# Phase 2: the ONE new rail segment — links the two real lines at LAX
# ---------------------------------------------------------------------------

folium.PolyLine(
    LEGACY_CONNECTOR,
    tooltip="New Connector (rail): LAX / Westchester → LAX / Metro Transit Center — opens after 2028",
    **PHASE2_STYLE,
).add_to(m)

connector_midpoint = (
    (LEGACY_CONNECTOR[0][0] + LEGACY_CONNECTOR[1][0]) / 2,
    (LEGACY_CONNECTOR[0][1] + LEGACY_CONNECTOR[1][1]) / 2,
)
folium.CircleMarker(
    location=connector_midpoint,
    radius=6,
    color=PHASE2_COLOR,
    fill=True,
    fill_color="white",
    fill_opacity=0.95,
    weight=3,
    popup=folium.Popup(f"<b>New Connector</b><br>{LEGACY_POPUP}", max_width=300),
    tooltip="New Connector — the one segment this project proposes",
).add_to(m)

# Downtown LA Connector — a second new Phase 2 segment (additive; same weight/color
# as the LAX connector above).
folium.PolyLine(
    DOWNTOWN_CONNECTOR_PATH,
    tooltip="New Connector (rail): Culver City / Palms → Downtown LA / Union Station",
    **PHASE2_STYLE,
).add_to(m)

for station in DOWNTOWN_CONNECTOR_STATIONS:
    folium.CircleMarker(
        location=station["coords"],
        radius=7,
        color=PHASE2_COLOR,
        fill=True,
        fill_color=PHASE2_COLOR,
        fill_opacity=0.95,
        weight=2,
        popup=folium.Popup(f"<b>{station['name']}</b><br>{DOWNTOWN_CONNECTOR_POPUP}", max_width=300),
        tooltip=f"{station['name']} — New Rail Connector, Downtown LA Branch",
    ).add_to(m)

# ---------------------------------------------------------------------------
# Phase 3: station-area density zones (0.5 mi walk buffer around every Phase 0 stop,
# plus the new Downtown LA Connector's Phase 2 stations)
# ---------------------------------------------------------------------------

for station in ALL_PHASE0_STATIONS + DOWNTOWN_CONNECTOR_STATIONS:
    folium.Circle(
        location=station["coords"],
        radius=805,  # ~0.5 mile, in meters
        color=PHASE3_COLOR,
        weight=1,
        fill=True,
        fill_color=PHASE3_COLOR,
        fill_opacity=0.15,
        tooltip=f"{station['name']} — 0.5 mi station-area density zone",
    ).add_to(m)

# ---------------------------------------------------------------------------
# Phase 4: future / planned regional links (not funded, shown for context)
# ---------------------------------------------------------------------------

folium.PolyLine(
    FUTURE_K_LINE_EXTENSION,
    tooltip="Future: K Line extension to Torrance — planned, not yet funded",
    **PHASE4_STYLE,
).add_to(m)

folium.CircleMarker(
    location=FUTURE_K_LINE_EXTENSION[0],
    radius=6,
    color=PHASE4_COLOR,
    fill=True,
    fill_color="white",
    fill_opacity=0.9,
    weight=2,
    popup=folium.Popup("<b>Redondo Beach</b><br>Future / Planned Regional Link — K Line extension, not yet funded.", max_width=260),
    tooltip="Redondo Beach — Future K Line extension",
).add_to(m)

folium.CircleMarker(
    location=FUTURE_K_LINE_EXTENSION[1],
    radius=6,
    color=PHASE4_COLOR,
    fill=True,
    fill_color="white",
    fill_opacity=0.9,
    weight=2,
    popup=folium.Popup("<b>Torrance Transit Center</b><br>Future / Planned Regional Link — K Line extension, not yet funded.", max_width=260),
    tooltip="Torrance Transit Center — Future K Line extension",
).add_to(m)

# ---------------------------------------------------------------------------
# Legend — all five phases, color + line style shown together
# ---------------------------------------------------------------------------

legend_html = """
<div style="
    position: fixed;
    bottom: 30px; left: 30px;
    z-index: 9999;
    background: white;
    padding: 12px 16px;
    border: 1px solid #999;
    border-radius: 6px;
    box-shadow: 0 2px 6px rgba(0,0,0,0.25);
    font-family: Arial, sans-serif;
    font-size: 13px;
    color: #333;
    line-height: 1.6;
">
<b style="font-size:14px;">Legend</b><br>
<i style="font-size:11px; color:#666;">Solid + thick = rail &nbsp;|&nbsp; Dashed/dotted + thin = bus / future</i><br><br>
<span style="display:inline-block;width:22px;height:4px;background:#8A8D91;margin-right:8px;"></span>
Phase 0 — Existing / Approved Metro Infrastructure<br>
<span style="display:inline-block;width:22px;height:0;border-top:3px dashed #E8720C;margin-right:8px;"></span>
Phase 1 — Bus feeder route<br>
<span style="display:inline-block;width:22px;height:4px;background:#1F9D6B;margin-right:8px;"></span>
Phase 2 — New Connector (Post-Games Legacy Rail)<br>
<span style="display:inline-block;width:16px;height:16px;background:rgba(242,183,5,0.3);border:1px solid #F2B705;border-radius:50%;margin-right:8px;"></span>
Phase 3 — Station-area density zone (0.5 mi)<br>
<span style="display:inline-block;width:22px;height:0;border-top:3px dotted #5B9BD9;margin-right:8px;"></span>
Phase 4 — Future / Planned Regional Links<br><br>
<span style="display:inline-block;width:12px;height:12px;background:#8A8D91;border-radius:50%;margin-right:8px;"></span>
Existing / approved station<br>
<span style="display:inline-block;width:12px;height:12px;background:#E8720C;border-radius:50%;margin-right:8px;"></span>
Bus stop / local business district
</div>
"""
m.get_root().html.add_child(folium.Element(legend_html))

# ---------------------------------------------------------------------------
# Save
# ---------------------------------------------------------------------------

os.makedirs("output", exist_ok=True)
output_path = "output/la_405_transit_concept.html"
m.save(output_path)
print(f"Interactive map saved to {output_path}")
