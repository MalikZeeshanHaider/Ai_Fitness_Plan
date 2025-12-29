"""
Custom CSS Styles for Streamlit Application.

This module provides additional CSS styling to enhance
the visual appearance of the application.

Usage:
    Import this module and call load_custom_css() in your Streamlit app.
"""


def get_custom_css() -> str:
    """
    Get the complete custom CSS for the application.
    
    Returns:
        str: CSS code as a string
    """
    return """
    <style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;800&display=swap');
    
    /* ============================================
       🎨 PROFESSIONAL COLOR SCHEME
       Primary: Navy Blue (#1E3A8A)
       Secondary: Teal (#0891B2)
       Accent: Sky Blue (#38BDF8)
       Dark: Slate (#0F172A)
       Light: White (#FFFFFF)
       ============================================ */
    
    :root {
        --primary: #1E3A8A;
        --primary-dark: #1E40AF;
        --primary-light: #3B82F6;
        --secondary: #0891B2;
        --secondary-dark: #0E7490;
        --secondary-light: #06B6D4;
        --accent: #38BDF8;
        --accent-dark: #0EA5E9;
        --success: #10B981;
        --warning: #F59E0B;
        --danger: #EF4444;
        --dark: #0F172A;
        --dark-2: #1E293B;
        --dark-3: #334155;
        --light: #FFFFFF;
        --light-2: #F1F5F9;
        --gray: #64748B;
        --gradient-primary: linear-gradient(135deg, #1E3A8A 0%, #3B82F6 100%);
        --gradient-secondary: linear-gradient(135deg, #0891B2 0%, #38BDF8 100%);
        --gradient-accent: linear-gradient(135deg, #38BDF8 0%, #0EA5E9 100%);
        --gradient-dark: linear-gradient(135deg, #0F172A 0%, #1E293B 100%);
        --gradient-professional: linear-gradient(135deg, #1E3A8A 0%, #0891B2 100%);
        --shadow-sm: 0 1px 3px rgba(0,0,0,0.12);
        --shadow-md: 0 4px 6px rgba(0,0,0,0.1);
        --shadow-lg: 0 10px 25px rgba(0,0,0,0.15);
        --shadow-xl: 0 20px 40px rgba(0,0,0,0.2);
    }
    
    /* Global Styles */
    * {
        font-family: 'Poppins', sans-serif;
    }
    
    /* Streamlit overrides for professional look */
    .stApp {
        background: linear-gradient(180deg, #F8FAFC 0%, #F1F5F9 100%);
    }
    
    .main .block-container {
        background: transparent;
    }
    
    /* Main container */
    .main {
        padding: 1.5rem;
        max-width: 1400px;
        margin: 0 auto;
    }
    
    .block-container {
        padding-top: 1.5rem;
        padding-bottom: 2rem;
    }
    
    /* Header styling - Professional Corporate */
    .header-container {
        background: linear-gradient(135deg, #1E3A8A 0%, #0891B2 100%);
        padding: 2.5rem 2rem;
        border-radius: 16px;
        margin-bottom: 2rem;
        color: white;
        text-align: center;
        box-shadow: 0 10px 25px rgba(30, 58, 138, 0.2);
        border: none;
        position: relative;
        overflow: hidden;
    }
    
    .header-title {
        font-size: 2.5rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
        letter-spacing: -0.5px;
        position: relative;
        z-index: 1;
    }
    
    .header-subtitle {
        font-size: 1.1rem;
        opacity: 0.95;
        font-weight: 400;
        position: relative;
        z-index: 1;
    }
    
    /* Card styling - Professional White Cards */
    .card {
        background: white;
        padding: 1.75rem;
        border-radius: 12px;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1),
                    0 1px 2px rgba(0, 0, 0, 0.06);
        margin-bottom: 1.25rem;
        border: 1px solid rgba(226, 232, 240, 0.8);
        transition: all 0.3s ease;
    }
    
    .card:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 20px rgba(30, 58, 138, 0.1),
                    0 6px 6px rgba(0, 0, 0, 0.05);
        border-color: rgba(30, 58, 138, 0.2);
    }
    
    /* Workout plan table */
    .workout-table {
        width: 100%;
        border-collapse: separate;
        border-spacing: 0;
        margin: 1.5rem 0;
        border-radius: 16px;
        overflow: hidden;
        box-shadow: 0 4px 24px rgba(0,0,0,0.2);
    }
    
    .workout-table th {
        background: linear-gradient(135deg, #1E3A8A 0%, #0891B2 100%);
        color: white;
        padding: 16px 18px;
        text-align: left;
        font-weight: 600;
        font-size: 0.9rem;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .workout-table td {
        padding: 14px 18px;
        border-bottom: 1px solid #E2E8F0;
        background: white;
        color: #334155;
        transition: all 0.2s ease;
    }
    
    .workout-table tr:hover td {
        background: #F8FAFC;
        color: #1E3A8A;
    }
    
    .workout-table tr:last-child td {
        border-bottom: none;
    }
    
    /* Metrics styling - Professional Cards */
    .metric-card {
        background: white;
        border: 1px solid #E2E8F0;
        color: #0F172A;
        padding: 2rem 1.5rem;
        border-radius: 12px;
        text-align: center;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .metric-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 3px;
        background: linear-gradient(90deg, #1E3A8A, #0891B2);
    }
    
    .metric-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 10px 20px rgba(30, 58, 138, 0.15);
        border-color: #1E3A8A;
    }
    
    .metric-value {
        font-size: 2.2rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
        color: #1E3A8A;
    }
    
    .metric-label {
        font-size: 0.875rem;
        color: #64748B;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    /* Success probability bar - Professional */
    .success-bar {
        height: 44px;
        background: #F1F5F9;
        border-radius: 22px;
        overflow: hidden;
        margin: 1.5rem 0;
        box-shadow: inset 0 2px 4px rgba(0,0,0,0.06);
        border: 1px solid #E2E8F0;
    }
    
    .success-fill {
        height: 100%;
        background: linear-gradient(90deg, #0891B2 0%, #38BDF8 100%);
        transition: width 1s ease;
        display: flex;
        align-items: center;
        justify-content: center;
        color: white;
        font-weight: 600;
        font-size: 1.1rem;
    }
    
    /* Exercise card - Professional White Cards */
    .exercise-card {
        background: white;
        border-left: 4px solid #0891B2;
        padding: 1.75rem;
        margin-bottom: 1.25rem;
        border-radius: 12px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        transition: all 0.3s ease;
        position: relative;
        border: 1px solid #E2E8F0;
        border-left-width: 4px;
    }
    
    .exercise-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(8, 145, 178, 0.15);
        border-left-color: #1E3A8A;
    }
    
    .exercise-name {
        font-size: 1.3rem;
        font-weight: 600;
        color: #0F172A;
        margin-bottom: 0.75rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    .exercise-details {
        color: #64748B;
        font-size: 0.95rem;
        line-height: 1.6;
    }
    
    /* Reasoning explanation - Professional Theme */
    .reasoning-section {
        background: white;
        border: 1px solid #E2E8F0;
        padding: 2rem;
        border-radius: 12px;
        margin: 1.5rem 0;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    }
    
    .reasoning-title {
        font-size: 1.5rem;
        font-weight: 600;
        color: #1E3A8A;
        margin-bottom: 1.5rem;
        padding-bottom: 0.75rem;
        border-bottom: 2px solid #E2E8F0;
    }
    
    .reasoning-step {
        background: #F8FAFC;
        padding: 1.25rem;
        margin-bottom: 1rem;
        border-radius: 8px;
        border-left: 3px solid #0891B2;
        box-shadow: 0 1px 2px rgba(0,0,0,0.05);
    }
        transition: all 0.3s ease;
        color: #E9ECEF;
    }
    
    .reasoning-step:hover {
        transform: translateX(8px);
        box-shadow: 0 4px 20px rgba(108, 99, 255, 0.2);
        border-left-color: #00F5D4;
    }
    
    /* Button styling - Gradient Glow */
    .stButton>button {
        background: linear-gradient(135deg, #FF6B35 0%, #FF8C61 50%, #6C63FF 100%);
        background-size: 200% 200%;
        color: white;
        border: none;
        padding: 1rem 3rem;
        border-radius: 14px;
        font-weight: 700;
        font-size: 1.1rem;
        cursor: pointer;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 0 6px 24px rgba(255, 107, 53, 0.35);
        text-transform: uppercase;
        letter-spacing: 1.5px;
        animation: button-gradient 3s ease infinite;
    }
    
    @keyframes button-gradient {
        0%, 100% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
    }
    
    .stButton>button:hover {
        transform: translateY(-4px) scale(1.02);
        box-shadow: 0 12px 36px rgba(255, 107, 53, 0.45),
                    0 0 40px rgba(108, 99, 255, 0.2);
    }
    
    .stButton>button:active {
        transform: translateY(-2px) scale(1.01);
    }
    
    /* Download buttons - Accent Glow */
    .stDownloadButton>button {
        background: linear-gradient(135deg, #00F5D4 0%, #00E5FF 100%);
        color: #1A1A2E;
        border: none;
        padding: 0.9rem 2.5rem;
        border-radius: 12px;
        font-weight: 700;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 0 4px 16px rgba(0, 245, 212, 0.3);
        letter-spacing: 1px;
    }
    
    .stDownloadButton>button:hover {
        transform: translateY(-4px);
        box-shadow: 0 8px 28px rgba(0, 245, 212, 0.5),
                    0 0 40px rgba(0, 245, 212, 0.2);
    }
    
    /* Warning/Info boxes - Professional Style */
    .warning-box {
        background: #FEF3C7;
        border-left: 4px solid #F59E0B;
        padding: 1.25rem 1.5rem;
        margin: 1.25rem 0;
        border-radius: 8px;
        color: #92400E;
    }
    
    .info-box {
        background: #DBEAFE;
        border-left: 4px solid #38BDF8;
        padding: 1.25rem 1.5rem;
        margin: 1.25rem 0;
        border-radius: 8px;
        color: #1E40AF;
    }
    
    .success-box {
        background: #D1FAE5;
        border-left: 4px solid #10B981;
        padding: 1.25rem 1.5rem;
        margin: 1.25rem 0;
        border-radius: 8px;
        color: #065F46;
    }
    
    .error-box {
        background: #FEE2E2;
        border-left: 4px solid #EF4444;
        padding: 1.25rem 1.5rem;
        margin: 1.25rem 0;
        border-radius: 8px;
        color: #991B1B;
    }
    
    /* Streamlit native components - Professional Light Theme */
    .stAlert {
        border-radius: 8px;
        border-left-width: 3px;
    }
    
    .stProgress > div > div {
        background: linear-gradient(90deg, #0891B2, #38BDF8);
        border-radius: 10px;
    }
    
    .stProgress > div {
        background: #E2E8F0;
        border-radius: 10px;
    }
    
    /* Form styling - Professional Light */
    .stTextInput>div>div>input,
    .stNumberInput>div>div>input,
    .stSelectbox>div>div>select {
        background: white !important;
        border-radius: 8px;
        border: 1px solid #CBD5E1;
        padding: 0.75rem;
        transition: all 0.2s ease;
    }
    
    .stTextInput>div>div>input:focus,
    .stNumberInput>div>div>input:focus,
    .stSelectbox>div>div>select:focus {
        border-color: #0891B2;
        box-shadow: 0 0 0 3px rgba(8, 145, 178, 0.1);
    }
    
    /* Slider styling - Professional Teal */
    .stSlider>div>div>div>div {
        background: linear-gradient(90deg, #1E3A8A 0%, #0891B2 100%) !important;
        border-radius: 8px;
        height: 6px;
    }
    
    .stSlider>div>div>div>div>div {
        background: #0891B2 !important;
        border: 2px solid white !important;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
        width: 20px !important;
        height: 20px !important;
        border-radius: 50%;
        transition: all 0.2s ease;
    }
    
    .stSlider>div>div>div>div>div:hover {
        transform: scale(1.15);
        box-shadow: 0 4px 8px rgba(8, 145, 178, 0.3);
    }
    
    /* Expander styling - Professional Light */
    .streamlit-expanderHeader {
        background: white !important;
        border-radius: 10px;
        padding: 1rem 1.25rem;
        font-weight: 600;
        color: #0F172A !important;
        border: 1px solid #E2E8F0;
        transition: all 0.2s ease;
    }
    
    .streamlit-expanderHeader:hover {
        background: #F8FAFC !important;
        border-color: #0891B2;
        box-shadow: 0 2px 8px rgba(8, 145, 178, 0.1);
    }
    
    .streamlit-expanderContent {
        background: white !important;
        border-radius: 0 0 10px 10px;
        border: 1px solid #E2E8F0;
        border-top: none;
        color: #334155 !important;
    }
    
    /* Footer - Professional Clean */
    .footer {
        text-align: center;
        padding: 2.5rem 2rem;
        color: #64748B;
        border-top: 1px solid #E2E8F0;
        margin-top: 3rem;
        background: white;
    }
    
    .footer p {
        margin: 0.4rem 0;
        color: #64748B;
    }
    
    .footer a {
        color: #0891B2;
        text-decoration: none;
        transition: all 0.2s ease;
    }
    
    .footer a:hover {
        color: #1E3A8A;
    }
    
    /* Sidebar styling - Professional Light */
    .css-1d391kg,
    [data-testid="stSidebar"] {
        background: white !important;
        border-right: 1px solid #E2E8F0;
    }
    
    [data-testid="stSidebar"]::before {
        content: '';
        position: absolute;
        top: 0;
        right: 0;
        width: 1px;
        height: 100%;
        background: linear-gradient(180deg, #1E3A8A, #0891B2);
    }
    
    [data-testid="stSidebar"] .stSelectbox label,
    [data-testid="stSidebar"] .stSlider label,
    [data-testid="stSidebar"] .stNumberInput label,
    [data-testid="stSidebar"] .stMultiSelect label {
        font-weight: 600;
        color: #334155 !important;
        font-size: 0.9rem;
    }
    
    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3 {
        color: #0F172A !important;
    }
    
    [data-testid="stSidebar"] p {
        color: #64748B !important;
    }
    
    /* Tab styling - Professional Light */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background: white;
        padding: 6px;
        border-radius: 10px;
        border: 1px solid #E2E8F0;
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px;
        padding: 12px 24px;
        background: transparent;
        font-weight: 600;
        color: #64748B;
        border: 1px solid transparent;
        transition: all 0.2s ease;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background: #F8FAFC;
        color: #0F172A;
        border-color: #E2E8F0;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #1E3A8A 0%, #0891B2 100%) !important;
        color: white !important;
        box-shadow: 0 2px 8px rgba(30, 58, 138, 0.2);
        border-color: transparent;
    }
    
    /* Metrics (native Streamlit) - Professional Style */
    [data-testid="stMetricValue"] {
        font-size: 2rem;
        font-weight: 700;
        color: #1E3A8A !important;
    }
    
    [data-testid="stMetricLabel"] {
        color: #64748B !important;
        font-weight: 500;
        font-size: 0.875rem !important;
    }
    
    [data-testid="stMetricDelta"] {
        color: #0891B2 !important;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Spinner styling - Professional */
    .stSpinner > div {
        border-top-color: #0891B2 !important;
        border-right-color: #1E3A8A !important;
        border-bottom-color: #38BDF8 !important;
        border-left-color: transparent !important;
    }
    
    /* Checkbox styling - Professional */
    .stCheckbox {
        padding: 0.5rem 0;
    }
    
    .stCheckbox label span {
        color: #334155 !important;
    }
    
    .stCheckbox [data-baseweb="checkbox"] {
        border-color: #CBD5E1 !important;
    }
    
    .stCheckbox [data-baseweb="checkbox"]:checked {
        background: #0891B2 !important;
        border-color: #0891B2 !important;
    }
    
    /* Multiselect styling - Neon Tags */
    .stMultiSelect [data-baseweb="tag"] {
        background: linear-gradient(135deg, #FF6B35 0%, #6C63FF 100%) !important;
        color: white !important;
        border-radius: 8px;
        font-weight: 600;
        padding: 4px 12px;
        border: none;
        box-shadow: 0 2px 10px rgba(255, 107, 53, 0.3);
    }
    
    .stMultiSelect [data-baseweb="tag"]:hover {
        box-shadow: 0 4px 15px rgba(255, 107, 53, 0.5);
        transform: translateY(-2px);
    }
    
    .stMultiSelect > div > div {
        background: rgba(26, 26, 46, 0.9) !important;
        border: 2px solid rgba(108, 99, 255, 0.3) !important;
        border-radius: 12px;
    }
    
    .stMultiSelect > div > div:focus-within {
        border-color: #6C63FF !important;
        box-shadow: 0 0 20px rgba(108, 99, 255, 0.3);
    }
    
    /* Radio buttons - Neon */
    .stRadio > div {
        background: rgba(26, 26, 46, 0.5);
        padding: 1rem;
        border-radius: 12px;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    .stRadio label {
        color: rgba(255, 255, 255, 0.9) !important;
        font-weight: 500;
    }
    
    .stRadio [data-baseweb="radio"] div:first-child {
        border-color: #6C63FF !important;
    }
    
    .stRadio [data-baseweb="radio"]:checked div:first-child {
        background: linear-gradient(135deg, #FF6B35, #6C63FF) !important;
    }
    
    /* Dataframe styling - Dark Neon */
    .stDataFrame {
        border-radius: 16px;
        overflow: hidden;
        border: 1px solid rgba(255, 107, 53, 0.2);
    }
    
    .stDataFrame [data-testid="stDataFrameResizable"] {
        background: rgba(26, 26, 46, 0.95) !important;
    }
    
    .stDataFrame th {
        background: linear-gradient(135deg, #FF6B35 0%, #6C63FF 100%) !important;
        color: white !important;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .stDataFrame td {
        background: rgba(26, 26, 46, 0.9) !important;
        color: rgba(255, 255, 255, 0.9) !important;
        border-color: rgba(255, 255, 255, 0.1) !important;
    }
    
    .stDataFrame tr:hover td {
        background: rgba(255, 107, 53, 0.1) !important;
    }
    
    /* Divider - Professional Gradient */
    hr {
        border: none;
        height: 1px;
        background: linear-gradient(90deg, transparent, #CBD5E1, transparent);
        margin: 1.5rem 0;
    }
    
    /* Scrollbar - Dark Neon */
    ::-webkit-scrollbar {
        width: 10px;
        height: 10px;
    }
    
    ::-webkit-scrollbar-track {
        background: rgba(15, 15, 30, 0.8);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(180deg, #FF6B35, #6C63FF);
        border-radius: 10px;
        border: 2px solid rgba(15, 15, 30, 0.8);
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(180deg, #FF8255, #8C83FF);
    }
    
    /* Text selection - Neon Accent */
    ::selection {
        background: rgba(0, 245, 212, 0.3);
        color: white;
    }
    
    /* Tooltip styling */
    [data-baseweb="tooltip"] {
        background: #0F172A !important;
        border: 1px solid #334155;
        border-radius: 6px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
    }
    
    /* Responsive design - Dark Theme */
    @media (max-width: 768px) {
        .header-title {
            font-size: 2rem;
        }
        
        .header-subtitle {
            font-size: 1rem;
        }
        
        .metric-card {
            margin-bottom: 1rem;
            padding: 1.5rem 1rem;
        }
        
        .metric-value {
            font-size: 2rem;
        }
        
        .main {
            padding: 1rem;
        }
        
        .card {
            padding: 1.5rem;
        }
    }
    
    @media (max-width: 480px) {
        .header-title {
            font-size: 1.5rem;
        }
        
        .metric-value {
            font-size: 1.5rem;
        }
        
        .stButton>button {
            padding: 0.7rem 1.5rem;
            font-size: 0.95rem;
        }
    }
    
    /* Animation classes */
    @keyframes fadeIn {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .fade-in {
        animation: fadeIn 0.5s ease-out;
    }
    
    @keyframes slideIn {
        from {
            transform: translateX(-100%);
        }
        to {
            transform: translateX(0);
        }
    }
    
    .slide-in {
        animation: slideIn 0.4s ease-out;
    }
    
    @keyframes pulse {
        0%, 100% {
            box-shadow: 0 0 20px rgba(0, 245, 212, 0.4);
        }
        50% {
            box-shadow: 0 0 40px rgba(0, 245, 212, 0.8);
        }
    }
    
    .pulse {
        animation: pulse 2s infinite;
    }
    
    @keyframes float {
        0%, 100% {
            transform: translateY(0);
        }
        50% {
            transform: translateY(-10px);
        }
    }
    
    .float {
        animation: float 3s ease-in-out infinite;
    }
    
    /* Loading skeleton - Dark Neon */
    .skeleton {
        background: linear-gradient(90deg, rgba(26, 26, 46, 0.8) 25%, rgba(40, 40, 70, 0.8) 50%, rgba(26, 26, 46, 0.8) 75%);
        background-size: 200% 100%;
        animation: loading 1.5s infinite;
        border-radius: 8px;
    }
    
    @keyframes loading {
        0% {
            background-position: 200% 0;
        }
        100% {
            background-position: -200% 0;
        }
    }
    
    /* Glow effects for special elements */
    .glow-primary {
        box-shadow: 0 0 30px rgba(255, 107, 53, 0.5);
    }
    
    .glow-secondary {
        box-shadow: 0 0 30px rgba(108, 99, 255, 0.5);
    }
    
    .glow-accent {
        box-shadow: 0 0 30px rgba(0, 245, 212, 0.5);
    }
    
    /* Gradient text utility */
    .gradient-text {
        background: linear-gradient(135deg, #FF6B35, #6C63FF, #00F5D4);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    /* Glass card utility */
    .glass-card {
        background: rgba(26, 26, 46, 0.7);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 16px;
    }
    
    /* Neon border utility */
    .neon-border {
        border: 2px solid transparent;
        background-image: linear-gradient(rgba(26, 26, 46, 1), rgba(26, 26, 46, 1)), 
                          linear-gradient(135deg, #FF6B35, #6C63FF, #00F5D4);
        background-origin: border-box;
        background-clip: padding-box, border-box;
    }
    </style>
    """


def load_custom_css() -> None:
    """
    Load custom CSS into the Streamlit application.
    
    This function should be called early in the main app function.
    """
    import streamlit as st
    st.markdown(get_custom_css(), unsafe_allow_html=True)
