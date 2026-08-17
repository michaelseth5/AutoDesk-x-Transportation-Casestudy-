"""
LA Connect — Sepulveda + C Line Network
Generates an interactive Folium map showing a five-phase "car-free LA" concept that
connects two REAL Metro assets — the existing C Line (I-105 corridor) and the K Line
(Crenshaw/LAX corridor) — plus Metro's real, selected-but-unfunded Sepulveda Transit
Corridor Locally Preferred Alternative (Van Nuys <-> Expo/Sepulveda), an LA Connect
"extension concept" that is NOT part of that official alternative, a bus feeder layer,
station-area density zones, and future regional links. Phase 0 (the real/selected
lines) is not proposed by this project; only Phase 2 (the connectors) and the
Sepulveda extension concept are genuinely new/unofficial.

Facts corrected against an August 2026 fact-check — see README / correction summary
for the full list of what changed and why.

Run: python3 generate_map.py
Output: output/la_405_transit_concept.html
"""

import os

import folium

# ---------------------------------------------------------------------------
# Palette + phase styling
# ---------------------------------------------------------------------------
# Phase 0 (existing/real): solid, thick, muted gray — no new funding needed.
# Phase 1 (bus feeders): dashed, thin, orange.
# Phase 2 (the new rail connectors this project proposes): solid, thick, green.
# Phase 3 (density zones): translucent gold radius circles, not a line.
# Phase 4 / concept-extension (future/planned/unofficial links): dotted, thin, light blue.

PHASE0_COLOR = "#8A8D91"  # muted gray — existing / real Metro service
PHASE1_COLOR = "#E8720C"  # orange — bus feeders
PHASE2_COLOR = "#1F9D6B"  # green — new rail connectors this project proposes
PHASE3_COLOR = "#F2B705"  # gold — station-area density zones
PHASE4_COLOR = "#5B9BD9"  # light blue — future / planned / concept-only links

RAIL_WEIGHT = 6
BUS_WEIGHT = 3.5

PHASE0_STYLE = dict(color=PHASE0_COLOR, weight=RAIL_WEIGHT, opacity=0.9)
PHASE1_STYLE = dict(color=PHASE1_COLOR, weight=BUS_WEIGHT, opacity=0.85, dash_array="8,6")
PHASE2_STYLE = dict(color=PHASE2_COLOR, weight=RAIL_WEIGHT, opacity=0.95)
PHASE4_STYLE = dict(color=PHASE4_COLOR, weight=2.5, opacity=0.85, dash_array="2,8")

# ---------------------------------------------------------------------------
# Data — Phase 0: Metro C Line (real, in service today)
# LAX/Metro Transit Center <-> Norwalk, 12 stations, 17.8 mi, opened Aug 12, 1995.
# Connects to the A Line at Willowbrook/Rosa Parks and the J Line busway at Harbor
# Freeway. Frequency: approximately every 10 min for most of the day, approximately
# every 20 min early mornings/late evenings.
# ---------------------------------------------------------------------------

C_LINE_STATIONS = [
    {"name": "LAX / Metro Transit Center", "coords": (33.9382, -118.4076)},
    {"name": "Aviation / Century", "coords": (33.9434, -118.3928)},
    {"name": "Aviation / Imperial", "coords": (33.9296, -118.3756)},
    {"name": "Hawthorne / Lennox", "coords": (33.9247, -118.3562)},
    {"name": "Crenshaw", "coords": (33.9252, -118.3265)},
    {"name": "Vermont / Athens", "coords": (33.9252, -118.2917)},
    {"name": "Harbor Freeway", "coords": (33.9256, -118.2775)},
    {"name": "Avalon", "coords": (33.9258, -118.2652)},
    {"name": "Willowbrook / Rosa Parks", "coords": (33.9271, -118.2489)},
    {"name": "Lynwood", "coords": (33.9271, -118.2107)},
    {"name": "Lakewood Boulevard", "coords": (33.9271, -118.1554)},
    {"name": "Norwalk", "coords": (33.9188, -118.1156)},
]

