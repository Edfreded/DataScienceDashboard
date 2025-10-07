from shiny import ui

class DashboardCards:
    """Generic card components for dashboard elements"""
    
    @staticmethod
    def card(content, css_class="card"):
        return ui.div(content, class_=css_class)

    @staticmethod
    def card_stat(content, css_class="card-stat"):
        return ui.div(content, class_=css_class)

    @staticmethod
    def card_graph(content, css_class="card-graph"):
        return ui.div(content, class_=css_class)