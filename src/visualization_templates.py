"""
High-level visualization templates combining multiple modules
"""

import pandas as pd
from .plotting import (create_performance_comparison_plot,
                       create_feature_impact_plot,
                       create_temporal_trend_plot)
from .metrics import format_metric_table


def generate_model_comparison_report(model_results, output_path='figures/model_comparison'):
    """
    Generate complete model comparison report with plots and tables

    Args:
        model_results: Dict of {model_name: {'train': metrics, 'test': metrics}}
        output_path: Base path for output files

    Returns:
        pd.DataFrame: Summary table
    """
    # Prepare data for plotting
    data = {'Model': []}
    for model_name, results in model_results.items():
        data['Model'].append(model_name)
        for metric, value in results['train'].items():
            col_name = f'Train {metric}'
            if col_name not in data:
                data[col_name] = []
            data[col_name].append(value)
        for metric, value in results['test'].items():
            col_name = f'Test {metric}'
            if col_name not in data:
                data[col_name] = []
            data[col_name].append(value)

    df = pd.DataFrame(data)

    # Identify test and train metrics
    test_cols = [c for c in df.columns if c.startswith('Test ')]
    train_cols = [c for c in df.columns if c.startswith('Train ')]

    # Create visualization
    create_performance_comparison_plot(
        df, test_cols, train_cols,
        output_path=output_path,
        title='Model Performance Comparison'
    )

    # Print summary
    print("\nModel Performance Summary:")
    print(df.to_string(index=False))

    return df


def generate_feature_impact_report(lr_results, rf_results, feature_name,
                                   output_path='figures/feature_impact'):
    """
    Generate feature impact analysis report

    Args:
        lr_results: Dict with 'without' and 'with' metrics for LR
        rf_results: Dict with 'without' and 'with' metrics for RF
        feature_name: Name of the feature being analyzed
        output_path: Base path for output files

    Returns:
        tuple: (lr_df, rf_df) DataFrames with impact analysis
    """
    # Prepare LR data
    lr_data = {
        'Metric': ['Test Accuracy', 'Test Sensitivity', 'Test Specificity'],
        f'Without {feature_name}': [
            lr_results['without']['Accuracy'],
            lr_results['without']['Sensitivity'],
            lr_results['without']['Specificity']
        ],
        f'With {feature_name}': [
            lr_results['with']['Accuracy'],
            lr_results['with']['Sensitivity'],
            lr_results['with']['Specificity']
        ]
    }
    lr_df = pd.DataFrame(lr_data)
    lr_df['Change'] = lr_df[f'With {feature_name}'] - lr_df[f'Without {feature_name}']

    # Prepare RF data
    rf_data = {
        'Metric': ['Test Accuracy', 'Test Sensitivity', 'Test Specificity'],
        f'Without {feature_name}': [
            rf_results['without']['Accuracy'],
            rf_results['without']['Sensitivity'],
            rf_results['without']['Specificity']
        ],
        f'With {feature_name}': [
            rf_results['with']['Accuracy'],
            rf_results['with']['Sensitivity'],
            rf_results['with']['Specificity']
        ]
    }
    rf_df = pd.DataFrame(rf_data)
    rf_df['Change'] = rf_df[f'With {feature_name}'] - rf_df[f'Without {feature_name}']

    # Create visualization
    create_feature_impact_plot(lr_df, rf_df, output_path=output_path)

    # Print summary
    print(f"\nLogistic Regression - {feature_name} Impact:")
    print(lr_df.to_string(index=False))
    print(f"\nRandom Forest - {feature_name} Impact:")
    print(rf_df.to_string(index=False))

    return lr_df, rf_df


def generate_temporal_analysis_report(visit_results, baseline=None,
                                      output_path='figures/temporal'):
    """
    Generate temporal progression analysis report

    Args:
        visit_results: Dict of {visit_id: metrics} or DataFrame
        baseline: Baseline accuracy (optional)
        output_path: Base path for output files

    Returns:
        pd.DataFrame: Temporal progression data
    """
    if isinstance(visit_results, dict):
        # Convert dict to DataFrame
        data = {
            'Visit': list(visit_results.keys()),
            'Test Accuracy': [results.get('Accuracy', 0) for results in visit_results.values()]
        }
        df = pd.DataFrame(data)

        # Extract visit numbers for plotting
        df['Visit Number'] = df['Visit'].str.extract(r'V?(\d+)').astype(int)
    else:
        df = visit_results.copy()
        if 'Visit Number' not in df.columns:
            df['Visit Number'] = df['Visit'].str.extract(r'V?(\d+)').astype(int)

    # Create visualization
    create_temporal_trend_plot(
        df, 'Visit Number', 'Test Accuracy',
        baseline=baseline,
        output_path=output_path,
        title='Temporal Progression of Classification Accuracy\n(3-Label Parkinson\'s Disease Classification)',
        xlabel='Visit Number',
        ylabel='Test Accuracy'
    )

    # Print summary
    print("\nVisit-Based Accuracy Summary:")
    print(df[['Visit', 'Test Accuracy']].to_string(index=False))

    if baseline is not None:
        print(f"\nBaseline Accuracy: {baseline:.2%}")

    if len(df) > 1:
        improvement = df['Test Accuracy'].iloc[-1] - df['Test Accuracy'].iloc[0]
        print(f"Improvement from {df['Visit'].iloc[0]} to {df['Visit'].iloc[-1]}: +{improvement:.1%}")

    return df
