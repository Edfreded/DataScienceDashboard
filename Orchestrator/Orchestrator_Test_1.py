from Extract.Extract_Test import extract_car_data
from Transform.Transform_Test import clean_and_transform_data, create_summary_stats
from Load.Load_Test_Dashboard1 import create_dashboard_layout
import dash
import plotly.io as pio

def orchestrator_test_1():
    """
    Main orchestrator for the car sales dashboard
    Coordinates Extract, Transform, and Load operations
    """
    print("Starting Car Sales Dashboard Orchestrator...")
    
    # Step 1: Extract
    print("Step 1: Extracting data...")
    raw_data = extract_car_data()
    
    if raw_data.empty:
        print("No data extracted. Exiting.")
        return
    
    # Step 2: Transform
    print("Step 2: Transforming data...")
    cleaned_data = clean_and_transform_data(raw_data)
    summary_stats = create_summary_stats(cleaned_data)
    
    # Step 3: Load (Create Dashboard)
    print("Step 3: Creating dashboard...")
    
    # Create custom template matching Bootstrap DARKLY theme
    custom_template = {
        'layout': {
            'paper_bgcolor': '#343a40',  # Bootstrap dark background
            'plot_bgcolor': '#495057',   # Slightly lighter for plot area
            'font': {'color': '#f8f9fa'}, # Bootstrap light text
            'colorway': [
                '#007bff',  # Bootstrap primary
                '#28a745',  # Bootstrap success  
                '#dc3545',  # Bootstrap danger
                '#ffc107',  # Bootstrap warning
                '#17a2b8',  # Bootstrap info
                '#6f42c1',  # Bootstrap purple
                '#fd7e14',  # Bootstrap orange
                '#20c997'   # Bootstrap teal
            ],
            'xaxis': {
                'gridcolor': '#6c757d',
                'linecolor': '#6c757d',
                'tickcolor': '#6c757d'
            },
            'yaxis': {
                'gridcolor': '#6c757d', 
                'linecolor': '#6c757d',
                'tickcolor': '#6c757d'
            }
        }
    }
    
    # Register and set the custom template
    pio.templates["bootstrap_dark"] = custom_template
    pio.templates.default = "bootstrap_dark"
    
    app = dash.Dash(__name__)
    
    # Embed CSS directly to avoid file serving issues
    app.index_string = '''
    <!DOCTYPE html>
    <html>
        <head>
            {%metas%}
            <title>{%title%}</title>
            {%favicon%}
            {%css%}
            <style>
                * {
                    margin: 0;
                    padding: 0;
                    box-sizing: border-box;
                }
                html, body {
                    background-color: #343a40;
                    color: #f8f9fa;
                    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                    line-height: 1.5;
                    height: 100vh;
                    overflow: hidden;
                }
                .dashboard-container {
                    background-color: #343a40;
                    height: 100vh;
                    padding: 1rem;
                    display: grid;
                    grid-template-rows: auto 1fr;
                    gap: 1rem;
                }
                .dashboard-header {
                    text-align: center;
                }
                .dashboard-title {
                    font-size: 1.8rem;
                    font-weight: 300;
                    color: #f8f9fa;
                    margin-bottom: 0.5rem;
                }
                .dashboard-divider {
                    height: 2px;
                    background: linear-gradient(90deg, transparent, #007bff, transparent);
                    border: none;
                    margin: 0.5rem auto;
                    width: 150px;
                }
                .main-content {
                    display: grid;
                    grid-template-columns: 300px 1fr;
                    gap: 1rem;
                    height: 100%;
                    overflow: hidden;
                }
                .left-sidebar {
                    display: flex;
                    flex-direction: column;
                    gap: 1rem;
                }
                .stats-container {
                    display: flex;
                    flex-direction: column;
                    gap: 1rem;
                }
                .stat-card {
                    background-color: #495057;
                    border-radius: 8px;
                    padding: 1rem;
                    text-align: center;
                    transition: transform 0.2s ease, box-shadow 0.2s ease;
                    border: 1px solid #6c757d;
                }
                .stat-card:hover {
                    transform: translateY(-2px);
                    box-shadow: 0 4px 15px rgba(0, 123, 255, 0.15);
                }
                .stat-value {
                    font-size: 1.5rem;
                    font-weight: 600;
                    color: #007bff;
                    margin-bottom: 0.3rem;
                }
                .stat-label {
                    font-size: 0.8rem;
                    color: #adb5bd;
                    text-transform: uppercase;
                    letter-spacing: 0.5px;
                }
                .charts-area {
                    display: grid;
                    grid-template-columns: 1fr 1fr;
                    grid-template-rows: 1fr 1fr;
                    gap: 1rem;
                    height: 100%;
                }
                .chart-container {
                    background-color: #495057;
                    border-radius: 8px;
                    padding: 0.5rem;
                    border: 1px solid #6c757d;
                    overflow: hidden;
                }
                .chart-container.full-width {
                    grid-column: 1 / -1;
                }
                .js-plotly-plot, .plotly-graph-div {
                    background-color: transparent !important;
                    height: 100% !important;
                }
                @media (max-width: 768px) {
                    .main-content {
                        grid-template-columns: 1fr;
                        grid-template-rows: auto 1fr;
                    }
                    .stats-container {
                        flex-direction: row;
                        gap: 0.5rem;
                    }
                    .charts-area {
                        grid-template-columns: 1fr;
                        grid-template-rows: repeat(3, 300px);
                        height: auto;
                    }
                }
            </style>
        </head>
        <body>
            {%app_entry%}
            <footer>
                {%config%}
                {%scripts%}
                {%renderer%}
            </footer>
        </body>
    </html>
    '''
    
    # Set the layout
    app.layout = create_dashboard_layout(summary_stats, cleaned_data)
    print("Dashboard ready! Starting server...")

    return app