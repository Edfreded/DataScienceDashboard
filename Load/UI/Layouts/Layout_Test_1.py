from shiny import ui
from shinywidgets import output_widget
from Load.UI.Components.Cards.Card_test import DashboardCards
from Load.UI.Components.Rows.Rows_test import DashboardRows

def create_dashboard_ui(css_file=None):
    """Create the main dashboard UI using component hierarchy"""
    
    # CSS setup
    head_elements = []
    css_to_use = css_file or 'css/default_theme.css'
    head_elements.append(ui.tags.link(rel="stylesheet", href=css_to_use))
    
    # JavaScript for Plotly (keeping your existing JS)
    plotly_js = ui.tags.script("""
        // Force Plotly charts to resize properly with anti-flicker
        function resizePlotlyCharts() {
            var plots = document.querySelectorAll('.js-plotly-plot');
            plots.forEach(function(plot) {
                if (window.Plotly && plot._fullLayout) {
                    plot.style.opacity = '0';
                    window.Plotly.Plots.resize(plot).then(function() {
                        plot.setAttribute('data-resized', 'true');
                        plot.style.opacity = '1';
                    }).catch(function() {
                        plot.setAttribute('data-resized', 'true');
                        plot.style.opacity = '1';
                    });
                } else if (plot) {
                    setTimeout(function() {
                        if (window.Plotly && plot._fullLayout) {
                            window.Plotly.Plots.resize(plot).then(function() {
                                plot.setAttribute('data-resized', 'true');
                                plot.style.opacity = '1';
                            });
                        } else {
                            plot.setAttribute('data-resized', 'true');
                            plot.style.opacity = '1';
                        }
                    }, 50);
                }
            });
        }
        
        window.addEventListener('resize', function() {
            setTimeout(resizePlotlyCharts, 10);
        });
        
        var observer = new MutationObserver(function(mutations) {
            var hasPlotChanges = false;
            mutations.forEach(function(mutation) {
                if (mutation.type === 'childList') {
                    mutation.addedNodes.forEach(function(node) {
                        if (node.nodeType === 1 && 
                            (node.classList.contains('js-plotly-plot') || 
                             node.querySelector('.js-plotly-plot'))) {
                            hasPlotChanges = true;
                        }
                    });
                }
            });
            
            if (hasPlotChanges) {
                setTimeout(resizePlotlyCharts, 20);
            }
        });
        
        document.addEventListener('DOMContentLoaded', function() {
            observer.observe(document.body, {
                childList: true,
                subtree: true
            });
            setTimeout(resizePlotlyCharts, 100);
        });
    """)
    
    return ui.page_fluid(
        ui.tags.head(*head_elements, plotly_js),
        ui.div(
            ui.h1("Car Sales Dashboard", class_="dashboard-title"),
            
            # Controls section (keeping as is since styling is done)
            create_controls_section(),
            
            # Stats row - 4 stat cards
            DashboardRows.stats_row(
                DashboardCards.stat_card(ui.output_ui("total_cars_card")),
                DashboardCards.stat_card(ui.output_ui("avg_price_card")),
                DashboardCards.stat_card(ui.output_ui("fuel_types_card")),
                DashboardCards.stat_card(ui.output_ui("locations_card"))
            ),
            
            # Charts row - 2 charts side by side
            DashboardRows.two_card_row(
                DashboardCards.chart_card(output_widget("fuel_chart")),
                DashboardCards.chart_card(output_widget("location_chart"))
            ),
            
            # Full width charts - each in their own row
            DashboardRows.charts_row(
                DashboardCards.full_width_card(output_widget("year_trend_chart")),
                DashboardCards.full_width_card(output_widget("price_distribution_chart"))
            ),
            
            class_="dashboard-container"
        )
    )

def create_controls_section():
    """Controls section with built-in styling"""
    return ui.div(
        ui.h3("Filters & Controls", style="color: var(--text-accent); margin-bottom: var(--spacing-md);"),
        ui.div(
            ui.div(
                ui.div("Price Range (Lakhs)", class_="control-label"),
                ui.input_slider("price_range", "", min=0, max=100, value=[0, 50], step=1),
                class_="control-group"
            ),
            ui.div(
                ui.div("Fuel Type", class_="control-label"),
                ui.input_selectize("fuel_filter", "", choices=[], multiple=True),
                class_="control-group"
            ),
            ui.div(
                ui.div("Location", class_="control-label"),
                ui.input_selectize("location_filter", "", choices=[], multiple=True),
                class_="control-group"
            ),
            ui.div(
                ui.div("Year Range", class_="control-label"),
                ui.input_slider("year_range", "", min=2000, max=2024, value=[2010, 2024], step=1),
                class_="control-group"
            ),
            class_="controls-grid"
        ),
        class_="controls-section"
    )