"""
LA 405 Rail + Bus Feeder Network - Interactive Map
Generates an interactive Folium map showing a conceptual underground/grade-separated
rail trunk along the I-405 corridor with express bus feeder routes branching into
nearby neighborhoods.

Run: python3 generate_map.py
Output: output/la_405_transit_concept.html
"""

import folium
from folium import DivIcon

# ---------------------------------------------------------------------------
# Data
# ---------------------------------------------------------------------------

RAIL_STATIONS = [
    {"name": "LAX / Westchester Station", "coords": (33.9416, -118.4085)},
    {"name": "Culver City / Palms Station", "coords": (34.0211, -118.3965)},
    {"name": "Sepulveda Pass / UCLA Station", "coords": (34.0736, -118.4390)},
    {"name": "Sherman Oaks / Van Nuys Station", "coords": (34.1510, -118.4480)},
]

BUS_FEEDERS = [
    {"from": "LAX / Westchester Station", "to": "Westchester", "coords": (33.9597, -118.3965)},
    {"from": "LAX / Westchester Station", "to": "Playa Vista", "coords": (33.9760, -118.4180)},
    {"from": "Culver City / Palms Station", "to": "Palms", "coords": (34.0203, -118.4140)},
    {"from": "Culver City / Palms Station", "to": "Mar Vista", "coords": (34.0037, -118.4300)},
    {"from": "Sepulveda Pass / UCLA Station", "to": "UCLA / Westwood", "coords": (34.0689, -118.4452)},
    {"from": "Sepulveda Pass / UCLA Station", "to": "Brentwood", "coords": (34.0522, -118.4695)},
    {"from": "Sherman Oaks / Van Nuys Station", "to": "Sherman Oaks", "coords": (34.1511, -118.4490)},
    {"from": "Sherman Oaks / Van Nuys Station", "to": "Van Nuys", "coords": (34.1867, -118.4489)},
]

# Post-Games Legacy Network — Phase 2 rail extension opening after the 2028 Olympics,
# branching from the existing Culver City / Palms hub into two corridors.
LEGACY_STATIONS = [
    {"name": "Downtown LA / Union Station", "coords": (34.0561, -118.2365)},
    {"name": "Downtown LA / LA Live & Convention Center", "coords": (34.0430, -118.2673)},
    {"name": "Compton Station", "coords": (33.8958, -118.2201)},
    {"name": "Inglewood / SoFi Stadium", "coords": (33.9535, -118.3392)},
    {"name": "Watts / 103rd Street", "coords": (33.9425, -118.2412)},
    {"name": "Long Beach (North Long Beach Hub)", "coords": (33.8853, -118.1937)},
]

CULVER_CITY_COORDS = (34.0211, -118.3965)

# North corridor: Culver City -> Downtown LA / LA Live -> Downtown LA / Union Station
LEGACY_NORTH_CORRIDOR = [
    CULVER_CITY_COORDS,
    (34.0430, -118.2673),
    (34.0561, -118.2365),
]

# South corridor: Culver City -> Inglewood/SoFi -> Watts -> Compton -> Long Beach
LEGACY_SOUTH_CORRIDOR = [
    CULVER_CITY_COORDS,
    (33.9535, -118.3392),
    (33.9425, -118.2412),
    (33.8958, -118.2201),
    (33.8853, -118.1937),
]

LEGACY_FARE = 4.25  # flat fare, USD — higher than feeder-bus fare, reflecting longer distances
LEGACY_SPEED_MPH = 40  # same standard urban/commuter rail assumption as the Games-era trunk

RAIL_COLOR = "#0B3C6B"    # dark blue — Games-era rail (unchanged)
BUS_COLOR = "#E8720C"     # orange — Games-era bus feeders (unchanged)
LEGACY_COLOR = "#1F9D6B"  # deep green — Post-Games legacy extension (new, distinct layer)

STATION_POPUP = (
    "Underground Rail Station — 2 through tracks, one in each direction. "
    "Timed transfers connect to express bus feeders."
)

LEGACY_POPUP_TEMPLATE = (
    "Post-Games Legacy Extension — opens after 2028.<br>"
    "Permanent rail service beyond the Olympics window.<br>"
    "Flat fare: ${fare:.2f}"
)

# ---------------------------------------------------------------------------
# Map setup
# ---------------------------------------------------------------------------

center_lat = sum(s["coords"][0] for s in RAIL_STATIONS) / len(RAIL_STATIONS)
center_lon = sum(s["coords"][1] for s in RAIL_STATIONS) / len(RAIL_STATIONS)

