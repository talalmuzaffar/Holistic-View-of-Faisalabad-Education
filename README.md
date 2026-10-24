# Faisalabad Education Access Dashboard

An interactive dashboard built with Streamlit to visualize and analyze education access disparities in Faisalabad. The dashboard presents data on literacy rates, out-of-school children, and education access across different tehsils and demographics.

## Features

- Interactive visualizations using Plotly
- Gender-disaggregated data analysis
- Rural vs Urban comparison
- Tehsil-wise breakdown of education metrics
- Animated data storytelling using Lottie

## Setup

1. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running the Dashboard

To run the dashboard locally:

```bash
streamlit run app.py
```

The dashboard will open in your default web browser at `http://localhost:8501`.

## Project Structure

```
Holistic-View-of-Faisalabad-Education/
├── app.py                          # Overview page (Streamlit entry point)
├── pages/
│   ├── 1_📚_Literacy_Rates.py
│   ├── 2_🚫_Out_of_School.py
│   └── 3_❌_Never_Attended.py
├── faisalabad_education/
│   ├── __init__.py
│   ├── config.py                   # Data file paths and SDG colours
│   ├── data.py                     # Cached data loading and per-page calculations
│   ├── charts.py                   # Plotly charts
│   ├── styles.py                   # Page CSS
│   └── components.py               # Number formatting and stat cards
├── data/
│   └── data_2023.csv               # Census 2023 education indicators
├── requirements.txt
├── packages.txt
└── runtime.txt
```

## Data Source

The dashboard uses education data from the [Pakistan Bureau of Statistics Digital Census 2023](https://www.pbs.gov.pk/digital-census/detailed-results), focusing on Faisalabad District metrics including:
- Literacy rates by gender and region
- Out-of-school children statistics
- School attendance metrics
- Urban vs rural education disparities

## Development

This project was developed by Global Shapers Faisalabad Hub as part of their initiative to highlight and address educational disparities in the region.

## Contributing

Feel free to open issues or submit pull requests to improve the dashboard.

## License

This project is open source and available under the MIT License. 