from shiny import ui
from shinywidgets import output_widget
from Load.UI.Components.Cards.Card_test import DashboardCards
from Load.UI.Components.Rows.Rows_test import DashboardRows
from Load.UI.Components.Containers.Containers_test import DashboardContainers

def create_dashboard_ui():
    return ui.div(
        DashboardRows.row_6(
            DashboardCards.card_map("productivity_world_tfp_map"),
            DashboardCards.card_graph("productivity_tfp_growth_map"),
            DashboardCards.card_graph("productivity_tfp_gdp_scatter")
        ),
        DashboardRows.row_6(
            DashboardCards.card_graph("productivity_tfp_trend_chart"),
            DashboardCards.card_graph("productivity_tfp_relative_us"),
            DashboardCards.card_graph("productivity_hc_tfp_interaction")
        ),
        class_="dashboard-container"
    )