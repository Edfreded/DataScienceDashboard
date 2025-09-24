import dash
from dash import dcc, html, Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go

def create_dashboard_layout(summary_stats, df):
    """
    Create the main dashboard layout
    """
    if not summary_stats or df.empty:
        return html.Div([
            html.H1("Car Sales Dashboard", className="text-center mb-4"),
            html.P("No data available", className="text-center")
        ])
    
    # Create charts
    fuel_chart = create_fuel_type_chart(summary_stats)
    location_chart = create_location_chart(summary_stats)
    year_chart = create_year_trend_chart(summary_stats)
    
    layout = dbc.Container([
        dbc.Row([
            dbc.Col([
                html.H1("Car Sales Dashboard", className="text-center mb-4"),
                html.Hr()
            ])
        ]),
        
        # Summary cards
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H4(f"{summary_stats['total_cars']:,}", className="card-title"),
                        html.P("Total Cars", className="card-text")
                    ])
                ])
            ], width=3),
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H4(f"₹{summary_stats['avg_price']:.1f}L", className="card-title"),
                        html.P("Average Price", className="card-text")
                    ])
                ])
            ], width=3)
        ], className="mb-4"), 
       
        # Charts
        dbc.Row([
            dbc.Col([
                dcc.Graph(figure=fuel_chart)
            ], width=6),
            dbc.Col([
                dcc.Graph(figure=location_chart)
            ], width=6)
        ], className="mb-4"),
        
        dbc.Row([
            dbc.Col([
                dcc.Graph(figure=year_chart)
            ], width=12)
        ])
        
    ], fluid=True)
    
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