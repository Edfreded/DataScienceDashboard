from shiny import ui, reactive

def create_sidebar(): 

    return ui.sidebar(
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
                        value=[1950, 2019],
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
            )