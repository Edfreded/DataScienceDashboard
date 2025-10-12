from shiny import ui, render, reactive
import plotly.express as px
import plotly.graph_objects as go
from shinywidgets import render_widget

def create_dashboard_server(cleaned_data=None, summary_stats=None):
    def server(input, output, session):
        
        # Reactive data loading
        @reactive.calc
        def get_cleaned_data():
            return cleaned_data
        
        @reactive.calc  
        def get_summary_stats():
            return summary_stats
        
        @reactive.calc
        def get_latest_year_data():
            data = get_cleaned_data()
            if data is None or data.empty:
                return None
            latest_year = data['year'].max()
            return data[data['year'] == latest_year]
        
        # Stat Cards
        @output
        @render.ui
        def total_countries_card():
            stats = get_summary_stats()
            if stats is None:
                return ui.div("No data", class_="card-value")
            
            return ui.div(
                ui.div(f"{stats['total_countries']:,}", class_="card-value"),
                ui.div("Countries", class_="card-label")
            )
        
        @output
        @render.ui
        def latest_year_card():
            stats = get_summary_stats()
            if stats is None:
                return ui.div("No data", class_="card-value")
            
            return ui.div(
                ui.div(str(stats['latest_year']), class_="card-value"),
                ui.div("Latest Year", class_="card-label")
            )
        
        @output
        @render.ui
        def avg_gdp_card():
            stats = get_summary_stats()
            if stats is None:
                return ui.div("No data", class_="card-value")
            
            avg_gdp = stats.get('avg_gdp_per_capita', 0)
            return ui.div(
                ui.div(f"${avg_gdp:,.0f}", class_="card-value"),
                ui.div("Avg GDP per Capita", class_="card-label")
            )
        
        @output
        @render.ui
        def top_country_card():
            stats = get_summary_stats()
            if stats is None or not stats.get('top_gdp_countries'):
                return ui.div("No data", class_="card-value")
            
            top_country = stats['top_gdp_countries'][0]['country']
            return ui.div(
                ui.div(top_country, class_="card-value"),
                ui.div("Richest Country", class_="card-label")
            )

        # World Map - GDP per Capita
        @output
        @render_widget
        def world_gdp_map():
            data = get_latest_year_data()
            if data is None or data.empty:
                fig = go.Figure().add_annotation(text="No data available")
                return fig
            
            fig = px.choropleth(
                data,
                locations="countrycode",
                color="gdp_per_capita",
                hover_name="country",
                hover_data={
                    'gdp_per_capita': ':,.0f',
                    'year': True
                },
                color_continuous_scale="Viridis",
                title=f"GDP per Capita by Country ({data['year'].iloc[0]})",
                labels={'gdp_per_capita': 'GDP per Capita ($)'}
            )
            
            fig.update_layout(
                geo=dict(
                    showframe=False,
                    showcoastlines=True,
                    projection_type='equirectangular'
                ),
                margin=dict(l=0, r=0, t=50, b=0),
                autosize=True
            )
            
            return fig
        
        # World Map - GDP Growth
        @output
        @render_widget
        def world_growth_map():
            data = get_latest_year_data()
            if data is None or data.empty:
                fig = go.Figure().add_annotation(text="No data available")
                return fig
            
            # Filter out extreme outliers for better visualization
            growth_data = data.dropna(subset=['gdp_growth'])
            if growth_data.empty:
                fig = go.Figure().add_annotation(text="No growth data available")
                return fig
            
            fig = px.choropleth(
                growth_data,
                locations="countrycode",
                color="gdp_growth",
                hover_name="country",
                hover_data={
                    'gdp_growth': ':.2f',
                    'year': True
                },
                color_continuous_scale="RdYlGn",
                color_continuous_midpoint=0,
                title=f"GDP Growth Rate by Country ({growth_data['year'].iloc[0]})",
                labels={'gdp_growth': 'GDP Growth (%)'}
            )
            
            fig.update_layout(
                geo=dict(
                    showframe=False,
                    showcoastlines=True,
                    projection_type='equirectangular'
                ),
                margin=dict(l=0, r=0, t=50, b=0),
                autosize=True
            )
            
            return fig

        # Top Countries Bar Chart
        @output
        @render_widget
        def top_countries_chart():
            stats = get_summary_stats()
            if stats is None or not stats.get('top_gdp_countries'):
                fig = go.Figure().add_annotation(text="No data available")
                return fig
            
            top_countries = stats['top_gdp_countries']
            countries = [c['country'] for c in top_countries]
            gdp_values = [c['gdp_per_capita'] for c in top_countries]
            
            fig = px.bar(
                x=gdp_values,
                y=countries,
                orientation='h',
                title="Top 5 Countries by GDP per Capita",
                labels={'x': 'GDP per Capita ($)', 'y': 'Country'}
            )
            
            fig.update_layout(
                showlegend=False,
                margin=dict(l=100, r=50, t=60, b=50),
                autosize=True,
                yaxis={'categoryorder': 'total ascending'}
            )
            
            fig.update_traces(
                hovertemplate='<b>%{y}</b><br>GDP per Capita: $%{x:,.0f}<extra></extra>'
            )
            
            return fig
        
        # GDP Trend Over Time
        @output
        @render_widget
        def gdp_trend_chart():
            data = get_cleaned_data()
            if data is None or data.empty:
                fig = go.Figure().add_annotation(text="No data available")
                return fig
            
            # Calculate global average GDP per capita by year
            yearly_avg = data.groupby('year')['gdp_per_capita'].mean().reset_index()
            
            fig = px.line(
                yearly_avg,
                x='year',
                y='gdp_per_capita',
                title="Global Average GDP per Capita Over Time",
                labels={'year': 'Year', 'gdp_per_capita': 'GDP per Capita ($)'},
                markers=True
            )
            
            fig.update_layout(
                hovermode='x unified',
                margin=dict(l=50, r=50, t=60, b=50),
                autosize=True
            )
            
            fig.update_traces(
                hovertemplate='<b>Year %{x}</b><br>Avg GDP: $%{y:,.0f}<extra></extra>',
                line=dict(width=3),
                marker=dict(size=6)
            )
            
            return fig
    
    return server