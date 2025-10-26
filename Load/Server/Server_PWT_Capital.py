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
            
            avg_investment = data['csh_i'].mean() * 100
            return ui.div(
                ui.div(f"{avg_investment:.1f}%", class_="card-value"),
                ui.div("Avg Investment Rate", class_="card-label")
            )
        
        @output
        @render.ui
        def top_country_card():
            data = get_data()
            if data is None or len(data) == 0:
                return ui.div("No data", class_="card-value")
            
            latest_year = data['year'].max()
            latest_data = data[data['year'] == latest_year].dropna(subset=['k_per_worker'])
            if len(latest_data) == 0:
                return ui.div("No data", class_="card-value")
            
            top_country = latest_data.loc[latest_data['k_per_worker'].idxmax(), 'country']
            return ui.div(
                ui.div(top_country, class_="card-value"),
                ui.div("Highest K/Worker", class_="card-label")
            )



        # Capital-Output Ratio Analysis
        @output
        @render_widget
        def capital_output_ratio_chart():
            data = get_data()
            if data is None or len(data) == 0:
                fig = go.Figure().add_annotation(text="No data available")
                return fig
            
            # Calculate capital-output ratio (K/Y)
            data_copy = data.copy()
            data_copy['ky_ratio'] = data_copy['rnna'] / data_copy['rgdpo']
            
            latest_year = data_copy['year'].max()
            latest_data = data_copy[data_copy['year'] == latest_year].dropna(subset=['ky_ratio'])
            
            # Filter reasonable values
            latest_data = latest_data[(latest_data['ky_ratio'] > 0.5) & (latest_data['ky_ratio'] < 10)]
            top_15 = latest_data.nlargest(15, 'ky_ratio')
            
            fig = px.bar(
                top_15,
                x='ky_ratio',
                y='country',
                orientation='h',
                title=f"Capital-Output Ratios by Country ({latest_year})",
                labels={'ky_ratio': 'Capital-Output Ratio (K/Y)', 'country': 'Country'}
            )
            
            fig.update_layout(
                showlegend=False,
                margin=dict(l=120, r=50, t=60, b=50),
                autosize=True,
                yaxis={'categoryorder': 'total ascending'}
            )
            
            return fig
        




        # Net Investment Analysis
        @output
        @render_widget
        def capital_net_investment_chart():
            data = get_data()
            if data is None or len(data) == 0:
                fig = go.Figure().add_annotation(text="No data available")
                return fig
            
            # Calculate net investment if not available
            if 'net_investment' not in data.columns:
                data_copy = data.copy()
                if 'delta' in data.columns:
                    data_copy['net_investment'] = data_copy['csh_i'] - data_copy['delta']
                else:
                    data_copy['net_investment'] = data_copy['csh_i']  # Assume no depreciation
            else:
                data_copy = data.copy()
            
            # Time trend of net investment
            yearly_avg = data_copy.groupby('year')['net_investment'].mean().reset_index()
            yearly_avg['net_investment_pct'] = yearly_avg['net_investment'] * 100
            
            fig = px.line(
                yearly_avg,
                x='year',
                y='net_investment_pct',
                title="Global Average Net Investment Rate Over Time",
                labels={'year': 'Year', 'net_investment_pct': 'Net Investment Rate (%)'},
                markers=True
            )
            
            fig.update_layout(
                hovermode='x unified',
                margin=dict(l=50, r=50, t=60, b=50),
                autosize=True
            )
            
            return fig
    
    return server