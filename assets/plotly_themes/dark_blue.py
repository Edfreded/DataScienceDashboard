"""Dark blue Plotly theme configuration"""

DARK_BLUE_THEME = {
    'layout': {
        'paper_bgcolor': '#0f1419',  # Very dark blue-gray
        'plot_bgcolor': '#1a1f2e',   # Slightly lighter for plot area
        'font': {'color': '#64b5f6', 'family': 'Arial, sans-serif'},  # Light blue text
        'title': {'font': {'color': '#64b5f6', 'size': 18}},
        'colorway': [
            '#64b5f6',  # Light blue
            '#42a5f5',  # Medium blue
            '#2196f3',  # Blue
            '#1976d2',  # Dark blue
            '#0d47a1',  # Very dark blue
            '#81c784',  # Light green
            '#66bb6a',  # Green
            '#4caf50'   # Dark green
        ],
        'xaxis': {
            'gridcolor': '#2a3441',
            'linecolor': '#64b5f6',
            'tickcolor': '#64b5f6',
            'title': {'font': {'color': '#64b5f6'}},
            'tickfont': {'color': '#64b5f6'}
        },
        'yaxis': {
            'gridcolor': '#2a3441',
            'linecolor': '#64b5f6',
            'tickcolor': '#64b5f6',
            'title': {'font': {'color': '#64b5f6'}},
            'tickfont': {'color': '#64b5f6'}
        },
        'legend': {
            'font': {'color': '#64b5f6'},
            'bgcolor': 'rgba(15, 20, 25, 0.8)',
            'bordercolor': '#64b5f6'
        }
    }
}