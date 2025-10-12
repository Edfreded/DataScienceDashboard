from shiny import App
from Config import ASSETS_PATH
from Extract.Extract_PWT import extract_PWT
from Transform.Transform_PWT import clean_and_transform_data, create_summary_stats
from Load.Load_PWT import create_dashboard_ui, create_dashboard_server


def orchestrator_PWT(css_file=None):

    print("Extracting PWT Dataset...")
    raw_data = extract_PWT()

    print("Transforming PWT Dataset...")
    cleaned_data = clean_and_transform_data(raw_data)
    summary_stats = create_summary_stats(cleaned_data)

    print("Starting PWT Dashboard...")
    app_ui = create_dashboard_ui(css_file=css_file)
    app_server = create_dashboard_server(
        cleaned_data=cleaned_data, 
        summary_stats=summary_stats
    )

    print("Dashboard ready! Starting server...")

    return App(app_ui, app_server, static_assets=ASSETS_PATH)