"""
LA 405 Rail + Bus Feeder Network - Presentation Schematic
Generates a clean, minimal infographic (Matplotlib) showing the rail trunk,
four stations, bus feeder branches, and an underground station cross-section.

Run: python3 generate_schematic.py
Output: output/la_405_transit_schematic.png
"""

import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.patheffects as pe
from matplotlib.lines import Line2D

# ---------------------------------------------------------------------------
# Palette
# ---------------------------------------------------------------------------

RAIL_COLOR = "#0B3C6B"
BUS_COLOR = "#E8720C"
LEGACY_COLOR = "#1F9D6B"  # deep green — Post-Games legacy extension (Phase 2)
GRAY = "#6E6E6E"
LIGHT_GRAY = "#D9D9D9"
BG = "#FFFFFF"

# ---------------------------------------------------------------------------
# Figure setup
# ---------------------------------------------------------------------------

fig, ax = plt.subplots(figsize=(11, 23), dpi=200)
ax.set_xlim(0, 100)
ax.set_ylim(-58, 174)
ax.axis("off")
fig.patch.set_facecolor(BG)

# Title
ax.text(50, 170, "LA 405 Integrated Rail + Bus Feeder Concept", ha="center",
        fontsize=20, fontweight="bold", color=RAIL_COLOR, family="sans-serif")
ax.text(50, 166, "Rail for speed  \u2022  Buses for last-mile access", ha="center",
        fontsize=12.5, color=GRAY, style="italic")

# Manual legend rows (data coordinates, avoids overlap with title text and the trunk diagram below)
legend_y = 162
ax.plot([6, 12], [legend_y, legend_y], color=RAIL_COLOR, linewidth=4, solid_capstyle="round")
ax.text(14, legend_y, "Games-era rail trunk (2 tracks)", va="center", fontsize=8.7, color="#333333")
ax.plot([48, 54], [legend_y, legend_y], color=BUS_COLOR, linewidth=2, linestyle=(0, (5, 3)))
ax.text(56, legend_y, "Games-era bus feeder route", va="center", fontsize=8.7, color="#333333")
ax.scatter([6], [legend_y - 4], s=110, color=RAIL_COLOR, zorder=6, edgecolors="white", linewidths=1.2)
ax.text(9.5, legend_y - 4, "Rail station", va="center", fontsize=8.7, color="#333333")
ax.add_patch(patches.FancyBboxPatch((46, legend_y - 5.6), 4, 3.2,
                                     boxstyle="round,pad=0.2,rounding_size=0.8",
                                     facecolor="#FDEBD8", edgecolor=BUS_COLOR, linewidth=1))
ax.text(52, legend_y - 4, "Bus feeder stop / local business district",
        va="center", fontsize=8.7, color="#333333")
ax.plot([6, 12], [legend_y - 8, legend_y - 8], color=LEGACY_COLOR, linewidth=4, solid_capstyle="round")
ax.text(14, legend_y - 8, "Legacy rail extension (post-Games)", va="center", fontsize=8.7, color="#333333")
ax.text(56, legend_y - 8, "Solid + thick = rail  |  Dashed + thin = bus", va="center",
        fontsize=8, color="#666666", style="italic")

# ---------------------------------------------------------------------------
# Main schematic: vertical rail trunk with 4 stations
# ---------------------------------------------------------------------------

trunk_x_left = 47
trunk_x_right = 53
trunk_top = 145
trunk_bottom = 48

# Two parallel dark-blue tracks
ax.plot([trunk_x_left, trunk_x_left], [trunk_bottom, trunk_top],
        color=RAIL_COLOR, linewidth=4, solid_capstyle="round", zorder=2)
ax.plot([trunk_x_right, trunk_x_right], [trunk_bottom, trunk_top],
        color=RAIL_COLOR, linewidth=4, solid_capstyle="round", zorder=2)
ax.text(50, trunk_top + 2.2, "I-405 Rail Trunk (double track)", ha="center",
        fontsize=10.5, color=RAIL_COLOR, fontweight="bold")

stations = [
    {"name": "LAX / Westchester\nStation", "y": 134,
     "left": [("Westchester", 126), ("Playa Vista", 118)],
     "right": [("El Segundo area", 126)]},
    {"name": "Culver City / Palms\nStation", "y": 108,
     "left": [("Palms", 100), ("Mar Vista", 92)],
     "right": [("Culver City core", 100)]},
    {"name": "Sepulveda Pass / UCLA\nStation", "y": 80,
     "left": [("UCLA / Westwood", 72), ("Brentwood", 64)],
     "right": [("Bel-Air area", 72)]},
    {"name": "Sherman Oaks / Van Nuys\nStation", "y": 53,
     "left": [("Sherman Oaks", 45)],
     "right": [("Van Nuys", 45)]},
]

label_box_w = 15
label_box_h = 6.5


