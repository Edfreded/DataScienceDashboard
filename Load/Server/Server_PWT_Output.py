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
            
            avg_gdp = data['gdp_pc'].mean()
            return ui.div(
                ui.div(f"${avg_gdp:,.0f}", class_="card-value"),
                ui.div("Avg GDP per Capita", class_="card-label")
            )
        
        @output
        @render.ui
        def top_country_card():
            data = get_data()
            if data is None or len(data) == 0:
                return ui.div("No data", class_="card-value")
            
            latest_year = data['year'].max()
            latest_data = data[data['year'] == latest_year]
            top_country = latest_data.loc[latest_data['gdp_pc'].idxmax(), 'country']
            return ui.div(
                ui.div(top_country, class_="card-value"),
                ui.div("Richest Country", class_="card-label")
            )



        # Time Trends - Levels (from imputation notebook)
        @output
        @render_widget
        def output_levels_trend():
            data = get_data()
            if data is None or len(data) == 0:
                fig = go.Figure().add_annotation(text="No data available")
                return fig
            
            # Key economic variables to show levels over time (matching notebook)
            vars_to_show = ['emp', 'hc', 'rkna', 'rnna', 'labsh']
            var_labels = {
                'emp': 'Employment',
                'hc': 'Human Capital', 
                'rkna': 'Real Capital Stock',
                'rnna': 'Net Capital Stock',
                'labsh': 'Labor Share'
            }
            
            fig = go.Figure()
            
            for var in vars_to_show:
                if var in data.columns:
                    yearly_avg = data.groupby('year')[var].mean().reset_index()
                    
                    fig.add_trace(go.Scatter(
                        x=yearly_avg['year'],
                        y=yearly_avg[var],
                        mode='lines+markers',
                        name=var_labels.get(var, var),
                        line=dict(width=2),
                        marker=dict(size=4)
                    ))
            
            fig.update_layout(
                title="Global Mean Levels Over Time (Post-Imputation)",
                xaxis_title="Year",
                yaxis_title="Mean Value",
                hovermode='x unified',
                margin=dict(l=50, r=50, t=60, b=50),
                autosize=True,
                legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=1.02,
                    xanchor="right",
                    x=1
                )
            )
            
            return fig

        # Time Trends - Growth Rates (from imputation notebook)
        @output
        @render_widget
        def output_growth_rates_trend():
            data = get_data()
            if data is None or len(data) == 0:
                fig = go.Figure().add_annotation(text="No data available")
                return fig
            
            # Calculate growth rates for key variables (matching notebook)
            vars_to_show = ['emp', 'hc', 'rkna', 'rnna', 'labsh']
            var_labels = {
                'emp': 'Employment Growth',
                'hc': 'Human Capital Growth', 
                'rkna': 'Real Capital Stock Growth',
                'rnna': 'Net Capital Stock Growth',
                'labsh': 'Labor Share Growth'
            }
            
            data_copy = data.copy()
            
            # Calculate growth rates
            for var in vars_to_show:
                if var in data_copy.columns:
                    data_copy[f'{var}_growth'] = data_copy.groupby('countrycode')[var].pct_change() * 100
            
            fig = go.Figure()
            
            for var in vars_to_show:
                growth_var = f'{var}_growth'
                if growth_var in data_copy.columns:
                    yearly_avg = data_copy.groupby('year')[growth_var].mean().reset_index()
                    
                    fig.add_trace(go.Scatter(
                        x=yearly_avg['year'],
                        y=yearly_avg[growth_var],
                        mode='lines+markers',
                        name=var_labels.get(var, var),
                        line=dict(width=2),
                        marker=dict(size=4)
                    ))
            
            # Add zero line
            fig.add_hline(y=0, line_dash="dash", line_color="black", line_width=1)
            
            fig.update_layout(
                title="Average Annual Growth Rates Over Time",
                xaxis_title="Year",
                yaxis_title="Mean Growth Rate (%)",
                hovermode='x unified',
                margin=dict(l=50, r=50, t=60, b=50),
                autosize=True,
                legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=1.02,
                    xanchor="right",
                    x=1
                )
            )
            
            return fig
    
    return server