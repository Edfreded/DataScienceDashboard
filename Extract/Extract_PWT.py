import pandas as pd
import os

def extract_PWT():
    try:
        dataset_path = os.path.join('Datasets', 'pwt110_cleaned.csv')
        
        df = pd.read_csv(dataset_path)
        
        if 'Unnamed: 0' in df.columns:
            df = df.drop('Unnamed: 0', axis=1)
        
        print(f"Successfully extracted {len(df)} records from {dataset_path}")
        return df
        
    except Exception as e:
        print(f"Error extracting data: {e}")
        return pd.DataFrame()