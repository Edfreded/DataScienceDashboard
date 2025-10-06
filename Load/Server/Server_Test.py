from shiny import ui, render, reactive
import plotly.express as px
import plotly.graph_objects as go
from shinywidgets import render_widget
import pandas as pd
from Extract.Extract_Test import extract_car_data
from Transform.Transform_Test import clean_and_transform_data, create_summary_stats

def create_dashboard_server():
    """Create the server logic for the dashboard"""
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
        
        # Initialize filter choices
        @reactive.effect
        def update_filter_choices():
            data, _ = get_data()
            if data is not None:
                # Update fuel type choices
                fuel_types = sorted(data['Fuel_Type'].unique()) if 'Fuel_Type' in data.columns else []
                ui.update_selectize("fuel_filter", choices=fuel_types, selected=fuel_types)
                
                # Update location choices
                locations = sorted(data['Location'].unique()) if 'Location' in data.columns else []
                ui.update_selectize("location_filter", choices=locations, selected=locations)
                
                # Update price range
                if 'Price' in data.columns:
                    min_price = int(data['Price'].min())
                    max_price = int(data['Price'].max())
                    ui.update_slider("price_range", min=min_price, max=max_price, value=[min_price, max_price])
                
                # Update year range
                if 'Year' in data.columns:
                    min_year = int(data['Year'].min())
                    max_year = int(data['Year'].max())
                    ui.update_slider("year_range", min=min_year, max=max_year, value=[min_year, max_year])
        
        # Filtered data based on user inputs
        @reactive.calc
        def get_filtered_data():
            data, stats = get_data()
            if data is None:
                return None, None
            
            filtered_data = data.copy()
            
            # Apply filters with proper column names
            if input.fuel_filter() and 'Fuel_Type' in filtered_data.columns:
                filtered_data = filtered_data[filtered_data['Fuel_Type'].isin(input.fuel_filter())]
            
            if input.location_filter() and 'Location' in filtered_data.columns:
                filtered_data = filtered_data[filtered_data['Location'].isin(input.location_filter())]
            
            if input.price_range() and 'Price' in filtered_data.columns:
                min_price, max_price = input.price_range()
                filtered_data = filtered_data[
                    (filtered_data['Price'] >= min_price) & 
                    (filtered_data['Price'] <= max_price)
                ]
            
            if input.year_range() and 'Year' in filtered_data.columns:
                min_year, max_year = input.year_range()
                filtered_data = filtered_data[
                    (filtered_data['Year'] >= min_year) & 
                    (filtered_data['Year'] <= max_year)
                ]
            
            # Recalculate stats for filtered data
            filtered_stats = create_summary_stats(filtered_data)
            return filtered_data, filtered_stats
        
        # Stat Cards (using filtered data)
        @output
        @render.ui
        def total_cars_card():
            _, stats = get_filtered_data()
            if stats is None:
                return ui.div("No data", class_="stat-value")
            
            return ui.div(
                ui.div(f"{stats['total_cars']:,}", class_="stat-value"),
                ui.div("Total Cars", class_="stat-label")
            )
        
        @output
        @render.ui
        def avg_price_card():
            _, stats = get_filtered_data()
            if stats is None:
                return ui.div("No data", class_="stat-value")
            
            return ui.div(
                ui.div(f"₹{stats['avg_price']:.1f}L", class_="stat-value"),
                ui.div("Average Price", class_="stat-label")
            )
        
        @output
        @render.ui
        def fuel_types_card():
            _, stats = get_filtered_data()
            if stats is None:
                return ui.div("No data", class_="stat-value")
            
            fuel_count = len(stats.get('price_by_fuel', {}))
            return ui.div(
                ui.div(str(fuel_count), class_="stat-value"),
                ui.div("Fuel Types", class_="stat-label")
            )
        
        @output
        @render.ui
        def locations_card():
            _, stats = get_filtered_data()
            if stats is None:
                return ui.div("No data", class_="stat-value")
            
            location_count = len(stats.get('cars_by_location', {}))
            return ui.div(
                ui.div(str(location_count), class_="stat-value"),
                ui.div("Locations", class_="stat-label")
            )
        
        # Enhanced Plotly Charts using filtered data
        @output
        @render_widget
        def fuel_chart():
            _, stats = get_filtered_data()
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
            _, stats = get_filtered_data()
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
        
        @output
        @render_widget
        def year_trend_chart():
            _, stats = get_filtered_data()
            if stats is None:
                fig = go.Figure().add_annotation(text="No data available")
                fig.update_layout(height=400)
                return fig
            
            year_data = stats.get('cars_by_year', {})
            if not year_data:
                fig = go.Figure().add_annotation(text="No year data available")
                fig.update_layout(height=400)
                return fig
            
            sorted_years = sorted(year_data.items())
            fig = px.line(
                x=[year for year, count in sorted_years],
                y=[count for year, count in sorted_years],
                title="Number of Cars by Year",
                labels={'x': 'Year', 'y': 'Number of Cars'},
                markers=True
            )
            fig.update_layout(
                height=400,
                hovermode='x unified',
                margin=dict(l=50, r=50, t=60, b=50),
                autosize=True
            )
            fig.update_traces(
                hovertemplate='<b>Year %{x}</b><br>Cars: %{y}<extra></extra>',
                line=dict(width=3),
                marker=dict(size=8)
            )
            return fig
        
        @output
        @render_widget
        def price_distribution_chart():
            data, _ = get_filtered_data()
            if data is None:
                fig = go.Figure().add_annotation(text="No data available")
                fig.update_layout(height=400)
                return fig
            
            if 'Price' not in data.columns:
                fig = go.Figure().add_annotation(text="No price data available")
                fig.update_layout(height=400)
                return fig
            
            fig = px.histogram(
                data,
                x='Price',
                nbins=30,
                title="Price Distribution",
                labels={'Price': 'Price (Lakhs)', 'count': 'Number of Cars'}
            )
            fig.update_layout(
                height=400,
                showlegend=False,
                bargap=0.1,
                margin=dict(l=50, r=50, t=60, b=50),
                autosize=True
            )
            fig.update_traces(
                hovertemplate='<b>Price Range</b><br>₹%{x:.1f}L<br>Cars: %{y}<extra></extra>'
            )
            return fig
    
    return server