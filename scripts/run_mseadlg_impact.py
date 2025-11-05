"""
MSEADLG Feature Impact Analysis
Visualizes the impact of including MSEADLG feature on model performance
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.visualization_templates import generate_feature_impact_report

# Data for Logistic Regression
lr_results = {
    'without': {
        'Accuracy': 0.88125,
        'Sensitivity': 0.8875,
        'Specificity': 0.875
    },
    'with': {
        'Accuracy': 0.875,
        'Sensitivity': 0.8625,
        'Specificity': 0.8875
    }
}

# Data for Random Forest
rf_results = {
    'without': {
        'Accuracy': 0.9875,
        'Sensitivity': 0.975,
        'Specificity': 1.000
    },
    'with': {
        'Accuracy': 0.99375,
        'Sensitivity': 1.000,
        'Specificity': 0.9875
    }
}

if __name__ == '__main__':
    lr_df, rf_df = generate_feature_impact_report(
        lr_results,
        rf_results,
        feature_name='MSEADLG',
        output_path='figures/mseadlg_impact'
    )

    # Summary interpretation
    print("\nKey Findings:")
    print("- Logistic Regression: MSEADLG inclusion slightly decreased accuracy (-0.625%)")
    print("- Random Forest: MSEADLG inclusion improved accuracy (+0.625%)")
    print("- Suggests different models interact with MSEADLG feature differently")
