from shiny import ui
from shinywidgets import output_widget
from Load.UI.Components.Cards.Card_test_2 import DashboardCards
from Load.UI.Components.Rows.Rows_test_2 import DashboardRows
from Load.UI.Components.Rows.Rows_test_2 import DashboardContainers

def create_dashboard_ui(css_file=None):

    # CSS setup
    head_elements = []
    css_to_use = css_file or 'css/default_theme.css'
    head_elements.append(ui.tags.link(rel="stylesheet", href=css_to_use))
    

    
    return ui.page_fluid(
        ui.tags.head(*head_elements),
        ui.div(
            DashboardRows.row_2(
                DashboardCards.card_stat_ui("total_cars_card"),
                DashboardCards.card_stat_ui("avg_price_card"),
                DashboardCards.card_stat_ui("fuel_types_card"),
                DashboardCards.card_stat_ui("locations_card"),
            ),

            DashboardRows.row_4(
                DashboardContainers.horizontal_2_1(
                    DashboardCards.card_graph("fuel_chart"),
                    DashboardCards.card_graph("location_chart")
                )
            ),

            DashboardRows.row_6(
                DashboardCards.card_graph("year_trend_chart"),
                DashboardCards.card_graph("price_distribution_chart")
            ),
            
            class_="dashboard-container"
        )
    )