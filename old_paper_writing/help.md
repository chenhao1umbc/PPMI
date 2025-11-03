# Project Guide - Parkinson's Disease Classification Paper

## Project Overview

This is a **paper writing project**, not a research project. The experiments have been completed, and the goal is to write up the results as a journal article for submission to the Journal of Movement Disorders.

**Branch:** PDClssftnPPMI (Parkinson's Disease Classification using PPMI dataset)

## Research Summary

### Study Type
3-label classification of Parkinson's disease patients using the PPMI dataset:
- PD (Parkinson's Disease)
- SWEDD (Scans Without Evidence of Dopaminergic Deficit)
- Third label (not explicitly stated in results)

### Key Findings

1. **Model Performance:**
   - Logistic Regression: 87.5% test accuracy, 0.949 ROC AUC
   - Random Forest: 99.375% test accuracy, 1.0 ROC AUC (near-perfect)
   - Baseline accuracy: ~78-80%

2. **Feature Analysis (MSEADLG impact):**
   - Logistic Regression: Adding MSEADLG decreased accuracy by 0.625%
   - Random Forest: Adding MSEADLG improved accuracy by 0.625%

3. **Temporal/Visit-Based Analysis:**
   - V04 (early visit): 84.58% accuracy
   - V06: 97.5% accuracy (training can reach 100%)
   - V08: 96.67% accuracy
   - V10 (later visit): 99.44% accuracy
   - **Key insight:** Later visits show dramatically better prediction accuracy

4. **Important Features:**
   - **Urate:** Important feature but only useful for distinguishing SWEDD vs PD
   - **MSEADL:** Important but potentially misinterpreted in edge cases with medium values
   - Need to identify top 10 important features with drift detection

## Target Journal: Journal of Movement Disorders

### Journal Details
- Website: https://www.e-jmd.org/
- Open access, no article processing charges
- Published by Korean Movement Disorder Society
- Indexed in PubMed Central, Scopus, Web of Science

### Original Article Requirements
- **Abstract:** Structured (Objective, Methods, Results, Conclusion), ≤250 words
- **Main text:** <4,000 words
- **References:** ≤40
- **Figures/Tables:** Reasonable number (typically 5-7)

### Journal Emphasis
Based on review of published articles:
- **Clinical relevance** over pure technical innovation
- **Methodological rigor** with proper validation
- **Practical application** and accessibility
- **Balanced presentation** including clear limitations
- **Objective tone** characteristic of medical research

### Example Article Structure
From "Automatic Measurement of Postural Abnormalities" (2022):
- Clear problem statement with clinical context
- Detailed technical methodology
- Quantitative validation results
- Transparent discussion of limitations
- Emphasis on practical utility

## Project Structure

### Existing Files
- **results.txt:** Plain text summary of all experimental results
- **results.pptx:** PowerPoint with same results (7 slides)
- **main.py:** Placeholder Python file
- **pyproject.toml:** uv package management (Python 3.13)
- **README.md:** General repository description

### Files to Create

**Documentation:**
- task.md: Task tracking (checklist format)
- help.md: This file (project guidance)

**Code/Scripts:**
- scripts/model_comparison.py: Visualize LR vs RF performance
- scripts/mseadlg_impact.py: Feature impact comparison
- scripts/visit_temporal.py: Temporal accuracy trends
- figures/: Directory for generated plots

**Paper:**
- main.tex: LaTeX source
- figures/: Figures for inclusion in paper
- references.bib: Bibliography (if using BibTeX)

## Paper Structure Recommendation

### 1. Abstract (≤250 words, structured)
- **Objective:** State the problem and study goal
- **Methods:** Brief description of dataset, models, approach
- **Results:** Key quantitative findings (RF 99.4%, temporal progression)
- **Conclusion:** Clinical implications and significance

### 2. Introduction (~600 words)
- PD diagnosis challenges, especially in early stages
- Importance of differentiating SWEDD from PD
- Significance of PPMI dataset
- Temporal/longitudinal aspect of disease progression
- Study objectives and contributions

### 3. Methods (~1000 words)
- **Dataset:** PPMI description, inclusion/exclusion criteria, visit schedule
- **Features:** Clinical measures, with/without MSEADLG
- **Models:** Logistic Regression and Random Forest rationale
- **Visit-based approach:** Explain V04, V06, V08, V10 timepoints
- **Evaluation:** Metrics (accuracy, sensitivity, specificity, ROC AUC)
- **Validation:** Train/test split strategy

### 4. Results (~1200 words)
- Model performance comparison (Table 1)
- MSEADLG feature impact analysis (Table 2)
- Temporal progression findings (Figure with V04-V10 trend)
- Feature importance insights (urate, MSEADL)
- Present findings objectively with exact numbers

### 5. Discussion (~1000 words)
- **Main finding:** RF achieves near-perfect classification
- **Clinical significance:** High accuracy enables early diagnosis
- **Temporal insight:** Later visits more predictable (disease progression clearer)
- **Feature insights:**
  - Urate's specific role in SWEDD/PD differentiation
  - MSEADL interpretation challenges in edge cases
- **Model comparison:** Why RF outperforms LR (non-linear relationships)
- **Limitations:** Dataset specificity, generalizability, missing data, etc.
- **Future directions:** Validation on external cohorts, feature drift detection

### 6. Conclusion (~200 words)
- Summarize key findings
- Emphasize clinical relevance
- Future work

## Important Considerations

### Clinical Focus
- Always connect technical findings to clinical implications
- Explain what high accuracy means for patient care
- Discuss practical utility for clinicians

### Methodological Rigor
- Report exact metrics with appropriate precision
- Include confidence intervals if available
- Describe validation approach clearly
- Be transparent about limitations

### Writing Style
- Objective, measured tone
- Avoid overhyping results
- Balance strengths with limitations
- Use clear, accessible language (minimize jargon)

## Technical Setup

### Python Environment
- Package manager: uv
- Python version: 3.13
- Required packages: pandas, numpy, matplotlib, seaborn, scikit-learn

### Commands
```bash
# Install package
uv add <package-name>

# Run script
uv run python scripts/<script-name>.py

# Install LaTeX (if needed)
# macOS: brew install --cask mactex
# Linux: apt-get install texlive-full
```

## Next Steps for New Worker

1. Review results.txt and results.pptx thoroughly
2. Check task.md for current progress
3. Continue from where previous worker left off
4. Update task.md as you complete items
5. Maintain clinical focus throughout writing
6. Ensure journal requirements are met (<4000 words, ≤40 refs)

## Questions to Clarify with Supervisor

- What is the third label in 3-label classification?
- Are there raw data files or just summarized results?
- Who are the co-authors and their affiliations?
- What is the exact title for the paper?
- Are there any specific references that must be cited?
- Timeline for completion and submission?

## Last Updated
2025-10-22
