import pathlib

import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="LA Connect — App Prototype",
    page_icon="📱",
    layout="centered",
)

HTML_PATH = pathlib.Path(__file__).parent / "la_connect_prototype.html"

st.title("LA Connect — App Prototype")
st.caption("Trip planning, live arrivals, fare/wallet, and local perks — the rider-facing app.")

prototype_html = HTML_PATH.read_text(encoding="utf-8")
components.html(prototype_html, height=760, scrolling=False)
