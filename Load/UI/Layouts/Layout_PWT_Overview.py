from shiny import ui
from shinywidgets import output_widget
from Load.UI.Components.Cards.Card_test import DashboardCards
from Load.UI.Components.Rows.Rows_test import DashboardRows
from Load.UI.Components.Containers.Containers_test import DashboardContainers

def create_dashboard_ui():
    return ui.div(
        # Stats Cards Row
        DashboardRows.row_2(
            DashboardCards.card_stat_ui("total_countries_card"),
            DashboardCards.card_stat_ui("latest_year_card"),
            DashboardCards.card_stat_ui("avg_gdp_card"),
            DashboardCards.card_stat_ui("top_country_card")
        ),
        
        # World Maps Row
        DashboardRows.row_5(
            DashboardContainers.horizontal_2_1(
                DashboardCards.card_map("world_gdp_map"),
                DashboardCards.card_map("world_growth_map")    
            )            
        ),
        
        # Charts Row
        DashboardRows.row_5(
            DashboardCards.card_graph("top_countries_chart"),
            DashboardCards.card_graph("gdp_trend_chart")
        ),
        
        class_="dashboard-container"
    )