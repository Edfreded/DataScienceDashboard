from shiny import ui
from shinywidgets import output_widget
from Load.UI.Components.Cards.Card_test_2 import DashboardCards
from Load.UI.Components.Rows.Rows_test_2 import DashboardRows

def create_dashboard_ui(css_file=None):

    # CSS setup
    head_elements = []
    css_to_use = css_file or 'css/default_theme.css'
    head_elements.append(ui.tags.link(rel="stylesheet", href=css_to_use))
    

    
    return ui.page_fluid(
        ui.tags.head(*head_elements),
        ui.div(
            DashboardRows.row_standard(
                DashboardCards.card_stat(ui.output_ui("total_cars_card")),
                DashboardCards.card_stat(ui.output_ui("avg_price_card")),
                DashboardCards.card_stat(ui.output_ui("fuel_types_card")),
                DashboardCards.card_stat(ui.output_ui("locations_card")),
            ),
           
            DashboardRows.row_standard(
                DashboardCards.card(output_widget("fuel_chart")),
                DashboardCards.card(output_widget("location_chart"))
            ),
            
            class_="dashboard-container"
        )
    )