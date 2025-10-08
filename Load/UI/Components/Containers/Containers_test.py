from shiny import ui

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