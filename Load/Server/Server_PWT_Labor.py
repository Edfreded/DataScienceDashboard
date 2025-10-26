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
            
            avg_emp_rate = data['emp_rate'].mean() * 100
            return ui.div(
                ui.div(f"{avg_emp_rate:.1f}%", class_="card-value"),
                ui.div("Avg Employment Rate", class_="card-label")
            )
        
        @output
        @render.ui
        def top_country_card():
            data = get_data()
            if data is None or len(data) == 0:
                return ui.div("No data", class_="card-value")
            
            latest_year = data['year'].max()
            latest_data = data[data['year'] == latest_year].dropna(subset=['hc'])
            if len(latest_data) == 0:
                return ui.div("No data", class_="card-value")
            
            top_country = latest_data.loc[latest_data['hc'].idxmax(), 'country']
            return ui.div(
                ui.div(top_country, class_="card-value"),
                ui.div("Highest Human Capital", class_="card-label")
            )

        # World Map - Human Capital
        @output
        @render_widget
        def labor_world_hc_map():
            data = get_data()
            if data is None or len(data) == 0:
                fig = go.Figure().add_annotation(text="No data available")
                return fig
            
            latest_year = data['year'].max()
            latest_data = data[data['year'] == latest_year].dropna(subset=['hc'])
            
            fig = px.choropleth(
                latest_data,
                locations="countrycode",
                color="hc",
                hover_name="country",
                hover_data={'hc': ':.2f', 'year': True},
                color_continuous_scale="Viridis",
                title=f"Human Capital Index by Country ({latest_year})",
                labels={'hc': 'Human Capital Index'}
            )
            
            fig.update_layout(
                geo=dict(showframe=False, showcoastlines=True, projection_type='natural earth'),
                margin=dict(l=0, r=0, t=50, b=0),
                autosize=True
            )
            
            return fig
        
        # Employment Rate Map
        @output
        @render_widget
        def labor_employment_rate_map():
            data = get_data()
            if data is None or len(data) == 0:
                fig = go.Figure().add_annotation(text="No data available")
                return fig
            
            latest_year = data['year'].max()
            emp_data = data[data['year'] == latest_year].dropna(subset=['emp_rate'])
            emp_data = emp_data.copy()
            emp_data['employment_rate'] = emp_data['emp_rate'] * 100
            
            fig = px.choropleth(
                emp_data,
                locations="countrycode",
                color="employment_rate",
                hover_name="country",
                hover_data={'employment_rate': ':.1f', 'year': True},
                color_continuous_scale="Blues",
                title=f"Employment Rate by Country ({latest_year})",
                labels={'employment_rate': 'Employment Rate (%)'}
            )
            
            fig.update_layout(
                geo=dict(showframe=False, showcoastlines=True, projection_type='natural earth'),
                margin=dict(l=0, r=0, t=50, b=0),
                autosize=True
            )
            
            return fig

        # Human Capital vs GDP per Worker
        @output
        @render_widget
        def labor_hc_gdp_scatter():
            data = get_data()
            if data is None or len(data) == 0:
                fig = go.Figure().add_annotation(text="No data available")
                return fig
            
            latest_year = data['year'].max()
            latest_data = data[data['year'] == latest_year].dropna(subset=['hc', 'gdp_pw'])
            
            fig = px.scatter(
                latest_data,
                x='hc',
                y='gdp_pw',
                hover_name='country',
                title=f"Human Capital vs GDP per Worker ({latest_year})",
                labels={'hc': 'Human Capital Index', 'gdp_pw': 'GDP per Worker ($)'}
            )
            
            fig.update_layout(
                margin=dict(l=50, r=50, t=60, b=50),
                autosize=True
            )
            
            return fig
        
        # Human Capital Trend
        @output
        @render_widget
        def labor_hc_trend_chart():
            data = get_data()
            if data is None or len(data) == 0:
                fig = go.Figure().add_annotation(text="No data available")
                return fig
            
            yearly_avg = data.groupby('year')['hc'].mean().reset_index()
            
            fig = px.line(
                yearly_avg,
                x='year',
                y='hc',
                title="Global Average Human Capital Over Time",
                labels={'year': 'Year', 'hc': 'Human Capital Index'},
                markers=True
            )
            
            fig.update_layout(
                hovermode='x unified',
                margin=dict(l=50, r=50, t=60, b=50),
                autosize=True
            )
            
            return fig

        # Labor Share Trend
        @output
        @render_widget
        def labor_share_trend():
            data = get_data()
            if data is None or len(data) == 0:
                fig = go.Figure().add_annotation(text="No data available")
                return fig
            
            yearly_avg = data.groupby('year')['labsh'].mean().reset_index()
            yearly_avg['labor_share'] = yearly_avg['labsh'] * 100
            
            fig = px.line(
                yearly_avg,
                x='year',
                y='labor_share',
                title="Global Average Labor Share Over Time",
                labels={'year': 'Year', 'labor_share': 'Labor Share (%)'},
                markers=True
            )
            
            fig.update_layout(
                hovermode='x unified',
                margin=dict(l=50, r=50, t=60, b=50),
                autosize=True
            )
            
            return fig

        # Dependency Ratio vs GDP
        @output
        @render_widget
        def labor_dependency_ratio_chart():
            data = get_data()
            if data is None or len(data) == 0:
                fig = go.Figure().add_annotation(text="No data available")
                return fig
            
            latest_year = data['year'].max()
            latest_data = data[data['year'] == latest_year].dropna(subset=['dependency_ratio', 'gdp_pc'])
            
            fig = px.scatter(
                latest_data,
                x='dependency_ratio',
                y='gdp_pc',
                hover_name='country',
                title=f"Dependency Ratio vs GDP per Capita ({latest_year})",
                labels={'dependency_ratio': 'Dependency Ratio (Pop/Emp)', 'gdp_pc': 'GDP per Capita ($)'}
            )
            
            fig.update_layout(
                margin=dict(l=50, r=50, t=60, b=50),
                autosize=True
            )
            
            return fig
    
    return server