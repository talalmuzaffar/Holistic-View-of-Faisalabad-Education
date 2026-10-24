"""Data file paths and the SDG colour scheme."""
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent.parent / 'data'
DATA_PATH = DATA_DIR / 'data_2023.csv'
GEOJSON_PATH = DATA_DIR / 'faisalabad_tehsils.geojson'

# SDG colour scheme
SDG_RED = '#E5243B'
DARK_GREY = '#2E2E2E'
DARK_RED = '#7a0000'
