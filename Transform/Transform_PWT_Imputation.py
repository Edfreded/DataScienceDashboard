import pandas as pd
import numpy as np
import warnings


def pwt_impute(df):
    # Create proxy for rkna based on rnna (scaled within country)
    df['rkna_proxy'] = df.groupby('countrycode', observed=True)['rnna'].transform(
        lambda x: x / x.max() if pd.notna(x.max()) and x.max() != 0 else np.nan
    )

    # 1. Employment (emp) - interpolation only
    df = impute_timeseries(df, 'emp', use_proxy=False)

    # 2. Human Capital (hc) - interpolation + global mean
    df = impute_timeseries(df, 'hc', use_proxy=False)

    # For countries still fully missing, use year-based global mean
    if df['hc'].isna().any():
        global_mean = df.groupby('year', observed=True)['hc'].transform(lambda x: x.mean(skipna=True))
        mask = df['hc'].isna()
        df.loc[mask, 'hc'] = global_mean[mask]
        df.loc[mask, 'i_hc'] = 5

    # 3. Real Capital Stock (rkna) - with proxy
    df = impute_timeseries(df, 'rkna', proxy_var='rkna_proxy', use_proxy=True)

    # 4. Net Capital Stock (rnna) - with rgdpo proxy
    df = impute_timeseries(df, 'rnna', proxy_var='rgdpo', use_proxy=True)

    # 5. Labor Share (labsh) - DO NOT use proxy (it creates invalid values)
    # Labor share should stay within [0, 1] bounds, so we use interpolation only
    df = impute_timeseries(df, 'labsh', use_proxy=False)




    # 6. Total Factor Productivity (rtfpna)
    df = df.sort_values(['countrycode','year'])
    df = impute_rtfpna(df)




    # Remove countries with fully missing series (even after imputation)
    vars_to_check = ['emp', 'hc', 'rkna', 'rnna', 'labsh']

    for var in vars_to_check:
        full_missing = df.groupby('countrycode', observed=True)[var].apply(lambda x: x.isna().all())
        drop_countries = full_missing[full_missing].index.tolist()
        
        if drop_countries:
            df = df[~df['countrycode'].isin(drop_countries)]




    # Check for implausible economic ratios
    df['ky_ratio'] = df['rnna'] / df['rgdpo']  # Capital-output ratio
    df['kl_ratio'] = df['rnna'] / df['emp']     # Capital-labor ratio

    # Calculate share of implausible observations per country
    implausible_share = (
        df.groupby('countrycode', observed=True)
        .apply(lambda g: (
            (g['labsh'] < 0.05) | (g['labsh'] > 1) | 
            (g['ky_ratio'] < 0.3) | (g['ky_ratio'] > 20)
        ).mean())
    )
    implausible_share = implausible_share.reset_index(name='implausible_share')

    # Drop countries with >50% implausible observations
    to_drop = implausible_share.loc[implausible_share['implausible_share'] > 0.5, 'countrycode']

    if len(to_drop) > 0:
        df = df[~df['countrycode'].isin(to_drop)]




    # Remove temporary columns
    df = df.drop(columns=['rkna_proxy', 'ky_ratio', 'kl_ratio'], errors='ignore')

    return df



