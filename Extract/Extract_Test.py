import pandas as pd
import os

def extract_car_data():
    try:
        dataset_path = os.path.join('Datasets', 'dataset.csv')
        
        df = pd.read_csv(dataset_path)
        
        if 'Unnamed: 0' in df.columns:
            df = df.drop('Unnamed: 0', axis=1)
        
        print(f"Successfully extracted {len(df)} records from {dataset_path}")
        return df
        
    except Exception as e:
        print(f"Error extracting data: {e}")
        return pd.DataFrame()

