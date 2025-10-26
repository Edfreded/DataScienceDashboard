from shiny import ui
from shinywidgets import output_widget
from Load.UI.Components.Cards.Card_test import DashboardCards
from Load.UI.Components.Rows.Rows_test import DashboardRows
from Load.UI.Components.Containers.Containers_test import DashboardContainers

def create_dashboard_ui():
    return ui.div(
        DashboardRows.row_6(
            DashboardCards.card_map("labor_world_hc_map"),
            DashboardCards.card_map("labor_employment_rate_map"),
            DashboardCards.card_graph("labor_hc_gdp_scatter")
        ),
        DashboardRows.row_6(
            DashboardCards.card_graph("labor_hc_trend_chart"),
            DashboardCards.card_graph("labor_share_trend"),
            DashboardCards.card_graph("labor_dependency_ratio_chart")
        ),
        class_="dashboard-container"
    )