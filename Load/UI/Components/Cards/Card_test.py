from shiny import ui
from shinywidgets import output_widget

class DashboardCards:
    @staticmethod
    def card(content, css_class="card"):
        return ui.div(content, class_=css_class)
    
    @staticmethod
    def card_stat_ui(output_id, css_class="card-stat"):
        return ui.div(ui.output_ui(output_id), class_=css_class)
    
    @staticmethod
    def card_graph(widget_id, css_class="card-graph"):
        return ui.div(
            output_widget(widget_id, width="100%", height="100%"), 
            class_=css_class
        )