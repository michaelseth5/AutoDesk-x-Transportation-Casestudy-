"""
LA Connect — 110 Gateway Network - Presentation Schematic
Generates a clean, minimal infographic (Matplotlib) showing the I-110 rail trunk,
six Games-era stations, bus feeder branches (including the Culver City / Palms
second-hop hub), an underground station cross-section, and the Post-Games Legacy
rail expansion.

Run: python3 generate_schematic.py
Output: output/la_405_transit_schematic.png
"""

import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.patheffects as pe
from matplotlib.lines import Line2D

# ---------------------------------------------------------------------------
# Palette + shared line-weight/style constants
# ---------------------------------------------------------------------------
# Rule enforced everywhere: solid + thick (RAIL_WIDTH) = rail, regardless of phase.
# Dashed + thin (BUS_WIDTH) = bus, regardless of phase. Only color changes by phase.

RAIL_COLOR = "#0B3C6B"
BUS_COLOR = "#E8720C"
LEGACY_COLOR = "#1F9D6B"  # deep green — Post-Games legacy extension (Phase 2)
GRAY = "#6E6E6E"
LIGHT_GRAY = "#D9D9D9"
BG = "#FFFFFF"

RAIL_WIDTH = 4
BUS_WIDTH = 1.8
BUS_LINESTYLE = (0, (5, 3))

# ---------------------------------------------------------------------------
# Figure setup
# ---------------------------------------------------------------------------

fig, ax = plt.subplots(figsize=(11, 23), dpi=200)
ax.set_xlim(0, 100)
ax.set_ylim(-58, 174)
ax.axis("off")
fig.patch.set_facecolor(BG)

# Title
ax.text(50, 170, "LA Connect — 110 Gateway Network", ha="center",
        fontsize=20, fontweight="bold", color=RAIL_COLOR, family="sans-serif")
ax.text(50, 166, "Rail for speed  •  Buses for last-mile access", ha="center",
        fontsize=12.5, color=GRAY, style="italic")

# Manual legend rows (data coordinates, avoids overlap with title text and the trunk diagram below)
legend_y = 162
ax.plot([6, 12], [legend_y, legend_y], color=RAIL_COLOR, linewidth=RAIL_WIDTH, solid_capstyle="round")
ax.text(14, legend_y, "Games-era rail trunk (2 tracks)", va="center", fontsize=8.7, color="#333333")
ax.plot([48, 54], [legend_y, legend_y], color=BUS_COLOR, linewidth=BUS_WIDTH, linestyle=BUS_LINESTYLE)
ax.text(56, legend_y, "Games-era bus feeder route", va="center", fontsize=8.7, color="#333333")
ax.scatter([6], [legend_y - 4], s=110, color=RAIL_COLOR, zorder=6, edgecolors="white", linewidths=1.2)
ax.text(9.5, legend_y - 4, "Rail station", va="center", fontsize=8.7, color="#333333")
ax.add_patch(patches.FancyBboxPatch((46, legend_y - 5.6), 4, 3.2,
                                     boxstyle="round,pad=0.2,rounding_size=0.8",
                                     facecolor="#FDEBD8", edgecolor=BUS_COLOR, linewidth=1))
ax.text(52, legend_y - 4, "Bus feeder stop / local business district",
        va="center", fontsize=8.7, color="#333333")
ax.plot([6, 12], [legend_y - 8, legend_y - 8], color=LEGACY_COLOR, linewidth=RAIL_WIDTH, solid_capstyle="round")
ax.text(14, legend_y - 8, "Legacy rail extension (post-Games)", va="center", fontsize=8.7, color="#333333")
ax.text(56, legend_y - 8, "Solid + thick = rail  |  Dashed + thin = bus", va="center",
        fontsize=8, color="#666666", style="italic")

# ---------------------------------------------------------------------------
# Main schematic: vertical I-110 rail trunk with 6 stations
# ---------------------------------------------------------------------------

trunk_x_left = 47
trunk_x_right = 53
trunk_top = 145
trunk_bottom = 48

# Two parallel dark-blue tracks
ax.plot([trunk_x_left, trunk_x_left], [trunk_bottom, trunk_top],
        color=RAIL_COLOR, linewidth=RAIL_WIDTH, solid_capstyle="round", zorder=2)
ax.plot([trunk_x_right, trunk_x_right], [trunk_bottom, trunk_top],
        color=RAIL_COLOR, linewidth=RAIL_WIDTH, solid_capstyle="round", zorder=2)
ax.text(50, trunk_top + 2.2, "I-110 Rail Trunk (double track)", ha="center",
        fontsize=10.5, color=RAIL_COLOR, fontweight="bold")

