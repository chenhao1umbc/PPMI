"""
MSEADLG Feature Impact Analysis
Visualizes the impact of including MSEADLG feature on model performance
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Data for Logistic Regression
lr_data = {
    'Metric': ['Test Accuracy', 'Test Sensitivity', 'Test Specificity'],
    'Without MSEADLG': [0.88125, 0.8875, 0.875],
    'With MSEADLG': [0.875, 0.8625, 0.8875],
    'Change': [-0.00625, -0.025, +0.0125]
}

# Data for Random Forest
rf_data = {
    'Metric': ['Test Accuracy', 'Test Sensitivity', 'Test Specificity'],
    'Without MSEADLG': [0.9875, 0.975, 1.000],
    'With MSEADLG': [0.99375, 1.000, 0.9875],
    'Change': [+0.00625, +0.025, -0.0125]
}

lr_df = pd.DataFrame(lr_data)
rf_df = pd.DataFrame(rf_data)

# Create figure
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# Plot 1: Logistic Regression
metrics = lr_df['Metric'].tolist()
x = np.arange(len(metrics))
width = 0.35

axes[0].bar(x - width/2, lr_df['Without MSEADLG'], width,
            label='Without MSEADLG', color='#FF9800', alpha=0.8)
axes[0].bar(x + width/2, lr_df['With MSEADLG'], width,
            label='With MSEADLG', color='#FF5722', alpha=0.8)

axes[0].set_ylabel('Score', fontsize=12)
axes[0].set_title('Logistic Regression: MSEADLG Impact', fontsize=14, fontweight='bold')
axes[0].set_xticks(x)
axes[0].set_xticklabels(['Accuracy', 'Sensitivity', 'Specificity'], rotation=45, ha='right')
axes[0].set_ylim([0.8, 1.05])
axes[0].legend(fontsize=10)
axes[0].grid(axis='y', alpha=0.3)

# Add change annotations
for i, change in enumerate(lr_df['Change']):
    color = 'red' if change < 0 else 'green'
    sign = '' if change < 0 else '+'
    axes[0].text(i, 1.02, f'{sign}{change:.4f}',
                ha='center', va='bottom', fontsize=10, color=color, fontweight='bold')

# Plot 2: Random Forest
axes[1].bar(x - width/2, rf_df['Without MSEADLG'], width,
            label='Without MSEADLG', color='#2196F3', alpha=0.8)
axes[1].bar(x + width/2, rf_df['With MSEADLG'], width,
            label='With MSEADLG', color='#1976D2', alpha=0.8)

axes[1].set_ylabel('Score', fontsize=12)
axes[1].set_title('Random Forest: MSEADLG Impact', fontsize=14, fontweight='bold')
axes[1].set_xticks(x)
axes[1].set_xticklabels(['Accuracy', 'Sensitivity', 'Specificity'], rotation=45, ha='right')
axes[1].set_ylim([0.8, 1.05])
axes[1].legend(fontsize=10)
axes[1].grid(axis='y', alpha=0.3)

# Add change annotations
for i, change in enumerate(rf_df['Change']):
    color = 'red' if change < 0 else 'green'
    sign = '' if change < 0 else '+'
    axes[1].text(i, 1.02, f'{sign}{change:.4f}',
                ha='center', va='bottom', fontsize=10, color=color, fontweight='bold')

plt.tight_layout()
plt.savefig('figures/mseadlg_impact.png', dpi=300, bbox_inches='tight')
plt.savefig('figures/mseadlg_impact.pdf', bbox_inches='tight')
print("Figure saved: figures/mseadlg_impact.png and .pdf")
plt.close()

# Print summary tables
print("\nLogistic Regression - MSEADLG Impact:")
print(lr_df.to_string(index=False))
print("\nRandom Forest - MSEADLG Impact:")
print(rf_df.to_string(index=False))

# Summary interpretation
print("\nKey Findings:")
print("- Logistic Regression: MSEADLG inclusion slightly decreased accuracy (-0.625%)")
print("- Random Forest: MSEADLG inclusion improved accuracy (+0.625%)")
print("- Suggests different models interact with MSEADLG feature differently")
