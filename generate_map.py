"""
LA Connect — 110 Gateway Network - Interactive Map
Generates an interactive Folium map showing a conceptual underground/grade-separated
rail trunk along the I-110 corridor (Downtown LA -> South LA -> Long Beach) with
Games-era express bus feeders, plus a Post-Games Legacy rail expansion.

Run: python3 generate_map.py
Output: output/la_405_transit_concept.html
"""

import os

import folium

# ---------------------------------------------------------------------------
# Palette + shared line-style dicts
# ---------------------------------------------------------------------------
# Rule enforced everywhere: solid + thick = rail (regardless of phase),
# dashed + thin = bus (regardless of phase). Only the color changes by phase.

RAIL_COLOR = "#0B3C6B"    # dark blue — Games-era
BUS_COLOR = "#E8720C"     # orange — Games-era
LEGACY_COLOR = "#1F9D6B"  # deep green — Post-Games legacy phase

RAIL_WEIGHT = 6
BUS_WEIGHT = 3.5
BUS_DASH = "8,6"

GAMES_RAIL_STYLE = dict(color=RAIL_COLOR, weight=RAIL_WEIGHT, opacity=0.9)
GAMES_BUS_STYLE = dict(color=BUS_COLOR, weight=BUS_WEIGHT, opacity=0.85, dash_array=BUS_DASH)
LEGACY_RAIL_STYLE = dict(color=LEGACY_COLOR, weight=RAIL_WEIGHT, opacity=0.9)
LEGACY_BUS_STYLE = dict(color=LEGACY_COLOR, weight=BUS_WEIGHT, opacity=0.85, dash_array=BUS_DASH)  # unused: no legacy bus routes in this data set

# ---------------------------------------------------------------------------
# Data — Games-era I-110 trunk
# ---------------------------------------------------------------------------

TRUNK_STATIONS = [
    {"name": "Downtown LA / Union Station", "coords": (34.0561, -118.2365)},
    {"name": "Downtown LA / LA Live & Crypto.com Arena", "coords": (34.0430, -118.2673)},
    {"name": "USC / Exposition Park", "coords": (34.0224, -118.2851)},
    {"name": "Watts / 103rd Street", "coords": (33.9425, -118.2412)},
    {"name": "Compton Station", "coords": (33.8958, -118.2201)},
    {"name": "Long Beach (North Long Beach Hub)", "coords": (33.8853, -118.1937)},
]

# Culver City / Palms is a Games-era bus hub (not on the rail trunk) that becomes
# a Legacy rail station in Phase 2 — a "bus stop upgraded to permanent rail" story.
CULVER_CITY_PALMS_COORDS = (34.0211, -118.3965)

# Bus feeders branch off the nearest trunk station; Culver City / Palms is itself a
# second-hop hub with its own onward feeders (USC -> Culver City/Palms -> {...}).
BUS_FEEDERS = [
    {"from": "USC / Exposition Park", "to": "Culver City / Palms", "coords": CULVER_CITY_PALMS_COORDS},
    {"from": "USC / Exposition Park", "to": "Hollywood / Highland", "coords": (34.1016, -118.3269)},
    {"from": "Culver City / Palms", "to": "Santa Monica", "coords": (34.0195, -118.4912)},
    {"from": "Culver City / Palms", "to": "LAX / Inglewood", "coords": (33.9535, -118.3392)},
    {"from": "Culver City / Palms", "to": "SoFi Stadium", "coords": (33.9535, -118.3392)},
]

STATION_POPUP = (
    "Underground Rail Station — 2 through tracks, one in each direction. "
    "Timed transfers connect to express bus feeders."
)

# ---------------------------------------------------------------------------
# Data — Post-Games Legacy rail expansion (Phase 2)
# ---------------------------------------------------------------------------
# Two true rail extensions, both anchored at the former Culver City / Palms bus hub.
# LAX / Inglewood is likewise upgraded from a bus stop to a full rail station.

LAX_INGLEWOOD_COORDS = (33.9535, -118.3392)

LEGACY_STATIONS = [
    {"name": "Culver City / Palms Station", "coords": CULVER_CITY_PALMS_COORDS,
     "note": "Upgraded from a Games-era bus hub to a permanent rail station."},
    {"name": "LAX / Inglewood Station", "coords": LAX_INGLEWOOD_COORDS,
     "note": "Upgraded from a Games-era bus stop to a permanent rail station."},
]

