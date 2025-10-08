import pandas as pd
import numpy as np

def clean_and_transform_data(df):
    if df.empty:
        return df
    
    cleaned_df = df.copy()
    
    numeric_columns = ['Year', 'Kilometers_Driven', 'Seats', 'Price']
    for col in numeric_columns:
        if col in cleaned_df.columns:
            cleaned_df[col] = pd.to_numeric(cleaned_df[col], errors='coerce')
    
    cleaned_df = cleaned_df.dropna(subset=['Name', 'Price'])
    
    cleaned_df['Fuel_Type'] = cleaned_df['Fuel_Type'].fillna('Unknown')
    cleaned_df['Transmission'] = cleaned_df['Transmission'].fillna('Unknown')
    cleaned_df['Location'] = cleaned_df['Location'].fillna('Unknown')
    
    print(f"Data cleaned: {len(cleaned_df)} records remaining")
    return cleaned_df

def create_summary_stats(df):
    if df.empty:
        return {}
    
    summary = {
        'total_cars': len(df),
        'avg_price': df['Price'].mean(),
        'price_by_fuel': df.groupby('Fuel_Type')['Price'].mean().to_dict(),
        'cars_by_location': df['Location'].value_counts().to_dict(),
        'cars_by_year': df.groupby('Year')['Price'].count().to_dict(),
        'transmission_distribution': df['Transmission'].value_counts().to_dict()
    }
    
    return summary

