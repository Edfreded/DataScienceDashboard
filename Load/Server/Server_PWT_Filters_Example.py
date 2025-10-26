from shiny import reactive
import pandas as pd

def create_filters_server(cleaned_data=None, summary_stats=None):
    def server(input, output, session):
        
        # Reactive filtered data based on sidebar controls
        @reactive.calc
        def filtered_data():
            if cleaned_data is None or len(cleaned_data) == 0:
                return cleaned_data
            
            data = cleaned_data.copy()
            
            # Apply year range filter
            if hasattr(input, 'year_range') and input.year_range() is not None:
                year_min, year_max = input.year_range()
                data = data[
                    (data['year'] >= year_min) & 
                    (data['year'] <= year_max)
                ]
            
            # Apply region filter (placeholder for future implementation)
            if hasattr(input, 'region_filter') and input.region_filter() != "all":
                # You can add region filtering logic here based on your data structure
                # For now, this is a placeholder
                pass
            
            return data
        
        # Reactive summary stats based on filtered data
        @reactive.calc
        def filtered_summary_stats():
            data = filtered_data()
            if data is None or len(data) == 0:
                return summary_stats
            
            # Recalculate summary stats based on filtered data
            latest_year = data['year'].max()
            latest_year_data = data[data['year'] == latest_year]
            
            # Get top countries from filtered data
            top_countries = latest_year_data.nlargest(5, 'gdp_per_capita')[
                ['country', 'gdp_per_capita']
            ].to_dict('records')
            
            filtered_stats = {
                'total_countries': data['country'].nunique(),
                'latest_year': latest_year,
                'avg_gdp_per_capita': data['gdp_per_capita'].mean(),
                'top_gdp_countries': [
                    {
                        'country': row['country'], 
                        'gdp_per_capita': row['gdp_per_capita']
                    } 
                    for row in top_countries
                ]
            }
            
            return filtered_stats
        
        # Debug reactive effects to see filter changes
        @reactive.effect
        @reactive.event(input.year_range)
        def debug_year_filter():
            data = filtered_data()
            if data is not None:
                year_min, year_max = input.year_range()
                print(f"Year filter applied: {year_min}-{year_max}")
                print(f"Filtered data shape: {data.shape}")
                print(f"Years in filtered data: {sorted(data['year'].unique())}")
        
        @reactive.effect
        @reactive.event(input.region_filter)
        def debug_region_filter():
            print(f"Region filter changed to: {input.region_filter()}")
        
        @reactive.effect
        @reactive.event(input.theme_selector)
        def debug_theme_change():
            print(f"Theme changed to: {input.theme_selector()}")
        
        @reactive.effect
        @reactive.event(input.show_grid)
        def debug_grid_toggle():
            print(f"Grid visibility: {input.show_grid()}")
        
        # Return the reactive data for other servers to use
        return {
            'filtered_data': filtered_data,
            'filtered_summary_stats': filtered_summary_stats
        }
    
    return server