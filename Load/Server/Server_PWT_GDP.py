from shiny import ui, render, reactive
import plotly.express as px
import plotly.graph_objects as go
from shinywidgets import render_widget

def create_gdp_analysis_server(cleaned_data=None, summary_stats=None):
    def server(input, output, session):
        
        # Reactive data loading
        @reactive.calc
        def get_cleaned_data():
            return cleaned_data
        
        @reactive.calc
        def get_latest_year_data():
            data = get_cleaned_data()
            if data is None or len(data) == 0:
                return None
            latest_year = data['year'].max()
            return data[data['year'] == latest_year]

        # GDP Analysis Stats
        @output
        @render.ui
        def gdp_stats_1():
            data = get_cleaned_data()
            if data is None:
                return ui.div("No data", class_="card-value")
            
            max_gdp = data['gdp_per_capita'].max()
            return ui.div(
                ui.div(f"${max_gdp:,.0f}", class_="card-value"),
                ui.div("Highest GDP", class_="card-label")
            )
        
        @output
        @render.ui
        def gdp_stats_2():
            data = get_cleaned_data()
            if data is None:
                return ui.div("No data", class_="card-value")
            
            min_gdp = data['gdp_per_capita'].min()
            return ui.div(
                ui.div(f"${min_gdp:,.0f}", class_="card-value"),
                ui.div("Lowest GDP", class_="card-label")
            )
        
        @output
        @render.ui
        def gdp_stats_3():
            data = get_cleaned_data()
            if data is None:
                return ui.div("No data", class_="card-value")
            
            median_gdp = data['gdp_per_capita'].median()
            return ui.div(
                ui.div(f"${median_gdp:,.0f}", class_="card-value"),
                ui.div("Median GDP", class_="card-label")
            )
        
        @output
        @render.ui
        def gdp_stats_4():
            data = get_cleaned_data()
            if data is None:
                return ui.div("No data", class_="card-value")
            
            std_gdp = data['gdp_per_capita'].std()
            return ui.div(
                ui.div(f"${std_gdp:,.0f}", class_="card-value"),
                ui.div("GDP Std Dev", class_="card-label")
            )

        @output
        @render_widget
        def gdp_distribution_chart():
            data = get_cleaned_data()
            if data is None or len(data) == 0:
                fig = go.Figure().add_annotation(text="No data available")
                return fig
            
            latest_data = get_latest_year_data()
            
            fig = px.histogram(
                latest_data,
                x='gdp_per_capita',
                nbins=30,
                title="GDP per Capita Distribution",
                labels={'gdp_per_capita': 'GDP per Capita ($)', 'count': 'Number of Countries'}
            )
            
            fig.update_layout(
                margin=dict(l=50, r=50, t=60, b=50),
                autosize=True
            )
            
            return fig

        @output
        @render_widget
        def gdp_correlation_chart():
            data = get_cleaned_data()
            if data is None or len(data) == 0:
                fig = go.Figure().add_annotation(text="No data available")
                return fig
            
            latest_data = get_latest_year_data()
            
            fig = px.scatter(
                latest_data,
                x='hc',
                y='gdp_per_capita',
                hover_name='country',
                title="GDP vs Human Capital",
                labels={'hc': 'Human Capital Index', 'gdp_per_capita': 'GDP per Capita ($)'}
            )
            
            fig.update_layout(
                margin=dict(l=50, r=50, t=60, b=50),
                autosize=True
            )
            
            return fig

        @output
        @render_widget
        def gdp_regional_trends():
            fig = go.Figure().add_annotation(
                text="Regional GDP Trends<br>(Placeholder)",
                font=dict(size=16)
            )
            fig.update_layout(
                title="GDP Regional Analysis",
                margin=dict(l=50, r=50, t=60, b=50),
                autosize=True
            )
            return fig

        @output
        @render_widget
        def gdp_growth_analysis():
            fig = go.Figure().add_annotation(
                text="GDP Growth Analysis<br>(Placeholder)",
                font=dict(size=16)
            )
            fig.update_layout(
                title="GDP Growth Patterns",
                margin=dict(l=50, r=50, t=60, b=50),
                autosize=True
            )
            return fig
    
    return server