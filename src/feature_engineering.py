"""
Feature engineering utilities for PPMI classification
"""

import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from scipy import stats


def check_skewness(series):
    """
    Calculate skewness of a feature

    Args:
        series: pandas Series

    Returns:
        float: Skewness value
    """
    return stats.skew(series.dropna())


def apply_transformation(series, transformation='log'):
    """
    Apply transformation to reduce skewness

    Args:
        series: pandas Series
        transformation: Type of transformation ('log', 'sqrt', 'boxcox', 'reciprocal')

    Returns:
        pandas Series: Transformed series
    """
    # Handle negative values by shifting
    min_val = series.min()
    if min_val <= 0 and transformation in ['log', 'sqrt']:
        series = series - min_val + 1

    if transformation == 'log':
        return np.log(series)
    elif transformation == 'sqrt':
        return np.sqrt(series)
    elif transformation == 'reciprocal':
        return 1 / (series + 1e-10)
    elif transformation == 'boxcox':
        if (series > 0).all():
            transformed, _ = stats.boxcox(series)
            return pd.Series(transformed, index=series.index)
        else:
            return series
    else:
        return series


def engineer_features(df, feature_cols, skewness_threshold=0.75):
    """
    Engineer features with normalization and transformation

    Args:
        df: DataFrame with features
        feature_cols: List of feature column names
        skewness_threshold: Threshold for applying transformation

    Returns:
        tuple: (engineered_df, feature_names, skewness_info)
    """
    engineered_data = {}
    feature_names = []
    skewness_info = []

    # Normalize original features
    scaler = StandardScaler()
    normalized = scaler.fit_transform(df[feature_cols])

    for i, col in enumerate(feature_cols):
        # Add normalized feature
        engineered_data[col] = normalized[:, i]
        feature_names.append(col)

        # Check skewness
        skew = check_skewness(df[col])
        skewness_info.append({
            'feature': col,
            'skewness': skew,
            'transformed': False,
            'transformation': None
        })

        # Apply transformation if highly skewed
        if abs(skew) > skewness_threshold:
            # Choose transformation based on skewness direction and magnitude
            if skew > 0:  # Right skewed
                if abs(skew) > 2:
                    transformation = 'log'
                elif abs(skew) > 1:
                    transformation = 'sqrt'
                else:
                    transformation = 'log'
            else:  # Left skewed
                transformation = 'reciprocal'

            # Apply transformation
            try:
                transformed = apply_transformation(df[col].copy(), transformation)
                # Normalize transformed feature
                transformed_norm = StandardScaler().fit_transform(transformed.values.reshape(-1, 1)).flatten()

                col_enhanced = f"{col}_enhance"
                engineered_data[col_enhanced] = transformed_norm
                feature_names.append(col_enhanced)

                # Update skewness info
                new_skew = check_skewness(transformed)
                skewness_info[-1]['transformed'] = True
                skewness_info[-1]['transformation'] = transformation
                skewness_info[-1]['new_skewness'] = new_skew
            except:
                pass

    return pd.DataFrame(engineered_data), feature_names, skewness_info


def add_aggregate_features(df, feature_cols):
    """
    Add aggregate statistics as features

    Args:
        df: DataFrame with features
        feature_cols: List of feature column names

    Returns:
        pd.DataFrame: DataFrame with added aggregate features
    """
    df_copy = df.copy()

    # Calculate aggregates per sample
    df_copy['feat_mean'] = df[feature_cols].mean(axis=1)
    df_copy['feat_max'] = df[feature_cols].max(axis=1)
    df_copy['feat_min'] = df[feature_cols].min(axis=1)
    df_copy['feat_std'] = df[feature_cols].std(axis=1)
    df_copy['feat_range'] = df_copy['feat_max'] - df_copy['feat_min']

    return df_copy


def get_feature_combination(df, combination_name):
    """
    Extract features based on combination name

    Args:
        df: Full PPMI DataFrame
        combination_name: Name of combination

    Returns:
        list: Feature column names for this combination
    """
    from .data_preprocessing import extract_feature_groups

    biomarker_cols = extract_feature_groups(df, 'biomarker')
    updrs_cols = extract_feature_groups(df, 'updrs')
    cognitive_cols = extract_feature_groups(df, 'cognitive')

    # Clinical assessments = UPDRS + cognitive
    clinical_cols = list(set(updrs_cols + cognitive_cols))

    # Disease progression features (milestone indicators)
    progression_cols = [col for col in df.columns if col.startswith('pm_')]

    combinations = {
        'Biomarkers': biomarker_cols,
        'Clinical': clinical_cols,
        'Progression': progression_cols,
        'Bio+Clinical': biomarker_cols + clinical_cols,
        'Bio+Progression': biomarker_cols + progression_cols,
        'Clinical+Progression': clinical_cols + progression_cols,
        'All': biomarker_cols + clinical_cols + progression_cols
    }

    return combinations.get(combination_name, [])


def prepare_feature_combination(df, combination_name, add_aggregates=True, skewness_threshold=0.75):
    """
    Prepare features for a specific combination

    Args:
        df: Full PPMI DataFrame
        combination_name: Name of combination
        add_aggregates: Whether to add aggregate features
        skewness_threshold: Threshold for transformation

    Returns:
        tuple: (X, feature_info)
    """
    # Get feature columns for this combination
    feature_cols = get_feature_combination(df, combination_name)

    # Filter to numeric features and drop all-NaN columns
    feature_cols = [col for col in feature_cols if col in df.columns]
    df_subset = df[feature_cols].select_dtypes(include=[np.number])
    df_subset = df_subset.dropna(axis=1, how='all')
    feature_cols = df_subset.columns.tolist()

    if len(feature_cols) == 0:
        return None, None

    # Fill NaN with median before engineering
    df_filled = df[feature_cols].copy()
    df_filled = df_filled.fillna(df_filled.median())

    # Engineer features
    X_engineered, feature_names, skewness_info = engineer_features(df_filled, feature_cols, skewness_threshold)

    # Add aggregates if requested
    if add_aggregates and len(feature_cols) > 1:
        X_engineered = add_aggregate_features(X_engineered, feature_cols)
        feature_names.extend(['feat_mean', 'feat_max', 'feat_min', 'feat_std', 'feat_range'])

    # Final check: ensure no NaN values remain
    X_engineered = X_engineered.fillna(0)

    feature_info = {
        'combination': combination_name,
        'n_original_features': len(feature_cols),
        'n_total_features': len(feature_names),
        'skewness_info': skewness_info
    }

    return X_engineered, feature_info
