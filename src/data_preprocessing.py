"""
Data preprocessing and feature engineering utilities
"""

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.impute import SimpleImputer


def split_train_test(X, y, test_size=0.25, random_state=42):
    """
    Split data into train and test sets

    Args:
        X: Features
        y: Labels
        test_size: Proportion for test set
        random_state: Random seed for reproducibility

    Returns:
        tuple: X_train, X_test, y_train, y_test
    """
    return train_test_split(X, y, test_size=test_size,
                           random_state=random_state, stratify=y)


def impute_missing(X, strategy='median'):
    """
    Impute missing values

    Args:
        X: Feature matrix
        strategy: Imputation strategy ('median', 'mean', 'most_frequent')

    Returns:
        tuple: (Imputed data, fitted imputer)
    """
    imputer = SimpleImputer(strategy=strategy)
    X_imputed = imputer.fit_transform(X)
    return X_imputed, imputer


def normalize_features(X, method='standard'):
    """
    Normalize features

    Args:
        X: Feature matrix
        method: Normalization method ('standard', 'minmax')

    Returns:
        tuple: (Normalized data, fitted scaler)
    """
    if method == 'standard':
        from sklearn.preprocessing import StandardScaler
        scaler = StandardScaler()
    elif method == 'minmax':
        from sklearn.preprocessing import MinMaxScaler
        scaler = MinMaxScaler()
    else:
        raise ValueError(f"Unknown method: {method}")

    X_scaled = scaler.fit_transform(X)
    return X_scaled, scaler


def extract_feature_groups(df, group_type):
    """
    Extract features by category

    Args:
        df: PPMI dataframe
        group_type: Feature group ('biomarker', 'imaging', 'updrs', 'cognitive', 'genetic')

    Returns:
        list: Column names for the specified group
    """
    group_patterns = {
        'biomarker': ['tau', 'abeta', 'synuclein', 'urate', 'neurofilament', 'plasma', 'csf', 'serum'],
        'imaging': ['caudate', 'putamen', 'striatum', 'datscan'],
        'updrs': ['updrs'],
        'cognitive': ['moca', 'hvlt', 'naming', 'clock', 'trail', 'letter', 'symbol', 'benton'],
        'genetic': ['apoe']
    }

    if group_type not in group_patterns:
        raise ValueError(f"Unknown group type: {group_type}")

    patterns = group_patterns[group_type]
    cols = [col for col in df.columns
            if any(pattern in col.lower() for pattern in patterns)]
    return cols
