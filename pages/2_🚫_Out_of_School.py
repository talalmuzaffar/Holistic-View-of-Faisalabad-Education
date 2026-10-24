import streamlit as st

from faisalabad_education.charts import out_of_school_bar_chart, urban_rural_bar_chart
from faisalabad_education.components import format_large_number, stat_card
from faisalabad_education.data import (
    calculate_out_of_school_totals,
    filter_out_of_school_by_region,
    filter_out_of_school_urban_rural,
    load_out_of_school_data,
)
from faisalabad_education.styles import PAGE_CSS

# Set page config
st.set_page_config(
    page_title="Out-of-School Children - Education Access in Faisalabad",
    page_icon="🚫",
    layout="wide"
)

# Custom CSS
st.markdown(PAGE_CSS, unsafe_allow_html=True)

# Load data
df = load_out_of_school_data()

# Page title
st.title("🚫 Out-of-School Children Crisis")

# Introduction
st.markdown("""
<div class="insight-box">
    <h3>The Scale of Educational Exclusion</h3>
    <p>Over 470,000 children aged 5-16 are currently out of school in Faisalabad District. 
    Rural areas face the greatest challenges, with some tehsils showing alarming rates of educational exclusion.</p>
</div>
""", unsafe_allow_html=True)

# Key Statistics
col1, col2, col3 = st.columns(3)

# Calculate statistics
total_count, male_count, female_count = calculate_out_of_school_totals(df)

with col1:
    stat_card(format_large_number(total_count), "Total Out-of-School Children")

with col2:
    stat_card(format_large_number(male_count), "Boys Out of School")

with col3:
    stat_card(format_large_number(female_count), "Girls Out of School")

# Main visualization
st.subheader("Out-of-School Children by Region and Gender")

# Filter data for out-of-school children
oosc_data = filter_out_of_school_by_region(df)

# Create horizontal bar chart
fig_oosc = out_of_school_bar_chart(oosc_data)

st.plotly_chart(fig_oosc, use_container_width=True)

# Urban vs Rural Comparison
st.subheader("Urban vs Rural Distribution")

# Filter data for urban/rural comparison
urban_rural_data = filter_out_of_school_urban_rural(df)

# Create comparison chart
fig_comparison = urban_rural_bar_chart(urban_rural_data)

st.plotly_chart(fig_comparison, use_container_width=True)

# Additional insights
st.markdown("""
<div class="insight-box">
    <h3>Key Findings</h3>
    <ul>
        <li>Rural areas have significantly higher numbers of out-of-school children</li>
        <li>Gender disparities are more pronounced in certain regions</li>
        <li>Economic factors and accessibility to schools play crucial roles</li>
        <li>Immediate intervention is needed to address this educational crisis</li>
    </ul>
</div>
""", unsafe_allow_html=True) 