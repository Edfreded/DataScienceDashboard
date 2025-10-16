from shiny import ui
from Load.UI.Components.Cards.Card_test import DashboardCards
from Load.UI.Components.Rows.Rows_test import DashboardRows

def create_data_explorer_ui():
    return ui.div(
        # Data exploration tools
        DashboardRows.row_4(
            DashboardCards.card_graph("data_table"),
            DashboardCards.card_graph("country_selector"),
            DashboardCards.card_graph("year_range_selector")
        ),
        
        # Interactive data visualization
        DashboardRows.row_6(
            DashboardCards.card_graph("interactive_scatter"),
        ),
        
        class_="dashboard-container"
    )