C_LINE_POPUP = (
    "The existing C Line provides an east-west connection between Norwalk and the "
    "LAX/Metro Transit Center, with transfers to the A Line at Willowbrook/Rosa Parks "
    "and the J Line at Harbor Freeway. 12 stations, 17.8 miles, opened August 12, 1995. "
    "Frequency: approximately every 10 minutes for most of the day, approximately "
    "every 20 minutes early mornings and late evenings."
)

# ---------------------------------------------------------------------------
# Data — Phase 0: Metro K Line (real, in service today)
# 13 stations, continuous service Expo/Crenshaw <-> Redondo Beach. The Crenshaw/LAX
# segment opened Oct 2022; the LAX/Metro Transit Center segment opened June 2025,
# completing through-service. Shares LAX/Metro Transit Center and Aviation/Century
# with the C Line. Does NOT share a platform with the E Line — riders transfer at
# Expo/Crenshaw via a short at-grade crossing, not an in-station transfer.
# "K Line" is the primary/current name; "Crenshaw/LAX Line" is a legacy/informal
# alt-name from construction.
# ---------------------------------------------------------------------------

K_LINE_STATIONS = [
    {"name": "Expo / Crenshaw", "coords": (34.0227, -118.3382)},
    {"name": "Martin Luther King Jr.", "coords": (34.0089, -118.3358)},
    {"name": "Leimert Park", "coords": (34.0084, -118.3323)},
    {"name": "Hyde Park", "coords": (33.9934, -118.3358)},
    {"name": "Fairview Heights", "coords": (33.9885, -118.3358)},
    {"name": "Downtown Inglewood", "coords": (33.9556, -118.3550)},
    {"name": "Westchester / Veterans", "coords": (33.9611, -118.3970)},
    {"name": "LAX / Metro Transit Center", "coords": (33.9382, -118.4076)},
    {"name": "Aviation / Century", "coords": (33.9434, -118.3928)},
    {"name": "Mariposa", "coords": (33.9200, -118.3875)},
    {"name": "El Segundo", "coords": (33.9137, -118.3875)},
    {"name": "Douglas", "coords": (33.8975, -118.3875)},
    {"name": "Redondo Beach", "coords": (33.8497, -118.3887)},
]

K_LINE_POPUP = (
    "K Line (formerly known informally as the Crenshaw/LAX Line during construction) "
    "— 13 stations, continuous service between Expo/Crenshaw and Redondo Beach. The "
    "Crenshaw/LAX segment opened October 2022; the LAX/Metro Transit Center segment "
    "opened June 2025, completing through-service. Shares LAX/Metro Transit Center "
    "and Aviation/Century with the C Line. Does not share a platform with the E Line "
    "at Expo/Crenshaw — transfer is via a short at-grade crossing, not same-platform."
)

ALL_PHASE0_STATIONS = C_LINE_STATIONS + K_LINE_STATIONS

PHASE0_POPUP = "Existing Metro Infrastructure.<br>{note} This project connects to it — it does not propose or fund it."

# ---------------------------------------------------------------------------
# Data — Phase 0 (real, selected, unfunded): Sepulveda Transit Corridor Locally
# Preferred Alternative. In January 2026, Metro's Board selected "Modified
# Alternative 5" — underground heavy rail — as the LPA. This is a real, formal
# milestone, but the project remains in planning/environmental review, NOT approved
# as fully funded or shovel-ready. Alignment: Van Nuys Metrolink Station -> Van Nuys
# Blvd/G Line transfer -> Sepulveda Pass -> E Line Expo/Sepulveda Station (endpoint).
# Metro's concept contemplates trains capable of 2.5-minute peak headways. No
# confirmed opening date exists. Cost estimates in the $6-15B range circulating
# publicly are a concept estimate, not an official Metro cost.
# ---------------------------------------------------------------------------