m = folium.Map(
    location=[center_lat, center_lon],
    zoom_start=11,
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
LA 405 Integrated Rail + Bus Feeder Concept
</div>
"""
m.get_root().html.add_child(folium.Element(title_html))

# ---------------------------------------------------------------------------
# Rail trunk line
# ---------------------------------------------------------------------------

rail_coords = [s["coords"] for s in RAIL_STATIONS]
folium.PolyLine(
    rail_coords,
    color=RAIL_COLOR,
    weight=6,
    opacity=0.9,
    tooltip="405 Rail Trunk (underground / grade-separated, double track)",
).add_to(m)

# ---------------------------------------------------------------------------
# Rail stations
# ---------------------------------------------------------------------------

for station in RAIL_STATIONS:
    lat, lon = station["coords"]
    folium.Marker(
        location=[lat, lon],
        popup=folium.Popup(f"<b>{station['name']}</b><br>{STATION_POPUP}", max_width=280),
        tooltip=station["name"],
        icon=folium.Icon(color="blue", icon="train", prefix="fa"),
    ).add_to(m)

# ---------------------------------------------------------------------------
# Bus feeder routes + destination markers
# ---------------------------------------------------------------------------

station_lookup = {s["name"]: s["coords"] for s in RAIL_STATIONS}

for feeder in BUS_FEEDERS:
    start = station_lookup[feeder["from"]]
    end = feeder["coords"]

    folium.PolyLine(
        [start, end],
        color=BUS_COLOR,
        weight=3.5,
        opacity=0.85,
        dash_array="8,6",
        tooltip=f"Express bus feeder: {feeder['from']} to {feeder['to']}",
    ).add_to(m)

    folium.CircleMarker(
        location=end,
        radius=8,
        color=BUS_COLOR,
        fill=True,
        fill_color=BUS_COLOR,
        fill_opacity=0.9,
        popup=folium.Popup(
            f"<b>{feeder['to']}</b><br>Bus Feeder Stop / Local Business District<br>"
            f"<i>Food perk redemptions available for riders</i>",
            max_width=260,
        ),
        tooltip=f"{feeder['to']} — Bus Feeder Stop / Local Business District",
    ).add_to(m)

# ---------------------------------------------------------------------------
# Post-Games Legacy Network (Phase 2) — distinct green layer
# ---------------------------------------------------------------------------

folium.PolyLine(
    LEGACY_NORTH_CORRIDOR,
    color=LEGACY_COLOR,
    weight=6,  # solid + thick, matching the Games-era rail trunk — this is rail, not a bus feeder
    opacity=0.9,
    tooltip="Legacy North Corridor (rail): Culver City / Palms → Downtown LA — opens after 2028",
).add_to(m)

folium.PolyLine(
    LEGACY_SOUTH_CORRIDOR,
    color=LEGACY_COLOR,
    weight=6,  # solid + thick, matching the Games-era rail trunk — this is rail, not a bus feeder
    opacity=0.9,
    tooltip="Legacy South Corridor (rail): Culver City / Palms → Long Beach — opens after 2028",
).add_to(m)

for station in LEGACY_STATIONS:
    lat, lon = station["coords"]
    folium.CircleMarker(
        location=[lat, lon],
        radius=9,
        color=LEGACY_COLOR,
        fill=True,
        fill_color=LEGACY_COLOR,
        fill_opacity=0.95,
        weight=2,
        popup=folium.Popup(
            f"<b>{station['name']}</b><br>{LEGACY_POPUP_TEMPLATE.format(fare=LEGACY_FARE)}",
            max_width=280,
        ),
        tooltip=f"{station['name']} — Legacy Phase",
    ).add_to(m)

# ---------------------------------------------------------------------------
# Legend
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
<i style="font-size:11px; color:#666;">Solid + thick = rail &nbsp;|&nbsp; Dashed + thin = bus</i><br><br>
<span style="display:inline-block;width:22px;height:4px;background:#0B3C6B;margin-right:8px;"></span>
Games-era rail trunk<br>
<span style="display:inline-block;width:22px;height:0;border-top:3px dashed #E8720C;margin-right:8px;"></span>
Games-era bus feeder route<br>
<span style="display:inline-block;width:22px;height:4px;background:#1F9D6B;margin-right:8px;"></span>
Legacy rail extension (post-Games)<br>
<span style="display:inline-block;width:12px;height:12px;background:#3186cc;border-radius:50%;margin-right:8px;"></span>
Rail station<br>
<span style="display:inline-block;width:12px;height:12px;background:#E8720C;border-radius:50%;margin-right:8px;"></span>
Bus stop / local business district
</div>
"""
m.get_root().html.add_child(folium.Element(legend_html))

# ---------------------------------------------------------------------------
# Save
# ---------------------------------------------------------------------------

import os

os.makedirs("output", exist_ok=True)
output_path = "output/la_405_transit_concept.html"
m.save(output_path)
print(f"Interactive map saved to {output_path}")
