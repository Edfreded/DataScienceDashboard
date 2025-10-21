from shiny import ui, reactive
from Load.UI.Layouts.Layout_PWT_Overview import create_dashboard_ui as create_overview_ui
from Load.UI.Layouts.Layout_PWT_GDP import create_gdp_analysis_ui
from Load.UI.Layouts.Layout_PWT_Economic import create_economic_indicators_ui
from Load.UI.Layouts.Layout_PWT_Explorer import create_data_explorer_ui

from Load.Server.Server_PWT_Overview import create_dashboard_server as create_overview_server
from Load.Server.Server_PWT_GDP import create_gdp_analysis_server
from Load.Server.Server_PWT_Economic import create_economic_indicators_server
from Load.Server.Server_PWT_Explorer import create_data_explorer_server

def create_dashboard_ui(css_file=None):
    head_elements = []
    css_to_use = css_file or 'css/default_theme.css'
    head_elements.append(ui.tags.link(rel="stylesheet", href=css_to_use))
    
    return ui.page_fluid(
        ui.tags.head(
            *head_elements,
            ui.tags.script("""
                Shiny.addCustomMessageHandler('toggle_sidebar', function(message) {
                    const sidebar = document.getElementById(message.target);
                    if (sidebar.style.display === 'none' || sidebar.style.display === '') {
                        sidebar.style.display = 'block';
                    } else {
                        sidebar.style.display = 'none';
                    }
                });
            """)
        ),
        
        # Single sidebar button positioned outside navset_tab
        ui.div(
            ui.input_action_button(
                "sidebar_toggle", 
                "☰", 
                class_="custom-sidebar-btn"
            ),
            class_="floating-sidebar-btn"
        ),
        
        # Navbar with content panels
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
        ),
        
        # Collapsible sidebar content
        ui.div(
            ui.div(
                ui.h4("Navigation", style="color: var(--text-accent); margin-bottom: 1rem;"),
                ui.hr(style="border-color: var(--border-color);"),
                ui.p("Dashboard Controls", style="color: var(--text-secondary); font-size: 0.9rem;"),
                ui.input_selectize("theme_selector", "Theme:", choices=["retro", "dark", "light"]),
                ui.input_checkbox("show_grid", "Show Grid Lines", value=True),
                # Add more sidebar content here
            ),
            id="custom_sidebar",
            class_="custom-sidebar-content",
            style="display: none;"
        )
    )

def create_dashboard_server(cleaned_data=None, summary_stats=None):
    def server(input, output, session):
        # Sidebar toggle functionality
        @reactive.effect
        @reactive.event(input.sidebar_toggle)
        def toggle_sidebar():
            session.send_custom_message(
                "toggle_sidebar", 
                {"target": "custom_sidebar"}
            )
        
        create_overview_server(cleaned_data, summary_stats)(input, output, session)
        create_gdp_analysis_server(cleaned_data, summary_stats)(input, output, session)
        create_economic_indicators_server(cleaned_data, summary_stats)(input, output, session)
        create_data_explorer_server(cleaned_data, summary_stats)(input, output, session)
    
    return server