def impute_rtfpna(df, group_col='countrycode'):
    """
    Reconstructs and imputes rtfpna using the production-function residual,
    aligns scale to PWT where overlapping, anchors to 2021=1 otherwise,
    and falls back to global mean TFP growth if needed.

    Flags in i_rtfpna:
      0 = original kept
      1 = residual from inputs (scaled)
      2 = log-linear interpolation
      5 = global mean growth proxy
    """
    out = df.copy()
    flag = 'i_rtfpna'
    if flag not in out.columns:
        out[flag] = 0

    # Safety clips to avoid invalid logs
    eps = 1e-12
    for v in ['rgdpo','rnna','emp','hc']:
        out[v] = out[v].astype(float)
        out[v] = out[v].where(out[v] > 0, np.nan)

    # Compute alpha = capital share = 1 - labsh (clip to sensible range)
    alpha = (1 - out['labsh'].astype(float)).clip(0.05, 0.95)

    # Log residual: logA = logY - alpha*logK - (1-alpha)*(logL + logH)
    logY = np.log(out['rgdpo'])
    logK = np.log(out['rnna'])
    logL = np.log(out['emp'])
    logH = np.log(out['hc'])
    logA = logY - alpha * logK - (1 - alpha) * (logL + logH)
    A_raw = np.exp(logA)

    # Precompute global mean growth of A_raw by year for fallback
    tmp = out[['year']].copy()
    tmp['A_raw'] = A_raw
    global_growth = (
        tmp.sort_values('year')
           .groupby('year', observed=True)['A_raw']
           .apply(lambda s: np.nan if s.isna().all() else s.pct_change(fill_method=None).median(skipna=True))
           .fillna(0.0)  # if a year has no info, assume 0 growth
    )

    def process_country(g):
        g = g.sort_values('year').copy()
        a_raw = A_raw.loc[g.index]

        # If any original rtfpna exists, align scale on overlap
        orig = g['rtfpna']
        has_orig = orig.notna().any()
        has_raw = a_raw.notna().any()

        if has_raw:
            if has_orig and (orig.notna() & a_raw.notna()).any():
                s = np.median((orig / a_raw)[orig.notna() & a_raw.notna()])
                a_scaled = a_raw * s
            else:
                # Anchor to 2021 = 1 if present, else last available year = 1
                if (g['year'] == 2021).any():
                    idx_2021 = g.index[g['year'] == 2021][0]
                    base = a_raw.loc[idx_2021]
                    s = 1.0 / base if pd.notna(base) and base > 0 else 1.0
                else:
                    last_idx = a_raw.dropna().index[-1]
                    base = a_raw.loc[last_idx]
                    s = 1.0 / base if pd.notna(base) and base > 0 else 1.0
                a_scaled = a_raw * s
        else:
            a_scaled = pd.Series(index=g.index, dtype=float)

        # Start from original
        out_series = orig.copy()
        # Fill using residual where original is missing
        fill_mask = out_series.isna() & a_scaled.notna()
        out_series.loc[fill_mask] = a_scaled.loc[fill_mask]
        g.loc[fill_mask, 'i_rtfpna'] = 1

        # Interpolate remaining gaps in log space
        if out_series.isna().any():
            with np.errstate(invalid='ignore'):
                ln = np.log(out_series)
            ln_interp = ln.interpolate(method='linear', limit_direction='both')
            new_mask = out_series.isna() & ln_interp.notna()
            out_series.loc[new_mask] = np.exp(ln_interp.loc[new_mask])
            g.loc[new_mask, 'i_rtfpna'] = 2
        
        # Country-specific chaining using own residual growth, before global fallback
        if out_series.isna().any():
            # country log TFP growth from residual
            with np.errstate(invalid='ignore'):
                ga = np.log(a_raw).diff()  # Δlog A_raw, country-specific

            years = g['year'].values
            # choose an anchor: if any original or scaled residual level exists, use the first available
            if out_series.notna().any():
                anchor_idx = out_series.dropna().index[0]
                anchor_level = out_series.loc[anchor_idx]
            else:
                # if nothing yet, set anchor to 2021 if present, else first year, level 1.0
                if (g['year'] == 2021).any():
                    anchor_idx = g.index[g['year'] == 2021][0]
                else:
                    anchor_idx = g.index.min()
                anchor_level = 1.0
                out_series.loc[anchor_idx] = anchor_level
                g.loc[anchor_idx, 'i_rtfpna'] = 1

            # forward chain using country growth
            ordered = g.index.sort_values()
            passed_anchor = False
            for idx in ordered:
                if idx == anchor_idx:
                    passed_anchor = True
                    continue
                if passed_anchor and pd.isna(out_series.loc[idx]):
                    py = g.index[g.index.get_loc(idx) - 1]
                    if pd.notna(out_series.loc[py]) and pd.notna(ga.loc[idx]):
                        out_series.loc[idx] = out_series.loc[py] * np.exp(ga.loc[idx])
                        g.loc[idx, 'i_rtfpna'] = 1

            # backward chain using country growth
            for idx in ordered[::-1]:
                if idx == anchor_idx:
                    break
                ny_pos = g.index.get_loc(idx) + 1
                if ny_pos < len(ordered):
                    ny = ordered[ny_pos]
                    if pd.isna(out_series.loc[idx]) and pd.notna(out_series.loc[ny]) and pd.notna(ga.loc[ny]):
                        out_series.loc[idx] = out_series.loc[ny] / np.exp(ga.loc[ny])
                        g.loc[idx, 'i_rtfpna'] = 1

        # Global-growth fallback if still entirely empty or has NaNs
        if out_series.isna().any():
            # Build a chain from an anchor using global median growth by year
            years = g['year'].values
            # Choose anchor: 2021 if available, else first nonmissing year in series
            if (years == 2021).any():
                anchor_year = 2021
            else:
                anchor_year = years[np.isfinite(years)].min()
            # If anchor level missing, set to 1.0
            if out_series[g.index[g['year'] == anchor_year]].isna().all():
                out_series.loc[g.index[g['year'] == anchor_year]] = 1.0
                g.loc[g.index[g['year'] == anchor_year], 'i_rtfpna'] = 5

            # Forward chain
            for y in sorted(years):
                idx = g.index[g['year'] == y][0]
                if pd.isna(out_series.loc[idx]):
                    prev_years = years[years < y]
                    if len(prev_years) > 0:
                        py = prev_years.max()
                        pidx = g.index[g['year'] == py][0]
                        if pd.notna(out_series.loc[pidx]):
                            gy = global_growth.get(y, 0.0)
                            out_series.loc[idx] = out_series.loc[pidx] * (1.0 + (0.0 if pd.isna(gy) else gy))
                            g.loc[idx, 'i_rtfpna'] = 5

            # Backward chain
            for y in sorted(years, reverse=True):
                idx = g.index[g['year'] == y][0]
                if pd.isna(out_series.loc[idx]):
                    next_years = years[years > y]
                    if len(next_years) > 0:
                        ny = next_years.min()
                        nidx = g.index[g['year'] == ny][0]
                        if pd.notna(out_series.loc[nidx]):
                            gy = global_growth.get(ny, 0.0)
                            out_series.loc[idx] = out_series.loc[nidx] / (1.0 + (0.0 if pd.isna(gy) else gy))
                            g.loc[idx, 'i_rtfpna'] = 5

        g['rtfpna'] = out_series
        return g

    out = out.groupby(group_col, group_keys=False, observed=True).apply(process_country)
    return out



