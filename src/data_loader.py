"""
Data loading utilities for PPMI dataset
"""

import pandas as pd
from pathlib import Path


def load_ppmi_data(data_dir='PPMI_Curated_Data_Cut_Public_20250321'):
    """
    Load main PPMI dataset

    Args:
        data_dir: Path to data directory

    Returns:
        pd.DataFrame: Main PPMI data
    """
    data_path = Path(data_dir) / '20250310-Table 1.csv'
    return pd.read_csv(data_path)


def load_data_dictionary(data_dir='PPMI_Curated_Data_Cut_Public_20250321'):
    """
    Load data dictionary with variable definitions

    Args:
        data_dir: Path to data directory

    Returns:
        pd.DataFrame: Data dictionary
    """
    dict_path = Path(data_dir) / 'Data dictionary-Table 1.csv'
    return pd.read_csv(dict_path)


def filter_by_visit(df, visit_ids):
    """
    Filter data by visit event IDs

    Args:
        df: PPMI dataframe
        visit_ids: List of visit IDs (e.g., ['BL', 'V04', 'V06'])

    Returns:
        pd.DataFrame: Filtered data
    """
    if isinstance(visit_ids, str):
        visit_ids = [visit_ids]
    return df[df['EVENT_ID'].isin(visit_ids)].copy()


def filter_by_cohort(df, cohorts):
    """
    Filter data by patient cohort

    Args:
        df: PPMI dataframe
        cohorts: List of cohorts (e.g., ['PD', 'HC'])

    Returns:
        pd.DataFrame: Filtered data
    """
    if isinstance(cohorts, str):
        cohorts = [cohorts]
    return df[df['COHORT'].isin(cohorts)].copy()


def get_unique_patients(df):
    """
    Get unique patient IDs

    Args:
        df: PPMI dataframe

    Returns:
        list: Unique patient numbers
    """
    return df['PATNO'].unique().tolist()
