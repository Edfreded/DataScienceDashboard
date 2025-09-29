from .plotly_themes.theme_loader import setup_plotly_theme, get_available_themes

# Available themes configuration
THEMES = {
    'default': {
        'css_file': 'css/default_theme.css',
        'plotly_theme': 'plotly'
    },
    'retro': {
        'css_file': 'css/retro_theme.css',
        'plotly_theme': 'retro_purple'
    },
    'dark': {
        'css_file': 'css/dark.css',
        'plotly_theme': 'plotly_dark'
    },
    'dark_blue': {
        'css_file': 'css/dark_blue.css',
        'plotly_theme': 'dark_blue'
    }
}

# Default theme
DEFAULT_THEME = 'retro'