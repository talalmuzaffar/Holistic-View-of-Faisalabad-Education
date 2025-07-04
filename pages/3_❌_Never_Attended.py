import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import json

# Set page config
st.set_page_config(
    page_title="Never Attended School Analysis",
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
    .metric-card {
        background-color: white;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        text-align: left;
    }
    .metric-value {
        font-size: 2.5rem;
        font-weight: bold;
        color: #E5243B;
        margin: 0;
        line-height: 1;
    }
    .metric-label {
        color: #666;
        font-size: 1rem;
        margin-top: 8px;
    }
    .header-container {
        background-color: #FEF2F2;
        padding: 2rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        border-left: 5px solid #E5243B;
    }
    .header-title {
        font-size: 2.5rem;
        color: #1F2937;
        margin-bottom: 1rem;
    }
    .header-description {
        color: #4B5563;
        font-size: 1.1rem;
        line-height: 1.5;
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
    with open('faisalabad_tehsils.geojson') as f:
        geojson = json.load(f)
    return df, geojson

df, geojson = load_data()

# Title and description
st.markdown("""
<div class="header-container">
    <h1 class="header-title">❌ Never Attended School Crisis</h1>
    <p class="header-description">
        Analyzing children aged 5-16 who have never enrolled in formal education in Faisalabad District. 
        This represents a critical gap in educational access, with significant variations across urban and rural areas.
    </p>
</div>
""", unsafe_allow_html=True)

# Filter data for never attended school (specifically for age group 5-16)
never_attended_df = df[df['Indicator'] == 'Never to School (5-16)'].copy()

# Get district level statistics
district_stats = never_attended_df[
    (never_attended_df['Region'] == 'Faisalabad District') & 
    (never_attended_df['AreaType'] == 'Total')
].iloc[0]

# Create metrics cards
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(f"""
    <div class="metric-card">
        <p class="metric-value">{district_stats['Total']:,.1f}K</p>
        <p class="metric-label">Total Children Never Attended School</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="metric-card">
        <p class="metric-value">{district_stats['Male']:,.1f}K</p>
        <p class="metric-label">Boys Never Attended School</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="metric-card">
        <p class="metric-value">{district_stats['Female']:,.1f}K</p>
        <p class="metric-label">Girls Never Attended School</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# Prepare data for visualization
viz_data = never_attended_df[never_attended_df['Region'] != 'Faisalabad District'].copy()
viz_data = viz_data[viz_data['AreaType'] != 'Total']

# Ensure both Urban and Rural exist for each region
all_regions = viz_data['Region'].unique()
all_area_types = ['Urban', 'Rural']
complete_data = []

for region in all_regions:
    region_data = viz_data[viz_data['Region'] == region]
    total_region = region_data['Total'].sum()
    
    for area_type in all_area_types:
        area_data = region_data[region_data['AreaType'] == area_type]
        if len(area_data) == 0:
            # If this area type doesn't exist, add it with 0 values
            complete_data.append({
                'Region': region,
                'AreaType': area_type,
                'Total': 0,
                'Male': 0,
                'Female': 0
            })
        else:
            complete_data.extend(area_data.to_dict('records'))

viz_data = pd.DataFrame(complete_data)

# Calculate percentages for each area type
viz_data['Percentage'] = (viz_data['Total'] / viz_data.groupby('Region')['Total'].transform('sum') * 100).round(1)

# Create tabs for different visualizations
tab1, tab2 = st.tabs(["📊 Distribution Overview", "📈 Detailed Comparison"])

with tab1:
    # Create treemap
    treemap_data = viz_data.copy()
    treemap_data['Percentage_Label'] = treemap_data['Percentage'].apply(lambda x: f'{x:.1f}%')
    
    # Create color mapping
    treemap_data['Color'] = treemap_data['AreaType'].map({
        'Urban': '#7a0000',  # Dark red for urban
        'Rural': '#E5243B'   # Light red for rural
    })
    
    fig_treemap = px.treemap(
        treemap_data,
        path=[px.Constant("Faisalabad"), 'Region', 'AreaType'],
        values='Total',
        color='AreaType',
        color_discrete_map={
            'Urban': '#7a0000',  # Dark red for urban
            'Rural': '#E5243B'   # Light red for rural
        },
        custom_data=['Total', 'Percentage_Label']
    )
    
    fig_treemap.update_traces(
        textinfo="label",
        hovertemplate="""
<b>%{label}</b><br>
Number of children: %{customdata[0]:,.0f}<br>
Percentage: %{customdata[1]}<extra></extra>
""",
        textfont={"color": "white"}  # Make text white for better visibility
    )
    
    fig_treemap.update_layout(
        title={
            'text': 'Distribution of Out-of-School Children by Region',
            'y':0.95,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top'
        },
        height=600,
        # Remove color axis since we're using discrete colors
        coloraxis_showscale=False
    )
    
    st.plotly_chart(fig_treemap, use_container_width=True)

with tab2:
    # Create bar chart
    fig_bar = go.Figure()

    # Add bars for Urban
    urban_data = viz_data[viz_data['AreaType'] == 'Urban']
    fig_bar.add_trace(go.Bar(
        name='Urban',
        x=urban_data['Region'],
        y=urban_data['Total'],
        text=urban_data['Total'].apply(lambda x: f'{x:,.0f}'),
        textposition='auto',
        marker_color='#7a0000',  # Dark red for urban
        hovertemplate='<b>%{x}</b><br>' +
                    'Urban Areas<br>' +
                    'Children: %{text}<br>' +
                    'Percentage: %{customdata}%<extra></extra>',
        customdata=urban_data['Percentage'].round(1)
    ))

    # Add bars for Rural
    rural_data = viz_data[viz_data['AreaType'] == 'Rural']
    fig_bar.add_trace(go.Bar(
        name='Rural',
        x=rural_data['Region'],
        y=rural_data['Total'],
        text=rural_data['Total'].apply(lambda x: f'{x:,.0f}'),
        textposition='auto',
        marker_color='#E5243B',  # Light red for rural
        hovertemplate='<b>%{x}</b><br>' +
                    'Rural Areas<br>' +
                    'Children: %{text}<br>' +
                    'Percentage: %{customdata}%<extra></extra>',
        customdata=rural_data['Percentage'].round(1)
    ))

    # Update layout
    fig_bar.update_layout(
        title={
            'text': 'Urban vs Rural Distribution of Out-of-School Children',
            'y':0.95,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top'
        },
        xaxis_title="Region",
        yaxis_title="Number of Children",
        barmode='group',
        bargap=0.2,
        bargroupgap=0.1,
        height=500,
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
    fig_bar.update_xaxes(
        tickangle=45,
        title_font={"size": 14},
        title_standoff=25,
        gridcolor='#F0F0F0'
    )

    fig_bar.update_yaxes(
        title_font={"size": 14},
        title_standoff=25,
        gridcolor='#F0F0F0',
        zeroline=True,
        zerolinecolor='#E0E0E0',
        zerolinewidth=1
    )

    # Display the chart
    st.plotly_chart(fig_bar, use_container_width=True)

# Add insights
st.markdown("""
### Key Insights

1. **Regional Distribution**: The treemap visualization shows how the number of out-of-school children varies across different tehsils, helping identify priority areas.

2. **Urban-Rural Comparison**: The data reveals disparities between urban and rural areas, with rural areas generally showing higher numbers of out-of-school children.

3. **Priority Areas**: Some tehsils show significantly higher percentages of children who have never attended school, indicating where educational interventions are most needed.

4. **Gender Analysis**: The distribution between boys and girls who have never attended school helps identify gender-specific barriers to education access.
""")

# Display raw data in an expander
with st.expander("View Tehsil-wise Data"):
    st.markdown("""
    This table shows the breakdown of children (ages 5-16) who have never attended school across different tehsils of Faisalabad.
    Numbers are based on Census 2023 data.
    """)
    display_cols = ['Region', 'AreaType', 'Total', 'Male', 'Female', 'Percentage']
    formatted_df = viz_data[display_cols].copy()
    formatted_df = formatted_df.sort_values(['Region', 'AreaType'])
    st.dataframe(
        formatted_df,
        column_config={
            'Total': st.column_config.NumberColumn(
                help="Total number of children who never attended school",
                format="%d"
            ),
            'Percentage': st.column_config.NumberColumn(
                help="Percentage of total children in the region",
                format="%.1f%%"
            )
        }
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