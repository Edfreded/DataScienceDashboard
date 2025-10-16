from shiny import ui, render, reactive
import plotly.express as px
import plotly.graph_objects as go
from shinywidgets import render_widget

def create_data_explorer_server(cleaned_data=None, summary_stats=None):
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

        @output
        @render_widget
        def data_table():
            fig = go.Figure().add_annotation(
                text="Data Table<br>(Placeholder)",
                font=dict(size=16)
            )
            fig.update_layout(
                title="Raw Data View",
                margin=dict(l=50, r=50, t=60, b=50),
                autosize=True
            )
            return fig

        @output
        @render_widget
        def country_selector():
            fig = go.Figure().add_annotation(
                text="Country Selector<br>(Placeholder)",
                font=dict(size=16)
            )
            fig.update_layout(
                title="Country Filter",
                margin=dict(l=50, r=50, t=60, b=50),
                autosize=True
            )
            return fig

        @output
        @render_widget
        def year_range_selector():
            fig = go.Figure().add_annotation(
                text="Year Range Selector<br>(Placeholder)",
                font=dict(size=16)
            )
            fig.update_layout(
                title="Time Period Filter",
                margin=dict(l=50, r=50, t=60, b=50),
                autosize=True
            )
            return fig

        @output
        @render_widget
        def interactive_scatter():
            data = get_cleaned_data()
            if data is None or len(data) == 0:
                fig = go.Figure().add_annotation(text="No data available")
                return fig
            
            latest_data = get_latest_year_data()
            
            fig = px.scatter(
                latest_data,
                x='csh_i',
                y='gdp_per_capita',
                size='pop',
                hover_name='country',
                title="Interactive Data Explorer",
                labels={
                    'csh_i': 'Investment Share (%)',
                    'gdp_per_capita': 'GDP per Capita ($)',
                    'pop': 'Population'
                }
            )
            
            fig.update_layout(
                margin=dict(l=50, r=50, t=60, b=50),
                autosize=True
            )
            
            return fig
    
    return server