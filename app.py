import pathlib

import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="LA 405 Integrated Rail + Bus Feeder Concept",
    page_icon="🚆",
    layout="wide",
)

HTML_PATH = pathlib.Path(__file__).parent / "la_405_3d_map.html"

st.title("LA 405 Integrated Rail + Bus Feeder Concept")
st.caption("Rail for speed, buses for last-mile access — an interactive 3D concept map of the I-405 corridor.")

map_html = HTML_PATH.read_text(encoding="utf-8")
components.html(map_html, height=900, scrolling=False)
