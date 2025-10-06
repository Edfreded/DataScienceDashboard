from shiny import ui

class DashboardRows:
    """Row components that hold multiple cards with consistent layouts"""
    
    @staticmethod
    def two_card_row(*cards, css_class="row-2-cards"):
        """Row with 2 cards side by side (50% each)"""
        return ui.div(*cards, class_=css_class)
    
    @staticmethod
    def three_card_row(*cards, css_class="row-3-cards"):
        """Row with 3 cards side by side (33% each)"""
        return ui.div(*cards, class_=css_class)
    
    @staticmethod
    def four_card_row(*cards, css_class="row-4-cards"):
        """Row with 4 cards side by side (25% each)"""
        return ui.div(*cards, class_=css_class)
    
    @staticmethod
    def five_card_row(*cards, css_class="row-5-cards"):
        """Row with 5 cards side by side (20% each)"""
        return ui.div(*cards, class_=css_class)
    
    @staticmethod
    def stats_row(*cards, css_class="stats-grid"):
        """Special row for stat cards - responsive grid"""
        return ui.div(*cards, class_=css_class)
    
    @staticmethod
    def charts_row(*cards, css_class="charts-grid"):
        """Special row for chart cards - responsive grid"""
        return ui.div(*cards, class_=css_class)