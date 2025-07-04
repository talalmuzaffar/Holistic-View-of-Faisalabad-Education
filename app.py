import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from streamlit_lottie import st_lottie
import json
import requests

# Set page config
st.set_page_config(
    page_title="Overview - Education Access in Faisalabad",
    page_icon="��",
    layout="wide",
    initial_sidebar_state="collapsed"  # This will collapse the sidebar by default
)

# Helper functions
def format_large_number(num):
    if num >= 1_000_000:
        return f"{num/1_000_000:.1f}M"
    elif num >= 1_000:
        return f"{num/1_000:.1f}K"
    return str(num)

def calculate_percentage_change(value1, value2):
    return ((value2 - value1) / value1) * 100

# Custom CSS with SDG color scheme
st.markdown("""
<style>
    /* Hide Streamlit's default top padding */
    .block-container {
        padding-top: 1rem !important;
        padding-bottom: 0rem !important;
    }
    
    /* Hide the header decoration */
    .decoration {
        display: none !important;
    }
    
    /* Adjust header margins */
    header {
        margin-bottom: 0 !important;
    }
    
    /* Main Styles */
    .main {
        padding: 0;
    }
    
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
    .insights-container {
        margin-top: 3rem;
    }
    .insight-card {
        background-color: white;
        padding: 1.2rem;
        border-radius: 10px;
        border: 1px solid #DEE2E6;
        margin-bottom: 1rem;
        max-width: 400px;
        height: 100%;
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
    }
    .insight-stat {
        font-size: 1.1rem;
        font-weight: 600;
        color: #E5243B;
        margin-top: 0.5rem;
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
        margin-top: 0.5rem;
        transition: all 0.2s ease;
    }
    .view-details-btn:hover {
        background-color: #E5243B;
        color: white;
    }
    .divider {
        height: 3px;
        background-color: #FCE4E4;
        margin: 2rem 0;
        border-radius: 2px;
    }
</style>
""", unsafe_allow_html=True)

# Load and prepare data
@st.cache_data
def load_data():
    df = pd.read_csv('data_2023.csv')
    return df

df = load_data()

# Helper function to load Lottie files
def load_lottie_url(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

# Load Lottie animation
lottie_education = load_lottie_url('https://assets4.lottiefiles.com/packages/lf20_h6ykqbyg.json')

# Hero Section
st.markdown("""
<div class="hero-container">
    <h1 class="hero-title">📚 Education Access in Faisalabad</h1>
    <p class="hero-subtitle">Exploring Educational Disparities and SDG 4 Progress</p>
    <div class="sdg-pill">SDG 4: Quality Education • Census 2023</div>
</div>
""", unsafe_allow_html=True)

# Key Metrics Row
col1, col2, col3 = st.columns(3)

# Calculate key metrics
total_out_of_school = df[
    (df['Indicator'] == 'Out of School Children (5-16)') & 
    (df['AreaType'] == 'Total') & 
    (df['Region'] == 'Faisalabad District')
]['Total'].values[0]

lowest_female_literacy = df[
    (df['Indicator'] == 'Literate %') & 
    (df['AreaType'] == 'Rural')
]['Female'].min()

total_never_attended = df[
    (df['Indicator'] == 'Never to School (all)') & 
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
    (df['Indicator'] == 'Literate %') & 
    (df['Region'] == 'Faisalabad District')
]
urban_literacy = urban_rural_literacy[urban_rural_literacy['AreaType'] == 'Urban']['Total'].values[0]
rural_literacy = urban_rural_literacy[urban_rural_literacy['AreaType'] == 'Rural']['Total'].values[0]
literacy_gap = urban_literacy - rural_literacy

gender_data = df[
    (df['Indicator'] == 'Out of School Children (5-16)') & 
    (df['AreaType'] == 'Total') & 
    (df['Region'] == 'Faisalabad District')
]
female_ratio = (gender_data['Female'].values[0] / gender_data['Total'].values[0]) * 100

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
        <a href="Literacy_Rates" class="view-details-btn">View Details →</a>
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
        <a href="Out_of_School" class="view-details-btn">View Details →</a>
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
        <a href="Never_Attended" class="view-details-btn">View Details →</a>
    </div>
    """, unsafe_allow_html=True)
