from Extract.Extract_Test import extract_car_data
from Transform.Transform_Test import clean_and_transform_data, create_summary_stats
from Load.Load_Test_Dashboard1 import create_dashboard_layout
import dash
import dash_bootstrap_components as dbc

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
    app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
    
    # Set the layout
    app.layout = create_dashboard_layout(summary_stats, cleaned_data)
    
    print("Dashboard ready! Starting server...")
    print("Access the dashboard at: http://localhost:8050")
    
    # Run the app
    app.run(host='0.0.0.0', port=8050, debug=True)

