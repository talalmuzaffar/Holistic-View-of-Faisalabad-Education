"""Plotly charts used on the analysis pages."""
import plotly.express as px
import plotly.graph_objects as go

from faisalabad_education.config import DARK_GREY, DARK_RED, SDG_RED

# Poppins font and transparent background shared by the Literacy and Out of School charts
POPPINS_LAYOUT = dict(
    font_family="Poppins",
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)',
    hoverlabel=dict(font_family="Poppins"),
    title_font_family="Poppins"
)


# Literacy rates by gender and region (Literacy Rates)
def literacy_bar_chart(literacy_data):
    fig_literacy = px.bar(
        literacy_data,
        x='Region',
        y=['Male', 'Female'],
        barmode='group',
        title='Literacy Rates by Gender and Region',
        color_discrete_sequence=[DARK_GREY, SDG_RED],
        labels={'value': 'Literacy Rate (%)', 'variable': 'Gender'}
    )

    fig_literacy.update_layout(
        **POPPINS_LAYOUT,
        xaxis_title="Region",
        yaxis_title="Literacy Rate (%)",
        legend_title="Gender"
    )
    return fig_literacy


# Horizontal stacked bar chart of boys and girls out of school (Out of School)
def out_of_school_bar_chart(oosc_data):
    fig_oosc = go.Figure()

    fig_oosc.add_trace(go.Bar(
        y=oosc_data['Region'],
        x=oosc_data['Male'],
        name='Boys',
        orientation='h',
        marker_color=DARK_GREY
    ))

    fig_oosc.add_trace(go.Bar(
        y=oosc_data['Region'],
        x=oosc_data['Female'],
        name='Girls',
        orientation='h',
        marker_color=SDG_RED
    ))

    fig_oosc.update_layout(
        barmode='stack',
        title='Out-of-School Children Distribution',
        **POPPINS_LAYOUT,
        xaxis_title="Number of Children",
        yaxis_title="Region"
    )
    return fig_oosc


# Urban vs rural comparison chart (Out of School)
def urban_rural_bar_chart(urban_rural_data):
    fig_comparison = px.bar(
        urban_rural_data,
        x='Region',
        y='Total',
        color='AreaType',
        barmode='group',
        title='Urban vs Rural Out-of-School Children',
        color_discrete_sequence=[DARK_GREY, SDG_RED]
    )

    fig_comparison.update_layout(
        **POPPINS_LAYOUT,
        xaxis_title="Region",
        yaxis_title="Number of Children"
    )
    return fig_comparison


# Treemap of children who never attended school (Never Attended)
def never_attended_treemap(viz_data):
    treemap_data = viz_data.copy()
    treemap_data['Percentage_Label'] = treemap_data['Percentage'].apply(lambda x: f'{x:.1f}%')

    # Create color mapping
    treemap_data['Color'] = treemap_data['AreaType'].map({
        'Urban': DARK_RED,  # Dark red for urban
        'Rural': SDG_RED   # Light red for rural
    })

    fig_treemap = px.treemap(
        treemap_data,
        path=[px.Constant("Faisalabad"), 'Region', 'AreaType'],
        values='Total',
        color='AreaType',
        color_discrete_map={
            'Urban': DARK_RED,  # Dark red for urban
            'Rural': SDG_RED   # Light red for rural
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
    return fig_treemap


# Urban vs rural grouped bar chart (Never Attended)
def never_attended_bar_chart(viz_data):
    fig_bar = go.Figure()

    # Add bars for Urban
    urban_data = viz_data[viz_data['AreaType'] == 'Urban']
    fig_bar.add_trace(go.Bar(
        name='Urban',
        x=urban_data['Region'],
        y=urban_data['Total'],
        text=urban_data['Total'].apply(lambda x: f'{x:,.0f}'),
        textposition='auto',
        marker_color=DARK_RED,  # Dark red for urban
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
        marker_color=SDG_RED,  # Light red for rural
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
    return fig_bar
