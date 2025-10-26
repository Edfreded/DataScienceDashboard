from shiny import App
from Config import ASSETS_PATH
from Extract.Extract_PWT import extract_PWT
from Transform.Transform_PWT_Cleaning import pwt_clean
from Transform.Transform_PWT_Imputation import pwt_impute
from Transform.Transform_PWT_Features import pwt_feature
from Load.Load_PWT import create_dashboard_ui, create_dashboard_server


def orchestrator_PWT(css_file=None):

    print("Extracting PWT Dataset...")
    raw_data = extract_PWT()

    print("Transforming PWT Dataset...")
    
    cleaned_data = pwt_clean(raw_data)
    imputed_data = pwt_impute(cleaned_data)
    featured_data = pwt_feature(imputed_data)

    print("Starting PWT Dashboard...")
    app_ui = create_dashboard_ui(css_file=css_file)
    app_server = create_dashboard_server(
        cleaned_data=featured_data, 
    )

    print("Dashboard ready! Starting server...")

    return App(app_ui, app_server, static_assets=ASSETS_PATH)