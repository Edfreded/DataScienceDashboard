from shiny import ui, render, reactive
import plotly.express as px
import plotly.graph_objects as go
from shinywidgets import render_widget
import pandas as pd
import numpy as np

def create_dashboard_server(filtered_data):
    def server(input, output, session):
        
        @reactive.calc
        def get_data():
            if hasattr(filtered_data, '__call__'):
                return filtered_data()
            return filtered_data
        
        # Stat Cards
        @output
        @render.ui
        def total_countries_card():
            data = get_data()
            if data is None or len(data) == 0:
                return ui.div("No data", class_="card-value")
            
            total_countries = data['countrycode'].nunique()
            return ui.div(
                ui.div(f"{total_countries:,}", class_="card-value"),
                ui.div("Countries", class_="card-label")
            )
        
        @output
        @render.ui
        def latest_year_card():
            data = get_data()
            if data is None or len(data) == 0:
                return ui.div("No data", class_="card-value")
            
            latest_year = data['year'].max()
            return ui.div(
                ui.div(str(latest_year), class_="card-value"),
                ui.div("Latest Year", class_="card-label")
            )
        
        @output
        @render.ui
        def avg_gdp_card():
            data = get_data()
            if data is None or len(data) == 0:
                return ui.div("No data", class_="card-value")
            
            avg_tfp = data['rtfpna'].mean()
            return ui.div(
                ui.div(f"{avg_tfp:.2f}", class_="card-value"),
                ui.div("Avg TFP", class_="card-label")
            )
        
        @output
        @render.ui
        def top_country_card():
            data = get_data()
            if data is None or len(data) == 0:
                return ui.div("No data", class_="card-value")
            
            latest_year = data['year'].max()
            latest_data = data[data['year'] == latest_year].dropna(subset=['rtfpna'])
            if len(latest_data) == 0:
                return ui.div("No data", class_="card-value")
            
            top_country = latest_data.loc[latest_data['rtfpna'].idxmax(), 'country']
            return ui.div(
                ui.div(top_country, class_="card-value"),
                ui.div("Highest TFP", class_="card-label")
            )



        # TFP Growth Acceleration Analysis
        @output
        @render_widget
        def productivity_tfp_acceleration():
            data = get_data()
            if data is None or len(data) == 0:
                fig = go.Figure().add_annotation(text="No data available")
                return fig
            
            latest_year = data['year'].max()
            latest_data = data[data['year'] == latest_year].dropna(subset=['tfp_growth_accel'])
            
            # Filter reasonable values
            latest_data = latest_data[
                (latest_data['tfp_growth_accel'] > -10) & 
                (latest_data['tfp_growth_accel'] < 10)
            ]
            
            # Show both positive and negative acceleration
            top_positive = latest_data.nlargest(8, 'tfp_growth_accel')
            top_negative = latest_data.nsmallest(7, 'tfp_growth_accel')
            combined = pd.concat([top_negative, top_positive])
            
            fig = px.bar(
                combined,
                x='tfp_growth_accel',
                y='country',
                orientation='h',
                title=f"TFP Growth Acceleration by Country ({latest_year})",
                labels={'tfp_growth_accel': 'TFP Growth Acceleration (pp)', 'country': 'Country'},
                color='tfp_growth_accel',
                color_continuous_scale='RdYlGn'
            )
            
            fig.update_layout(
                showlegend=False,
                margin=dict(l=120, r=50, t=60, b=50),
                autosize=True,
                yaxis={'categoryorder': 'total ascending'}
            )
            
            return fig

        # Technology Gap Analysis (TFP relative to frontier)
        @output
        @render_widget
        def productivity_technology_gap():
            data = get_data()
            if data is None or len(data) == 0:
                fig = go.Figure().add_annotation(text="No data available")
                return fig
            
            latest_year = data['year'].max()
            latest_data = data[data['year'] == latest_year].dropna(subset=['rtfpna'])
            
            # Calculate TFP relative to frontier (max TFP)
            tfp_frontier = latest_data['rtfpna'].max()
            latest_data = latest_data.copy()
            latest_data['tfp_gap'] = (tfp_frontier - latest_data['rtfpna']) / tfp_frontier * 100
            
            # Show countries with largest technology gaps
            largest_gaps = latest_data.nlargest(15, 'tfp_gap')
            
            fig = px.bar(
                largest_gaps,
                x='tfp_gap',
                y='country',
                orientation='h',
                title=f"Technology Gap: Distance from TFP Frontier ({latest_year})",
                labels={'tfp_gap': 'Technology Gap (%)', 'country': 'Country'}
            )
            
            fig.update_layout(
                showlegend=False,
                margin=dict(l=120, r=50, t=60, b=50),
                autosize=True,
                yaxis={'categoryorder': 'total ascending'}
            )
            
            return fig



        # Productivity Decomposition Over Time
        @output
        @render_widget
        def productivity_decomposition():
            data = get_data()
            if data is None or len(data) == 0:
                fig = go.Figure().add_annotation(text="No data available")
                return fig
            
            # Calculate global averages for productivity components
            yearly_stats = data.groupby('year').agg({
                'rtfpna': 'mean',
                'hc': 'mean',
                'k_per_worker': 'mean'
            }).reset_index()
            
            # Normalize to base year (first year = 100)
            base_year = yearly_stats['year'].min()
            for col in ['rtfpna', 'hc', 'k_per_worker']:
                base_value = yearly_stats[yearly_stats['year'] == base_year][col].iloc[0]
                yearly_stats[f'{col}_index'] = (yearly_stats[col] / base_value) * 100
            
            fig = go.Figure()
            
            fig.add_trace(go.Scatter(
                x=yearly_stats['year'],
                y=yearly_stats['rtfpna_index'],
                mode='lines+markers',
                name='Total Factor Productivity',
                line=dict(color='red', width=3)
            ))
            
            fig.add_trace(go.Scatter(
                x=yearly_stats['year'],
                y=yearly_stats['hc_index'],
                mode='lines+markers',
                name='Human Capital',
                line=dict(color='blue', width=2)
            ))
            
            fig.add_trace(go.Scatter(
                x=yearly_stats['year'],
                y=yearly_stats['k_per_worker_index'],
                mode='lines+markers',
                name='Capital per Worker',
                line=dict(color='green', width=2)
            ))
            
            fig.update_layout(
                title="Global Productivity Components Over Time (Index, Base Year = 100)",
                xaxis_title="Year",
                yaxis_title="Index (Base Year = 100)",
                hovermode='x unified',
                margin=dict(l=50, r=50, t=60, b=50),
                autosize=True
            )
            
            return fig
    
    return server