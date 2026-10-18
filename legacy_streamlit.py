from pathlib import Path

import streamlit as st
import streamlit.components.v1 as components


st.set_page_config(
    page_title="SmartBin 360",
    page_icon="🗑️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown(
    """
    <style>
    [data-testid="stHeader"],
    [data-testid="stToolbar"],
    [data-testid="stDecoration"],
    footer,
    #MainMenu {
        display: none;
    }

    [data-testid="stAppViewContainer"] .main .block-container {
        max-width: none;
        padding: 0;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

app_html = Path(__file__).with_name("index.html").read_text(encoding="utf-8")
components.html(app_html, height=900, scrolling=True)
