from shiny import ui
from shinywidgets import output_widget
from Load.UI.Components.Cards.Card_test import DashboardCards
from Load.UI.Components.Rows.Rows_test import DashboardRows
from Load.UI.Components.Containers.Containers_test import DashboardContainers

def create_dashboard_ui(css_file=None):

    # CSS setup
    head_elements = []
    css_to_use = css_file or 'css/default_theme.css'
    head_elements.append(ui.tags.link(rel="stylesheet", href=css_to_use))
    
    return ui.page_fluid(
        ui.tags.head(*head_elements),
        ui.div(
            # Stats Cards Row
            DashboardRows.row_2(
                DashboardCards.card_stat_ui("total_countries_card"),
                DashboardCards.card_stat_ui("latest_year_card"),
                DashboardCards.card_stat_ui("avg_gdp_card"),
                DashboardCards.card_stat_ui("top_country_card")
            ),
            
            # World Maps Row
            DashboardRows.row_6(
                DashboardCards.card_map("world_gdp_map"),
                DashboardCards.card_map("world_growth_map")                
            ),
            
            # Charts Row
            DashboardRows.row_4(
                DashboardCards.card_graph("top_countries_chart"),
                DashboardCards.card_graph("gdp_trend_chart")
            ),
            
            class_="dashboard-container"
        )
    )