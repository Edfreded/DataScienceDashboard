import pandas as pd
import numpy as np


def pwt_clean(df):
    # Set Data Types
    text_cols = ['countrycode', 'country', 'currency_unit']
    data_information_flags = ['i_cig', 'i_xm', 'i_xr', 'i_outlier', 'i_irr']

    for c in text_cols:
        df[c] = df[c].astype('category')

    numerical_cols = [c for c in df.columns 
                if c not in text_cols + ['year'] + data_information_flags]
    for c in numerical_cols:
        df[c] = pd.to_numeric(df[c], errors='coerce')


    # Remove Invalid Entries
    df = df.dropna(subset=['rgdpo'])
    df = df.drop_duplicates(subset=['countrycode', 'year'])


    # Encode Data Quality Flags
    for col in ['i_cig', 'i_xm', 'i_xr', 'i_outlier', 'i_irr']:
        df[col] = df[col].astype(str).str.strip()

    cig_map = {
        'Extrapolated': 0,
        'Benchmark': 1,
        'Interpolated': 2,
        'ICP PPP timeseries: benchmark or interpolated': 3,
        'ICP PPP timeseries: extrapolated': 4
    }
    xm_map = {'Extrapolated': 0, 'Benchmark': 1, 'Interpolated': 2}
    irr_map = {
        'Regular': 0,
        'Low capital share': 1,
        'Lower bound': 2,
        'Outlier': 3
    }

    xr_map = {'Market-based': 0, 'Estimated': 1}
    outlier_map = {'Regular': 0, 'Outlier': 1}


    df['i_cig_encoded'] = df['i_cig'].map(cig_map).astype('Int8')
    df['i_xm_encoded'] = df['i_xm'].map(xm_map).astype('Int8')
    df['i_xr_encoded'] = df['i_xr'].map(xr_map).astype('Int8')
    df['i_outlier_encoded'] = df['i_outlier'].map(outlier_map).astype('Int8')
    df['i_irr_encoded'] = df['i_irr'].map(irr_map).astype('Int8')


    df = df.drop(columns=['i_cig', 'i_xm', 'i_xr', 'i_outlier', 'i_irr'])


    # Data Quality Validation

    # === VALUE SANITY CHECKS ===
    invalid_pop = df.loc[df['pop'] <= 0, ['countrycode', 'year', 'pop']]
    invalid_emp = df.loc[df['emp'] < 0, ['countrycode', 'year', 'emp']]
    invalid_gdp = df.loc[df['rgdpo'] < 0, ['countrycode', 'year', 'rgdpo']]


    # === CROSS-VARIABLE CONSISTENCY ===
    inconsistent_emp = df.loc[df['emp'] > df['pop'], ['countrycode', 'year', 'emp', 'pop']]

    # === NUMERIC OUTLIER SCAN (|z| > 5) ===
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    z_scores = np.abs((df[numeric_cols] - df[numeric_cols].mean()) / df[numeric_cols].std())
    outlier_counts = (z_scores > 5).sum().sort_values(ascending=False)


    # === MISSING DATA SUMMARY ===
    missing_summary = df.isna().mean().sort_values(ascending=False)


    # === TIME COVERAGE (first 5 countries) ===
    coverage = (
        df.groupby('countrycode', observed=True)['year']
        .agg(['min', 'max', 'count'])
        .sort_values('count', ascending=False)
    )


    # === SUMMARY STATS (key columns) ===
    key_cols = ['rgdpo', 'pop', 'emp', 'labsh', 'irr']
    for col in key_cols:
        if col in df.columns:
            desc = df[col].describe(percentiles=[.01, .5, .99])

    return df