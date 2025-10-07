from shiny import ui, render, reactive
import plotly.express as px
import plotly.graph_objects as go
from shinywidgets import render_widget
import pandas as pd
from Extract.Extract_Test import extract_car_data
from Transform.Transform_Test import clean_and_transform_data, create_summary_stats

def create_dashboard_server():
    def server(input, output, session):
        # Reactive data loading
        @reactive.calc
        def get_data():
            print("Loading data...")
            raw_data = extract_car_data()
            if raw_data.empty:
                return None, None
            
            cleaned_data = clean_and_transform_data(raw_data)
            summary_stats = create_summary_stats(cleaned_data)
            return cleaned_data, summary_stats
        
        
        # Stat Cards (using raw data - no filtering)
        @output
        @render.ui
        def total_cars_card():
            _, stats = get_data()
            if stats is None:
                return ui.div("No data", class_="card-value")
            
            return ui.div(
                ui.div(f"{stats['total_cars']:,}", class_="card-value"),
                ui.div("Total Cars", class_="card-label")
            )
        
        @output
        @render.ui
        def avg_price_card():
            _, stats = get_data()
            if stats is None:
                return ui.div("No data", class_="card-value")
            
            return ui.div(
                ui.div(f"₹{stats['avg_price']:.1f}L", class_="card-value"),
                ui.div("Average Price", class_="card-label")
            )
        
        @output
        @render.ui
        def fuel_types_card():
            _, stats = get_data()
            if stats is None:
                return ui.div("No data", class_="card-value")
            
            fuel_count = len(stats.get('price_by_fuel', {}))
            return ui.div(
                ui.div(str(fuel_count), class_="card-value"),
                ui.div("Fuel Types", class_="card-label")
            )
        
        @output
        @render.ui
        def locations_card():
            _, stats = get_data()
            if stats is None:
                return ui.div("No data", class_="card-value")
            
            location_count = len(stats.get('cars_by_location', {}))
            return ui.div(
                ui.div(str(location_count), class_="card-value"),
                ui.div("Locations", class_="card-label")
            )

        # Charts
        @output
        @render_widget
        def fuel_chart():
            _, stats = get_data()
            if stats is None:
                fig = go.Figure().add_annotation(text="No data available")
                fig.update_layout(height=400)
                return fig
            
            fuel_data = stats.get('price_by_fuel', {})
            if not fuel_data:
                fig = go.Figure().add_annotation(text="No fuel data available")
                fig.update_layout(height=400)
                return fig
            
            fig = px.bar(
                x=list(fuel_data.keys()),
                y=list(fuel_data.values()),
                title="Average Price by Fuel Type",
                labels={'x': 'Fuel Type', 'y': 'Average Price (Lakhs)'}
            )
            fig.update_layout(
                height=400,
                showlegend=False,
                hovermode='x unified',
                margin=dict(l=50, r=50, t=60, b=50),
                autosize=True
            )
            fig.update_traces(
                hovertemplate='<b>%{x}</b><br>Avg Price: ₹%{y:.1f}L<extra></extra>'
            )
            return fig
        
        @output
        @render_widget
        def location_chart():
            _, stats = get_data()
            if stats is None:
                fig = go.Figure().add_annotation(text="No data available")
                fig.update_layout(height=400)
                return fig
            
            location_data = stats.get('cars_by_location', {})
            if not location_data:
                fig = go.Figure().add_annotation(text="No location data available")
                fig.update_layout(height=400)
                return fig
            
            fig = px.pie(
                values=list(location_data.values()),
                names=list(location_data.keys()),
                title="Cars by Location"
            )
            fig.update_layout(
                height=400,
                margin=dict(l=50, r=50, t=60, b=50),
                autosize=True
            )
            fig.update_traces(
                hovertemplate='<b>%{label}</b><br>Cars: %{value}<br>Percentage: %{percent}<extra></extra>'
            )
            return fig
    
    return server