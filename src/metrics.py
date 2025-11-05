"""
Evaluation metrics and reporting utilities
"""

import pandas as pd
from sklearn.metrics import accuracy_score, roc_auc_score
from sklearn.metrics import confusion_matrix
import numpy as np


def calculate_sensitivity_specificity(y_true, y_pred, positive_label=1):
    """
    Calculate sensitivity and specificity

    Args:
        y_true: True labels
        y_pred: Predicted labels
        positive_label: Label considered as positive class

    Returns:
        tuple: (sensitivity, specificity)
    """
    cm = confusion_matrix(y_true, y_pred)

    if len(cm) == 2:
        tn, fp, fn, tp = cm.ravel()
        sensitivity = tp / (tp + fn) if (tp + fn) > 0 else 0
        specificity = tn / (tn + fp) if (tn + fp) > 0 else 0
    else:
        # Multi-class: macro-average
        sensitivities = []
        specificities = []
        for i in range(len(cm)):
            tp = cm[i, i]
            fn = cm[i, :].sum() - tp
            fp = cm[:, i].sum() - tp
            tn = cm.sum() - tp - fn - fp

            sens = tp / (tp + fn) if (tp + fn) > 0 else 0
            spec = tn / (tn + fp) if (tn + fp) > 0 else 0

            sensitivities.append(sens)
            specificities.append(spec)

        sensitivity = np.mean(sensitivities)
        specificity = np.mean(specificities)

    return sensitivity, specificity


def calculate_metrics(y_true, y_pred, y_prob=None):
    """
    Calculate comprehensive evaluation metrics

    Args:
        y_true: True labels
        y_pred: Predicted labels
        y_prob: Predicted probabilities (optional, for ROC AUC)

    Returns:
        dict: Dictionary of metrics
    """
    metrics = {}

    metrics['Accuracy'] = accuracy_score(y_true, y_pred)
    sensitivity, specificity = calculate_sensitivity_specificity(y_true, y_pred)
    metrics['Sensitivity'] = sensitivity
    metrics['Specificity'] = specificity

    if y_prob is not None:
        try:
            if len(np.unique(y_true)) == 2:
                metrics['ROC AUC'] = roc_auc_score(y_true, y_prob)
            else:
                metrics['ROC AUC'] = roc_auc_score(y_true, y_prob, multi_class='ovr')
        except ValueError:
            metrics['ROC AUC'] = None

    return metrics


def format_metric_table(metrics_dict, model_names=None):
    """
    Format metrics as a printable table

    Args:
        metrics_dict: Dict of {model_name: metrics_dict} or single metrics dict
        model_names: List of model names (if metrics_dict is not nested)

    Returns:
        pd.DataFrame: Formatted metrics table
    """
    if not isinstance(list(metrics_dict.values())[0], dict):
        metrics_dict = {model_names[0]: metrics_dict}

    df = pd.DataFrame(metrics_dict).T
    df.index.name = 'Model'
    return df


def compare_models(model_results):
    """
    Compare multiple model results

    Args:
        model_results: Dict of {model_name: {metric_name: value}}

    Returns:
        pd.DataFrame: Comparison table with differences
    """
    df = pd.DataFrame(model_results).T

    if len(df) == 2:
        diff = df.iloc[1] - df.iloc[0]
        diff.name = 'Difference'
        df = pd.concat([df, diff.to_frame().T])

    return df


def calculate_improvements(before, after):
    """
    Calculate metric improvements

    Args:
        before: Dict of metrics before change
        after: Dict of metrics after change

    Returns:
        dict: Improvement deltas
    """
    improvements = {}
    for key in before.keys():
        if key in after:
            improvements[key] = after[key] - before[key]
    return improvements
