"""
LA Connect — Sepulveda + C Line Network - Presentation Schematic
Generates a clean, minimal infographic (Matplotlib) showing Metro's real C Line and
K Line, the real (selected-but-unfunded) Sepulveda Transit Corridor Locally
Preferred Alternative, and — kept separately and clearly labeled as an unofficial
concept — the LA Connect "Sepulveda Extension Concept" this project originally
sketched (at-grade, 405-corridor stations) along with its bus feeders, an
underground station cross-section, the new rail connectors this project proposes,
station-area density zones, and future/long-range regional links.

Facts corrected against an August 2026 fact-check — see README / correction summary
for the full list of what changed and why.

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
# Phase 0 (existing/real Metro): solid, thick, muted gray.
# Phase 1 (bus feeders): dashed, thin, orange.
# Phase 2 (new rail connectors this project proposes): solid, thick, green.
# Phase 3 (density zones): translucent dotted-edge gold rings around stations.
# Phase 4 / concept-only (future/planned/LA Connect extension concept): dotted, thin, light blue.

PHASE0_COLOR = "#8A8D91"
PHASE1_COLOR = "#E8720C"
PHASE2_COLOR = "#1F9D6B"
PHASE3_COLOR = "#F2B705"
PHASE4_COLOR = "#5B9BD9"
EXT_CONCEPT_COLOR = PHASE4_COLOR  # the LA Connect Sepulveda Extension Concept is unofficial, styled like Phase 4
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

fig, ax = plt.subplots(figsize=(11, 32.5), dpi=200)
ax.set_xlim(0, 100)
ax.set_ylim(-145, 174)
ax.axis("off")
fig.patch.set_facecolor(BG)


def draw_density_ring(x, y, r=2.6):
    """Phase 3: a small translucent dotted-edge gold ring representing a 0.5 mi walk zone."""
    ring = patches.Circle((x, y), r, fill=True, facecolor=PHASE3_COLOR, alpha=0.18,
                           edgecolor=PHASE3_COLOR, linewidth=0.8, linestyle=FUTURE_LINESTYLE, zorder=1)
    ax.add_patch(ring)


def draw_station_row(y, stops, color, label_fontsize=7, dot_size=110):
    """Draws an evenly-spaced horizontal row of stations with alternating above/below labels.

    stops: list of station names, drawn left to right, evenly spaced from x=8 to x=92.
    """
    n = len(stops)
    step = (92 - 8) / (n - 1) if n > 1 else 0
    for i, name in enumerate(stops):
        x = 8 + i * step
        draw_density_ring(x, y)
        ax.scatter([x], [y], s=dot_size, color=color, zorder=6, edgecolors="white", linewidths=1.3)
        side = "above" if i % 2 == 0 else "below"
        label_y = y + 5 if side == "above" else y - 5
        va = "bottom" if side == "above" else "top"
        ax.text(x, label_y, name, ha="center", va=va, fontsize=label_fontsize, fontweight="bold",
                color="#1A1A1A", zorder=5,
                path_effects=[pe.withStroke(linewidth=2.2, foreground="white")])
    ax.plot([8, 8 + (n - 1) * step], [y, y], color=color, linewidth=RAIL_WIDTH,
             solid_capstyle="round", zorder=2)


# Title
ax.text(50, 170, "LA Connect — Sepulveda + C Line Network", ha="center",
        fontsize=20, fontweight="bold", color=PHASE0_COLOR, family="sans-serif")
ax.text(50, 166, "Built on LA's real rail network — connecting what exists to what's next", ha="center",
        fontsize=12, color=GRAY, style="italic")

# ---------------------------------------------------------------------------
# Legend — all phases, two columns per row
# ---------------------------------------------------------------------------

legend_y = 162
ax.plot([6, 12], [legend_y, legend_y], color=PHASE0_COLOR, linewidth=RAIL_WIDTH, solid_capstyle="round")
ax.text(14, legend_y, "Phase 0 — Existing / Selected (real Metro)", va="center", fontsize=8.7, color="#333333")
ax.plot([55, 61], [legend_y, legend_y], color=PHASE1_COLOR, linewidth=BUS_WIDTH, linestyle=BUS_LINESTYLE)
ax.text(63, legend_y, "Phase 1 — Bus Feeder Route", va="center", fontsize=8.7, color="#333333")

ax.plot([6, 12], [legend_y - 4, legend_y - 4], color=PHASE2_COLOR, linewidth=RAIL_WIDTH, solid_capstyle="round")
ax.text(14, legend_y - 4, "Phase 2 — New Rail Connector (concept)", va="center", fontsize=8.7, color="#333333")
draw_density_ring(58, legend_y - 4, r=2.2)
ax.text(63, legend_y - 4, "Phase 3 — Density Zone (0.5 mi)", va="center", fontsize=8.7, color="#333333")

ax.plot([6, 12], [legend_y - 8, legend_y - 8], color=PHASE4_COLOR, linewidth=2, linestyle=FUTURE_LINESTYLE)
ax.text(14, legend_y - 8, "Phase 4 — Future / Planned / Extension Concept", va="center", fontsize=8.7, color="#333333")
ax.text(63, legend_y - 8, "Solid = real rail  |  Dashed/dotted = bus/future/concept", va="center",
        fontsize=7.6, color="#666666", style="italic")
ax.text(50, legend_y - 12,
        "Phase 4 also covers this project's own “Sepulveda Extension Concept” — an unofficial idea, "
        "not part of Metro's selected Sepulveda alternative.",
        ha="center", va="center", fontsize=7, color="#666666", style="italic")

# ---------------------------------------------------------------------------
# Main schematic: Sepulveda Extension Concept (Phase 4 / unofficial) with
# Phase 1 bus feeders — same geometry as the original design, recolored to
# make clear this is NOT Metro's selected Sepulveda alternative.
# ---------------------------------------------------------------------------

trunk_x_left = 47
trunk_x_right = 53
trunk_top = 145
trunk_bottom = 48

ax.plot([trunk_x_left, trunk_x_left], [trunk_bottom, trunk_top],
        color=EXT_CONCEPT_COLOR, linewidth=RAIL_WIDTH, solid_capstyle="round", zorder=2)
ax.plot([trunk_x_right, trunk_x_right], [trunk_bottom, trunk_top],
        color=EXT_CONCEPT_COLOR, linewidth=RAIL_WIDTH, solid_capstyle="round", zorder=2)
ax.text(50, trunk_top + 2.2, "Sepulveda Extension Concept (LA Connect proposal — concept only)", ha="center",
        fontsize=10, color=EXT_CONCEPT_COLOR, fontweight="bold")
ax.text(50, trunk_top + 5.6,
        "NOT part of Metro's selected Sepulveda Transit Corridor Locally Preferred Alternative "
        "(Van Nuys ↔ Expo/Sepulveda, selected Jan 2026) — see the real LPA below.",
        ha="center", fontsize=7.6, color="#666666", style="italic")

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
    ax.scatter([50], [y], s=180, color=EXT_CONCEPT_COLOR, zorder=6,
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
# Underground station cross-section (bottom panel) — illustrative station design
# for the extension concept, not built infrastructure.
# ---------------------------------------------------------------------------

cs_bottom = 2
cs_top = 34
cs_left = 12
cs_right = 88

ax.plot([cs_left - 2, cs_right + 2], [cs_top, cs_top], color=GRAY, linewidth=0.8)
ax.text(50, cs_top + 4, "Underground Station Cross-Section (illustrative — extension concept)", ha="center",
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
                                     facecolor="#EAF1F8", edgecolor=EXT_CONCEPT_COLOR, linewidth=1.2, zorder=2))
ax.text(cs_left + 2, station_box_y + station_box_h - 1.5, "Underground station box",
        fontsize=8.5, fontweight="bold", color=EXT_CONCEPT_COLOR, va="top")

ax.plot([esc_x, esc_x], [station_box_y + station_box_h, road_y - 1.5],
        color=GRAY, linewidth=1.2, linestyle=(0, (3, 2)), zorder=1)

track1_y = station_box_y + station_box_h - 5
ax.add_patch(patches.Rectangle((cs_left + 3, track1_y - 1.2), cs_right - cs_left - 6, 2.4,
                                facecolor=EXT_CONCEPT_COLOR, alpha=0.85, zorder=3))
ax.text(50, track1_y, "Track 1 — Northbound", ha="center", va="center",
        fontsize=7.8, color="white", fontweight="bold", zorder=4)

platform_y = track1_y - 4
ax.add_patch(patches.Rectangle((cs_left + 3, platform_y - 1.4), cs_right - cs_left - 6, 2.8,
                                facecolor=LIGHT_GRAY, edgecolor=GRAY, linewidth=0.6, zorder=3))
ax.text(50, platform_y, "Platform", ha="center", va="center",
        fontsize=7.8, color="#333333", fontweight="bold", zorder=4)

track2_y = platform_y - 4
ax.add_patch(patches.Rectangle((cs_left + 3, track2_y - 1.2), cs_right - cs_left - 6, 2.4,
                                facecolor=EXT_CONCEPT_COLOR, alpha=0.85, zorder=3))
ax.text(50, track2_y, "Track 2 — Southbound", ha="center", va="center",
        fontsize=7.8, color="white", fontweight="bold", zorder=4)

ax.text(50, cs_bottom - 0.5,
        "Two-track rail is the baseline: one track in each direction.\n"
        "Major future hubs could expand to four tracks for express and local service.",
        ha="center", va="top", fontsize=9, color="#333333", style="italic",
        family="sans-serif")

# ---------------------------------------------------------------------------
# Phase 0 + Phase 2 — where the extension concept meets Metro's real C Line
# (corrected to the real 12-station C Line: LAX/Metro Transit Center <-> Norwalk,
# opened Aug 12, 1995, ~10 min midday / ~20 min early-late headways)
# ---------------------------------------------------------------------------

ax.plot([2, 98], [-2, -2], color=GRAY, linewidth=0.8)
ax.text(50, -7, "Phase 0 + Phase 2 — Connecting to Metro's Real C Line", ha="center", va="center",
        fontsize=14.5, fontweight="bold", color="#1A1A1A", family="sans-serif")
ax.text(50, -11.5,
        "The extension concept (above) meets Metro's real, existing C Line at LAX — "
        "this project's connector is a concept, contingent on the extension concept being built",
        ha="center", va="center", fontsize=8.6, color="#333333", style="italic")

row_y = -21
c_line_real_stations = [
    "LAX / Metro Transit Center", "Aviation / Century", "Aviation / Imperial",
    "Hawthorne / Lennox", "Crenshaw", "Vermont / Athens", "Harbor Freeway",
    "Avalon", "Willowbrook / Rosa Parks", "Lynwood", "Lakewood Boulevard", "Norwalk",
]
c_line_stops = ["LAX / Westchester (concept)"] + c_line_real_stations
n_stops = len(c_line_stops)
step = (92 - 8) / (n_stops - 1)
connector_x0 = 8
connector_x1 = 8 + step

# Phase 2: the new connector (short, green, same weight as Phase 0 rail) — concept
ax.plot([connector_x0, connector_x1], [row_y, row_y],
        color=PHASE2_COLOR, linewidth=RAIL_WIDTH, solid_capstyle="round", zorder=3)
ax.text((connector_x0 + connector_x1) / 2, row_y + 4.5, "New Connector\n(concept)",
        ha="center", va="center", fontsize=7.5, fontweight="bold", color=PHASE2_COLOR)

# Phase 0: the real C Line trunk (gray, same weight as elsewhere)
ax.plot([connector_x1, 8 + (n_stops - 1) * step], [row_y, row_y],
        color=PHASE0_COLOR, linewidth=RAIL_WIDTH, solid_capstyle="round", zorder=2)

for i, name in enumerate(c_line_stops):
    x = 8 + i * step
    color = PHASE2_COLOR if i == 0 else PHASE0_COLOR
    draw_density_ring(x, row_y)
    ax.scatter([x], [row_y], s=100, color=color, zorder=6, edgecolors="white", linewidths=1.2)
    side = "above" if i % 2 == 0 else "below"
    label_y = row_y + 5 if side == "above" else row_y - 5
    va = "bottom" if side == "above" else "top"
    ax.text(x, label_y, name, ha="center", va=va, fontsize=6.3, fontweight="bold",
            color="#1A1A1A", zorder=5, rotation=0,
            path_effects=[pe.withStroke(linewidth=2, foreground="white")])

ax.text(50, row_y - 9,
        "C Line: 12 stations, 17.8 mi, opened Aug 12, 1995. Transfers: A Line at Willowbrook/Rosa Parks, "
        "J Line at Harbor Freeway. Frequency: ~10 min most of the day, ~20 min early/late (approximate).",
        ha="center", va="top", fontsize=7.4, color="#333333", style="italic")

# ---------------------------------------------------------------------------
# Phase 0 — Metro K Line (real, 13 stations, continuous since June 2025)
# ---------------------------------------------------------------------------

k_line_header_y = -31
k_row_y = -44
ax.text(50, k_line_header_y, "Phase 0 — Metro K Line (real, continuous service since June 2025)",
        ha="center", va="center", fontsize=12.5, fontweight="bold", color="#1A1A1A")
ax.text(50, k_line_header_y - 4,
        "13 stations, Expo/Crenshaw ↔ Redondo Beach. Crenshaw/LAX segment opened Oct 2022; "
        "LAX/Metro Transit Center segment opened June 2025, completing through-service. Shares "
        "LAX/Metro Transit Center and Aviation/Century with the C Line. Transfers to the E Line at "
        "Expo/Crenshaw are a short at-grade crossing, not same-platform.",
        ha="center", va="center", fontsize=7.4, color="#333333", style="italic")

k_line_stations = [
    "Expo / Crenshaw", "Martin Luther King Jr.", "Leimert Park", "Hyde Park",
    "Fairview Heights", "Downtown Inglewood", "Westchester / Veterans",
    "LAX / Metro Transit Center", "Aviation / Century", "Mariposa", "El Segundo",
    "Douglas", "Redondo Beach",
]
draw_station_row(k_row_y, k_line_stations, PHASE0_COLOR, label_fontsize=6.2, dot_size=95)

# ---------------------------------------------------------------------------
# Phase 0 — Sepulveda Transit Corridor LPA (real, selected Jan 2026, unfunded)
# ---------------------------------------------------------------------------

lpa_header_y = -58
lpa_row_y = -66
ax.text(50, lpa_header_y,
        "Phase 0 — Sepulveda Transit Corridor: Locally Preferred Alternative (real, selected Jan 2026)",
        ha="center", va="center", fontsize=12.5, fontweight="bold", color="#1A1A1A")

lpa_stations = ["Van Nuys Metrolink Station", "Van Nuys Blvd / G Line", "Sepulveda Pass", "E Line Expo / Sepulveda"]
draw_station_row(lpa_row_y, lpa_stations, PHASE0_COLOR, label_fontsize=7.5, dot_size=140)

ax.text(50, lpa_row_y - 8,
        "Metro's Board selected underground heavy rail (“Modified Alternative 5”) as the LPA in "
        "January 2026. Environmental review, design, funding, and a construction schedule remain "
        "pending. Concept contemplates 2.5-minute peak headways. No confirmed opening date. Publicly "
        "circulated cost figures ($6–15B) are a concept estimate, not an official Metro cost.",
        ha="center", va="top", fontsize=7.4, color="#333333", style="italic")

# ---------------------------------------------------------------------------
# Phase 4 — future / planned regional links + long-range extensions (not funded)
# ---------------------------------------------------------------------------

future_header_y = -79
ax.text(50, future_header_y, "Phase 4 — Future / Planned Regional Links (not funded / long-range)",
        ha="center", va="center", fontsize=10.5, fontweight="bold", color=PHASE4_COLOR, family="sans-serif")

future_y = -87
ax.plot([40, 60], [future_y, future_y], color=PHASE4_COLOR, linewidth=2, linestyle=FUTURE_LINESTYLE, zorder=2)
for name, x in [("Redondo Beach", 40), ("Torrance Transit Center", 60)]:
    ax.scatter([x], [future_y], s=90, color="white", edgecolors=PHASE4_COLOR, linewidths=1.8, zorder=6)
    ax.text(x, future_y - 4, name, ha="center", va="top", fontsize=7.4, fontweight="bold",
            color=PHASE4_COLOR, zorder=5)
ax.text(50, future_y + 4.5, "K Line Extension to Torrance", ha="center", va="bottom",
        fontsize=7.6, color=PHASE4_COLOR, style="italic")

ax.text(50, -96,
        "K Line Extension to Torrance: Final EIR certified and approved Jan 22, 2026 (Hawthorne Option), "
        "~4.5 mi from Redondo Beach (Marine) to Torrance Transit Center. Estimated opening 2036; "
        "construction possibly starting as early as 2027. Operates as part of the K Line, not the C Line.\n"
        "K Line Northern Extension (toward Mid-City / West Hollywood / Hollywood): long-range only — "
        "construction funding unavailable until 2041, projected opening 2047–2049. Not relevant to 2028.\n"
        "Also of note: the D Line Extension, Section 1 opened May 8, 2026, adding three underground "
        "stations toward Beverly Hills — existing/approved, shown for regional context only.",
        ha="center", va="top", fontsize=7.8, color="#333333", style="italic", family="sans-serif")

# ---------------------------------------------------------------------------
# Phase 2 — Downtown LA Connector: a second new segment this project proposes,
# branching off the Sepulveda Extension Concept's Culver City / Palms station and
# following the real E Line alignment into Downtown LA.
# ---------------------------------------------------------------------------

ax.plot([2, 98], [-101, -101], color=GRAY, linewidth=0.8)
ax.text(50, -106, "Phase 2 — Downtown LA Connector (concept)", ha="center", va="center",
        fontsize=14.5, fontweight="bold", color="#1A1A1A", family="sans-serif")
ax.text(50, -110.5,
        "A second new segment this project proposes — branches from the extension concept's Culver "
        "City / Palms and follows the real E Line alignment into Downtown LA. Its Expo/Crenshaw stop "
        "reuses the real K Line station's coordinate but is a separate, unofficial concept segment.",
        ha="center", va="center", fontsize=8.2, color="#333333", style="italic")

downtown_row_y = -120
downtown_stops = [
    ("Culver City / Palms", 8, "below", EXT_CONCEPT_COLOR),
    ("La Cienega / Jefferson", 24.8, "above", PHASE2_COLOR),
    ("Expo / Crenshaw", 41.6, "below", PHASE2_COLOR),
    ("Expo Park / USC", 58.4, "above", PHASE2_COLOR),
    ("7th St / Metro Center", 75.2, "below", PHASE2_COLOR),
    ("Downtown LA / Union Station", 92, "above", PHASE2_COLOR),
]

# The entire branch is Phase 2 (green) — including the leg out of Culver City / Palms,
# which is itself a Sepulveda Extension Concept station shown on the main trunk above.
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

ax.text(50, -131,
        "New connector rail assumed at 35-45 mph (concept, same standard urban rail speed as the "
        "extension concept). Flat fare on the new connector: $4.25.",
        ha="center", va="top", fontsize=8.6, color="#333333", style="italic", family="sans-serif")

# ---------------------------------------------------------------------------
# Save
# ---------------------------------------------------------------------------

os.makedirs("output", exist_ok=True)
output_path = "output/la_405_transit_schematic.png"
plt.savefig(output_path, dpi=200, bbox_inches="tight", facecolor=BG)
print(f"Schematic saved to {output_path}")
