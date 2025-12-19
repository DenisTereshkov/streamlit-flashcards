import streamlit as st

from session_state import init_session_state
from sidebar import render_sidebar
from main_content import render_main_content
from md_parser import get_markdown_files

st.set_page_config(
    layout="centered",
    page_title="Карточки для обучения",
)

init_session_state()

md_files = get_markdown_files()

render_sidebar()
render_main_content()
