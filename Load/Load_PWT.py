from shiny import ui, reactive
from Load.UI.Layouts.Layout_PWT_Overview import create_dashboard_ui as create_overview_ui
from Load.UI.Layouts.Layout_PWT_GDP import create_gdp_analysis_ui
from Load.UI.Layouts.Layout_PWT_Economic import create_economic_indicators_ui
from Load.UI.Layouts.Layout_PWT_Explorer import create_data_explorer_ui

from Load.UI.Sidebars.Sidebar_PWT import create_sidebar

from Load.Server.Server_PWT_Overview import create_dashboard_server as create_overview_server
from Load.Server.Server_PWT_GDP import create_gdp_analysis_server
from Load.Server.Server_PWT_Economic import create_economic_indicators_server
from Load.Server.Server_PWT_Explorer import create_data_explorer_server
from Load.Server.Server_PWT_Filters import create_filters_server

def create_dashboard_ui(css_file=None):
    head_elements = []
    css_to_use = css_file or 'css/default_theme.css'
    head_elements.append(ui.tags.link(rel="stylesheet", href=css_to_use))
    
    return ui.page_sidebar(        
        create_sidebar(),

        ui.div(
            ui.tags.head(*head_elements),
            ui.navset_tab(
                ui.nav_panel(
                    "Overview",
                    create_overview_ui()
                ),
                
                ui.nav_panel(
                    "GDP Analysis", 
                    create_gdp_analysis_ui()
                ),
                
                ui.nav_panel(
                    "Economic Indicators",
                    create_economic_indicators_ui()
                ),
                
                ui.nav_panel(
                    "Data Explorer",
                    create_data_explorer_ui()
                ),
                id="main_tabs"
            )
        )
    )

def create_dashboard_server(cleaned_data=None, summary_stats=None):
    def server(input, output, session):
        # Initialize filters server and get reactive filtered data
        filters_server = create_filters_server(cleaned_data, summary_stats)(input, output, session)
        filtered_data = filters_server['filtered_data']
        filtered_summary_stats = filters_server['filtered_summary_stats']
        
        # Pass filtered data to dashboard servers
        create_overview_server(filtered_data, filtered_summary_stats)(input, output, session)
        create_gdp_analysis_server(filtered_data, filtered_summary_stats)(input, output, session)
        create_economic_indicators_server(filtered_data, filtered_summary_stats)(input, output, session)
        create_data_explorer_server(filtered_data, filtered_summary_stats)(input, output, session)
    
    return server