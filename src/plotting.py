"""
Reusable plotting utilities for publication-quality figures
"""

import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path


def create_performance_comparison_plot(df, test_metrics, train_metrics,
                                       output_path='figures/comparison.png',
                                       title='Model Performance Comparison',
                                       model_col='Model', colors=None):
    """
    Create side-by-side bar charts comparing model performance

    Args:
        df: DataFrame with model performance data
        test_metrics: List of test metric column names
        train_metrics: List of train metric column names
        output_path: Output file path (will save .png and .pdf)
        title: Figure title
        model_col: Column name containing model names
        colors: List of colors for each model (default: green and blue)
    """
    if colors is None:
        colors = ['#4CAF50', '#2196F3']

    fig, axes = plt.subplots(1, 2, figsize=(12, 5))

    x = np.arange(len(test_metrics))
    width = 0.35

    # Prepare data for each model
    model_names = df[model_col].tolist()
    test_values = [[df[metric].iloc[i] for metric in test_metrics]
                   for i in range(len(model_names))]
    train_values = [[df[metric].iloc[i] for metric in train_metrics]
                    for i in range(len(model_names))]

    # Plot test performance
    for i, (name, values) in enumerate(zip(model_names, test_values)):
        offset = (i - len(model_names)/2 + 0.5) * width
        axes[0].bar(x + offset, values, width, label=name,
                   color=colors[i], alpha=0.8)

        for j, val in enumerate(values):
            axes[0].text(j + offset, val + 0.01, f'{val:.3f}',
                        ha='center', va='bottom', fontsize=9)

    axes[0].set_ylabel('Score', fontsize=12)
    axes[0].set_title('Test Set Performance', fontsize=14, fontweight='bold')
    axes[0].set_xticks(x)
    metric_labels = [m.replace('Test ', '') for m in test_metrics]
    axes[0].set_xticklabels(metric_labels, rotation=45, ha='right')
    axes[0].set_ylim([0.8, 1.05])
    axes[0].legend(loc='lower right', fontsize=10)
    axes[0].grid(axis='y', alpha=0.3)

    # Plot train performance
    for i, (name, values) in enumerate(zip(model_names, train_values)):
        offset = (i - len(model_names)/2 + 0.5) * width
        axes[1].bar(x + offset, values, width, label=name,
                   color=colors[i], alpha=0.8)

        for j, val in enumerate(values):
            axes[1].text(j + offset, val + 0.01, f'{val:.3f}',
                        ha='center', va='bottom', fontsize=9)

    axes[1].set_ylabel('Score', fontsize=12)
    axes[1].set_title('Training Set Performance', fontsize=14, fontweight='bold')
    axes[1].set_xticks(x)
    metric_labels = [m.replace('Train ', '') for m in train_metrics]
    axes[1].set_xticklabels(metric_labels, rotation=45, ha='right')
    axes[1].set_ylim([0.8, 1.05])
    axes[1].legend(loc='lower right', fontsize=10)
    axes[1].grid(axis='y', alpha=0.3)

    plt.tight_layout()
    save_figure(output_path)
    plt.close()


