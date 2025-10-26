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

        # World Map - Total Factor Productivity
        @output
        @render_widget
        def productivity_world_tfp_map():
            data = get_data()
            if data is None or len(data) == 0:
                fig = go.Figure().add_annotation(text="No data available")
                return fig
            
            latest_year = data['year'].max()
            latest_data = data[data['year'] == latest_year].dropna(subset=['rtfpna'])
            
            fig = px.choropleth(
                latest_data,
                locations="countrycode",
                color="rtfpna",
                hover_name="country",
                hover_data={'rtfpna': ':.3f', 'year': True},
                color_continuous_scale="Viridis",
                title=f"Total Factor Productivity by Country ({latest_year})",
                labels={'rtfpna': 'TFP Index'}
            )
            
            fig.update_layout(
                geo=dict(showframe=False, showcoastlines=True, projection_type='natural earth'),
                margin=dict(l=0, r=0, t=50, b=0),
                autosize=True
            )
            
            return fig
        
        # TFP Growth Rate Map
        @output
        @render_widget
        def productivity_tfp_growth_map():
            data = get_data()
            if data is None or len(data) == 0:
                fig = go.Figure().add_annotation(text="No data available")
                return fig
            
            latest_year = data['year'].max()
            growth_data = data[data['year'] == latest_year].dropna(subset=['rtfpna_growth'])
            
            fig = px.choropleth(
                growth_data,
                locations="countrycode",
                color="rtfpna_growth",
                hover_name="country",
                hover_data={'rtfpna_growth': ':.2f', 'year': True},
                color_continuous_scale="RdYlGn",
                color_continuous_midpoint=0,
                title=f"TFP Growth Rate by Country ({latest_year})",
                labels={'rtfpna_growth': 'TFP Growth (%)'}
            )
            
            fig.update_layout(
                geo=dict(showframe=False, showcoastlines=True, projection_type='natural earth'),
                margin=dict(l=0, r=0, t=50, b=0),
                autosize=True
            )
            
            return fig

        # TFP vs GDP per Worker
        @output
        @render_widget
        def productivity_tfp_gdp_scatter():
            data = get_data()
            if data is None or len(data) == 0:
                fig = go.Figure().add_annotation(text="No data available")
                return fig
            
            latest_year = data['year'].max()
            latest_data = data[data['year'] == latest_year].dropna(subset=['rtfpna', 'gdp_pw'])
            
            fig = px.scatter(
                latest_data,
                x='rtfpna',
                y='gdp_pw',
                hover_name='country',
                title=f"TFP vs GDP per Worker ({latest_year})",
                labels={'rtfpna': 'Total Factor Productivity', 'gdp_pw': 'GDP per Worker ($)'}
            )
            
            fig.update_layout(
                margin=dict(l=50, r=50, t=60, b=50),
                autosize=True
            )
            
            return fig
        
        # TFP Trend Over Time
        @output
        @render_widget
        def productivity_tfp_trend_chart():
            data = get_data()
            if data is None or len(data) == 0:
                fig = go.Figure().add_annotation(text="No data available")
                return fig
            
            yearly_avg = data.groupby('year')['rtfpna'].mean().reset_index()
            
            fig = px.line(
                yearly_avg,
                x='year',
                y='rtfpna',
                title="Global Average Total Factor Productivity Over Time",
                labels={'year': 'Year', 'rtfpna': 'TFP Index'},
                markers=True
            )
            
            fig.update_layout(
                hovermode='x unified',
                margin=dict(l=50, r=50, t=60, b=50),
                autosize=True
            )
            
            return fig

        # TFP Relative to US
        @output
        @render_widget
        def productivity_tfp_relative_us():
            data = get_data()
            if data is None or len(data) == 0:
                fig = go.Figure().add_annotation(text="No data available")
                return fig
            
            latest_year = data['year'].max()
            latest_data = data[data['year'] == latest_year].dropna(subset=['tfp_rel_us'])
            top_10 = latest_data.nlargest(10, 'tfp_rel_us')
            
            fig = px.bar(
                top_10,
                x='tfp_rel_us',
                y='country',
                orientation='h',
                title=f"TFP Relative to US ({latest_year})",
                labels={'tfp_rel_us': 'TFP Relative to US', 'country': 'Country'}
            )
            
            fig.update_layout(
                showlegend=False,
                margin=dict(l=100, r=50, t=60, b=50),
                autosize=True,
                yaxis={'categoryorder': 'total ascending'}
            )
            
            return fig

        # Human Capital x TFP Interaction
        @output
        @render_widget
        def productivity_hc_tfp_interaction():
            data = get_data()
            if data is None or len(data) == 0:
                fig = go.Figure().add_annotation(text="No data available")
                return fig
            
            latest_year = data['year'].max()
            latest_data = data[data['year'] == latest_year].dropna(subset=['hc_x_tfp', 'gdp_pc'])
            
            fig = px.scatter(
                latest_data,
                x='hc_x_tfp',
                y='gdp_pc',
                hover_name='country',
                title=f"Human Capital × TFP vs GDP per Capita ({latest_year})",
                labels={'hc_x_tfp': 'Human Capital × TFP', 'gdp_pc': 'GDP per Capita ($)'}
            )
            
            fig.update_layout(
                margin=dict(l=50, r=50, t=60, b=50),
                autosize=True
            )
            
            return fig
    
    return server