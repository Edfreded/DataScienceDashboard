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

        # World Map - GDP per Capita
        @output
        @render_widget
        def output_world_gdp_map():
            data = get_data()
            if data is None or len(data) == 0:
                fig = go.Figure().add_annotation(text="No data available")
                return fig
            
            latest_year = data['year'].max()
            latest_data = data[data['year'] == latest_year].dropna(subset=['gdp_pc'])
            
            fig = px.choropleth(
                latest_data,
                locations="countrycode",
                color="gdp_pc",
                hover_name="country",
                hover_data={'gdp_pc': ':,.0f', 'year': True},
                color_continuous_scale="Viridis",
                title=f"GDP per Capita by Country ({latest_year})",
                labels={'gdp_pc': 'GDP per Capita ($)'}
            )
            
            fig.update_layout(
                geo=dict(showframe=False, showcoastlines=True, projection_type='natural earth'),
                margin=dict(l=0, r=0, t=50, b=0),
                autosize=True
            )
            
            return fig
        
        # GDP Growth Rate Map
        @output
        @render_widget
        def output_world_growth_map():
            data = get_data()
            if data is None or len(data) == 0:
                fig = go.Figure().add_annotation(text="No data available")
                return fig
            
            latest_year = data['year'].max()
            growth_data = data[data['year'] == latest_year].dropna(subset=['gdp_pc_growth'])
            
            fig = px.choropleth(
                growth_data,
                locations="countrycode",
                color="gdp_pc_growth",
                hover_name="country",
                hover_data={'gdp_pc_growth': ':.2f', 'year': True},
                color_continuous_scale="RdYlGn",
                color_continuous_midpoint=0,
                title=f"GDP Growth Rate by Country ({latest_year})",
                labels={'gdp_pc_growth': 'GDP Growth (%)'}
            )
            
            fig.update_layout(
                geo=dict(showframe=False, showcoastlines=True, projection_type='natural earth'),
                margin=dict(l=0, r=0, t=50, b=0),
                autosize=True
            )
            
            return fig

        # Top Countries by GDP per Capita
        @output
        @render_widget
        def output_top_countries_chart():
            data = get_data()
            if data is None or len(data) == 0:
                fig = go.Figure().add_annotation(text="No data available")
                return fig
            
            latest_year = data['year'].max()
            latest_data = data[data['year'] == latest_year].dropna(subset=['gdp_pc'])
            top_10 = latest_data.nlargest(10, 'gdp_pc')
            
            fig = px.bar(
                top_10,
                x='gdp_pc',
                y='country',
                orientation='h',
                title="Top 10 Countries by GDP per Capita",
                labels={'gdp_pc': 'GDP per Capita ($)', 'country': 'Country'}
            )
            
            fig.update_layout(
                showlegend=False,
                margin=dict(l=100, r=50, t=60, b=50),
                autosize=True,
                yaxis={'categoryorder': 'total ascending'}
            )
            
            return fig
        
        # GDP Trend Over Time
        @output
        @render_widget
        def output_gdp_trend_chart():
            data = get_data()
            if data is None or len(data) == 0:
                fig = go.Figure().add_annotation(text="No data available")
                return fig
            
            yearly_avg = data.groupby('year')['gdp_pc'].mean().reset_index()
            
            fig = px.line(
                yearly_avg,
                x='year',
                y='gdp_pc',
                title="Global Average GDP per Capita Over Time",
                labels={'year': 'Year', 'gdp_pc': 'GDP per Capita ($)'},
                markers=True
            )
            
            fig.update_layout(
                hovermode='x unified',
                margin=dict(l=50, r=50, t=60, b=50),
                autosize=True
            )
            
            return fig

        # GDP vs Population Scatter
        @output
        @render_widget
        def output_gdp_population_scatter():
            data = get_data()
            if data is None or len(data) == 0:
                fig = go.Figure().add_annotation(text="No data available")
                return fig
            
            latest_year = data['year'].max()
            latest_data = data[data['year'] == latest_year].dropna(subset=['gdp_pc', 'pop'])
            
            fig = px.scatter(
                latest_data,
                x='pop',
                y='gdp_pc',
                hover_name='country',
                title=f"GDP per Capita vs Population ({latest_year})",
                labels={'pop': 'Population (millions)', 'gdp_pc': 'GDP per Capita ($)'},
                log_x=True,
                log_y=True
            )
            
            fig.update_layout(
                margin=dict(l=50, r=50, t=60, b=50),
                autosize=True
            )
            
            return fig

        # Trade Openness vs GDP
        @output
        @render_widget
        def output_trade_gdp_scatter():
            data = get_data()
            if data is None or len(data) == 0:
                fig = go.Figure().add_annotation(text="No data available")
                return fig
            
            latest_year = data['year'].max()
            latest_data = data[data['year'] == latest_year].dropna(subset=['trade_open', 'gdp_pc'])
            
            fig = px.scatter(
                latest_data,
                x='trade_open',
                y='gdp_pc',
                hover_name='country',
                title=f"Trade Openness vs GDP per Capita ({latest_year})",
                labels={'trade_open': 'Trade Openness (%)', 'gdp_pc': 'GDP per Capita ($)'}
            )
            
            fig.update_layout(
                margin=dict(l=50, r=50, t=60, b=50),
                autosize=True
            )
            
            return fig
    
    return server