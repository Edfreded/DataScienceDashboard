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

        # World Map - Capital per Worker
        @output
        @render_widget
        def capital_world_capital_map():
            data = get_data()
            if data is None or len(data) == 0:
                fig = go.Figure().add_annotation(text="No data available")
                return fig
            
            latest_year = data['year'].max()
            latest_data = data[data['year'] == latest_year].dropna(subset=['k_per_worker'])
            
            fig = px.choropleth(
                latest_data,
                locations="countrycode",
                color="k_per_worker",
                hover_name="country",
                hover_data={'k_per_worker': ':,.0f', 'year': True},
                color_continuous_scale="Viridis",
                title=f"Capital per Worker by Country ({latest_year})",
                labels={'k_per_worker': 'Capital per Worker ($)'}
            )
            
            fig.update_layout(
                geo=dict(showframe=False, showcoastlines=True, projection_type='natural earth'),
                margin=dict(l=0, r=0, t=50, b=0),
                autosize=True
            )
            
            return fig
        
        # Investment Rate Map
        @output
        @render_widget
        def capital_investment_rate_map():
            data = get_data()
            if data is None or len(data) == 0:
                fig = go.Figure().add_annotation(text="No data available")
                return fig
            
            latest_year = data['year'].max()
            investment_data = data[data['year'] == latest_year].dropna(subset=['csh_i'])
            investment_data = investment_data.copy()
            investment_data['investment_rate'] = investment_data['csh_i'] * 100
            
            fig = px.choropleth(
                investment_data,
                locations="countrycode",
                color="investment_rate",
                hover_name="country",
                hover_data={'investment_rate': ':.1f', 'year': True},
                color_continuous_scale="Blues",
                title=f"Investment Rate by Country ({latest_year})",
                labels={'investment_rate': 'Investment Rate (%)'}
            )
            
            fig.update_layout(
                geo=dict(showframe=False, showcoastlines=True, projection_type='natural earth'),
                margin=dict(l=0, r=0, t=50, b=0),
                autosize=True
            )
            
            return fig

        # Capital Intensity vs GDP
        @output
        @render_widget
        def capital_intensity_scatter():
            data = get_data()
            if data is None or len(data) == 0:
                fig = go.Figure().add_annotation(text="No data available")
                return fig
            
            latest_year = data['year'].max()
            latest_data = data[data['year'] == latest_year].dropna(subset=['capital_intensity', 'gdp_pc'])
            
            fig = px.scatter(
                latest_data,
                x='capital_intensity',
                y='gdp_pc',
                hover_name='country',
                title=f"Capital Intensity vs GDP per Capita ({latest_year})",
                labels={'capital_intensity': 'Capital Intensity (K/Y)', 'gdp_pc': 'GDP per Capita ($)'}
            )
            
            fig.update_layout(
                margin=dict(l=50, r=50, t=60, b=50),
                autosize=True
            )
            
            return fig
        
        # Investment Rate Trend
        @output
        @render_widget
        def capital_investment_trend_chart():
            data = get_data()
            if data is None or len(data) == 0:
                fig = go.Figure().add_annotation(text="No data available")
                return fig
            
            yearly_avg = data.groupby('year')['csh_i'].mean().reset_index()
            yearly_avg['investment_rate'] = yearly_avg['csh_i'] * 100
            
            fig = px.line(
                yearly_avg,
                x='year',
                y='investment_rate',
                title="Global Average Investment Rate Over Time",
                labels={'year': 'Year', 'investment_rate': 'Investment Rate (%)'},
                markers=True
            )
            
            fig.update_layout(
                hovermode='x unified',
                margin=dict(l=50, r=50, t=60, b=50),
                autosize=True
            )
            
            return fig

        # Capital per Worker Growth
        @output
        @render_widget
        def capital_growth_chart():
            data = get_data()
            if data is None or len(data) == 0:
                fig = go.Figure().add_annotation(text="No data available")
                return fig
            
            latest_year = data['year'].max()
            latest_data = data[data['year'] == latest_year].dropna(subset=['k_per_worker_growth'])
            top_10 = latest_data.nlargest(10, 'k_per_worker_growth')
            
            fig = px.bar(
                top_10,
                x='k_per_worker_growth',
                y='country',
                orientation='h',
                title=f"Top 10 Countries by Capital per Worker Growth ({latest_year})",
                labels={'k_per_worker_growth': 'K/Worker Growth (%)', 'country': 'Country'}
            )
            
            fig.update_layout(
                showlegend=False,
                margin=dict(l=100, r=50, t=60, b=50),
                autosize=True,
                yaxis={'categoryorder': 'total ascending'}
            )
            
            return fig

        # Investment Efficiency
        @output
        @render_widget
        def capital_investment_efficiency_chart():
            data = get_data()
            if data is None or len(data) == 0:
                fig = go.Figure().add_annotation(text="No data available")
                return fig
            
            latest_year = data['year'].max()
            latest_data = data[data['year'] == latest_year].dropna(subset=['investment_efficiency'])
            # Filter out extreme outliers
            latest_data = latest_data[
                (latest_data['investment_efficiency'] > 0) & 
                (latest_data['investment_efficiency'] < latest_data['investment_efficiency'].quantile(0.95))
            ]
            top_10 = latest_data.nlargest(10, 'investment_efficiency')
            
            fig = px.bar(
                top_10,
                x='investment_efficiency',
                y='country',
                orientation='h',
                title=f"Top 10 Countries by Investment Efficiency ({latest_year})",
                labels={'investment_efficiency': 'Investment Efficiency (TFP/Investment)', 'country': 'Country'}
            )
            
            fig.update_layout(
                showlegend=False,
                margin=dict(l=100, r=50, t=60, b=50),
                autosize=True,
                yaxis={'categoryorder': 'total ascending'}
            )
            
            return fig
    
    return server