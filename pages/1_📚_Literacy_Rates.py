import streamlit as st
import pandas as pd
import plotly.express as px

# Set page config
st.set_page_config(
    page_title="Literacy Rates - Education Access in Faisalabad",
    page_icon="📚",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    /* Typography */
    * {
        font-family: 'Poppins', sans-serif;
    }
    
    /* Insight Box */
    .insight-box {
        background-color: #FCE4E4;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 5px solid #E5243B;
        margin: 1rem 0;
    }
    
    /* Stats Container */
    .stats-container {
        background-color: white;
        padding: 1.5rem;
        border-radius: 10px;
        border: 1px solid #DEE2E6;
        margin: 1rem 0;
    }
    .stat-value {
        font-size: 2rem;
        font-weight: 600;
        color: #E5243B;
    }
    .stat-label {
        font-size: 0.9rem;
        color: #2E2E2E;
        opacity: 0.7;
    }
</style>
""", unsafe_allow_html=True)

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv('data_2023.csv')
    return df

df = load_data()

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
urban_literacy = df[
    (df['Indicator'] == 'Literate %') & 
    (df['AreaType'] == 'Urban') & 
    (df['Region'] == 'Faisalabad District')
]['Total'].values[0]

rural_literacy = df[
    (df['Indicator'] == 'Literate %') & 
    (df['AreaType'] == 'Rural') & 
    (df['Region'] == 'Faisalabad District')
]['Total'].values[0]

gender_gap = df[
    (df['Indicator'] == 'Literate %') & 
    (df['AreaType'] == 'Total') & 
    (df['Region'] == 'Faisalabad District')
]
male_female_gap = float(gender_gap['Male'].values[0]) - float(gender_gap['Female'].values[0])

with col1:
    st.markdown(f"""
    <div class="stats-container">
        <div class="stat-value">{urban_literacy:.1f}%</div>
        <div class="stat-label">Urban Literacy Rate</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="stats-container">
        <div class="stat-value">{rural_literacy:.1f}%</div>
        <div class="stat-label">Rural Literacy Rate</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="stats-container">
        <div class="stat-value">{male_female_gap:.1f}%</div>
        <div class="stat-label">Gender Gap in Literacy</div>
    </div>
    """, unsafe_allow_html=True)

# Main visualization
st.subheader("Literacy Rates by Region and Gender")

# Filter data for literacy rates
literacy_data = df[
    (df['Indicator'] == 'Literate %') & 
    (df['AreaType'].isin(['Rural', 'Urban']))
].copy()

# Create bar chart
fig_literacy = px.bar(
    literacy_data,
    x='Region',
    y=['Male', 'Female'],
    barmode='group',
    title='Literacy Rates by Gender and Region',
    color_discrete_sequence=['#2E2E2E', '#E5243B'],
    labels={'value': 'Literacy Rate (%)', 'variable': 'Gender'}
)

fig_literacy.update_layout(
    font_family="Poppins",
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)',
    xaxis_title="Region",
    yaxis_title="Literacy Rate (%)",
    legend_title="Gender",
    hoverlabel=dict(font_family="Poppins"),
    title_font_family="Poppins"
)

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