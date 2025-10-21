from shiny import ui, reactive
from Load.UI.Layouts.Layout_PWT_Overview import create_dashboard_ui as create_overview_ui
from Load.UI.Layouts.Layout_PWT_GDP import create_gdp_analysis_ui
from Load.UI.Layouts.Layout_PWT_Economic import create_economic_indicators_ui
from Load.UI.Layouts.Layout_PWT_Explorer import create_data_explorer_ui

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
        ui.sidebar(
            ui.h4("Dashboard Controls", style="color: var(--text-accent); margin-bottom: 1rem; text-align: center;"),
            ui.hr(style="border-color: var(--border-color); margin: 1rem 0;"),
            
            # Theme Selection
            ui.div(
                ui.h6("Appearance", style="color: var(--text-secondary); margin-bottom: 0.5rem;"),
                ui.input_selectize(
                    "theme_selector", 
                    "Theme:", 
                    choices={
                        "retro": "Retro",
                        "dark": "Dark", 
                        "light": "Light",
                        "dark_blue": "Dark Blue"
                    },
                    selected="retro"
                ),
                ui.input_checkbox("show_grid", "Show Grid Lines", value=True),
                style="margin-bottom: 1.5rem;"
            ),
            
            # Data Filters
            ui.div(
                ui.h6("Data Filters", style="color: var(--text-secondary); margin-bottom: 0.5rem;"),
                ui.input_slider(
                    "year_range", 
                    "Year Range:", 
                    min=1950, 
                    max=2019, 
                    value=[2000, 2019],
                    step=1
                ),
                ui.input_selectize(
                    "region_filter",
                    "Region:",
                    choices={
                        "all": "All Regions",
                        "europe": "Europe",
                        "asia": "Asia", 
                        "americas": "Americas",
                        "africa": "Africa",
                        "oceania": "Oceania"
                    },
                    selected="all"
                ),
                style="margin-bottom: 1.5rem;"
            ),
            
            # Quick Stats
            ui.div(
                ui.h6("Quick Info", style="color: var(--text-secondary); margin-bottom: 0.5rem;"),
                ui.p("Use the controls above to customize your dashboard view.", 
                     style="color: var(--text-primary); font-size: 0.85rem; line-height: 1.4;"),
                ui.p("Switch between tabs to explore different economic indicators.", 
                     style="color: var(--text-primary); font-size: 0.85rem; line-height: 1.4;"),
            ),
            bg="transparent",
            open="closed",
            width="300px"
        ),
        
        # Main content with navbar and panels
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