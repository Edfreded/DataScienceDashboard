"""Dynamic theme loader for Plotly themes"""

import plotly.io as pio
from .retro_purple import RETRO_PURPLE_THEME
from .dark_blue import DARK_BLUE_THEME

# Theme registry - add new themes here
THEME_REGISTRY = {
    'retro_purple': RETRO_PURPLE_THEME,
    'dark_blue': DARK_BLUE_THEME,
}

def load_custom_theme(theme_name, theme_config):
    """Load a custom theme into Plotly templates"""
    pio.templates[theme_name] = theme_config

def setup_plotly_theme(theme_name="plotly"):
    """Set up Plotly theme based on theme name"""
    if theme_name in THEME_REGISTRY:
        load_custom_theme(theme_name, THEME_REGISTRY[theme_name])
        pio.templates.default = theme_name
    elif theme_name == "plotly_dark":
        pio.templates.default = "plotly_dark"
    elif theme_name == "plotly_white":
        pio.templates.default = "plotly_white"
    else:
        # Default plotly theme
        pio.templates.default = "plotly"

def get_available_themes():
    """Get list of all available themes"""
    builtin_themes = ["plotly", "plotly_dark", "plotly_white"]
    custom_themes = list(THEME_REGISTRY.keys())
    return builtin_themes + custom_themes