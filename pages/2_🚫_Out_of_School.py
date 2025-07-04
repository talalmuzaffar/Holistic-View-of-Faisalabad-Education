import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

# Set page config
st.set_page_config(
    page_title="Out-of-School Children - Education Access in Faisalabad",
    page_icon="🚫",
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

# Helper functions
def format_large_number(num):
    if num >= 1_000_000:
        return f"{num/1_000_000:.1f}M"
    elif num >= 1_000:
        return f"{num/1_000:.1f}K"
    return str(num)

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv('data_2023.csv')
    return df

df = load_data()

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
total_oosc = df[
    (df['Indicator'] == 'Out of School Children (5-16)') & 
    (df['AreaType'] == 'Total') & 
    (df['Region'] == 'Faisalabad District')
]

total_count = total_oosc['Total'].values[0]
male_count = total_oosc['Male'].values[0]
female_count = total_oosc['Female'].values[0]

with col1:
    st.markdown(f"""
    <div class="stats-container">
        <div class="stat-value">{format_large_number(total_count)}</div>
        <div class="stat-label">Total Out-of-School Children</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="stats-container">
        <div class="stat-value">{format_large_number(male_count)}</div>
        <div class="stat-label">Boys Out of School</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="stats-container">
        <div class="stat-value">{format_large_number(female_count)}</div>
        <div class="stat-label">Girls Out of School</div>
    </div>
    """, unsafe_allow_html=True)

# Main visualization
st.subheader("Out-of-School Children by Region and Gender")

# Filter data for out-of-school children
oosc_data = df[
    (df['Indicator'] == 'Out of School Children (5-16)') & 
    (df['AreaType'] == 'Total')
].copy()

# Create horizontal bar chart
fig_oosc = go.Figure()

fig_oosc.add_trace(go.Bar(
    y=oosc_data['Region'],
    x=oosc_data['Male'],
    name='Boys',
    orientation='h',
    marker_color='#2E2E2E'
))

fig_oosc.add_trace(go.Bar(
    y=oosc_data['Region'],
    x=oosc_data['Female'],
    name='Girls',
    orientation='h',
    marker_color='#E5243B'
))

fig_oosc.update_layout(
    barmode='stack',
    title='Out-of-School Children Distribution',
    font_family="Poppins",
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)',
    xaxis_title="Number of Children",
    yaxis_title="Region",
    hoverlabel=dict(font_family="Poppins"),
    title_font_family="Poppins"
)

st.plotly_chart(fig_oosc, use_container_width=True)

# Urban vs Rural Comparison
st.subheader("Urban vs Rural Distribution")

# Filter data for urban/rural comparison
urban_rural_data = df[
    (df['Indicator'] == 'Out of School Children (5-16)') & 
    (df['AreaType'].isin(['Urban', 'Rural']))
].copy()

# Create comparison chart
fig_comparison = px.bar(
    urban_rural_data,
    x='Region',
    y='Total',
    color='AreaType',
    barmode='group',
    title='Urban vs Rural Out-of-School Children',
    color_discrete_sequence=['#2E2E2E', '#E5243B']
)

fig_comparison.update_layout(
    font_family="Poppins",
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)',
    xaxis_title="Region",
    yaxis_title="Number of Children",
    hoverlabel=dict(font_family="Poppins"),
    title_font_family="Poppins"
)

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