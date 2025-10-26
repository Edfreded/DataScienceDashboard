import pandas as pd
import numpy as np


def pwt_feature(df):
    # Check if DataFrame is empty or has no countries
    if df.empty or df['countrycode'].nunique() == 0:
        return df
    
    # Productivity and Structural Indicators
    df["gdp_pc"] = df["rgdpo"] / df["pop"]
    df["gdp_pw"] = df["rgdpo"] / df["emp"]
    
    # Handle missing avh column
    if "avh" in df.columns:
        df["gdp_ph"] = df["rgdpo"] / (df["emp"] * df["avh"])
    else:
        df["gdp_ph"] = np.nan

    df["emp_rate"] = df["emp"] / df["pop"]

    if "rkna" in df.columns:
        df["k_per_worker"] = df["rkna"] / df["emp"]

    df["trade_open"] = df["csh_x"] + df["csh_m"]
    df["net_exports"] = df["csh_x"] - df["csh_m"]

    df["eff_labor"] = df["hc"] * df["emp"]
    df["gdp_per_eff_worker"] = df["rgdpo"] / df["eff_labor"]
        
    # Time based
    df = df.sort_values(["countrycode", "year"])

    df["gdp_pc_lag1"] = df.groupby("countrycode")["gdp_pc"].shift(1)

    for var in ["gdp_pc", "pop", "hc", "rtfpna", "csh_i"]:
        df[f"{var}_growth"] = df.groupby("countrycode")[var].pct_change() * 100

    # Only calculate rolling averages for countries with sufficient data
    def safe_rolling_mean(group):
        if len(group) > 0:
            return group.rolling(window=5, min_periods=1).mean()
        else:
            return pd.Series(dtype=float, index=group.index)
    
    df["gdp_pc_growth_5yr"] = (
        df.groupby("countrycode")["gdp_pc_growth"]
        .apply(safe_rolling_mean)
        .reset_index(level=0, drop=True)
    )
        
    # Transformations and Interactions
    df["log_gdp_pc"] = np.log(df["gdp_pc"])
    df["log_gdp_pc_lag1"] = np.log(df["gdp_pc_lag1"])

    df["gdp_pc_rel_world"] = df["gdp_pc"] / df.groupby("year")["gdp_pc"].transform("mean")

    df["era_globalization"] = (df["year"] >= 1990).astype(int)

    df["hc_x_tfp"] = df["hc"] * df["rtfpna"]
    df["hc_x_investment"] = df["hc"] * df["csh_i"]
    df["trade_x_hc"] = df["trade_open"] * df["hc"]


    # Investment and Capital Dynamics
    if "delta" in df.columns:
        df["net_investment"] = df["csh_i"] - df["delta"]
    else:
        df["net_investment"] = df["csh_i"]  # Assume no depreciation if delta missing
    df["capital_intensity"] = df["rkna"] / df["rgdpo"]

    df["k_per_worker_growth"] = df.groupby("countrycode")["k_per_worker"].pct_change() * 100

    df["investment_efficiency"] = df["rtfpna"] / df["csh_i"]
        

    # Labor Market Dynamics
    df["labsh_growth"] = df.groupby("countrycode")["labsh"].pct_change() * 100

    df["hc_returns"] = (df["gdp_per_eff_worker"] - df["gdp_pw"]) / df["gdp_pw"]

    df["dependency_ratio"] = df["pop"] / df["emp"]
        

    # Price Level Comparisons
    df["rel_price_level"] = df["pl_gdpo"]

    df["terms_of_trade"] = df["pl_x"] / df["pl_m"]

    df["investment_price"] = df["pl_i"]

    df["penn_effect"] = df["log_gdp_pc"] * df["pl_gdpo"]
        

    # Convergence Analysis
    frontier_gdp = df.groupby("year")["gdp_pc"].transform("max")
    df["dist_from_frontier"] = frontier_gdp - df["gdp_pc"]

    df["catchup_speed"] = (df["gdp_pc"] - df["gdp_pc_lag1"]) / (frontier_gdp - df["gdp_pc_lag1"])

    df["rel_to_frontier"] = df["gdp_pc"] / frontier_gdp
        
    # TFP and Efficiency Measures
    us_data = df[df["countrycode"] == "USA"]
    if not us_data.empty:
        us_tfp = us_data.set_index("year")["rtfpna"]
        df["tfp_rel_us"] = df.apply(lambda row: row["rtfpna"] / us_tfp.get(row["year"], np.nan) if pd.notna(row["rtfpna"]) else np.nan, axis=1)
    else:
        df["tfp_rel_us"] = np.nan

    # Handle missing rwtfpna column
    if "rwtfpna" in df.columns:
        df["welfare_tfp"] = df["rwtfpna"]
    else:
        df["welfare_tfp"] = np.nan

    df["tfp_growth_accel"] = df.groupby("countrycode")["rtfpna_growth"].diff()
        

    # Volatility and Crisis Indicators
    def safe_rolling_std(group):
        if len(group) > 0:
            return group.rolling(window=5, min_periods=1).std()
        else:
            return pd.Series(dtype=float, index=group.index)
    
    df["growth_volatility"] = (
        df.groupby("countrycode")["gdp_pc_growth"]
        .apply(safe_rolling_std)
        .reset_index(level=0, drop=True)
    )

    df["recession_dummy"] = (df["gdp_pc_growth"] < 0).astype(int)
    df["recession_count"] = df.groupby("countrycode")["recession_dummy"].cumsum()

    df["crisis_dummy"] = (df["gdp_pc_growth"] < -3).astype(int)
     
    return df