def draw_branch_label(ax, x, y, text, align="left"):
    """Draw a small rounded label box for a neighborhood destination."""
    box_x = x if align == "left" else x - label_box_w
    box = patches.FancyBboxPatch(
        (box_x, y - label_box_h / 2), label_box_w, label_box_h,
        boxstyle="round,pad=0.3,rounding_size=1.2",
        linewidth=1, edgecolor=BUS_COLOR, facecolor="#FDEBD8", zorder=4,
    )
    ax.add_patch(box)
    ax.text(box_x + label_box_w / 2, y, text, ha="center", va="center",
            fontsize=8.3, color="#7A3B00", fontweight="bold", zorder=5)


for st in stations:
    y = st["y"]

    # Station node on trunk
    ax.scatter([50], [y], s=180, color=RAIL_COLOR, zorder=6,
               edgecolors="white", linewidths=1.5)
    ax.text(50, y + 3.6, st["name"], ha="center", va="bottom",
            fontsize=9.5, fontweight="bold", color="#1A1A1A", zorder=6,
            path_effects=[pe.withStroke(linewidth=3, foreground="white")])

    # Left branches (orange, dashed)
    n_left = len(st["left"])
    for i, (label, ly) in enumerate(st["left"]):
        ax.plot([trunk_x_left, 30, 15], [y, y, ly],
                color=BUS_COLOR, linewidth=1.8, linestyle=(0, (5, 3)), zorder=3)
        draw_branch_label(ax, 0, ly, label, align="left")

    # Right branches (orange, dashed)
    for i, (label, ly) in enumerate(st["right"]):
        ax.plot([trunk_x_right, 70, 85], [y, y, ly],
                color=BUS_COLOR, linewidth=1.8, linestyle=(0, (5, 3)), zorder=3)
        draw_branch_label(ax, 100, ly, label, align="right")

# ---------------------------------------------------------------------------
# Underground station cross-section (bottom panel)
# ---------------------------------------------------------------------------

cs_bottom = 2
cs_top = 34
cs_left = 12
cs_right = 88

ax.plot([cs_left - 2, cs_right + 2], [cs_top, cs_top], color=GRAY, linewidth=0.8)
ax.text(50, cs_top + 4, "Underground Station Cross-Section", ha="center",
        fontsize=12, fontweight="bold", color="#1A1A1A")

# Road / freeway surface
road_y = 23
ax.add_patch(patches.Rectangle((cs_left, road_y - 1.5), cs_right - cs_left, 3,
                                facecolor=LIGHT_GRAY, edgecolor=GRAY, linewidth=0.8, zorder=2))
ax.text(50, road_y, "I-405 Freeway (surface)", ha="center", va="center",
        fontsize=8.5, color="#333333", fontweight="bold", zorder=3)

# Bus transfer plaza (surface, off to the side, above the freeway level, below the divider)
plaza_x, plaza_w, plaza_h = 66, 20, 5
plaza_y = 29
plaza = patches.FancyBboxPatch((plaza_x, plaza_y), plaza_w, plaza_h,
                                boxstyle="round,pad=0.3,rounding_size=1", facecolor="#FDEBD8",
                                edgecolor=BUS_COLOR, linewidth=1.2, zorder=3)
ax.add_patch(plaza)
ax.text(plaza_x + plaza_w / 2, plaza_y + plaza_h / 2 + 1, "Bus transfer plaza",
        ha="center", va="center", fontsize=7.6, fontweight="bold", color="#7A3B00", zorder=4)
ax.text(plaza_x + plaza_w / 2, plaza_y + plaza_h / 2 - 1.6, "Local business perks",
        ha="center", va="center", fontsize=7, color="#7A3B00", zorder=4, style="italic")

# Escalator connector (plaza down through freeway level to platform below)
esc_x = plaza_x + plaza_w / 2
ax.plot([esc_x, esc_x], [plaza_y, road_y - 1.5], color=GRAY, linewidth=1.2,
        linestyle=(0, (3, 2)), zorder=1)
ax.text(esc_x + 2, plaza_y - 3, "Escalator /\nelevator", fontsize=6.8,
        color=GRAY, va="center", ha="left")

# Underground station box
station_box_y = cs_bottom + 2
station_box_h = 13
ax.add_patch(patches.FancyBboxPatch((cs_left, station_box_y), cs_right - cs_left, station_box_h,
                                     boxstyle="round,pad=0.3,rounding_size=1.5",
                                     facecolor="#EAF1F8", edgecolor=RAIL_COLOR, linewidth=1.2, zorder=2))
ax.text(cs_left + 2, station_box_y + station_box_h - 1.5, "Underground station box",
        fontsize=8.5, fontweight="bold", color=RAIL_COLOR, va="top")

# Escalator continues down into station box
ax.plot([esc_x, esc_x], [station_box_y + station_box_h, road_y - 1.5],
        color=GRAY, linewidth=1.2, linestyle=(0, (3, 2)), zorder=1)

# Track 1 (northbound)
track1_y = station_box_y + station_box_h - 5
ax.add_patch(patches.Rectangle((cs_left + 3, track1_y - 1.2), cs_right - cs_left - 6, 2.4,
                                facecolor=RAIL_COLOR, alpha=0.85, zorder=3))
