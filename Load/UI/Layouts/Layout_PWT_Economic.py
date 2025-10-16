from shiny import ui
from Load.UI.Components.Cards.Card_test import DashboardCards
from Load.UI.Components.Rows.Rows_test import DashboardRows

def create_economic_indicators_ui():
    return ui.div(
        # Economic indicator stats
        DashboardRows.row_2(
            DashboardCards.card_stat_ui("investment_stat"),
            DashboardCards.card_stat_ui("trade_stat"),
            DashboardCards.card_stat_ui("productivity_stat"),
            DashboardCards.card_stat_ui("human_capital_stat")
        ),
        
        # Economic indicator visualizations
        DashboardRows.row_8(
            DashboardCards.card_graph("investment_trends"),
            DashboardCards.card_graph("trade_balance_chart")
        ),
        
        class_="dashboard-container"
    )