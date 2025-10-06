from shiny import ui

class DashboardCards:
    """Generic card components for dashboard elements"""
    
    @staticmethod
    def stat_card(content, css_class="stat-card"):
        """Standard stat card - holds numbers, metrics, KPIs"""
        return ui.div(content, class_=css_class)
    
    @staticmethod
    def chart_card(content, css_class="chart-card"):
        """Standard chart card - holds plots, graphs, visualizations"""
        return ui.div(content, class_=css_class)
    
    @staticmethod
    def info_card(content, css_class="info-card"):
        """Info card - holds text, descriptions, alerts"""
        return ui.div(content, class_=css_class)
    
    @staticmethod
    def control_card(content, css_class="control-card"):
        """Control card - holds filters, inputs, buttons"""
        return ui.div(content, class_=css_class)
    
    @staticmethod
    def full_width_card(content, css_class="chart-card chart-full-width"):
        """Full width card - spans entire row width"""
        return ui.div(content, class_=css_class)
    
    @staticmethod
    def custom_card(content, css_class="custom-card"):
        """Custom card with user-defined styling"""
        return ui.div(content, class_=css_class)

# Card size variants
class CardSizes:
    """Predefined card size classes"""
    SMALL = "card-small"
    MEDIUM = "card-medium" 
    LARGE = "card-large"
    FULL_WIDTH = "card-full-width"
    SQUARE = "card-square"
    TALL = "card-tall"