# Downtown connector: Culver City/Palms -> LA Live -> Union Station (shared trunk endpoints)
LEGACY_DOWNTOWN_CONNECTOR = [
    CULVER_CITY_PALMS_COORDS,
    (34.0430, -118.2673),  # Downtown LA / LA Live & Crypto.com Arena
    (34.0561, -118.2365),  # Downtown LA / Union Station
]

# West Side spine: Culver City/Palms -> LAX/Inglewood -> Watts -> Compton -> Long Beach
LEGACY_WEST_SPINE = [
    CULVER_CITY_PALMS_COORDS,
    LAX_INGLEWOOD_COORDS,
    (33.9425, -118.2412),  # Watts / 103rd Street
    (33.8958, -118.2201),  # Compton Station
    (33.8853, -118.1937),  # Long Beach (North Long Beach Hub)
]

LEGACY_FARE = 4.25  # flat fare, USD — higher than feeder-bus fare, reflecting longer distances
LEGACY_SPEED_MPH = 40  # same standard urban/commuter rail assumption as the Games-era trunk

LEGACY_POPUP_TEMPLATE = (
    "Post-Games Legacy Extension — opens after 2028.<br>"
    "{note}<br>"
    "Flat fare: ${fare:.2f}"
)

# ---------------------------------------------------------------------------
# Map setup
# ---------------------------------------------------------------------------

center_lat = sum(s["coords"][0] for s in TRUNK_STATIONS) / len(TRUNK_STATIONS)
center_lon = sum(s["coords"][1] for s in TRUNK_STATIONS) / len(TRUNK_STATIONS)

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
LA Connect — 110 Gateway Network
</div>
"""
m.get_root().html.add_child(folium.Element(title_html))

# ---------------------------------------------------------------------------
# Games-era rail trunk + stations
# ---------------------------------------------------------------------------

trunk_coords = [s["coords"] for s in TRUNK_STATIONS]
folium.PolyLine(
    trunk_coords,
    tooltip="I-110 Rail Trunk (underground / grade-separated, double track)",
    **GAMES_RAIL_STYLE,
).add_to(m)

for station in TRUNK_STATIONS:
    lat, lon = station["coords"]
    folium.Marker(
        location=[lat, lon],
        popup=folium.Popup(f"<b>{station['name']}</b><br>{STATION_POPUP}", max_width=280),
        tooltip=station["name"],
        icon=folium.Icon(color="blue", icon="train", prefix="fa"),
    ).add_to(m)

# ---------------------------------------------------------------------------
# Games-era bus feeders (two-hop: trunk -> Culver City/Palms -> onward stops)
# ---------------------------------------------------------------------------

station_lookup = {s["name"]: s["coords"] for s in TRUNK_STATIONS}
station_lookup["Culver City / Palms"] = CULVER_CITY_PALMS_COORDS

for feeder in BUS_FEEDERS:
    start = station_lookup[feeder["from"]]
    end = feeder["coords"]

    folium.PolyLine(
        [start, end],
        tooltip=f"Express bus feeder: {feeder['from']} to {feeder['to']}",
        **GAMES_BUS_STYLE,
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
# Post-Games Legacy rail expansion (Phase 2) — solid + thick, matching trunk weight
# ---------------------------------------------------------------------------

folium.PolyLine(
    LEGACY_DOWNTOWN_CONNECTOR,
    tooltip="Legacy Downtown Connector (rail): Culver City / Palms → Downtown LA / Union Station — opens after 2028",
    **LEGACY_RAIL_STYLE,
).add_to(m)

folium.PolyLine(
    LEGACY_WEST_SPINE,
    tooltip="Legacy West Side Spine (rail): Culver City / Palms → Long Beach — opens after 2028",
    **LEGACY_RAIL_STYLE,
).add_to(m)

for station in LEGACY_STATIONS:
    lat, lon = station["coords"]
    folium.Marker(
        location=[lat, lon],
        popup=folium.Popup(
            f"<b>{station['name']}</b><br>"
            + LEGACY_POPUP_TEMPLATE.format(note=station["note"], fare=LEGACY_FARE),
            max_width=300,
        ),
        tooltip=f"{station['name']} — Legacy Phase",
        icon=folium.Icon(color="green", icon="train", prefix="fa"),
    ).add_to(m)

# ---------------------------------------------------------------------------
# Legend — four line-style/color combinations (color + line style, not color alone)
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

os.makedirs("output", exist_ok=True)
output_path = "output/la_405_transit_concept.html"
m.save(output_path)
print(f"Interactive map saved to {output_path}")
