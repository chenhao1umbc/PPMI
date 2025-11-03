"""
Model Performance Comparison: Logistic Regression vs Random Forest
Generates publication-quality comparison plot for Journal of Movement Disorders
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Data from results (with MSEADL)
data = {
    'Model': ['Logistic Regression', 'Random Forest'],
    'Train Sensitivity': [0.90625, 1.00000],
    'Train Specificity': [0.95, 1.00],
    'Train ROC AUC': [0.970693, 1.000000],
    'Train Accuracy': [0.928125, 1.000000],
    'Test Sensitivity': [0.8625, 1.0000],
    'Test Specificity': [0.8875, 0.9875],
    'Test ROC AUC': [0.948594, 1.000000],
    'Test Accuracy': [0.87500, 0.99375]
}

df = pd.DataFrame(data)

# Create figure with subplots
fig, axes = plt.subplots(1, 2, figsize=(12, 5))

# Define metrics to plot
test_metrics = ['Test Accuracy', 'Test Sensitivity', 'Test Specificity', 'Test ROC AUC']
train_metrics = ['Train Accuracy', 'Train Sensitivity', 'Train Specificity', 'Train ROC AUC']

# Plot 1: Test Performance
x = np.arange(len(test_metrics))
width = 0.35

lr_test_values = [df[metric].iloc[0] for metric in test_metrics]
rf_test_values = [df[metric].iloc[1] for metric in test_metrics]

axes[0].bar(x - width/2, lr_test_values, width, label='Logistic Regression', color='#4CAF50', alpha=0.8)
axes[0].bar(x + width/2, rf_test_values, width, label='Random Forest', color='#2196F3', alpha=0.8)

axes[0].set_ylabel('Score', fontsize=12)
axes[0].set_title('Test Set Performance', fontsize=14, fontweight='bold')
axes[0].set_xticks(x)
axes[0].set_xticklabels(['Accuracy', 'Sensitivity', 'Specificity', 'ROC AUC'], rotation=45, ha='right')
axes[0].set_ylim([0.8, 1.05])
axes[0].legend(loc='lower right', fontsize=10)
axes[0].grid(axis='y', alpha=0.3)

# Add value labels on bars
for i, (lr_val, rf_val) in enumerate(zip(lr_test_values, rf_test_values)):
    axes[0].text(i - width/2, lr_val + 0.01, f'{lr_val:.3f}', ha='center', va='bottom', fontsize=9)
    axes[0].text(i + width/2, rf_val + 0.01, f'{rf_val:.3f}', ha='center', va='bottom', fontsize=9)

# Plot 2: Train Performance
lr_train_values = [df[metric].iloc[0] for metric in train_metrics]
rf_train_values = [df[metric].iloc[1] for metric in train_metrics]

axes[1].bar(x - width/2, lr_train_values, width, label='Logistic Regression', color='#4CAF50', alpha=0.8)
axes[1].bar(x + width/2, rf_train_values, width, label='Random Forest', color='#2196F3', alpha=0.8)

axes[1].set_ylabel('Score', fontsize=12)
axes[1].set_title('Training Set Performance', fontsize=14, fontweight='bold')
axes[1].set_xticks(x)
axes[1].set_xticklabels(['Accuracy', 'Sensitivity', 'Specificity', 'ROC AUC'], rotation=45, ha='right')
axes[1].set_ylim([0.8, 1.05])
axes[1].legend(loc='lower right', fontsize=10)
axes[1].grid(axis='y', alpha=0.3)

# Add value labels on bars
for i, (lr_val, rf_val) in enumerate(zip(lr_train_values, rf_train_values)):
    axes[1].text(i - width/2, lr_val + 0.01, f'{lr_val:.3f}', ha='center', va='bottom', fontsize=9)
    axes[1].text(i + width/2, rf_val + 0.01, f'{rf_val:.3f}', ha='center', va='bottom', fontsize=9)

plt.tight_layout()
plt.savefig('figures/model_comparison.png', dpi=300, bbox_inches='tight')
plt.savefig('figures/model_comparison.pdf', bbox_inches='tight')
print("Figure saved: figures/model_comparison.png and .pdf")
plt.close()

# Print summary table for paper
print("\nModel Performance Summary:")
print(df.to_string(index=False))
