from .theme_config import THEMES, DEFAULT_THEME, THEME_COLORS
import plotly.io as pio

def get_theme_css_file(theme_name=None):
    """Get CSS file path for theme"""
    theme_name = theme_name or DEFAULT_THEME
    return THEMES.get(theme_name, THEMES[DEFAULT_THEME])

def get_theme_colors(theme_name=None):
    """Get color palette for Plotly charts"""
    theme_name = theme_name or DEFAULT_THEME
    return THEME_COLORS.get(theme_name, THEME_COLORS[DEFAULT_THEME])

def get_available_themes():
    """Get list of available theme names"""
    return list(THEMES.keys())

def setup_plotly_colors(theme_name=None):
    """Set up Plotly to use theme colors from config"""
    theme_name = theme_name or DEFAULT_THEME
    colors = get_theme_colors(theme_name)
    
    # Set dark template for better contrast with your themes
    pio.templates.default = "plotly_dark"
    
    # Apply the theme colors to the dark template
    pio.templates["plotly_dark"].layout.colorway = colors
    
    return colors