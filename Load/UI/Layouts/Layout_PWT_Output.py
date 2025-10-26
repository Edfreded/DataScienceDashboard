from shiny import ui
from shinywidgets import output_widget
from Load.UI.Components.Cards.Card_test import DashboardCards
from Load.UI.Components.Rows.Rows_test import DashboardRows
from Load.UI.Components.Containers.Containers_test import DashboardContainers

def create_dashboard_ui():
    return ui.div(
        DashboardRows.row_6(
            DashboardCards.card_graph("output_levels_trend"),
        ),
        DashboardRows.row_6(
            DashboardCards.card_graph("output_growth_rates_trend"),
        ),
        class_="dashboard-container"
    )