SEPULVEDA_LPA_STATIONS = [
    {"name": "Van Nuys Metrolink Station", "coords": (34.1858, -118.4489)},
    {"name": "Van Nuys Blvd / G Line", "coords": (34.1817, -118.4489)},
    {"name": "Sepulveda Pass", "coords": (34.1000, -118.4460)},
    {"name": "E Line Expo / Sepulveda", "coords": (34.0247, -118.4368)},
]

SEPULVEDA_LPA_POPUP = (
    "Metro selected an underground heavy-rail alternative between Van Nuys and "
    "Expo/Sepulveda as its Locally Preferred Alternative (\"Modified Alternative 5\") "
    "in January 2026; environmental review, design, funding, and a construction "
    "schedule remain pending. Concept contemplates trains capable of 2.5-minute peak "
    "headways. No confirmed opening date exists. Publicly circulated cost figures "
    "($6-15B) are a concept estimate, not an official Metro cost."
)

# ---------------------------------------------------------------------------
# Data — Sepulveda Extension Concept (LA Connect proposal ONLY — NOT part of
# Metro's selected Locally Preferred Alternative). This is the original at-grade
# "405 corridor" alignment this project sketched before the Jan 2026 LPA selection;
# it is kept here as a labeled concept extension, not real/approved infrastructure,
# since the Phase 2 connectors below still reference it.
# ---------------------------------------------------------------------------

SEPULVEDA_EXTENSION_CONCEPT_STATIONS = [
    {"name": "Sherman Oaks / Van Nuys", "coords": (34.1510, -118.4480)},
    {"name": "Sepulveda Pass / UCLA", "coords": (34.0736, -118.4390)},
    {"name": "Culver City / Palms", "coords": (34.0211, -118.3965)},
    {"name": "LAX / Westchester", "coords": (33.9416, -118.4085)},
]

SEPULVEDA_EXTENSION_CONCEPT_POPUP = (
    "LA Connect Extension Concept — NOT part of Metro's selected Sepulveda Transit "
    "Corridor Locally Preferred Alternative (which runs Van Nuys ↔ Expo/Sepulveda, "
    "selected January 2026). This is an unofficial concept extension sketched by this "
    "project; it is not funded, approved, or under environmental review."
)

# ---------------------------------------------------------------------------
# Data — Phase 1: bus feeders off the Sepulveda Extension Concept
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
# Data — Phase 2: new rail connectors this project proposes (concept, contingent
# on the Sepulveda Extension Concept above)
# ---------------------------------------------------------------------------

LEGACY_CONNECTOR = [
    (33.9416, -118.4085),  # LAX / Westchester — Sepulveda Extension Concept terminus
    (33.9382, -118.4076),  # LAX / Metro Transit Center — C Line terminus
]
LEGACY_FARE = 4.25  # flat fare, USD
LEGACY_SPEED_MPH = 40  # standard urban rail assumption

LEGACY_POPUP = (
    "New Connector — Post-Games Legacy Rail (concept).<br>"
    "A short link this project proposes joining the LA Connect Sepulveda Extension "
    "Concept to Metro's real C Line at LAX. Contingent on that extension concept, "
    "which is not part of Metro's selected Sepulveda Transit Corridor alternative.<br>"
    f"Flat fare: ${LEGACY_FARE:.2f}"
)

# Downtown LA Connector — a second new Phase 2 segment, branching off the
# Sepulveda Extension Concept's Culver City / Palms station and following the
# real E Line alignment through Exposition Park / USC into Downtown LA.
DOWNTOWN_CONNECTOR_STATIONS = [
    {"name": "La Cienega / Jefferson", "coords": (34.0217, -118.3776)},
    {"name": "Expo / Crenshaw", "coords": (34.0227, -118.3382)},
    {"name": "Expo Park / USC", "coords": (34.0181, -118.2868)},
    {"name": "7th St / Metro Center", "coords": (34.0489, -118.2588)},
    {"name": "Downtown LA / Union Station", "coords": (34.0561, -118.2365)},
]
CULVER_CITY_PALMS_COORD = next(
    s["coords"] for s in SEPULVEDA_EXTENSION_CONCEPT_STATIONS if s["name"] == "Culver City / Palms"
)
DOWNTOWN_CONNECTOR_PATH = [CULVER_CITY_PALMS_COORD] + [s["coords"] for s in DOWNTOWN_CONNECTOR_STATIONS]

