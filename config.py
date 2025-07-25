"""Configuration and styling for the F1 Dashboard"""

import streamlit as st

def setup_page_config():
    """Configure Streamlit page settings"""
    st.set_page_config(
        page_title="F1 Statistics Dashboard",
        page_icon="🏎️",
        layout="wide",
        initial_sidebar_state="expanded"
    )

def apply_custom_css():
    """Apply custom CSS styling with Roboto Mono font everywhere."""
    import streamlit as st
    st.markdown("""
    <link href="https://fonts.googleapis.com/css2?family=Roboto+Mono:wght@400;500;600;700&display=swap" rel="stylesheet">
    <style>
        /* Global font override - most important */
        * {
            font-family: 'Roboto Mono', monospace !important;
        }
        
        /* HTML and body */
        html, body {
            font-family: 'Roboto Mono', monospace !important;
        }
        
        /* All Streamlit components */
        .stApp, .stApp * {
            font-family: 'Roboto Mono', monospace !important;
        }
        
        /* Headers and markdown */
        h1, h2, h3, h4, h5, h6 {
            font-family: 'Roboto Mono', monospace !important;
        }
        
        .stMarkdown, .stMarkdown * {
            font-family: 'Roboto Mono', monospace !important;
        }
        
        /* Sidebar */
        .css-1d391kg, .css-1d391kg * {
            font-family: 'Roboto Mono', monospace !important;
        }
        
        /* Selectbox and other inputs */
        .stSelectbox, .stSelectbox * {
            font-family: 'Roboto Mono', monospace !important;
        }
        
        .stTextInput, .stTextInput * {
            font-family: 'Roboto Mono', monospace !important;
        }
        
        .stButton, .stButton * {
            font-family: 'Roboto Mono', monospace !important;
        }
        
        .stRadio, .stRadio * {
            font-family: 'Roboto Mono', monospace !important;
        }
        
        /* Data components */
        .stDataFrame, .stDataFrame * {
            font-family: 'Roboto Mono', monospace !important;
        }
        
        /* AG Grid */
        .ag-theme-streamlit, .ag-theme-streamlit * {
            font-family: 'Roboto Mono', monospace !important;
        }
        
        .st-aggrid, .st-aggrid * {
            font-family: 'Roboto Mono', monospace !important;
        }
        
        /* AG Grid header and cell styling */
        .ag-header-cell-text {
            font-size: 16px !important;
            font-weight: bold !important;
            text-align: left !important;
            padding-left: 10px !important;
        }
        
        .ag-cell {
            font-size: 16px !important;
            text-align: left !important;
        }
        
        /* Custom class for left-aligned headers */
        .ag-header-cell-left .ag-header-cell-text {
            text-align: left !important;
            padding-left: 10px !important;
        }
        
        /* All data-testid elements */
        [data-testid] {
            font-family: 'Roboto Mono', monospace !important;
        }
        
        [data-testid] * {
            font-family: 'Roboto Mono', monospace !important;
        }
        
        /* Specific Streamlit test IDs */
        [data-testid="stHeader"], [data-testid="stHeader"] * {
            font-family: 'Roboto Mono', monospace !important;
        }
        
        [data-testid="stSidebar"], [data-testid="stSidebar"] * {
            font-family: 'Roboto Mono', monospace !important;
        }
        
        [data-testid="stMarkdownContainer"], [data-testid="stMarkdownContainer"] * {
            font-family: 'Roboto Mono', monospace !important;
        }
        
        [data-testid="stSelectbox"], [data-testid="stSelectbox"] * {
            font-family: 'Roboto Mono', monospace !important;
        }
        
        /* Add more space above the results view dropdown */
        [data-testid="stSelectbox"] {
            margin-top: 30px;
        }
        
        /* All CSS classes that might contain text */
        [class*="css"], [class*="css"] * {
            font-family: 'Roboto Mono', monospace !important;
        }
        
        /* Fallback for all HTML elements */
        p, div, span, label, input, textarea, select, button, a, li, ul, ol {
            font-family: 'Roboto Mono', monospace !important;
        }
        
        /* Force override for any remaining elements */
        body *, .stApp *, [data-testid] *, [class*="css"] * {
            font-family: 'Roboto Mono', monospace !important;
        }
    </style>
    """, unsafe_allow_html=True)