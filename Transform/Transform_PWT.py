import pandas as pd

def clean_and_transform_data(df):
    # Clean and prepare data
    df["gdp_per_capita"] = (df["rgdpe"] * 1e6) / (df["pop"] * 1e6)
    df["gdp_growth"] = df.groupby("countrycode")["gdp_per_capita"].pct_change() * 100
    df["net_exports"] = df["csh_x"] - df["csh_m"]
    
    # Handle missing values
    df = df.dropna(subset=['countrycode', 'country'])
    
    print(f"Data cleaned: {len(df)} records remaining")
    return df

def create_summary_stats(df):
    if df.empty:
        return {}
    
    latest_year = df["year"].max()
    latest_data = df[df["year"] == latest_year]
    
    summary = {
        'total_countries': len(latest_data),
        'latest_year': latest_year,
        'avg_gdp_per_capita': latest_data['gdp_per_capita'].mean(),
        'top_gdp_countries': latest_data.nlargest(5, 'gdp_per_capita')[['country', 'gdp_per_capita']].to_dict('records'),
        'year_range': [df['year'].min(), df['year'].max()],
        'available_metrics': {
            'gdp_per_capita': 'GDP per Capita',
            'gdp_growth': 'GDP Growth (%)',
            'hc': 'Human Capital',
            'csh_i': 'Investment Share',
            'net_exports': 'Net Exports'
        }
    }
    
    return summary