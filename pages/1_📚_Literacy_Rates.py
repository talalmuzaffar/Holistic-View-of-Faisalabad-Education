import streamlit as st

from faisalabad_education.charts import literacy_bar_chart
from faisalabad_education.components import stat_card
from faisalabad_education.data import calculate_statistics, load_literacy_data, prepare_visualization_data
from faisalabad_education.styles import PAGE_CSS

# Set page config
st.set_page_config(
    page_title="Literacy Rates - Education Access in Faisalabad",
    page_icon="📚",
    layout="wide"
)

# Custom CSS
st.markdown(PAGE_CSS, unsafe_allow_html=True)

# Load data with caching
df = load_literacy_data()

# Page title
st.title("📚 Literacy Rate Analysis")

# Introduction
st.markdown("""
<div class="insight-box">
    <h3>Understanding Literacy Disparities</h3>
    <p>Significant gender gaps persist in literacy rates across Faisalabad, particularly in rural areas. 
    While urban areas show higher literacy rates, rural women continue to face the greatest challenges in accessing education.</p>
</div>
""", unsafe_allow_html=True)

# Key Statistics
col1, col2, col3 = st.columns(3)

# Calculate statistics
urban_literacy, rural_literacy, male_female_gap = calculate_statistics(df)

with col1:
    stat_card(f"{urban_literacy:.1f}%", "Urban Literacy Rate")

with col2:
    stat_card(f"{rural_literacy:.1f}%", "Rural Literacy Rate")

with col3:
    stat_card(f"{male_female_gap:.1f}%", "Gender Gap in Literacy")

# Main visualization
st.subheader("Literacy Rates by Region and Gender")

# Filter data for literacy rates
literacy_data = prepare_visualization_data(df)

# Create bar chart
fig_literacy = literacy_bar_chart(literacy_data)

st.plotly_chart(fig_literacy, use_container_width=True)

# Additional insights
st.markdown("""
<div class="insight-box">
    <h3>Key Takeaways</h3>
    <ul>
        <li>Urban areas consistently show higher literacy rates compared to rural regions</li>
        <li>The gender gap is more pronounced in rural areas</li>
        <li>Female literacy rates in rural areas need immediate attention and intervention</li>
    </ul>
</div>
""", unsafe_allow_html=True) 