from shiny import ui
from shinywidgets import output_widget
from Load.UI.Components.Cards.Card_test import DashboardCards
from Load.UI.Components.Rows.Rows_test import DashboardRows
from Load.UI.Components.Containers.Containers_test import DashboardContainers

def create_dashboard_ui():
    return ui.div(
        DashboardRows.row_6(
            DashboardCards.card_stat_ui("1"),
            DashboardCards.card_stat_ui("2"),
            DashboardCards.card_stat_ui("3"),
        ),
        DashboardRows.row_6(
            DashboardCards.card_stat_ui("4"),
            DashboardCards.card_stat_ui("5"),
            DashboardCards.card_stat_ui("6"),
        ),
        class_="dashboard-container"
    )