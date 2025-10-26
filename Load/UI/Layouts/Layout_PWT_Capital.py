from shiny import ui
from shinywidgets import output_widget
from Load.UI.Components.Cards.Card_test import DashboardCards
from Load.UI.Components.Rows.Rows_test import DashboardRows
from Load.UI.Components.Containers.Containers_test import DashboardContainers

def create_dashboard_ui():
    return ui.div(
        DashboardRows.row_6(
            DashboardCards.card_graph("capital_output_ratio_chart"),
        ),
        DashboardRows.row_6(
            DashboardCards.card_graph("capital_net_investment_chart"),
        ),
        class_="dashboard-container"
    )