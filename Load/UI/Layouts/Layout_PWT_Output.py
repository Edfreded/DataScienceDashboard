from shiny import ui
from shinywidgets import output_widget
from Load.UI.Components.Cards.Card_test import DashboardCards
from Load.UI.Components.Rows.Rows_test import DashboardRows
from Load.UI.Components.Containers.Containers_test import DashboardContainers

def create_dashboard_ui():
    return ui.div(
        DashboardRows.row_6(
            DashboardCards.card_map("output_world_gdp_map"),
            DashboardCards.card_map("output_world_growth_map"),
            DashboardCards.card_graph("output_top_countries_chart")
        ),
        DashboardRows.row_6(
            DashboardCards.card_graph("output_gdp_trend_chart"),
            DashboardCards.card_graph("output_gdp_population_scatter"),
            DashboardCards.card_graph("output_trade_gdp_scatter")
        ),
        class_="dashboard-container"
    )