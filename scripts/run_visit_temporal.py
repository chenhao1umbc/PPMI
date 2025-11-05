"""
Visit-Based Temporal Analysis
Shows how prediction accuracy improves across different visit timepoints (V04-V10)
"""

import pandas as pd
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.visualization_templates import generate_temporal_analysis_report

# Data from results
visit_data = {
    'Visit': ['V04', 'V06', 'V08', 'V10'],
    'Test Accuracy': [0.8458, 0.975, 0.9667, 0.9944],
    'Visit Number': [4, 6, 8, 10]
}

df = pd.DataFrame(visit_data)
baseline_accuracy = 0.7875

if __name__ == '__main__':
    result_df = generate_temporal_analysis_report(
        df,
        baseline=baseline_accuracy,
        output_path='figures/visit_temporal'
    )

    # Clinical interpretation
    print("\nClinical Interpretation:")
    print("- Early visit (V04): 84.58% accuracy")
    print("- Later visits (V06-V10): >96% accuracy")
    print("- Suggests disease progression becomes more distinguishable over time")
    print("- V10 achieves near-perfect classification (99.44%)")