DOWNTOWN_CONNECTOR_POPUP = (
    "New Rail Connector — Downtown LA Branch (concept).<br>"
    "Part of the new rail connector this project proposes, linking the Sepulveda "
    "Extension Concept into Downtown LA via Culver City / Palms. Note: this branch's "
    "Expo / Crenshaw stop reuses the real K Line station's coordinate but is a "
    "separate, unofficial concept segment, not part of the K Line.<br>"
    f"Flat fare: ${LEGACY_FARE:.2f}"
)

# ---------------------------------------------------------------------------
# Data — Phase 4: future / planned / concept-only regional links
# ---------------------------------------------------------------------------

# K Line Extension to Torrance — real. Final EIR certified and approved Jan 22,
# 2026, using the Hawthorne Option, ~4.5 mi from Redondo Beach (Marine) to Torrance
# Transit Center. Estimated opening 2036; construction possibly starting as early
# as 2027. (Operates as part of the K Line, not the C Line.)
FUTURE_K_LINE_TORRANCE = [
    (33.8497, -118.3887),  # Redondo Beach
    (33.8358, -118.3406),  # Torrance Transit Center
]
FUTURE_K_LINE_TORRANCE_POPUP = (
    "K Line Extension to Torrance — Final EIR certified and approved January 22, "
    "2026 (Hawthorne Option), ~4.5 miles from Redondo Beach (Marine) to Torrance "
    "Transit Center. Estimated opening 2036; construction possibly starting as early "
    "as 2027. Operates as part of the K Line, not the C Line."
)

# K Line Northern Extension (toward Mid-City / West Hollywood / Hollywood) —
# long-range only; construction funding not available until 2041, projected
# opening 2047-2049. Not relevant to the 2028 Games.
FUTURE_K_LINE_NORTH = [
    (34.0227, -118.3382),  # Expo / Crenshaw — shared with the K Line
    (34.0912, -118.3617),  # approximate northern extension direction, Mid-City / WeHo
]
FUTURE_K_LINE_NORTH_POPUP = (
    "K Line Northern Extension (toward Mid-City / West Hollywood / Hollywood) — "
    "long-range only. Construction funding is not available until 2041; projected "
    "opening 2047-2049. Not relevant to the 2028 Olympics."
)

# D Line Extension Section 1 — real, opened May 8, 2026, three new underground
# stations toward Beverly Hills. Shown as a single Phase 0 marker for regional
# Westside context; not otherwise modeled on this map.
D_LINE_EXTENSION_MARKER = (34.0620, -118.3610)
D_LINE_EXTENSION_POPUP = (
    "D Line Extension, Section 1 — opened May 8, 2026, adding three underground "
    "stations toward Beverly Hills. Existing / approved Metro infrastructure, shown "
    "for regional Olympic-travel and Westside-access context; not otherwise modeled "
    "on this map."
)

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


def add_rail_group(stations, style, popup_note, tooltip_label, marker_color=None):
    """Draws a trunk polyline + circle markers for a list of {"name","coords"} stations."""
    color = marker_color or style["color"]
    coords = [s["coords"] for s in stations]
    folium.PolyLine(coords, tooltip=tooltip_label, **style).add_to(m)
    for station in stations:
        folium.CircleMarker(
            location=station["coords"],
            radius=7,
            color=color,
            fill=True,
            fill_color=color,
            fill_opacity=0.95,
            weight=2,
            popup=folium.Popup(f"<b>{station['name']}</b><br>{popup_note}", max_width=320),
            tooltip=f"{station['name']} — {tooltip_label}",
        ).add_to(m)


# ---------------------------------------------------------------------------
# Phase 0: Metro C Line (existing, real, in service today)
# ---------------------------------------------------------------------------

