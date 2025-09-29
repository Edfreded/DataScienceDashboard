"""Retro purple-pink Plotly theme configuration"""

RETRO_PURPLE_THEME = {
    'layout': {
        'paper_bgcolor': '#1a0d2e',  # Deep purple background
        'plot_bgcolor': '#16213e',   # Slightly lighter purple for plot area
        'font': {'color': '#ff6b9d', 'family': 'Orbitron, Arial, sans-serif'},  # Pink text
        'title': {'font': {'color': '#ff6b9d', 'size': 18}},
        'colorway': [
            '#ff6b9d',  # Hot pink
            '#c44569',  # Deep pink
            '#f8b500',  # Golden yellow
            '#ff9ff3',  # Light pink
            '#54a0ff',  # Electric blue
            '#5f27cd',  # Purple
            '#00d2d3',  # Cyan
            '#ff9f43'   # Orange
        ],
        'xaxis': {
            'gridcolor': '#3c2a4d',
            'linecolor': '#ff6b9d',
            'tickcolor': '#ff6b9d',
            'title': {'font': {'color': '#ff6b9d'}},
            'tickfont': {'color': '#ff6b9d'}
        },
        'yaxis': {
            'gridcolor': '#3c2a4d',
            'linecolor': '#ff6b9d',
            'tickcolor': '#ff6b9d',
            'title': {'font': {'color': '#ff6b9d'}},
            'tickfont': {'color': '#ff6b9d'}
        },
        'legend': {
            'font': {'color': '#ff6b9d'},
            'bgcolor': 'rgba(26, 13, 46, 0.8)',
            'bordercolor': '#ff6b9d'
        }
    }
}