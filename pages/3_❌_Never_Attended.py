import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Set page config
st.set_page_config(
    page_title="Never Attended School - Education Access in Faisalabad",
    page_icon="❌",
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
st.title("❌ Never Attended School Analysis")

# Introduction
st.markdown("""
# Never Attended School Distribution
Analyzing the population that has never had access to formal education across different regions of Faisalabad.
""")

# Filter data for never attended school
never_attended_df = df[df['Indicator'] == 'Never to School (all)'].copy()

# Create comparison metrics
total_stats = never_attended_df[never_attended_df['Region'] == 'Faisalabad District'].iloc[0]
urban_stats = never_attended_df[never_attended_df['AreaType'] == 'Urban']
rural_stats = never_attended_df[never_attended_df['AreaType'] == 'Rural']

# Metrics row
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Total Never Attended", f"{total_stats['Total']:,.0f}")
with col2:
    st.metric("Urban Population", f"{total_stats['Male']:,.0f} males, {total_stats['Female']:,.0f} females")
with col3:
    st.metric("Rural Population", f"{rural_stats['Total'].sum():,.0f}")

st.markdown("---")

# Prepare data for visualization
viz_data = never_attended_df[never_attended_df['Region'] != 'Faisalabad District'].copy()
viz_data = viz_data[viz_data['AreaType'] != 'Total']

# Calculate percentages
viz_data['Percentage'] = (viz_data['Total'] / viz_data.groupby('Region')['Total'].transform('sum') * 100).round(1)

# Create bar chart
fig = go.Figure()

# Add bars for Urban
urban_data = viz_data[viz_data['AreaType'] == 'Urban']
fig.add_trace(go.Bar(
    name='Urban',
    x=urban_data['Region'],
    y=urban_data['Percentage'],
    text=urban_data['Percentage'].apply(lambda x: f'{x:.1f}%'),
    textposition='auto',
    marker_color='#E5243B',
    hovertemplate='<b>%{x}</b><br>' +
                  'Urban: %{text}<br>' +
                  'Total: %{customdata:,.0f}<extra></extra>',
    customdata=urban_data['Total']
))

# Add bars for Rural
rural_data = viz_data[viz_data['AreaType'] == 'Rural']
fig.add_trace(go.Bar(
    name='Rural',
    x=rural_data['Region'],
    y=rural_data['Percentage'],
    text=rural_data['Percentage'].apply(lambda x: f'{x:.1f}%'),
    textposition='auto',
    marker_color='#FCE4E4',
    hovertemplate='<b>%{x}</b><br>' +
                  'Rural: %{text}<br>' +
                  'Total: %{customdata:,.0f}<extra></extra>',
    customdata=rural_data['Total']
))

# Update layout
fig.update_layout(
    title={
        'text': 'Percentage Distribution of Population Never Attended School by Region',
        'y':0.95,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top'
    },
    xaxis_title="Region",
    yaxis_title="Percentage of Population (%)",
    barmode='group',
    bargap=0.2,
    bargroupgap=0.1,
    height=600,
    showlegend=True,
    legend=dict(
        yanchor="top",
        y=0.99,
        xanchor="right",
        x=0.99
    ),
    plot_bgcolor='white',
    paper_bgcolor='white',
)

# Update axes
fig.update_xaxes(
    tickangle=45,
    title_font={"size": 14},
    title_standoff=25,
    gridcolor='#F0F0F0'
)

fig.update_yaxes(
    title_font={"size": 14},
    title_standoff=25,
    gridcolor='#F0F0F0',
    zeroline=True,
    zerolinecolor='#E0E0E0',
    zerolinewidth=1
)

# Display the chart
st.plotly_chart(fig, use_container_width=True)

# Add insights
st.markdown("""
### Key Insights

1. **Urban-Rural Divide**: The data shows significant differences in school attendance between urban and rural areas across all regions.

2. **Regional Variations**: Some tehsils show higher percentages of people who have never attended school, indicating areas that need focused intervention.

3. **Gender Distribution**: The metrics show the breakdown between males and females who have never attended school, highlighting gender-based disparities in education access.
""")

# Display raw data in an expander
with st.expander("View Raw Data"):
    st.dataframe(
        viz_data[['Region', 'AreaType', 'Total', 'Male', 'Female', 'Percentage']]
        .sort_values(['Region', 'AreaType'])
    )

# Additional insights
st.markdown("""
<div class="insight-box">
    <h3>Key Insights</h3>
    <ul>
        <li>Rural areas show significantly higher percentages of children never attending school</li>
        <li>Girls are more likely to never attend school, especially in rural areas</li>
        <li>The urban-rural divide is most pronounced in certain tehsils</li>
        <li>Targeted interventions are needed to address barriers to school entry</li>
    </ul>
</div>
""", unsafe_allow_html=True)

# Call to Action
st.markdown("""
<div class="insight-box" style="background-color: #E5243B; color: white; border-left: none;">
    <h3 style="color: white;">Take Action</h3>
    <p>These statistics represent real children who have never had the opportunity to attend school. 
    Each number is a story of potential waiting to be unlocked. Together, we can work to ensure every 
    child has access to quality education.</p>
</div>
""", unsafe_allow_html=True) 