# Main Imputation Function
def impute_timeseries(df, var, group_col='countrycode', proxy_var=None, use_proxy=True):
    """
    Hierarchical imputation for time series data.

    Imputation flag meanings:
        0 = Original data
        1 = Log-linear interpolation
        2 = Linear interpolation
        3 = Growth-rate extrapolation (short edges)
        4 = Constant fill (LOCF/BOCF)
        5 = Proxy-based substitution (for completely missing series)

    Parameters
    ----------
    df : pd.DataFrame
        Input dataset.
    var : str
        Variable name to impute.
    group_col : str
        Grouping column (e.g., 'countrycode').
    proxy_var : str, optional
        Proxy variable for substitution of entirely missing series.
    use_proxy : bool, default True
        Whether to apply proxy substitution.

    Returns
    -------
    pd.DataFrame
        Dataset with imputed variable and flag column.
    """
    df = df.copy()
    flag_col = f"i_{var}"
    df[flag_col] = 0  # Initialize flag

    def _impute_group(g):
        """Apply hierarchical imputation to a single group."""
        x = g[var].copy()

        # (1) Log-linear interpolation
        try:
            mask = x.isna()
            if (x > 0).sum() > 1:  # Need at least 2 positive values
                log_x = np.log(x)
                log_interp = log_x.interpolate(method='linear', limit_direction='both')
                new_x = np.exp(log_interp)
                g.loc[mask & new_x.notna(), flag_col] = 1
                x = x.fillna(new_x)
        except Exception:
            pass

        # (2) Linear interpolation
        if x.isna().sum() > 0:
            lin_interp = x.interpolate(method='linear', limit_direction='both')
            newly_filled = x.isna() & lin_interp.notna()
            g.loc[newly_filled, flag_col] = 2
            x = x.fillna(lin_interp)

        # (3) Growth-rate extrapolation (for edge gaps)
        if x.isna().sum() > 0:
            valid = x.dropna()
            if len(valid) >= 2:
                avg_growth = valid.pct_change(fill_method=None).mean()
                first_valid = x.first_valid_index()
                last_valid = x.last_valid_index()

                # Backward extrapolation
                if first_valid is not None:
                    before = x.loc[:first_valid].iloc[:-1]
                    for i in before.index[::-1]:
                        next_idx = x.index.get_loc(i) + 1
                        if next_idx < len(x):
                            next_val = x.iloc[next_idx]
                            if pd.notna(next_val):
                                x.loc[i] = next_val / (1 + avg_growth)
                                g.loc[i, flag_col] = 3

                # Forward extrapolation
                if last_valid is not None:
                    after = x.loc[last_valid:]
                    for i in after.index[1:]:
                        prev_idx = x.index.get_loc(i) - 1
                        if prev_idx >= 0:
                            prev_val = x.iloc[prev_idx]
                            if pd.notna(prev_val):
                                x.loc[i] = prev_val * (1 + avg_growth)
                                g.loc[i, flag_col] = 3

        # (4) Constant fill (LOCF/BOCF)
        if x.isna().sum() > 0:
            ffilled = x.ffill().bfill()
            newly_filled = x.isna() & ffilled.notna()
            g.loc[newly_filled, flag_col] = 4
            x = x.fillna(ffilled)

        # Update the original column
        g[var] = x
        return g

    # Apply imputation per group
    df = df.groupby(group_col, group_keys=False, observed=True).apply(_impute_group)

    # (5) Proxy-based substitution for entirely missing series
    if use_proxy and proxy_var is not None and proxy_var in df.columns:
        # Compute median ratio var/proxy_var where both exist
        ratio = (df[var] / df[proxy_var]).replace([np.inf, -np.inf], np.nan)
        median_ratio = ratio.median(skipna=True)

        # Only proceed if median ratio is meaningful
        if pd.notna(median_ratio) and median_ratio > 0:
            # Identify countries with no valid data
            missing_countries = (
                df.groupby(group_col, observed=True)[var]
                .apply(lambda x: x.notna().sum() == 0)
            )
            missing_countries = missing_countries[missing_countries].index.tolist()

            if missing_countries:
                for c in missing_countries:
                    mask = df[group_col] == c
                    df.loc[mask, var] = df.loc[mask, proxy_var] * median_ratio
                    df.loc[mask, flag_col] = 5

    return df


