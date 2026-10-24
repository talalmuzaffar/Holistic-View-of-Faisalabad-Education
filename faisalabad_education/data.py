"""Loading the census data and preparing it for each page."""
import json

import pandas as pd
import streamlit as st

from faisalabad_education.config import DATA_PATH, GEOJSON_PATH


# Load and prepare data with caching (Overview)
@st.cache_data(ttl=3600)
def load_data():
    df = pd.read_csv(DATA_PATH)
    # Pre-calculate common filters
    df['is_literacy'] = df['Indicator'] == 'Literate %'
    df['is_out_of_school'] = df['Indicator'] == 'Out of School Children (5-16)'
    df['is_never_attended'] = df['Indicator'] == 'Never to School (all)'
    return df


# Load data with caching (Literacy Rates)
@st.cache_data(ttl=3600)  # Cache for 1 hour
def load_literacy_data():
    df = pd.read_csv(DATA_PATH)
    # Pre-calculate common filters
    df['is_literacy'] = df['Indicator'] == 'Literate %'
    return df


# Load data (Out of School)
@st.cache_data
def load_out_of_school_data():
    df = pd.read_csv(DATA_PATH)
    return df


# Load data (Never Attended)
@st.cache_data
def load_never_attended_data():
    df = pd.read_csv(DATA_PATH)
    with open(GEOJSON_PATH) as f:
        geojson = json.load(f)
    return df, geojson


# Calculate key metrics (Overview)
def calculate_key_metrics(df):
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

    return total_out_of_school, lowest_female_literacy, total_never_attended


# Calculate additional insights (Overview)
def calculate_literacy_gap(df):
    urban_rural_literacy = df[
        (df['is_literacy']) &
        (df['Region'] == 'Faisalabad District')
    ]
    urban_literacy = urban_rural_literacy[urban_rural_literacy['AreaType'] == 'Urban']['Total'].values[0]
    rural_literacy = urban_rural_literacy[urban_rural_literacy['AreaType'] == 'Rural']['Total'].values[0]
    literacy_gap = urban_literacy - rural_literacy
    return literacy_gap


# Pre-filter data for visualizations (Literacy Rates)
@st.cache_data
def prepare_visualization_data(df):
    literacy_data = df[
        (df['is_literacy']) &
        (df['AreaType'].isin(['Rural', 'Urban']))
    ].copy()
    return literacy_data


# Calculate statistics with caching (Literacy Rates)
@st.cache_data
def calculate_statistics(df):
    urban_literacy = df[
        (df['is_literacy']) &
        (df['AreaType'] == 'Urban') &
        (df['Region'] == 'Faisalabad District')
    ]['Total'].values[0]

    rural_literacy = df[
        (df['is_literacy']) &
        (df['AreaType'] == 'Rural') &
        (df['Region'] == 'Faisalabad District')
    ]['Total'].values[0]

    gender_gap = df[
        (df['is_literacy']) &
        (df['AreaType'] == 'Total') &
        (df['Region'] == 'Faisalabad District')
    ]
    male_female_gap = float(gender_gap['Male'].values[0]) - float(gender_gap['Female'].values[0])

    return urban_literacy, rural_literacy, male_female_gap


# Calculate statistics (Out of School)
def calculate_out_of_school_totals(df):
    total_oosc = df[
        (df['Indicator'] == 'Out of School Children (5-16)') &
        (df['AreaType'] == 'Total') &
        (df['Region'] == 'Faisalabad District')
    ]

    total_count = total_oosc['Total'].values[0]
    male_count = total_oosc['Male'].values[0]
    female_count = total_oosc['Female'].values[0]
    return total_count, male_count, female_count


# Filter data for out-of-school children (Out of School)
def filter_out_of_school_by_region(df):
    oosc_data = df[
        (df['Indicator'] == 'Out of School Children (5-16)') &
        (df['AreaType'] == 'Total')
    ].copy()
    return oosc_data


# Filter data for urban/rural comparison (Out of School)
def filter_out_of_school_urban_rural(df):
    urban_rural_data = df[
        (df['Indicator'] == 'Out of School Children (5-16)') &
        (df['AreaType'].isin(['Urban', 'Rural']))
    ].copy()
    return urban_rural_data


# Filter data for never attended school (specifically for age group 5-16)
def filter_never_attended(df):
    never_attended_df = df[df['Indicator'] == 'Never to School (5-16)'].copy()
    return never_attended_df


# Get district level statistics (Never Attended)
def get_district_stats(never_attended_df):
    district_stats = never_attended_df[
        (never_attended_df['Region'] == 'Faisalabad District') &
        (never_attended_df['AreaType'] == 'Total')
    ].iloc[0]
    return district_stats


# Prepare data for visualization (Never Attended)
def prepare_never_attended_viz_data(never_attended_df):
    viz_data = never_attended_df[never_attended_df['Region'] != 'Faisalabad District'].copy()
    viz_data = viz_data[viz_data['AreaType'] != 'Total']

    # Ensure both Urban and Rural exist for each region
    all_regions = viz_data['Region'].unique()
    all_area_types = ['Urban', 'Rural']
    complete_data = []

    for region in all_regions:
        region_data = viz_data[viz_data['Region'] == region]

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
    return viz_data
