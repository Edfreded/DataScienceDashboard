import dash
from dash import dcc, html, Input, Output
import plotly.express as px
import plotly.graph_objects as go

def create_dashboard_layout(summary_stats, df):
    """
    Create the main dashboard layout
    """
    if not summary_stats or df.empty:
        return html.Div([
            html.H1("Car Sales Dashboard", className="dashboard-title"),
            html.P("No data available", style={'text-align': 'center'})
        ], className="dashboard-container")
    
    # Create charts
    fuel_chart = create_fuel_type_chart(summary_stats)
    location_chart = create_location_chart(summary_stats)
    year_chart = create_year_trend_chart(summary_stats)
    
    layout = html.Div([
        # Header
        html.Div([
            html.H1("Car Sales Dashboard", className="dashboard-title"),
            html.Hr(className="dashboard-divider")
        ], className="dashboard-header"),
        
        # Main content - 2 column layout
        html.Div([
            # Left sidebar with stats
            html.Div([
                html.Div([
                    html.Div([
                        html.Div(f"{summary_stats['total_cars']:,}", className="stat-value"),
                        html.Div("Total Cars", className="stat-label")
                    ], className="stat-card"),
                    html.Div([
                        html.Div(f"₹{summary_stats['avg_price']:.1f}L", className="stat-value"),
                        html.Div("Average Price", className="stat-label")
                    ], className="stat-card")
                ], className="stats-container")
            ], className="left-sidebar"),
            
            # Right area with charts in 2x2 grid
            html.Div([
                html.Div([
                    dcc.Graph(figure=fuel_chart, style={'height': '100%'})
                ], className="chart-container"),
                html.Div([
                    dcc.Graph(figure=location_chart, style={'height': '100%'})
                ], className="chart-container"),
                html.Div([
                    dcc.Graph(figure=year_chart, style={'height': '100%'})
                ], className="chart-container full-width")
            ], className="charts-area")
            
        ], className="main-content")
        
    ], className="dashboard-container")
    
    return layout

def create_fuel_type_chart(summary_stats):
    """Create fuel type distribution chart"""
    fuel_data = summary_stats.get('price_by_fuel', {})
    if not fuel_data:
        return go.Figure()
    
    fig = px.bar(
        x=list(fuel_data.keys()),
        y=list(fuel_data.values()),
        title="Average Price by Fuel Type",
        labels={'x': 'Fuel Type', 'y': 'Average Price (Lakhs)'}
    )
    return fig

def create_location_chart(summary_stats):
    """Create location distribution chart"""
    location_data = summary_stats.get('cars_by_location', {})
    if not location_data:
        return go.Figure()
    
    fig = px.pie(
        values=list(location_data.values()),
        names=list(location_data.keys()),
        title="Cars by Location"
    )
    return fig

def create_year_trend_chart(summary_stats):
    """Create year trend chart"""
    year_data = summary_stats.get('cars_by_year', {})
    if not year_data:
        return go.Figure()
    
    sorted_years = sorted(year_data.items())
    fig = px.line(
        x=[year for year, count in sorted_years],
        y=[count for year, count in sorted_years],
        title="Number of Cars by Year",
        labels={'x': 'Year', 'y': 'Number of Cars'}
    )
    return fig