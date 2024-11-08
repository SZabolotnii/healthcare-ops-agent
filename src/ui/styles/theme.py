from dataclasses import dataclass
from typing import Dict, Any

@dataclass
class HealthcareTheme:
    """Healthcare UI theme configuration"""
    
    # Color palette
    colors = {
        'primary': '#2196f3',        # Main blue
        'primary_light': '#e3f2fd',  # Light blue
        'primary_dark': '#1976d2',   # Dark blue
        'success': '#4caf50',        # Green
        'warning': '#ff9800',        # Orange
        'error': '#f44336',          # Red
        'info': '#2196f3',          # Blue
        'background': '#f0f8ff',     # Light blue background
        'surface': '#ffffff',        # White
        'text': '#2c3e50',          # Dark gray
        'text_secondary': '#707070'  # Medium gray
    }
    
    # Typography
    fonts = {
        'primary': '"Source Sans Pro", -apple-system, BlinkMacSystemFont, sans-serif',
        'monospace': '"Roboto Mono", monospace'
    }
    
    # Spacing
    spacing = {
        'xs': '0.25rem',
        'sm': '0.5rem',
        'md': '1rem',
        'lg': '1.5rem',
        'xl': '2rem'
    }
    
    # Border radius
    radius = {
        'sm': '4px',
        'md': '8px',
        'lg': '12px',
        'xl': '16px',
        'pill': '9999px'
    }
    
    # Shadows
    shadows = {
        'sm': '0 1px 3px rgba(0,0,0,0.12)',
        'md': '0 2px 4px rgba(0,0,0,0.1)',
        'lg': '0 4px 6px rgba(0,0,0,0.1)',
        'xl': '0 8px 12px rgba(0,0,0,0.1)'
    }
    
    @classmethod
    def get_streamlit_config(cls) -> Dict[str, Any]:
        """Get Streamlit theme configuration"""
        return {
            "theme": {
                "primaryColor": cls.colors['primary'],
                "backgroundColor": cls.colors['background'],
                "secondaryBackgroundColor": cls.colors['surface'],
                "textColor": cls.colors['text'],
                "font": cls.fonts['primary']
            }
        }
    
    @classmethod
    def apply_theme(cls):
        """Apply theme to Streamlit application"""
        import streamlit as st
        
        # Apply theme configuration
        st.set_page_config(**cls.get_streamlit_config())
        
        # Apply custom CSS
        st.markdown("""
            <style>
                /* Import fonts */
                @import url('https://fonts.googleapis.com/css2?family=Source+Sans+Pro:wght@400;600;700&display=swap');
                @import url('https://fonts.googleapis.com/css2?family=Roboto+Mono&display=swap');
                
                /* Base styles */
                .stApp {
                    font-family: var(--primary-font);
                    color: var(--text-color);
                }
                
                /* Custom CSS Variables */
                :root {
                    --primary-color: """ + cls.colors['primary'] + """;
                    --primary-light: """ + cls.colors['primary_light'] + """;
                    --primary-dark: """ + cls.colors['primary_dark'] + """;
                    --background-color: """ + cls.colors['background'] + """;
                    --surface-color: """ + cls.colors['surface'] + """;
                    --text-color: """ + cls.colors['text'] + """;
                    --primary-font: """ + cls.fonts['primary'] + """;
                }
                
                /* Apply theme to Streamlit elements */
                .stButton>button {
                    background-color: var(--primary-color);
                    color: white;
                    border-radius: """ + cls.radius['pill'] + """;
                    padding: """ + cls.spacing['sm'] + """ """ + cls.spacing['lg'] + """;
                    border: none;
                    box-shadow: """ + cls.shadows['sm'] + """;
                }
                
                .stButton>button:hover {
                    background-color: var(--primary-dark);
                    box-shadow: """ + cls.shadows['md'] + """;
                }
                
                .stTextInput>div>div>input {
                    border-radius: """ + cls.radius['md'] + """;
                }
                
                .stSelectbox>div>div>div {
                    border-radius: """ + cls.radius['md'] + """;
                }
            </style>
        """, unsafe_allow_html=True)