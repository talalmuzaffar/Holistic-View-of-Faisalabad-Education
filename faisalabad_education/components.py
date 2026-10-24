"""Formatting helpers and HTML cards shared by the pages."""
import streamlit as st


# Helper functions
def format_large_number(num):
    if num >= 1_000_000:
        return f"{num/1_000_000:.1f}M"
    elif num >= 1_000:
        return f"{num/1_000:.1f}K"
    return str(num)


# The overview page (app.py) caches the formatting; the other pages call it directly
format_large_number_cached = st.cache_data(format_large_number)


def stat_card(value, label):
    st.markdown(f"""
    <div class="stats-container">
        <div class="stat-value">{value}</div>
        <div class="stat-label">{label}</div>
    </div>
    """, unsafe_allow_html=True)
