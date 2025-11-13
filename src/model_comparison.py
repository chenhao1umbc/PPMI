"""
Model comparison utilities for multi-class classification
"""

import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.model_selection import StratifiedKFold, cross_validate
from sklearn.metrics import make_scorer, accuracy_score
from xgboost import XGBClassifier
from lightgbm import LGBMClassifier

from .metrics import calculate_sensitivity_specificity


def sensitivity_score(y_true, y_pred):
    """Calculate sensitivity score"""
    sens, _ = calculate_sensitivity_specificity(y_true, y_pred)
    return sens


def specificity_score(y_true, y_pred):
    """Calculate specificity score"""
    _, spec = calculate_sensitivity_specificity(y_true, y_pred)
    return spec


def get_models():
    """
    Get dictionary of models to compare

    Returns:
        dict: Model name to model instance mapping
    """
    models = {
        'Logistic Regression': LogisticRegression(max_iter=5000, random_state=42),
        'Random Forest': RandomForestClassifier(n_estimators=100, random_state=42),
        'Gradient Boosting': GradientBoostingClassifier(n_estimators=100, random_state=42),
        'XGBoost': XGBClassifier(n_estimators=100, random_state=42, eval_metric='mlogloss'),
        'LightGBM': LGBMClassifier(n_estimators=100, random_state=42, verbose=-1)
    }
    return models


def run_cross_validation(X, y, n_splits=5, random_state=42):
    """
    Run k-fold cross-validation for multiple models

    Args:
        X: Feature matrix
        y: Labels
        n_splits: Number of CV folds
        random_state: Random seed

    Returns:
        dict: Results for each model
    """
    # Relabel classes to start from 0 for XGBoost compatibility
    unique_classes = np.unique(y)
    class_mapping = {old: new for new, old in enumerate(unique_classes)}
    y_relabeled = np.array([class_mapping[val] for val in y])

    models = get_models()

    # Define scorers
    scoring = {
        'accuracy': make_scorer(accuracy_score),
        'sensitivity': make_scorer(sensitivity_score),
        'specificity': make_scorer(specificity_score)
    }

    # Cross-validation
    cv = StratifiedKFold(n_splits=n_splits, shuffle=True, random_state=random_state)

    results = {}
    for name, model in models.items():
        cv_results = cross_validate(
            model, X, y_relabeled, cv=cv, scoring=scoring,
            return_train_score=True, n_jobs=-1
        )
        results[name] = {
            'train_accuracy': cv_results['train_accuracy'],
            'test_accuracy': cv_results['test_accuracy'],
            'test_sensitivity': cv_results['test_sensitivity'],
            'test_specificity': cv_results['test_specificity']
        }

    return results


def create_summary_dataframe(results):
    """
    Create summary DataFrame from cross-validation results

    Args:
        results: Dict of results from run_cross_validation

    Returns:
        pd.DataFrame: Summary table sorted by accuracy
    """
    summary = []
    for name, metrics in results.items():
        summary.append({
            'Model': name,
            'Accuracy': f"{metrics['test_accuracy'].mean():.4f} +/- {metrics['test_accuracy'].std():.4f}",
            'Sensitivity': f"{metrics['test_sensitivity'].mean():.4f} +/- {metrics['test_sensitivity'].std():.4f}",
            'Specificity': f"{metrics['test_specificity'].mean():.4f} +/- {metrics['test_specificity'].std():.4f}",
            'Accuracy_mean': metrics['test_accuracy'].mean()
        })

    return pd.DataFrame(summary).sort_values('Accuracy_mean', ascending=False)
