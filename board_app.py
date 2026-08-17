import pathlib

import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="LA Connect — Overview Board",
    page_icon="📊",
    layout="wide",
)

HTML_PATH = pathlib.Path(__file__).parent / "la_connect_board.html"

st.title("LA Connect — Overview Board")
st.caption(
    "One-page bento-dashboard overview: system map, key stats, business case, "
    "operating model, and the five-phase timeline."
)

board_html = HTML_PATH.read_text(encoding="utf-8")
components.html(board_html, height=2500, scrolling=True)
