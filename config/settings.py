"""
Configuration và CSS styling 
"""

# Page configuration
PAGE_CONFIG = {
    "page_title": "Financial Analytics Dashboard",
    "page_icon": "💰",
    "layout": "wide",
    "initial_sidebar_state": "expanded"
}

# CSS Styling
CUSTOM_CSS = """
<style>
    /* Main container styling */
    .main .block-container {
        padding-top: 1rem;
        padding-bottom: 1rem;
    }
    
    /* Metric card styling */
    div[data-testid="metric-container"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 15px;
        padding: 20px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
        color: white;
    }
    
    div[data-testid="metric-container"] > div {
        color: white !important;
    }
    
    div[data-testid="metric-container"] label {
        color: rgba(255, 255, 255, 0.8) !important;
    }
    
    div[data-testid="metric-container"] [data-testid="stMetricValue"] {
        color: white !important;
        font-size: 2rem !important;
        font-weight: bold !important;
    }
    
    div[data-testid="metric-container"] [data-testid="stMetricDelta"] {
        color: rgba(255, 255, 255, 0.9) !important;
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background: linear-gradient(180deg, #1a1a2e 0%, #16213e 100%);
    }
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background-color: #f0f2f6;
        border-radius: 8px;
        padding: 10px 20px;
        font-weight: 600;
    }
    
    .stTabs [aria-selected="true"] {
        background: #667eea;
        color: white;
    }
    
    /* Success/Warning boxes */
    .success-box {
        background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
        padding: 20px;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin: 10px 0;
    }
    
    .warning-box {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        padding: 20px;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin: 10px 0;
    }
    
    .info-box {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin: 10px 0;
    }
    
    /* Header styling */
    .dashboard-header {
        background: #667eea;
        padding: 30px;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin-bottom: 30px;
        box-shadow: 0 10px 30px rgba(102, 126, 234, 0.4);
    }
    
    .dashboard-header h1 {
        margin: 0;
        font-size: 2.5rem;
        font-weight: 700;
    }
    
    .dashboard-header p {
        margin: 10px 0 0 0;
        opacity: 0.9;
        font-size: 1.1rem;
    }
    
    /* Rate card styling */
    .rate-card {
        background: linear-gradient(135deg, #ff6b6b 0%, #feca57 100%);
        padding: 30px;
        border-radius: 20px;
        color: white;
        text-align: center;
        margin: 20px 0;
        box-shadow: 0 10px 30px rgba(255, 107, 107, 0.3);
    }
    
    .rate-card h2 {
        margin: 0;
        font-size: 3rem;
        font-weight: 700;
    }
    
    .rate-card p {
        margin: 10px 0 0 0;
        font-size: 1.2rem;
        opacity: 0.9;
    }
</style>
"""

# Grade mappings
GRADE_ORDER = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
GRADE_NUM_MAPPING = {'A': 1, 'B': 2, 'C': 3, 'D': 4, 'E': 5, 'F': 6, 'G': 7}

# Loan status colors
STATUS_COLORS = {
    'Fully Paid': '#38ef7d',
    'Current': '#667eea',
    'Charged Off': '#f5576c',
    'Unknown': '#95a5a6'
}

# Purpose options
PURPOSE_OPTIONS = [
    'Debt consolidation',
    'Credit card',
    'Home improvement',
    'Major purchase',
    'Medical',
    'Car',
    'Vacation',
    'Moving',
    'Wedding',
    'Other'
]

# Average rates by grade (for comparison)
AVG_RATES_BY_GRADE = {
    'A': 7.5, 'B': 10.5, 'C': 13.5, 'D': 17.0, 
    'E': 20.0, 'F': 23.0, 'G': 26.0
}