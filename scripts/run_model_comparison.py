"""
Model Performance Comparison: Logistic Regression vs Random Forest
Generates publication-quality comparison plot for Journal of Movement Disorders
"""

import pandas as pd
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.visualization_templates import generate_model_comparison_report

# Data from results (with MSEADL)
model_results = {
    'Logistic Regression': {
        'train': {
            'Accuracy': 0.928125,
            'Sensitivity': 0.90625,
            'Specificity': 0.95,
            'ROC AUC': 0.970693
        },
        'test': {
            'Accuracy': 0.87500,
            'Sensitivity': 0.8625,
            'Specificity': 0.8875,
            'ROC AUC': 0.948594
        }
    },
    'Random Forest': {
        'train': {
            'Accuracy': 1.000000,
            'Sensitivity': 1.00000,
            'Specificity': 1.00,
            'ROC AUC': 1.000000
        },
        'test': {
            'Accuracy': 0.99375,
            'Sensitivity': 1.0000,
            'Specificity': 0.9875,
            'ROC AUC': 1.000000
        }
    }
}

if __name__ == '__main__':
    generate_model_comparison_report(
        model_results,
        output_path='figures/model_comparison'
    )
