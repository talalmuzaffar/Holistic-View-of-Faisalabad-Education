import streamlit as st

from faisalabad_education.charts import never_attended_bar_chart, never_attended_treemap
from faisalabad_education.data import (
    filter_never_attended,
    get_district_stats,
    load_never_attended_data,
    prepare_never_attended_viz_data,
)
from faisalabad_education.styles import NEVER_ATTENDED_CSS

# Set page config
st.set_page_config(
    page_title="Never Attended School Analysis",
    page_icon="❌",
    layout="wide"
)

# Custom CSS
st.markdown(NEVER_ATTENDED_CSS, unsafe_allow_html=True)

# Load data
df, geojson = load_never_attended_data()

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
never_attended_df = filter_never_attended(df)

# Get district level statistics
district_stats = get_district_stats(never_attended_df)

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
viz_data = prepare_never_attended_viz_data(never_attended_df)

# Create tabs for different visualizations
tab1, tab2 = st.tabs(["📊 Distribution Overview", "📈 Detailed Comparison"])

with tab1:
    # Create treemap
    fig_treemap = never_attended_treemap(viz_data)

    st.plotly_chart(fig_treemap, use_container_width=True)

with tab2:
    # Create bar chart
    fig_bar = never_attended_bar_chart(viz_data)

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