add_rail_group(
    C_LINE_STATIONS,
    PHASE0_STYLE,
    PHASE0_POPUP.format(note=C_LINE_POPUP),
    "Metro C Line — existing light rail, in service today",
)

# ---------------------------------------------------------------------------
# Phase 0: Metro K Line (existing, real, continuous service since June 2025)
# ---------------------------------------------------------------------------

add_rail_group(
    K_LINE_STATIONS,
    PHASE0_STYLE,
    PHASE0_POPUP.format(note=K_LINE_POPUP),
    "Metro K Line — existing light rail, in service today",
)

# ---------------------------------------------------------------------------
# Phase 0: Sepulveda Transit Corridor LPA (real, selected, unfunded)
# ---------------------------------------------------------------------------

add_rail_group(
    SEPULVEDA_LPA_STATIONS,
    PHASE0_STYLE,
    PHASE0_POPUP.format(note=SEPULVEDA_LPA_POPUP),
    "Sepulveda Transit Corridor — Locally Preferred Alternative (selected Jan 2026, pending funding)",
)

# ---------------------------------------------------------------------------
# Sepulveda Extension Concept (LA Connect proposal only — NOT part of Metro's LPA)
# ---------------------------------------------------------------------------

add_rail_group(
    SEPULVEDA_EXTENSION_CONCEPT_STATIONS,
    PHASE4_STYLE,
    SEPULVEDA_EXTENSION_CONCEPT_POPUP,
    "LA Connect Extension Concept — not part of Metro's selected alternative",
    marker_color=PHASE4_COLOR,
)

# ---------------------------------------------------------------------------
# Phase 1: bus feeders off the Sepulveda Extension Concept
# ---------------------------------------------------------------------------

station_lookup = {s["name"]: s["coords"] for s in SEPULVEDA_EXTENSION_CONCEPT_STATIONS}

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
# Phase 2: new rail connectors this project proposes
# ---------------------------------------------------------------------------

folium.PolyLine(
    LEGACY_CONNECTOR,
    tooltip="New Connector (concept, rail): LAX / Westchester → LAX / Metro Transit Center",
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
    popup=folium.Popup(f"<b>New Connector</b><br>{LEGACY_POPUP}", max_width=320),
    tooltip="New Connector — concept, contingent on the Sepulveda Extension Concept",
).add_to(m)

# Downtown LA Connector — a second new Phase 2 segment (additive; same weight/color
# as the LAX connector above).
folium.PolyLine(
    DOWNTOWN_CONNECTOR_PATH,
    tooltip="New Connector (concept, rail): Culver City / Palms → Downtown LA / Union Station",
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
        popup=folium.Popup(f"<b>{station['name']}</b><br>{DOWNTOWN_CONNECTOR_POPUP}", max_width=320),
        tooltip=f"{station['name']} — New Rail Connector, Downtown LA Branch (concept)",
    ).add_to(m)

# ---------------------------------------------------------------------------
# LAX / Metro Transit Center — special note marker (served by both C and K Lines,
# opened June 6, 2025, plus bus bays; APM delayed)
# ---------------------------------------------------------------------------

LAX_TRANSIT_CENTER_POPUP = (
    "LAX/Metro Transit Center — opened June 6, 2025. Served by both the C Line and "
    "K Line, plus bus bays for Metro Lines 102, 111, 117, 120, 232 and municipal "
    "operators. The LAX Automated People Mover (APM) remains under testing and is "
    "expected to open later in 2026; until then, a free airport-operated shuttle "
    "links the LAX/Metro Transit Center with terminals."
)
folium.CircleMarker(
    location=(33.9382, -118.4076),
    radius=10,
    color="#0B2A4A",
    fill=True,
    fill_color="#0B2A4A",
    fill_opacity=0.9,
    weight=2,
    popup=folium.Popup(f"<b>LAX / Metro Transit Center</b><br>{LAX_TRANSIT_CENTER_POPUP}", max_width=320),
    tooltip="LAX / Metro Transit Center — C Line + K Line interchange",
).add_to(m)

