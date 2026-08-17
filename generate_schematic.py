"""
LA Connect — Sepulveda + C Line Network - Presentation Schematic
Generates a clean, minimal infographic (Matplotlib) showing the Sepulveda Transit
Corridor (existing/approved, underground) as the main trunk, its bus feeders, an
underground station cross-section, and — below that — how the corridor meets Metro's
real, existing C Line at LAX via the one new rail segment this project proposes,
plus station-area density zones and a future regional link.

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
# Phase 0 (existing/approved): solid, thick, muted gray.
# Phase 1 (bus feeders): dashed, thin, orange.
# Phase 2 (the one new rail segment): solid, thick, green.
# Phase 3 (density zones): translucent dotted-edge gold rings around stations.
# Phase 4 (future/planned regional link): dotted, thin, light blue.

PHASE0_COLOR = "#8A8D91"
PHASE1_COLOR = "#E8720C"
PHASE2_COLOR = "#1F9D6B"
PHASE3_COLOR = "#F2B705"
PHASE4_COLOR = "#5B9BD9"
GRAY = "#6E6E6E"
LIGHT_GRAY = "#D9D9D9"
BG = "#FFFFFF"

RAIL_WIDTH = 4
BUS_WIDTH = 1.8
BUS_LINESTYLE = (0, (5, 3))
FUTURE_LINESTYLE = (0, (1, 2))

# ---------------------------------------------------------------------------
# Figure setup
# ---------------------------------------------------------------------------

fig, ax = plt.subplots(figsize=(11, 27), dpi=200)
ax.set_xlim(0, 100)
ax.set_ylim(-92, 174)
ax.axis("off")
fig.patch.set_facecolor(BG)


def draw_density_ring(x, y, r=2.6):
    """Phase 3: a small translucent dotted-edge gold ring representing a 0.5 mi walk zone."""
    ring = patches.Circle((x, y), r, fill=True, facecolor=PHASE3_COLOR, alpha=0.18,
                           edgecolor=PHASE3_COLOR, linewidth=0.8, linestyle=FUTURE_LINESTYLE, zorder=1)
    ax.add_patch(ring)


# Title
ax.text(50, 170, "LA Connect — Sepulveda + C Line Network", ha="center",
        fontsize=20, fontweight="bold", color=PHASE0_COLOR, family="sans-serif")
ax.text(50, 166, "Built on LA's real rail network — connecting what exists to what's next", ha="center",
        fontsize=12, color=GRAY, style="italic")

# ---------------------------------------------------------------------------
# Legend — all five phases, two columns per row
# ---------------------------------------------------------------------------

legend_y = 162
ax.plot([6, 12], [legend_y, legend_y], color=PHASE0_COLOR, linewidth=RAIL_WIDTH, solid_capstyle="round")
ax.text(14, legend_y, "Phase 0 — Existing / Approved", va="center", fontsize=8.7, color="#333333")
ax.plot([55, 61], [legend_y, legend_y], color=PHASE1_COLOR, linewidth=BUS_WIDTH, linestyle=BUS_LINESTYLE)
ax.text(63, legend_y, "Phase 1 — Bus Feeder Route", va="center", fontsize=8.7, color="#333333")

ax.plot([6, 12], [legend_y - 4, legend_y - 4], color=PHASE2_COLOR, linewidth=RAIL_WIDTH, solid_capstyle="round")
ax.text(14, legend_y - 4, "Phase 2 — New Rail Connector", va="center", fontsize=8.7, color="#333333")
draw_density_ring(58, legend_y - 4, r=2.2)
ax.text(63, legend_y - 4, "Phase 3 — Density Zone (0.5 mi)", va="center", fontsize=8.7, color="#333333")

ax.plot([6, 12], [legend_y - 8, legend_y - 8], color=PHASE4_COLOR, linewidth=2, linestyle=FUTURE_LINESTYLE)
ax.text(14, legend_y - 8, "Phase 4 — Future Regional Link", va="center", fontsize=8.7, color="#333333")
ax.text(63, legend_y - 8, "Solid = rail  |  Dashed/dotted = bus/future", va="center",
        fontsize=7.6, color="#666666", style="italic")

# ---------------------------------------------------------------------------
# Main schematic: Sepulveda Transit Corridor (Phase 0, existing/approved) with
# Phase 1 bus feeders — same geometry as the original design, recolored gray.
# ---------------------------------------------------------------------------

trunk_x_left = 47
trunk_x_right = 53
trunk_top = 145
trunk_bottom = 48

ax.plot([trunk_x_left, trunk_x_left], [trunk_bottom, trunk_top],
        color=PHASE0_COLOR, linewidth=RAIL_WIDTH, solid_capstyle="round", zorder=2)
ax.plot([trunk_x_right, trunk_x_right], [trunk_bottom, trunk_top],
        color=PHASE0_COLOR, linewidth=RAIL_WIDTH, solid_capstyle="round", zorder=2)
ax.text(50, trunk_top + 2.2, "Sepulveda Transit Corridor (existing / approved, underground)", ha="center",
        fontsize=10, color=PHASE0_COLOR, fontweight="bold")

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
        linewidth=1, edgecolor=PHASE1_COLOR, facecolor="#FDEBD8", zorder=4,
    )
    ax.add_patch(box)
    ax.text(box_x + label_box_w / 2, y, text, ha="center", va="center",
            fontsize=8.3, color="#7A3B00", fontweight="bold", zorder=5)


for st in stations:
    y = st["y"]

    draw_density_ring(50, y)
    ax.scatter([50], [y], s=180, color=PHASE0_COLOR, zorder=6,
               edgecolors="white", linewidths=1.5)
    ax.text(50, y + 3.6, st["name"], ha="center", va="bottom",
            fontsize=9.5, fontweight="bold", color="#1A1A1A", zorder=6,
            path_effects=[pe.withStroke(linewidth=3, foreground="white")])

    for label, ly in st["left"]:
        ax.plot([trunk_x_left, 30, 15], [y, y, ly],
                color=PHASE1_COLOR, linewidth=BUS_WIDTH, linestyle=BUS_LINESTYLE, zorder=3)
        draw_branch_label(ax, 0, ly, label, align="left")

    for label, ly in st["right"]:
        ax.plot([trunk_x_right, 70, 85], [y, y, ly],
                color=PHASE1_COLOR, linewidth=BUS_WIDTH, linestyle=BUS_LINESTYLE, zorder=3)
        draw_branch_label(ax, 100, ly, label, align="right")

# ---------------------------------------------------------------------------
# Underground station cross-section (bottom panel) — Phase 0 infrastructure
# ---------------------------------------------------------------------------

cs_bottom = 2
cs_top = 34
cs_left = 12
cs_right = 88

ax.plot([cs_left - 2, cs_right + 2], [cs_top, cs_top], color=GRAY, linewidth=0.8)
ax.text(50, cs_top + 4, "Underground Station Cross-Section", ha="center",
        fontsize=12, fontweight="bold", color="#1A1A1A")

road_y = 23
ax.add_patch(patches.Rectangle((cs_left, road_y - 1.5), cs_right - cs_left, 3,
                                facecolor=LIGHT_GRAY, edgecolor=GRAY, linewidth=0.8, zorder=2))
ax.text(50, road_y, "I-405 Freeway (surface)", ha="center", va="center",
        fontsize=8.5, color="#333333", fontweight="bold", zorder=3)

plaza_x, plaza_w, plaza_h = 66, 20, 5
plaza_y = 29
plaza = patches.FancyBboxPatch((plaza_x, plaza_y), plaza_w, plaza_h,
                                boxstyle="round,pad=0.3,rounding_size=1", facecolor="#FDEBD8",
                                edgecolor=PHASE1_COLOR, linewidth=1.2, zorder=3)
ax.add_patch(plaza)
ax.text(plaza_x + plaza_w / 2, plaza_y + plaza_h / 2 + 1, "Bus transfer plaza",
        ha="center", va="center", fontsize=7.6, fontweight="bold", color="#7A3B00", zorder=4)
ax.text(plaza_x + plaza_w / 2, plaza_y + plaza_h / 2 - 1.6, "Local business perks",
        ha="center", va="center", fontsize=7, color="#7A3B00", zorder=4, style="italic")

esc_x = plaza_x + plaza_w / 2
ax.plot([esc_x, esc_x], [plaza_y, road_y - 1.5], color=GRAY, linewidth=1.2,
        linestyle=(0, (3, 2)), zorder=1)
ax.text(esc_x + 2, plaza_y - 3, "Escalator /\nelevator", fontsize=6.8,
        color=GRAY, va="center", ha="left")

station_box_y = cs_bottom + 2
station_box_h = 13
ax.add_patch(patches.FancyBboxPatch((cs_left, station_box_y), cs_right - cs_left, station_box_h,
                                     boxstyle="round,pad=0.3,rounding_size=1.5",
                                     facecolor="#EAF1F8", edgecolor=PHASE0_COLOR, linewidth=1.2, zorder=2))
ax.text(cs_left + 2, station_box_y + station_box_h - 1.5, "Underground station box",
        fontsize=8.5, fontweight="bold", color=PHASE0_COLOR, va="top")

ax.plot([esc_x, esc_x], [station_box_y + station_box_h, road_y - 1.5],
        color=GRAY, linewidth=1.2, linestyle=(0, (3, 2)), zorder=1)

track1_y = station_box_y + station_box_h - 5
ax.add_patch(patches.Rectangle((cs_left + 3, track1_y - 1.2), cs_right - cs_left - 6, 2.4,
                                facecolor=PHASE0_COLOR, alpha=0.85, zorder=3))
ax.text(50, track1_y, "Track 1 — Northbound", ha="center", va="center",
        fontsize=7.8, color="white", fontweight="bold", zorder=4)

platform_y = track1_y - 4
ax.add_patch(patches.Rectangle((cs_left + 3, platform_y - 1.4), cs_right - cs_left - 6, 2.8,
                                facecolor=LIGHT_GRAY, edgecolor=GRAY, linewidth=0.6, zorder=3))
ax.text(50, platform_y, "Platform", ha="center", va="center",
        fontsize=7.8, color="#333333", fontweight="bold", zorder=4)

track2_y = platform_y - 4
ax.add_patch(patches.Rectangle((cs_left + 3, track2_y - 1.2), cs_right - cs_left - 6, 2.4,
                                facecolor=PHASE0_COLOR, alpha=0.85, zorder=3))
ax.text(50, track2_y, "Track 2 — Southbound", ha="center", va="center",
        fontsize=7.8, color="white", fontweight="bold", zorder=4)

ax.text(50, cs_bottom - 0.5,
        "Two-track rail is the baseline: one track in each direction.\n"
        "Major future hubs could expand to four tracks for express and local service.",
        ha="center", va="top", fontsize=9, color="#333333", style="italic",
        family="sans-serif")

# ---------------------------------------------------------------------------
# Phase 0 + Phase 2 — where the Sepulveda Corridor meets Metro's real C Line
# ---------------------------------------------------------------------------

ax.plot([2, 98], [-2, -2], color=GRAY, linewidth=0.8)
ax.text(50, -7, "Phase 0 + Phase 2 — Connecting to Metro's Real C Line", ha="center", va="center",
        fontsize=14.5, fontweight="bold", color="#1A1A1A", family="sans-serif")
ax.text(50, -11.5,
        "The Sepulveda Corridor (above) meets Metro's real, existing C Line at LAX — "
        "this project adds one new connector",
        ha="center", va="center", fontsize=8.6, color="#333333", style="italic")

row_y = -21
c_line_stops = [
    ("LAX / Westchester", 8, "above", True),
    ("LAX / Metro Transit Center", 16.4, "below", True),
    ("Aviation / Century", 24.8, None, False),
    ("Hawthorne / Lennox", 33.2, None, False),
    ("Crenshaw", 41.6, "above", True),
    ("Vermont / Athens", 50.0, None, False),
    ("Harbor Freeway", 58.4, None, False),
    ("Willowbrook / Rosa Parks", 66.8, "below", True),
    ("Long Beach Blvd", 75.2, None, False),
    ("Lakewood Blvd", 83.6, None, False),
    ("Norwalk", 92.0, "above", True),
]

# Phase 2: the one new connector (short, green, same weight as Phase 0 rail)
ax.plot([c_line_stops[0][1], c_line_stops[1][1]], [row_y, row_y],
        color=PHASE2_COLOR, linewidth=RAIL_WIDTH, solid_capstyle="round", zorder=3)
ax.text((c_line_stops[0][1] + c_line_stops[1][1]) / 2, row_y + 4.5, "New Connector",
        ha="center", va="center", fontsize=8, fontweight="bold", color=PHASE2_COLOR)

# Phase 0: the real C Line trunk (gray, same weight as the Sepulveda Corridor above)
ax.plot([c_line_stops[1][1], c_line_stops[-1][1]], [row_y, row_y],
        color=PHASE0_COLOR, linewidth=RAIL_WIDTH, solid_capstyle="round", zorder=2)

# Single-line station labels only (kept short and on one line each, alternating
# above/below the row) so they can't collide vertically with the Phase 4 section
# below or the subheader above, regardless of how many characters a name has.
for name, x, side, labeled in c_line_stops:
    draw_density_ring(x, row_y)
    ax.scatter([x], [row_y], s=110, color=PHASE0_COLOR, zorder=6, edgecolors="white", linewidths=1.3)
    if labeled:
        label_y = row_y + 5 if side == "above" else row_y - 5
        va = "bottom" if side == "above" else "top"
        ax.text(x, label_y, name, ha="center", va=va, fontsize=7, fontweight="bold",
                color="#1A1A1A", zorder=5,
                path_effects=[pe.withStroke(linewidth=2.2, foreground="white")])

# ---------------------------------------------------------------------------
# Phase 4 — future / planned regional link (not funded, shown for context)
# ---------------------------------------------------------------------------

ax.text(50, -31, "Phase 4 — Future / Planned Regional Link (not funded)", ha="center", va="center",
        fontsize=10.5, fontweight="bold", color=PHASE4_COLOR, family="sans-serif")

future_y = -39
ax.plot([40, 60], [future_y, future_y], color=PHASE4_COLOR, linewidth=2, linestyle=FUTURE_LINESTYLE, zorder=2)
for name, x in [("Redondo Beach", 40), ("Torrance Transit Center", 60)]:
    ax.scatter([x], [future_y], s=90, color="white", edgecolors=PHASE4_COLOR, linewidths=1.8, zorder=6)
    ax.text(x, future_y - 4, name, ha="center", va="top", fontsize=7.4, fontweight="bold",
            color=PHASE4_COLOR, zorder=5)
ax.text(50, future_y + 4.5, "K Line extension to Torrance", ha="center", va="bottom",
        fontsize=7.6, color=PHASE4_COLOR, style="italic")

ax.text(50, -48,
        "New connector rail assumed at 35-45 mph (same standard urban rail speed as the Sepulveda Corridor).\n"
        "Flat fare on the new connector: $4.25 — reflects the longer trip distance to the C Line.",
        ha="center", va="top", fontsize=8.6, color="#333333", style="italic", family="sans-serif")

# ---------------------------------------------------------------------------
# Phase 2 — Downtown LA Connector: a second new segment this project proposes,
# branching off the existing Culver City / Palms station on the Sepulveda
# Corridor and following the real E Line alignment into Downtown LA.
# ---------------------------------------------------------------------------

ax.plot([2, 98], [-53, -53], color=GRAY, linewidth=0.8)
ax.text(50, -58, "Phase 2 — Downtown LA Connector", ha="center", va="center",
        fontsize=14.5, fontweight="bold", color="#1A1A1A", family="sans-serif")
ax.text(50, -62.5,
        "A second new segment this project proposes — branches from Culver City / Palms and "
        "follows the real E Line alignment into Downtown LA",
        ha="center", va="center", fontsize=8.6, color="#333333", style="italic")

downtown_row_y = -72
downtown_stops = [
    ("Culver City / Palms", 8, "below", PHASE0_COLOR),
    ("La Cienega / Jefferson", 24.8, "above", PHASE2_COLOR),
    ("Expo / Crenshaw", 41.6, "below", PHASE2_COLOR),
    ("Expo Park / USC", 58.4, "above", PHASE2_COLOR),
    ("7th St / Metro Center", 75.2, "below", PHASE2_COLOR),
    ("Downtown LA / Union Station", 92, "above", PHASE2_COLOR),
]

# The entire branch is Phase 2 (green) — including the leg out of Culver City / Palms,
# which is itself an existing Phase 0 station shown on the main trunk above.
ax.plot([downtown_stops[0][1], downtown_stops[-1][1]], [downtown_row_y, downtown_row_y],
        color=PHASE2_COLOR, linewidth=RAIL_WIDTH, solid_capstyle="round", zorder=2)

for name, x, side, dot_color in downtown_stops:
    draw_density_ring(x, downtown_row_y)
    ax.scatter([x], [downtown_row_y], s=110, color=dot_color, zorder=6, edgecolors="white", linewidths=1.3)
    label_y = downtown_row_y + 5 if side == "above" else downtown_row_y - 5
    va = "bottom" if side == "above" else "top"
    ax.text(x, label_y, name, ha="center", va=va, fontsize=7, fontweight="bold",
            color="#1A1A1A", zorder=5,
            path_effects=[pe.withStroke(linewidth=2.2, foreground="white")])

ax.text(50, -83,
        "New connector rail assumed at 35-45 mph (same standard urban rail speed as the Sepulveda Corridor).\n"
        "Flat fare on the new connector: $4.25.",
        ha="center", va="top", fontsize=8.6, color="#333333", style="italic", family="sans-serif")

# ---------------------------------------------------------------------------
# Save
# ---------------------------------------------------------------------------

os.makedirs("output", exist_ok=True)
output_path = "output/la_405_transit_schematic.png"
plt.savefig(output_path, dpi=200, bbox_inches="tight", facecolor=BG)
print(f"Schematic saved to {output_path}")
