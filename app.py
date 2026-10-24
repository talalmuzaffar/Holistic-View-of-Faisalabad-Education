import streamlit as st

from faisalabad_education.components import format_large_number_cached as format_large_number
from faisalabad_education.data import calculate_key_metrics, calculate_literacy_gap, load_data
from faisalabad_education.styles import OVERVIEW_CSS

# Set page config
st.set_page_config(
    page_title="Overview - Education Access in Faisalabad",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Load and prepare data with caching
df = load_data()

# Custom CSS with SDG color scheme
st.markdown(OVERVIEW_CSS, unsafe_allow_html=True)

# Hero Section
st.markdown("""
<div class="hero-container">
    <h1 class="hero-title">📚 Education Access in Faisalabad</h1>
    <p class="hero-subtitle">Exploring Educational Disparities and SDG 4 Progress</p>
    <div class="sdg-pill">SDG 4: Quality Education • Census 2023</div>
    <p style="margin-top: 1rem; font-size: 0.9rem; color: #666;">
        Data Source: <a href="https://www.pbs.gov.pk/digital-census/detailed-results" target="_blank" style="color: #E5243B;">Pakistan Bureau of Statistics Digital Census 2023</a><br>
        Developed by Global Shapers Faisalabad Hub
    </p>
</div>
""", unsafe_allow_html=True)

# Key Metrics Row
col1, col2, col3 = st.columns(3)

# Calculate key metrics
total_out_of_school, lowest_female_literacy, total_never_attended = calculate_key_metrics(df)

with col1:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">OUT OF SCHOOL CHILDREN</div>
        <div class="metric-value">{format_large_number(total_out_of_school)}</div>
        <div class="metric-subtext">Ages 5-16 not in education</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">LOWEST FEMALE LITERACY</div>
        <div class="metric-value">{lowest_female_literacy:.1f}%</div>
        <div class="metric-subtext">In rural areas</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">NEVER ATTENDED SCHOOL</div>
        <div class="metric-value">{format_large_number(total_never_attended)}</div>
        <div class="metric-subtext">Total population</div>
    </div>
    """, unsafe_allow_html=True)

# Calculate additional insights
literacy_gap = calculate_literacy_gap(df)

# Divider
st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

# Key Insights Section
st.markdown("<h2>Key Insights</h2>", unsafe_allow_html=True)

# Insights Grid - Three cards with navigation
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(f"""
    <div class="insight-card">
        <div class="insight-icon">📚</div>
        <div class="insight-title">Literacy Rates</div>
        <div class="insight-text">
            A significant gap exists between urban and rural literacy rates in Faisalabad, 
            with urban areas showing consistently higher rates.
        </div>
        <div class="insight-stat">
            {literacy_gap:.1f}% urban-rural gap
        </div>
        <a href="Literacy_Rates" class="view-details-btn">View Detailed Analysis →</a>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="insight-card">
        <div class="insight-icon">🚫</div>
        <div class="insight-title">Out of School Children</div>
        <div class="insight-text">
            Analysis of children aged 5-16 who are currently not enrolled in any educational institution.
        </div>
        <div class="insight-stat">
            {format_large_number(total_out_of_school)} children
        </div>
        <a href="Out_of_School" class="view-details-btn">View Detailed Analysis →</a>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="insight-card">
        <div class="insight-icon">❌</div>
        <div class="insight-title">Never Attended School</div>
        <div class="insight-text">
            Population that has never had access to formal education, highlighting systemic barriers.
        </div>
        <div class="insight-stat">
            {format_large_number(total_never_attended)} people
        </div>
        <a href="Never_Attended" class="view-details-btn">View Detailed Analysis →</a>
    </div>
    """, unsafe_allow_html=True)
