import pathlib

import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="LA Connect — Sepulveda + C Line",
    page_icon="🚆",
    layout="wide",
)

HTML_PATH = pathlib.Path(__file__).parent / "la_405_3d_map.html"

st.title("LA Connect — Sepulveda + C Line")
st.caption(
    "Starting at LAX, where the Sepulveda Corridor (405) meets the C Line (105) — "
    "an interactive 3D concept map of the network."
)

map_html = HTML_PATH.read_text(encoding="utf-8")
components.html(map_html, height=900, scrolling=False)
