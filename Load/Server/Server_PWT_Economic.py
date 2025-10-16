from shiny import ui, render, reactive
import plotly.graph_objects as go
from shinywidgets import render_widget

def create_economic_indicators_server(cleaned_data=None, summary_stats=None):
    def server(input, output, session):
        
        # Economic Indicators Stats
        @output
        @render.ui
        def investment_stat():
            return ui.div(
                ui.div("24.5%", class_="card-value"),
                ui.div("Avg Investment Share", class_="card-label")
            )
        
        @output
        @render.ui
        def trade_stat():
            return ui.div(
                ui.div("15.2%", class_="card-value"),
                ui.div("Avg Trade Balance", class_="card-label")
            )
        
        @output
        @render.ui
        def productivity_stat():
            return ui.div(
                ui.div("2.1%", class_="card-value"),
                ui.div("Productivity Growth", class_="card-label")
            )
        
        @output
        @render.ui
        def human_capital_stat():
            return ui.div(
                ui.div("2.8", class_="card-value"),
                ui.div("Avg Human Capital", class_="card-label")
            )

        @output
        @render_widget
        def investment_trends():
            fig = go.Figure().add_annotation(
                text="Investment Trends<br>(Placeholder)",
                font=dict(size=16)
            )
            fig.update_layout(
                title="Investment Share Analysis",
                margin=dict(l=50, r=50, t=60, b=50),
                autosize=True
            )
            return fig

        @output
        @render_widget
        def trade_balance_chart():
            fig = go.Figure().add_annotation(
                text="Trade Balance Analysis<br>(Placeholder)",
                font=dict(size=16)
            )
            fig.update_layout(
                title="Trade Balance Trends",
                margin=dict(l=50, r=50, t=60, b=50),
                autosize=True
            )
            return fig
    
    return server