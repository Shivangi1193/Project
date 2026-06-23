import streamlit as st
from navbar import show_navbar

st.set_page_config(
    page_title="Insights & Trends",
    page_icon="📈",
    layout="wide"
)

show_navbar()

st.title("📈 Insights & Trends")

st.write("Hello World - Insights & Trends Page")