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



        # Human Capital Returns Analysis
        @output
        @render_widget
        def labor_hc_returns_chart():
            data = get_data()
            if data is None or len(data) == 0:
                fig = go.Figure().add_annotation(text="No data available")
                return fig
            
            latest_year = data['year'].max()
            latest_data = data[data['year'] == latest_year].dropna(subset=['hc_returns'])
            
            # Filter reasonable values
            latest_data = latest_data[
                (latest_data['hc_returns'] > -0.5) & 
                (latest_data['hc_returns'] < 2.0)
            ]
            top_15 = latest_data.nlargest(15, 'hc_returns')
            
            fig = px.bar(
                top_15,
                x='hc_returns',
                y='country',
                orientation='h',
                title=f"Human Capital Returns by Country ({latest_year})",
                labels={'hc_returns': 'Human Capital Returns (Ratio)', 'country': 'Country'}
            )
            
            fig.update_layout(
                showlegend=False,
                margin=dict(l=120, r=50, t=60, b=50),
                autosize=True,
                yaxis={'categoryorder': 'total ascending'}
            )
            
            return fig

        # Labor Share Decline Analysis
        @output
        @render_widget
        def labor_share_decline():
            data = get_data()
            if data is None or len(data) == 0:
                fig = go.Figure().add_annotation(text="No data available")
                return fig
            
            # Calculate labor share change over time
            data_copy = data.copy()
            data_copy['labor_share_pct'] = data_copy['labsh'] * 100
            
            # Get countries with sufficient data
            country_data = []
            for country in data_copy['countrycode'].unique():
                country_subset = data_copy[data_copy['countrycode'] == country].sort_values('year')
                if len(country_subset) >= 10:  # At least 10 years of data
                    first_decade = country_subset.head(10)['labor_share_pct'].mean()
                    last_decade = country_subset.tail(10)['labor_share_pct'].mean()
                    change = last_decade - first_decade
                    country_data.append({
                        'country': country_subset['country'].iloc[0],
                        'countrycode': country,
                        'labor_share_change': change
                    })
            
            if country_data:
                change_df = pd.DataFrame(country_data)
                # Show countries with biggest declines
                biggest_declines = change_df.nsmallest(15, 'labor_share_change')
                
                fig = px.bar(
                    biggest_declines,
                    x='labor_share_change',
                    y='country',
                    orientation='h',
                    title="Largest Labor Share Declines (First vs Last Decade)",
                    labels={'labor_share_change': 'Labor Share Change (pp)', 'country': 'Country'}
                )
                
                fig.update_layout(
                    showlegend=False,
                    margin=dict(l=120, r=50, t=60, b=50),
                    autosize=True,
                    yaxis={'categoryorder': 'total ascending'}
                )
            else:
                fig = go.Figure().add_annotation(text="Insufficient data for analysis")
            
            return fig

        # Employment vs Human Capital Correlation
        @output
        @render_widget
        def labor_emp_hc_correlation():
            data = get_data()
            if data is None or len(data) == 0:
                fig = go.Figure().add_annotation(text="No data available")
                return fig
            
            # Calculate correlation by country over time
            correlations = []
            for country in data['countrycode'].unique():
                country_data = data[data['countrycode'] == country]
                if len(country_data) >= 5:  # Need at least 5 observations
                    corr = country_data['emp'].corr(country_data['hc'])
                    if pd.notna(corr):
                        correlations.append({
                            'country': country_data['country'].iloc[0],
                            'countrycode': country,
                            'emp_hc_correlation': corr
                        })
            
            if correlations:
                corr_df = pd.DataFrame(correlations)
                # Show distribution of correlations
                fig = px.histogram(
                    corr_df,
                    x='emp_hc_correlation',
                    nbins=20,
                    title="Distribution of Employment-Human Capital Correlations by Country",
                    labels={'emp_hc_correlation': 'Employment-Human Capital Correlation', 'count': 'Number of Countries'}
                )
                
                fig.update_layout(
                    margin=dict(l=50, r=50, t=60, b=50),
                    autosize=True,
                    showlegend=False
                )
            else:
                fig = go.Figure().add_annotation(text="Insufficient data for correlation analysis")
            
            return fig

        # Effective Labor Productivity
        @output
        @render_widget
        def labor_effective_productivity():
            data = get_data()
            if data is None or len(data) == 0:
                fig = go.Figure().add_annotation(text="No data available")
                return fig
            
            latest_year = data['year'].max()
            latest_data = data[data['year'] == latest_year].dropna(subset=['gdp_per_eff_worker', 'gdp_pw'])
            
            fig = px.scatter(
                latest_data,
                x='gdp_pw',
                y='gdp_per_eff_worker',
                hover_name='country',
                title=f"Raw vs Human Capital-Adjusted Productivity ({latest_year})",
                labels={'gdp_pw': 'GDP per Worker ($)', 'gdp_per_eff_worker': 'GDP per Effective Worker ($)'}
            )
            
            # Add 45-degree line
            if len(latest_data) > 0:
                min_val = min(latest_data['gdp_pw'].min(), latest_data['gdp_per_eff_worker'].min())
                max_val = max(latest_data['gdp_pw'].max(), latest_data['gdp_per_eff_worker'].max())
                fig.add_shape(
                    type="line",
                    x0=min_val, y0=min_val,
                    x1=max_val, y1=max_val,
                    line=dict(color="red", dash="dash"),
                )
            
            fig.update_layout(
                margin=dict(l=50, r=50, t=60, b=50),
                autosize=True
            )
            
            return fig
    
    return server