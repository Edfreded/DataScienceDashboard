from shiny import ui

class DashboardRows:

    @staticmethod
    def row_standard(*cards, css_class="card-grid"):
        return ui.div(*cards, class_=css_class)