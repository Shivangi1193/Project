
# navbar.py

import streamlit as st

def show_navbar():
    st.markdown("""
    <style>
    div[data-testid="stHorizontalBlock"] a {
        text-decoration: none !important;
        text-align: center;
        padding: 10px 12px;
        border-radius: 10px;
        font-weight: 600;
    }
    </style>
    """, unsafe_allow_html=True)

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.page_link("app.py", label="🏠 Home")

    with col2:
        st.page_link(
            "pages/A_Live_Matches.py",
            label="⚡ Live Matches"
        )

    with col3:
        st.page_link(
            "pages/B_Top_Player.py",
            label="📊 Top Players"
        )

    with col4:
        st.page_link(
            "pages/C_Insights_Trends.py",
            label="📈 Insights & Trends"
        )

    with col5:
        st.page_link(
            "pages/D_Data_control.py",
            label="🛠️ Data Control"
        )

    st.markdown("---")
