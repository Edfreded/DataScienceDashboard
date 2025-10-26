from shiny import ui, reactive

# UI
from Load.UI.Layouts.Layout_PWT_Output import create_dashboard_ui as create_output_ui
from Load.UI.Layouts.Layout_PWT_Labor import create_dashboard_ui as create_labor_ui
from Load.UI.Layouts.Layout_PWT_Productivity import create_dashboard_ui as create_productivity_ui
from Load.UI.Layouts.Layout_PWT_Capital import create_dashboard_ui as create_capital_ui

# Sidebar
from Load.UI.Sidebars.Sidebar_PWT import create_sidebar

# Servers
from Load.Server.Server_PWT_Output import create_dashboard_server as create_output_server
from Load.Server.Server_PWT_Productivity import create_dashboard_server as create_productivity_server
from Load.Server.Server_PWT_Capital import create_dashboard_server as create_capital_server
from Load.Server.Server_PWT_Labor import create_dashboard_server as create_labor_server
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
                    "Output", # Rgdpo
                    create_output_ui()
                ),
                ui.nav_panel(
                    "Productivity", # Total Factor Productivity
                    create_productivity_ui()
                ),
                ui.nav_panel(
                    "Capital", # rnna, capital share
                    create_capital_ui()
                ),
                ui.nav_panel(
                    "Labor", # Employment, Human Capital
                    create_labor_ui()
                ),
                id="main_tabs"
            )
        )
    )

def create_dashboard_server(cleaned_data=None):
    def server(input, output, session):
        # Initialize filters server and get reactive filtered data
        filters_server = create_filters_server(cleaned_data)(input, output, session)
        filtered_data = filters_server['filtered_data']
        
        # Pass filtered data to dashboard servers
        create_output_server(filtered_data)(input, output, session)
        create_productivity_server(filtered_data)(input, output, session)
        create_capital_server(filtered_data)(input, output, session)
        create_labor_server(filtered_data)(input, output, session)
    
    return server