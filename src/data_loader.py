"""
Data loading utilities for PPMI dataset
"""

import pandas as pd
from pathlib import Path

# COHORT code mapping
COHORT_CODES = {
    'PD': 1,
    'HC': 2,
    'SWEDD': 3,
    'Prodromal': 4,
    1: 1,
    2: 2,
    3: 3,
    4: 4
}


def load_ppmi_data(data_dir='PPMI_Curated_Data_Cut_Public_20250321'):
    """
    Load main PPMI dataset

    Args:
        data_dir: Path to data directory

    Returns:
        pd.DataFrame: Main PPMI data
    """
    data_path = Path(data_dir) / '20250310-Table 1.csv'

    # If path doesn't exist, try relative to project root
    if not data_path.exists():
        # Find project root by looking for pyproject.toml
        current = Path.cwd()
        for parent in [current] + list(current.parents):
            if (parent / 'pyproject.toml').exists():
                data_path = parent / data_dir / '20250310-Table 1.csv'
                break

    return pd.read_csv(data_path, low_memory=False)


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
        cohorts: List of cohorts (e.g., ['PD', 'HC'] or [1, 2])

    Returns:
        pd.DataFrame: Filtered data
    """
    if isinstance(cohorts, str):
        cohorts = [cohorts]

    # Convert string cohort names to integer codes
    cohort_codes = [COHORT_CODES.get(c, c) for c in cohorts]

    return df[df['COHORT'].isin(cohort_codes)].copy()


def get_unique_patients(df):
    """
    Get unique patient IDs

    Args:
        df: PPMI dataframe

    Returns:
        list: Unique patient numbers
    """
    return df['PATNO'].unique().tolist()