# ---------------------------------------------------------------------------
# Phase 3: station-area density zones (0.5 mi walk buffer around every Phase 0 stop,
# the Sepulveda Extension Concept, plus the new Downtown LA Connector's Phase 2
# stations)
# ---------------------------------------------------------------------------

for station in ALL_PHASE0_STATIONS + SEPULVEDA_LPA_STATIONS + SEPULVEDA_EXTENSION_CONCEPT_STATIONS + DOWNTOWN_CONNECTOR_STATIONS:
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
# Phase 4: future / planned / concept-only regional links (not funded, shown for
# context)
# ---------------------------------------------------------------------------

folium.PolyLine(
    FUTURE_K_LINE_TORRANCE,
    tooltip="Future: K Line extension to Torrance — EIR certified Jan 2026, opening ~2036",
    **PHASE4_STYLE,
).add_to(m)
for coord, name in zip(FUTURE_K_LINE_TORRANCE, ["Redondo Beach", "Torrance Transit Center"]):
    folium.CircleMarker(
        location=coord,
        radius=6,
        color=PHASE4_COLOR,
        fill=True,
        fill_color="white",
        fill_opacity=0.9,
        weight=2,
        popup=folium.Popup(f"<b>{name}</b><br>{FUTURE_K_LINE_TORRANCE_POPUP}", max_width=320),
        tooltip=f"{name} — K Line Extension to Torrance",
    ).add_to(m)

folium.PolyLine(
    FUTURE_K_LINE_NORTH,
    tooltip="Future: K Line Northern Extension — long-range, post-2040s",
    **PHASE4_STYLE,
).add_to(m)
folium.CircleMarker(
    location=FUTURE_K_LINE_NORTH[1],
    radius=6,
    color=PHASE4_COLOR,
    fill=True,
    fill_color="white",
    fill_opacity=0.9,
    weight=2,
    popup=folium.Popup(f"<b>K Line Northern Extension</b><br>{FUTURE_K_LINE_NORTH_POPUP}", max_width=320),
    tooltip="K Line Northern Extension — long-range, post-2040s",
).add_to(m)

folium.CircleMarker(
    location=D_LINE_EXTENSION_MARKER,
    radius=8,
    color=PHASE0_COLOR,
    fill=True,
    fill_color=PHASE0_COLOR,
    fill_opacity=0.95,
    weight=2,
    popup=folium.Popup(f"<b>D Line Extension, Section 1</b><br>{D_LINE_EXTENSION_POPUP}", max_width=320),
    tooltip="D Line Extension, Section 1 — Phase 0, existing/approved (opened May 2026)",
).add_to(m)

# ---------------------------------------------------------------------------
# Legend — all phases, color + line style shown together
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
<i style="font-size:11px; color:#666;">Solid + thick = real rail &nbsp;|&nbsp; Dashed/dotted + thin = bus / future / concept-only</i><br><br>
<span style="display:inline-block;width:22px;height:4px;background:#8A8D91;margin-right:8px;"></span>
Phase 0 — Existing Metro (C Line, K Line) + Sepulveda LPA (selected, unfunded)<br>
<span style="display:inline-block;width:22px;height:0;border-top:3px dashed #E8720C;margin-right:8px;"></span>
Phase 1 — Bus feeder route<br>
<span style="display:inline-block;width:22px;height:4px;background:#1F9D6B;margin-right:8px;"></span>
Phase 2 — New Connector (concept, contingent on the extension concept)<br>
<span style="display:inline-block;width:16px;height:16px;background:rgba(242,183,5,0.3);border:1px solid #F2B705;border-radius:50%;margin-right:8px;"></span>
Phase 3 — Station-area density zone (0.5 mi)<br>
<span style="display:inline-block;width:22px;height:0;border-top:3px dotted #5B9BD9;margin-right:8px;"></span>
Phase 4 — Future / Planned / LA Connect Extension Concept (not part of Metro's LPA)<br><br>
<span style="display:inline-block;width:12px;height:12px;background:#8A8D91;border-radius:50%;margin-right:8px;"></span>
Existing / real station<br>
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
