from shiny import ui
from Load.UI.Components.Cards.Card_test import DashboardCards
from Load.UI.Components.Rows.Rows_test import DashboardRows

def create_gdp_analysis_ui():
    return ui.div(
        # GDP-focused stats
        DashboardRows.row_2(
            DashboardCards.card_stat_ui("gdp_stats_1"),
            DashboardCards.card_stat_ui("gdp_stats_2"),
            DashboardCards.card_stat_ui("gdp_stats_3"),
            DashboardCards.card_stat_ui("gdp_stats_4")
        ),
        
        # Detailed GDP charts
        DashboardRows.row_6(
            DashboardCards.card_graph("gdp_distribution_chart"),
            DashboardCards.card_graph("gdp_correlation_chart")
        ),
        
        # GDP trends and comparisons
        DashboardRows.row_4(
            DashboardCards.card_graph("gdp_regional_trends"),
            DashboardCards.card_graph("gdp_growth_analysis")
        ),
        
        class_="dashboard-container"
    )