"""CSS injected with st.markdown by the overview and the analysis pages."""

# Overview page (app.py)
OVERVIEW_CSS = """
<style>
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
    .insight-card {
        background-color: white;
        padding: 1.5rem;
        border-radius: 10px;
        border: 1px solid #DEE2E6;
        margin-bottom: 1rem;
        height: 100%;
        min-height: 280px;
        display: flex;
        flex-direction: column;
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
        flex-grow: 1;
    }
    .insight-stat {
        font-size: 1.1rem;
        font-weight: 600;
        color: #E5243B;
        margin-top: auto;
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
        transition: all 0.2s ease;
        width: 100%;
        text-align: center;
    }
    .view-details-btn:hover {
        background-color: #E5243B;
        color: white;
    }
    .divider {
        height: 3px;
        background-color: #FCE4E4;
        margin: 1rem 0;
        border-radius: 2px;
    }
</style>
"""

# Rules shared by every analysis page
_PAGE_RULES = """
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
"""

# Extra rules for the Never Attended page
_NEVER_ATTENDED_RULES = """    .metric-card {
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
"""

# Literacy Rates and Out of School pages
PAGE_CSS = "\n<style>" + _PAGE_RULES + "</style>\n"

# Never Attended page
NEVER_ATTENDED_CSS = "\n<style>" + _PAGE_RULES + _NEVER_ATTENDED_RULES + "</style>\n"
