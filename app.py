import streamlit as st
import pandas as pd
import plotly.express as px

# Set page config
st.set_page_config(
    page_title="Overview - Education Access in Faisalabad",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Helper functions
@st.cache_data
def format_large_number(num):
    if num >= 1_000_000:
        return f"{num/1_000_000:.1f}M"
    elif num >= 1_000:
        return f"{num/1_000:.1f}K"
    return str(num)

# Load and prepare data with caching
@st.cache_data(ttl=3600)
def load_data():
    df = pd.read_csv('data_2023.csv')
    # Pre-calculate common filters
    df['is_literacy'] = df['Indicator'] == 'Literate %'
    df['is_out_of_school'] = df['Indicator'] == 'Out of School Children (5-16)'
    df['is_never_attended'] = df['Indicator'] == 'Never to School (all)'
    return df

df = load_data()

# Custom CSS with SDG color scheme
st.markdown("""
<style>
    /* Typography */
    * {
        font-family: 'Poppins', sans-serif;
    }
    
    /* Hero Section */
    .hero-container {
        background-color: #FCE4E4;
        padding: 1.5rem 2rem;
        border-radius: 0;
        margin: 0 0 1.5rem 0;
    }
    .hero-title {
        font-size: 2.5rem !important;
        font-weight: 700 !important;
        color: #E5243B !important;
        margin: 0 0 0.5rem 0 !important;
    }
    .hero-subtitle {
        font-size: 1.2rem !important;
        color: #2E2E2E !important;
        opacity: 0.9;
        margin: 0 !important;
    }
    .sdg-pill {
        background-color: #E5243B;
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        display: inline-block;
        margin-top: 1rem;
    }
    
    /* Metric Cards */
    .metric-card {
        background-color: white;
        padding: 1.5rem;
        border-radius: 10px;
        border: 1px solid #DEE2E6;
        height: 100%;
        transition: transform 0.2s ease;
    }
    .metric-card:hover {
        transform: translateY(-5px);
    }
    .metric-label {
        font-size: 0.9rem;
        color: #2E2E2E;
        opacity: 0.7;
    }
    .metric-value {
        font-size: 2.5rem;
        font-weight: 600;
        color: #E5243B;
        margin: 0.5rem 0;
    }
    .metric-subtext {
        font-size: 0.85rem;
        color: #2E2E2E;
        opacity: 0.8;
    }
    
    /* Insight Cards */
    .insight-card {
        background-color: white;
        padding: 1.5rem;
        border-radius: 10px;
        border: 1px solid #DEE2E6;
        margin-bottom: 1rem;
        height: 100%;
        min-height: 280px;
        display: flex;
        flex-direction: column;
    }
    .insight-icon {
        font-size: 1.3rem;
        margin-bottom: 0.8rem;
    }
    .insight-title {
        font-size: 1rem;
        font-weight: 600;
        color: #E5243B;
        margin-bottom: 0.5rem;
    }
    .insight-text {
        font-size: 0.9rem;
        color: #2E2E2E;
        line-height: 1.4;
        flex-grow: 1;
    }
    .insight-stat {
        font-size: 1.1rem;
        font-weight: 600;
        color: #E5243B;
        margin-top: auto;
        margin-bottom: 1rem;
    }
    .view-details-btn {
        display: inline-block;
        padding: 0.5rem 1rem;
        background-color: #FCE4E4;
        color: #E5243B;
        text-decoration: none;
        border-radius: 5px;
        font-size: 0.9rem;
        font-weight: 500;
        transition: all 0.2s ease;
        width: 100%;
        text-align: center;
    }
    .view-details-btn:hover {
        background-color: #E5243B;
        color: white;
    }
    .divider {
        height: 3px;
        background-color: #FCE4E4;
        margin: 1rem 0;
        border-radius: 2px;
    }
</style>
""", unsafe_allow_html=True)

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
total_out_of_school = df[
    (df['is_out_of_school']) & 
    (df['AreaType'] == 'Total') & 
    (df['Region'] == 'Faisalabad District')
]['Total'].values[0]

lowest_female_literacy = df[
    (df['is_literacy']) & 
    (df['AreaType'] == 'Rural')
]['Female'].min()

total_never_attended = df[
    (df['is_never_attended']) & 
    (df['AreaType'] == 'Total') & 
    (df['Region'] == 'Faisalabad District')
]['Total'].values[0]

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
urban_rural_literacy = df[
    (df['is_literacy']) & 
    (df['Region'] == 'Faisalabad District')
]
urban_literacy = urban_rural_literacy[urban_rural_literacy['AreaType'] == 'Urban']['Total'].values[0]
rural_literacy = urban_rural_literacy[urban_rural_literacy['AreaType'] == 'Rural']['Total'].values[0]
literacy_gap = urban_literacy - rural_literacy

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
