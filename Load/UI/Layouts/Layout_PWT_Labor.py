from shiny import ui
from shinywidgets import output_widget
from Load.UI.Components.Cards.Card_test import DashboardCards
from Load.UI.Components.Rows.Rows_test import DashboardRows
from Load.UI.Components.Containers.Containers_test import DashboardContainers

def create_dashboard_ui():
    return ui.div(
        DashboardRows.row_6(
            DashboardCards.card_graph("labor_hc_returns_chart"),
            DashboardCards.card_graph("labor_share_decline"),
        ),
        DashboardRows.row_6(
            DashboardCards.card_graph("labor_emp_hc_correlation"),
            DashboardCards.card_graph("labor_effective_productivity"),
        ),
        class_="dashboard-container"
    )