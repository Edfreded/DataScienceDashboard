from shiny import ui, render, reactive
import plotly.express as px
import plotly.graph_objects as go
from shinywidgets import output_widget, render_widget
from Extract.Extract_Test import extract_car_data
from Transform.Transform_Test import clean_and_transform_data, create_summary_stats

def create_dashboard_ui(css_file="retro_theme.css"):
    """Create the main dashboard UI"""
    return ui.page_fluid(
        ui.tags.head(
            ui.tags.link(rel="stylesheet", href=css_file)
        ),
        ui.div(
            ui.h1("Car Sales Dashboard", class_="dashboard-title"),
            
            # Stats Row
            ui.div(
                ui.div(ui.output_ui("total_cars_card"), class_="stat-card"),
                ui.div(ui.output_ui("avg_price_card"), class_="stat-card"),
                ui.div(ui.output_ui("fuel_types_card"), class_="stat-card"),
                ui.div(ui.output_ui("locations_card"), class_="stat-card"),
                class_="stats-grid"
            ),
            
            # Charts Grid
            ui.div(
                ui.div(output_widget("fuel_chart"), class_="chart-card"),
                ui.div(output_widget("location_chart"), class_="chart-card"),
                ui.div(output_widget("year_trend_chart"), class_="chart-card chart-full-width"),
                class_="charts-grid"
            ),
            
            class_="dashboard-container"
        )
    )

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
        
        # Stat Cards
        @output
        @render.ui
        def total_cars_card():
            _, stats = get_data()
            if stats is None:
                return ui.div("No data", class_="stat-value")
            
            return ui.div(
                ui.div(f"{stats['total_cars']:,}", class_="stat-value"),
                ui.div("Total Cars", class_="stat-label")
            )
        
        @output
        @render.ui
        def avg_price_card():
            _, stats = get_data()
            if stats is None:
                return ui.div("No data", class_="stat-value")
            
            return ui.div(
                ui.div(f"₹{stats['avg_price']:.1f}L", class_="stat-value"),
                ui.div("Average Price", class_="stat-label")
            )
        
        @output
        @render.ui
        def fuel_types_card():
            _, stats = get_data()
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
            _, stats = get_data()
            if stats is None:
                return ui.div("No data", class_="stat-value")
            
            location_count = len(stats.get('cars_by_location', {}))
            return ui.div(
                ui.div(str(location_count), class_="stat-value"),
                ui.div("Locations", class_="stat-label")
            )
        
        # Plotly Charts using shinywidgets
        @output
        @render_widget
        def fuel_chart():
            _, stats = get_data()
            if stats is None:
                return go.Figure().add_annotation(text="No data available")
            
            fuel_data = stats.get('price_by_fuel', {})
            if not fuel_data:
                return go.Figure().add_annotation(text="No fuel data available")
            
            fig = px.bar(
                x=list(fuel_data.keys()),
                y=list(fuel_data.values()),
                title="Average Price by Fuel Type",
                labels={'x': 'Fuel Type', 'y': 'Average Price (Lakhs)'}
            )
            fig.update_layout(height=400)
            return fig
        
        @output
        @render_widget
        def location_chart():
            _, stats = get_data()
            if stats is None:
                return go.Figure().add_annotation(text="No data available")
            
            location_data = stats.get('cars_by_location', {})
            if not location_data:
                return go.Figure().add_annotation(text="No location data available")
            
            fig = px.pie(
                values=list(location_data.values()),
                names=list(location_data.keys()),
                title="Cars by Location"
            )
            fig.update_layout(height=400)
            return fig
        
        @output
        @render_widget
        def year_trend_chart():
            _, stats = get_data()
            if stats is None:
                return go.Figure().add_annotation(text="No data available")
            
            year_data = stats.get('cars_by_year', {})
            if not year_data:
                return go.Figure().add_annotation(text="No year data available")
            
            sorted_years = sorted(year_data.items())
            fig = px.line(
                x=[year for year, count in sorted_years],
                y=[count for year, count in sorted_years],
                title="Number of Cars by Year",
                labels={'x': 'Year', 'y': 'Number of Cars'}
            )
            fig.update_layout(height=400)
            return fig
    
    return server