"""
Visit-Based Temporal Analysis
Shows how prediction accuracy improves across different visit timepoints (V04-V10)
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Data from results
visit_data = {
    'Visit': ['V04', 'V06', 'V08', 'V10'],
    'Test Accuracy': [0.8458, 0.975, 0.9667, 0.9944],
    'Visit Number': [4, 6, 8, 10]
}

df = pd.DataFrame(visit_data)

# Baseline accuracy
baseline_accuracy = 0.7875

# Create figure
fig, ax = plt.subplots(figsize=(10, 6))

# Plot temporal trend
ax.plot(df['Visit Number'], df['Test Accuracy'],
        marker='o', linewidth=2.5, markersize=10,
        color='#2196F3', label='Visit-based Accuracy')

# Add baseline reference line
ax.axhline(y=baseline_accuracy, color='red', linestyle='--',
          linewidth=2, alpha=0.7, label=f'Baseline ({baseline_accuracy:.2%})')

# Styling
ax.set_xlabel('Visit Number', fontsize=13, fontweight='bold')
ax.set_ylabel('Test Accuracy', fontsize=13, fontweight='bold')
ax.set_title('Temporal Progression of Classification Accuracy\n(3-Label Parkinson\'s Disease Classification)',
            fontsize=14, fontweight='bold')
ax.set_xticks(df['Visit Number'])
ax.set_xticklabels([f'V{v:02d}' for v in df['Visit Number']], fontsize=11)
ax.set_ylim([0.75, 1.01])
ax.grid(True, alpha=0.3, linestyle='--')
ax.legend(fontsize=11, loc='lower right')

# Add value labels on points
for i, row in df.iterrows():
    ax.text(row['Visit Number'], row['Test Accuracy'] + 0.008,
           f"{row['Test Accuracy']:.2%}",
           ha='center', va='bottom', fontsize=11, fontweight='bold')

# Add improvement annotation
improvement = df['Test Accuracy'].iloc[-1] - df['Test Accuracy'].iloc[0]
ax.annotate(f'Improvement: +{improvement:.1%}',
           xy=(df['Visit Number'].iloc[-1], df['Test Accuracy'].iloc[-1]),
           xytext=(8, 0.88),
           fontsize=11,
           bbox=dict(boxstyle='round,pad=0.5', facecolor='lightgreen', alpha=0.7),
           arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0.3', lw=1.5))

plt.tight_layout()
plt.savefig('figures/visit_temporal.png', dpi=300, bbox_inches='tight')
plt.savefig('figures/visit_temporal.pdf', bbox_inches='tight')
print("Figure saved: figures/visit_temporal.png and .pdf")
plt.close()

# Print summary
print("\nVisit-Based Accuracy Summary:")
print(df[['Visit', 'Test Accuracy']].to_string(index=False))
print(f"\nBaseline Accuracy: {baseline_accuracy:.2%}")
print(f"Improvement from V04 to V10: +{improvement:.1%}")

# Clinical interpretation
print("\nClinical Interpretation:")
print("- Early visit (V04): 84.58% accuracy")
print("- Later visits (V06-V10): >96% accuracy")
print("- Suggests disease progression becomes more distinguishable over time")
print("- V10 achieves near-perfect classification (99.44%)")
