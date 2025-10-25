from shiny import ui
from shinywidgets import output_widget
from Load.UI.Components.Cards.Card_test import DashboardCards
from Load.UI.Components.Rows.Rows_test import DashboardRows
from Load.UI.Components.Containers.Containers_test import DashboardContainers

def create_dashboard_ui():
    return ui.div(
        DashboardRows.row_6(
            DashboardCards.card_graph("data_table"),
            DashboardCards.card_graph("gdp_distribution_chart"),
            DashboardCards.card_graph("gdp_correlation_chart")
        ),
        DashboardRows.row_6(
            DashboardCards.card_map("world_gdp_map"),
            DashboardCards.card_graph("top_countries_chart"),
            DashboardCards.card_graph("gdp_trend_chart")
        ),
        class_="dashboard-container"
    )