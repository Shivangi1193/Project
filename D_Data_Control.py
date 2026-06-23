import streamlit as st
from navbar import show_navbar

st.set_page_config(
    page_title="Data Control",
    page_icon="🛠️",
    layout="wide"
)

show_navbar()

st.title("🛠️ Data Control")

st.write("Hello World - Data Control Page")