stations = [
    {"name": "Downtown LA /\nUnion Station", "y": 138, "left": [], "right": []},
    {"name": "Downtown LA / LA Live &\nCrypto.com Arena", "y": 121, "left": [], "right": []},
    {"name": "USC / Exposition\nPark", "y": 104,
     "left": [("Culver City / Palms — bus hub\n→ Santa Monica · LAX/Inglewood · SoFi Stadium", 104)],
     "right": [("Hollywood / Highland", 104)]},
    {"name": "Watts / 103rd\nStreet", "y": 87, "left": [], "right": []},
    {"name": "Compton\nStation", "y": 70, "left": [], "right": []},
    {"name": "Long Beach\n(North Long Beach Hub)", "y": 53, "left": [], "right": []},
]

label_box_w = 15
label_box_h = 6.5


def draw_branch_label(ax, x, y, text, align="left", w=label_box_w, h=label_box_h, fontsize=8.3):
    """Draw a small rounded label box for a neighborhood destination."""
    box_x = x if align == "left" else x - w
    box = patches.FancyBboxPatch(
        (box_x, y - h / 2), w, h,
        boxstyle="round,pad=0.3,rounding_size=1.2",
        linewidth=1, edgecolor=BUS_COLOR, facecolor="#FDEBD8", zorder=4,
    )
    ax.add_patch(box)
    ax.text(box_x + w / 2, y, text, ha="center", va="center",
            fontsize=fontsize, color="#7A3B00", fontweight="bold", zorder=5)


for st in stations:
    y = st["y"]

    # Station node on trunk
    ax.scatter([50], [y], s=180, color=RAIL_COLOR, zorder=6,
               edgecolors="white", linewidths=1.5)
    ax.text(50, y + 3.6, st["name"], ha="center", va="bottom",
            fontsize=9.5, fontweight="bold", color="#1A1A1A", zorder=6,
            path_effects=[pe.withStroke(linewidth=3, foreground="white")])

    # Left branches (orange, dashed) — the Culver City / Palms hub box is wider to
    # fit its onward stops (Santa Monica, LAX/Inglewood, SoFi Stadium) on one label.
    for label, ly in st["left"]:
        is_hub = "bus hub" in label
        w = 30 if is_hub else label_box_w
        ax.plot([trunk_x_left, 30, 15], [y, y, ly],
                color=BUS_COLOR, linewidth=BUS_WIDTH, linestyle=BUS_LINESTYLE, zorder=3)
        draw_branch_label(ax, 0, ly, label, align="left", w=w, h=9 if is_hub else label_box_h, fontsize=7.4 if is_hub else 8.3)

    # Right branches (orange, dashed)
    for label, ly in st["right"]:
        ax.plot([trunk_x_right, 70, 85], [y, y, ly],
                color=BUS_COLOR, linewidth=BUS_WIDTH, linestyle=BUS_LINESTYLE, zorder=3)
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
ax.text(50, road_y, "I-110 Freeway (surface)", ha="center", va="center",
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
        "Opens after 2028 — Culver City / Palms and LAX / Inglewood upgrade from bus stops to full rail stations",
        ha="center", va="center", fontsize=8.6, color="#333333", style="italic")

# Shared origin: Culver City / Palms — a NEW legacy rail station (green), not an existing one
origin_x, origin_y = 50, -18
ax.scatter([origin_x], [origin_y], s=180, color=LEGACY_COLOR, zorder=6, edgecolors="white", linewidths=1.5)
ax.text(origin_x, origin_y + 3.4, "Culver City / Palms Station\n(upgraded from bus hub)", ha="center", va="bottom",
        fontsize=8.3, fontweight="bold", color="#1A1A1A", zorder=6,
        path_effects=[pe.withStroke(linewidth=3, foreground="white")])

north_x = 28
south_x = 72

# Downtown Connector (rail — solid + thick, same weight as the Games-era trunk)
ax.plot([origin_x, north_x, north_x], [origin_y, -25, -33],
        color=LEGACY_COLOR, linewidth=RAIL_WIDTH, solid_capstyle="round", zorder=3)
ax.text(north_x, -21.5, "Downtown Connector (rail)", ha="center", va="center",
        fontsize=9.5, fontweight="bold", color=LEGACY_COLOR)

# West Side Spine (rail — solid + thick, same weight as the Games-era trunk)
ax.plot([origin_x, south_x, south_x, south_x, south_x], [origin_y, -25, -33, -41, -49],
        color=LEGACY_COLOR, linewidth=RAIL_WIDTH, solid_capstyle="round", zorder=3)
ax.text(south_x, -21.5, "West Side Spine (rail)", ha="center", va="center",
        fontsize=9.5, fontweight="bold", color=LEGACY_COLOR)

legacy_stops = [
    (north_x, -25, "Downtown LA / LA Live &\nCrypto.com Arena", "right"),
    (north_x, -33, "Downtown LA /\nUnion Station", "right"),
    (south_x, -25, "LAX / Inglewood Station\n(upgraded from bus stop)", "left"),
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
