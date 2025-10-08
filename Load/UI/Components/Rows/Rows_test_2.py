from shiny import ui

class DashboardRows:

    @staticmethod
    def row_1(*cards, css_class="card-grid-1"):
        return ui.div(*cards, class_=css_class)
    
    @staticmethod
    def row_2(*cards, css_class="card-grid-2"):
        return ui.div(*cards, class_=css_class)
    
    @staticmethod
    def row_3(*cards, css_class="card-grid-3"):
        return ui.div(*cards, class_=css_class)

    @staticmethod
    def row_4(*cards, css_class="card-grid-4"):
        return ui.div(*cards, class_=css_class)
    
    @staticmethod
    def row_6(*cards, css_class="card-grid-6"):
        return ui.div(*cards, class_=css_class)
    
    @staticmethod
    def row_8(*cards, css_class="card-grid-8"):
        return ui.div(*cards, class_=css_class)

    @staticmethod
    def row_10(*cards, css_class="card-grid-10"):
        return ui.div(*cards, class_=css_class)

    @staticmethod
    def row_12(*cards, css_class="card-grid-12"):
        return ui.div(*cards, class_=css_class)

    

class DashboardContainers:
    
    @staticmethod
    def horizontal(*sections):
        return ui.div(*sections, class_="container-horizontal")
    
    @staticmethod
    def vertical(*sections):
        return ui.div(*sections, class_="container-vertical")
    
    @staticmethod
    def horizontal_1_2(*sections):
        return ui.div(*sections, class_="container-horizontal-1-2")
    
    @staticmethod
    def horizontal_2_1(*sections):
        return ui.div(*sections, class_="container-horizontal-2-1")