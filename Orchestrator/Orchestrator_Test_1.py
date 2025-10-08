from shiny import App
from Config import ASSETS_PATH
from Extract.Extract_Test import extract_car_data
from Transform.Transform_Test import clean_and_transform_data, create_summary_stats
from Load.Load_Test_2 import create_dashboard_ui, create_dashboard_server


def orchestrator_test_1(css_file=None):

    print("Extracting Car Sales Dataset...")
    raw_data = extract_car_data()

    print("Transforming Car Sales Dataset...")
    cleaned_data = clean_and_transform_data(raw_data)
    summary_stats = create_summary_stats(cleaned_data)

    print("Starting Car Sales Dashboard Orchestrator...")
    app_ui = create_dashboard_ui(css_file=css_file)
    app_server = create_dashboard_server(
        cleaned_data=cleaned_data, 
        summary_stats=summary_stats
    )

    print("Dashboard ready! Starting server...")

    return App(app_ui, app_server, static_assets=ASSETS_PATH)