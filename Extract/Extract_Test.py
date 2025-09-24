import pandas as pd
import os

def extract_car_data():
    """
    Extract car sales data from CSV file
    Returns: pandas DataFrame with car sales data
    """
    try:
        # Get the dataset path
        dataset_path = os.path.join('Datasets', 'dataset.csv')
        
        # Read the CSV file
        df = pd.read_csv(dataset_path)
        
        # Drop the unnamed index column if it exists
        if 'Unnamed: 0' in df.columns:
            df = df.drop('Unnamed: 0', axis=1)
        
        print(f"Successfully extracted {len(df)} records from {dataset_path}")
        return df
        
    except Exception as e:
        print(f"Error extracting data: {e}")
        return pd.DataFrame()