ax.text(50, track1_y, "Track 1 — Northbound", ha="center", va="center",
        fontsize=7.8, color="white", fontweight="bold", zorder=4)

# Platform
platform_y = track1_y - 4
ax.add_patch(patches.Rectangle((cs_left + 3, platform_y - 1.4), cs_right - cs_left - 6, 2.8,
                                facecolor=LIGHT_GRAY, edgecolor=GRAY, linewidth=0.6, zorder=3))
ax.text(50, platform_y, "Platform", ha="center", va="center",
        fontsize=7.8, color="#333333", fontweight="bold", zorder=4)

# Track 2 (southbound)
track2_y = platform_y - 4
ax.add_patch(patches.Rectangle((cs_left + 3, track2_y - 1.2), cs_right - cs_left - 6, 2.4,
                                facecolor=RAIL_COLOR, alpha=0.85, zorder=3))
ax.text(50, track2_y, "Track 2 — Southbound", ha="center", va="center",
        fontsize=7.8, color="white", fontweight="bold", zorder=4)

# Caption
ax.text(50, cs_bottom - 0.5,
        "Two-track rail is the baseline: one track in each direction.\n"
        "Major future hubs could expand to four tracks for express and local service.",
        ha="center", va="top", fontsize=9, color="#333333", style="italic",
        family="sans-serif")

# ---------------------------------------------------------------------------
# Phase 2: Post-Games Legacy Network — separated section, distinct green layer
# ---------------------------------------------------------------------------

ax.plot([2, 98], [-2, -2], color=GRAY, linewidth=0.8)
ax.text(50, -7, "Phase 2: Post-Games Legacy Network", ha="center", va="center",
        fontsize=15, fontweight="bold", color=LEGACY_COLOR, family="sans-serif")
ax.text(50, -11.5,
        "Opens after 2028 — permanent service extending to Downtown LA, South LA, and Long Beach",
        ha="center", va="center", fontsize=8.8, color="#333333", style="italic")

# Shared origin: the existing Culver City / Palms hub (drawn in rail navy — it is not a new station)
origin_x, origin_y = 50, -18
ax.scatter([origin_x], [origin_y], s=170, color=RAIL_COLOR, zorder=6, edgecolors="white", linewidths=1.5)
ax.text(origin_x, origin_y + 3.4, "Culver City / Palms Station (existing hub)", ha="center", va="bottom",
        fontsize=8.3, fontweight="bold", color="#1A1A1A", zorder=6,
        path_effects=[pe.withStroke(linewidth=3, foreground="white")])

north_x = 28
south_x = 72

# North corridor branch line (rail — solid + thick, matching the Games-era trunk weight): origin -> Downtown LA
ax.plot([origin_x, north_x, north_x], [origin_y, -25, -33],
        color=LEGACY_COLOR, linewidth=4, solid_capstyle="round", zorder=3)
ax.text(north_x, -21.5, "North Corridor (rail)", ha="center", va="center",
        fontsize=9.5, fontweight="bold", color=LEGACY_COLOR)

# South corridor branch line (rail — solid + thick, matching the Games-era trunk weight): origin -> Long Beach
ax.plot([origin_x, south_x, south_x, south_x, south_x], [origin_y, -25, -33, -41, -49],
        color=LEGACY_COLOR, linewidth=4, solid_capstyle="round", zorder=3)
ax.text(south_x, -21.5, "South Corridor (rail)", ha="center", va="center",
        fontsize=9.5, fontweight="bold", color=LEGACY_COLOR)

legacy_stops = [
    (north_x, -25, "Downtown LA / LA Live &\nConvention Center", "right"),
    (north_x, -33, "Downtown LA /\nUnion Station", "right"),
    (south_x, -25, "Inglewood / SoFi Stadium", "left"),
    (south_x, -33, "Watts / 103rd Street", "left"),
    (south_x, -41, "Compton Station", "left"),
    (south_x, -49, "Long Beach\n(North Long Beach Hub)", "left"),
]

for x, y, label, side in legacy_stops:
    ax.scatter([x], [y], s=180, color=LEGACY_COLOR, zorder=6, edgecolors="white", linewidths=1.5)
    label_x = x - 3 if side == "right" else x + 3
    ha = "right" if side == "right" else "left"
    ax.text(label_x, y, label, ha=ha, va="center", fontsize=8, fontweight="bold",
            color="#0F5C40", zorder=5,
            path_effects=[pe.withStroke(linewidth=2.5, foreground="white")])

ax.text(50, -55,
        "Legacy rail extension assumed at 35-45 mph (same standard urban rail speed as Phase 1).\n"
        "Flat legacy fare: $4.25 — reflects longer trip distances beyond the Games-era network.",
        ha="center", va="top", fontsize=8.6, color="#333333", style="italic", family="sans-serif")

# ---------------------------------------------------------------------------
# Save
# ---------------------------------------------------------------------------

os.makedirs("output", exist_ok=True)
output_path = "output/la_405_transit_schematic.png"
plt.savefig(output_path, dpi=200, bbox_inches="tight", facecolor=BG)
print(f"Schematic saved to {output_path}")
