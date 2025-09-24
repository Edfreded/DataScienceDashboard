import dash
import plotly.io as pio
from Config import ASSETS_PATH
from Extract.Extract_Test import extract_car_data
from Transform.Transform_Test import clean_and_transform_data, create_summary_stats
from Load.Load_Test_Dashboard1 import create_dashboard_layout

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
    
    app = dash.Dash(__name__, assets_folder=ASSETS_PATH)
    
    # Set the layout
    app.layout = create_dashboard_layout(summary_stats, cleaned_data)
    print("Dashboard ready! Starting server...")

    return app