def create_feature_impact_plot(lr_df, rf_df, output_path='figures/feature_impact.png'):
    """
    Create side-by-side bar charts showing feature impact on two models

    Args:
        lr_df: DataFrame with logistic regression results (columns: Metric, Without X, With X, Change)
        rf_df: DataFrame with random forest results (columns: Metric, Without X, With X, Change)
        output_path: Output file path
    """
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    metrics = lr_df['Metric'].tolist()
    x = np.arange(len(metrics))
    width = 0.35

    # Plot 1: Logistic Regression
    without_col = [c for c in lr_df.columns if 'Without' in c][0]
    with_col = [c for c in lr_df.columns if 'With' in c][0]

    axes[0].bar(x - width/2, lr_df[without_col], width,
                label=without_col, color='#FF9800', alpha=0.8)
    axes[0].bar(x + width/2, lr_df[with_col], width,
                label=with_col, color='#FF5722', alpha=0.8)

    axes[0].set_ylabel('Score', fontsize=12)
    axes[0].set_title('Logistic Regression: Feature Impact', fontsize=14, fontweight='bold')
    axes[0].set_xticks(x)
    metric_labels = [m.replace('Test ', '') for m in metrics]
    axes[0].set_xticklabels(metric_labels, rotation=45, ha='right')
    axes[0].set_ylim([0.8, 1.05])
    axes[0].legend(fontsize=10)
    axes[0].grid(axis='y', alpha=0.3)

    # Add change annotations
    for i, change in enumerate(lr_df['Change']):
        color = 'red' if change < 0 else 'green'
        sign = '' if change < 0 else '+'
        axes[0].text(i, 1.02, f'{sign}{change:.4f}',
                    ha='center', va='bottom', fontsize=10,
                    color=color, fontweight='bold')

    # Plot 2: Random Forest
    axes[1].bar(x - width/2, rf_df[without_col], width,
                label=without_col, color='#2196F3', alpha=0.8)
    axes[1].bar(x + width/2, rf_df[with_col], width,
                label=with_col, color='#1976D2', alpha=0.8)

    axes[1].set_ylabel('Score', fontsize=12)
    axes[1].set_title('Random Forest: Feature Impact', fontsize=14, fontweight='bold')
    axes[1].set_xticks(x)
    axes[1].set_xticklabels(metric_labels, rotation=45, ha='right')
    axes[1].set_ylim([0.8, 1.05])
    axes[1].legend(fontsize=10)
    axes[1].grid(axis='y', alpha=0.3)

    # Add change annotations
    for i, change in enumerate(rf_df['Change']):
        color = 'red' if change < 0 else 'green'
        sign = '' if change < 0 else '+'
        axes[1].text(i, 1.02, f'{sign}{change:.4f}',
                    ha='center', va='bottom', fontsize=10,
                    color=color, fontweight='bold')

    plt.tight_layout()
    save_figure(output_path)
    plt.close()


def create_temporal_trend_plot(df, x_col, y_col, baseline=None,
                               output_path='figures/temporal.png',
                               title='Temporal Progression',
                               xlabel='Visit', ylabel='Accuracy'):
    """
    Create line plot showing temporal trends

    Args:
        df: DataFrame with temporal data
        x_col: Column name for x-axis
        y_col: Column name for y-axis
        baseline: Baseline value for reference line (optional)
        output_path: Output file path
        title: Plot title
        xlabel: X-axis label
        ylabel: Y-axis label
    """
    fig, ax = plt.subplots(figsize=(10, 6))

    ax.plot(df[x_col], df[y_col],
            marker='o', linewidth=2.5, markersize=10,
            color='#2196F3', label=f'{ylabel} over time')

    if baseline is not None:
        ax.axhline(y=baseline, color='red', linestyle='--',
                  linewidth=2, alpha=0.7,
                  label=f'Baseline ({baseline:.2%})')

    ax.set_xlabel(xlabel, fontsize=13, fontweight='bold')
    ax.set_ylabel(ylabel, fontsize=13, fontweight='bold')
    ax.set_title(title, fontsize=14, fontweight='bold')
    ax.set_xticks(df[x_col])
    ax.grid(True, alpha=0.3, linestyle='--')
    ax.legend(fontsize=11, loc='lower right')

    # Add value labels
    for i, row in df.iterrows():
        ax.text(row[x_col], row[y_col] + 0.008,
               f"{row[y_col]:.2%}",
               ha='center', va='bottom', fontsize=11, fontweight='bold')

    # Add improvement annotation if data available
    if len(df) > 1:
        improvement = df[y_col].iloc[-1] - df[y_col].iloc[0]
        mid_x = df[x_col].iloc[len(df)//2]
        mid_y = df[y_col].max() * 0.9
        ax.annotate(f'Improvement: +{improvement:.1%}',
                   xy=(df[x_col].iloc[-1], df[y_col].iloc[-1]),
                   xytext=(mid_x, mid_y),
                   fontsize=11,
                   bbox=dict(boxstyle='round,pad=0.5',
                            facecolor='lightgreen', alpha=0.7),
                   arrowprops=dict(arrowstyle='->',
                                 connectionstyle='arc3,rad=0.3', lw=1.5))

    plt.tight_layout()
    save_figure(output_path)
    plt.close()


def save_figure(output_path, dpi=300):
    """
    Save figure in both PNG and PDF formats

    Args:
        output_path: Output file path
        dpi: Resolution for PNG
    """
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    png_path = path.with_suffix('.png')
    pdf_path = path.with_suffix('.pdf')

    plt.savefig(png_path, dpi=dpi, bbox_inches='tight')
    plt.savefig(pdf_path, bbox_inches='tight')

    print(f"Figure saved: {png_path} and {pdf_path}")
