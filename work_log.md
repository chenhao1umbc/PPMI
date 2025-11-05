# PPMI Project Work Log

Detailed project history, dataset information, findings, and research progress.

Last Updated: November 2, 2025

---

## Dataset Details

### Source
PPMI Curated Data Cut (Public Release: March 21, 2025)
- Location: `PPMI_Curated_Data_Cut_Public_20250321/`
- Main data: `20250310-Table 1.csv`
- Data dictionary: `Data dictionary-Table 1.csv`
- Information file: `Information-Table 1.csv`

### Dataset Characteristics
- **Total records**: 15,316 patient visits
- **Features**: 181 variables
- **Study type**: Longitudinal (up to 13 years of follow-up)
- **Last update**: March 10, 2025

### Patient Cohorts
- **PD**: Parkinson's Disease patients
- **Healthy Controls**: Age-matched healthy individuals
- **SWEDD**: Scans Without Evidence of Dopaminergic Deficit
- **Prodromal**: At-risk individuals showing early signs

### Visit Schedule
- Baseline (BL)
- Annual follow-ups: V04 (Year 1), V06 (Year 2), V08 (Year 3), V10 (Year 4), V12-V20 (Years 5-13)

### Feature Categories (181 total)

#### 1. Demographics (14 variables)
- Age, sex, education, race, ethnicity
- Family history of PD
- Handedness, sexual orientation, ancestry

#### 2. Genetics (3 variables)
- APOE genotype
- APOE E4 allele count

#### 3. Biomarkers (24 variables)
**CSF**: alpha-synuclein, abeta, ptau, tau, CSF SAA
**Plasma**: bd_tau_plasma, ptau217_plasma
**Serum**: urate, neurofilament light
**Urine**: BMP species
**Blood**: hemoglobin indicators

#### 4. Imaging (13 variables)
**DATSCAN measures**:
- Caudate (left/right/contralateral/ipsilateral/mean)
- Putamen (left/right/contralateral/ipsilateral/mean)
- Striatum
- Age-adjusted ratios

#### 5. Clinical Assessments (91 variables)

**Motor Function**:
- UPDRS Parts I-IV (Unified Parkinson's Disease Rating Scale)
- Hoehn & Yahr staging
- PIGD scores (Postural Instability and Gait Difficulty)
- TD/PIGD classification (Tremor Dominant vs PIGD)

**Cognitive Function**:
- MoCA (Montreal Cognitive Assessment)
- HVLT (Hopkins Verbal Learning Test)
- Boston Naming Test
- Clock Drawing Test
- Trail Making Tests A & B
- Letter Number Sequencing
- Symbol Digit Modalities Test
- Benton Line Orientation

**Functional Status**:
- MSEADLG (Modified Schwab & England Activities of Daily Living)
- LEDD (Levodopa Equivalent Daily Dose)

**Non-Motor Symptoms**:
- UPSIT (University of Pennsylvania Smell Identification Test)
- Epworth Sleepiness Scale
- RBDSQ (REM Sleep Behavior Disorder Screening)
- GDS (Geriatric Depression Scale)
- STAI (State-Trait Anxiety Inventory)
- SCOPA-AUT (Scales for Outcomes in PD - Autonomic)
- QUIP (Questionnaire for Impulsive-Compulsive Disorders)
- Orthostatic hypotension measures

**Disease Characteristics**:
- Age at onset/diagnosis
- Disease duration
- Dominant side
- Initial symptom presentation

#### 6. Disease Progression (7 variables)
Milestone indicators for:
- Activities of Daily Living (ADL)
- Autonomic dysfunction
- Cognitive decline
- Motor complications
- Walking and balance impairment

#### 7. NSD-ISS Staging (7 variables)
- Neuronal alpha-synuclein disease staging system (NEW in March 2025)
- Modified UPDRS scores for staging

---

## Previous Findings (From old_paper_writing/)

### Model Performance (3-class classification: PD vs SWEDD vs Healthy)

#### Random Forest
- **Test Accuracy**: 99.38%
- **Sensitivity**: 100%
- **Specificity**: 98.75%
- **ROC AUC**: 1.00

#### Logistic Regression
- **Test Accuracy**: 87.50%
- **Sensitivity**: 86.25%
- **Specificity**: 88.75%
- **ROC AUC**: 0.949

**Key Finding**: Random Forest outperformed Logistic Regression by 11.88 percentage points.

### Temporal Progression Analysis (V04-V10)
- **V04 (Year 1)**: 84.58% accuracy
- **V06 (Year 2)**: 97.50% accuracy
- **V08 (Year 3)**: 96.67% accuracy
- **V10 (Year 4)**: 99.44% accuracy

**Key Insight**: 14.86% improvement from Year 1 to Year 4, indicating that disease characteristics become increasingly distinguishable over time.

### Feature Impact Analysis
- **MSEADLG**: Model-dependent effects (improves RF, decreases LR)
- **Urate**: Particularly useful for SWEDD vs PD differentiation
- **MSEADL**: Interpretation challenges in medium-value edge cases

### Sample Size (Previous Analysis)
- Training: 640 samples
- Test: 320 samples
- Total: 960 samples

---

## Research Objectives

### Current Focus
1. **Data Exploration**: Discover new patterns and relationships in the 181-feature dataset
2. **Multi-Modal Integration**: Combine clinical + imaging + genetic + biomarker data
3. **Biomarker Discovery**: Investigate novel biomarkers (especially March 2025 additions)
4. **Temporal Modeling**: Analyze disease progression trajectories over time
5. **Deep Data Mining**: Find hidden patterns to enrich manuscript

### Unexplored Opportunities
- **NSD-ISS Staging Variables**: Newly added in March 2025 data cut
- **Plasma Biomarkers**: ptau217_plasma, bd_tau_plasma
- **Genetic Integration**: APOE genotype effects on progression
- **Prodromal Cohort**: Early detection and prediction
- **Extended Temporal Range**: Data available up to Year 13 (V20)
- **Multi-modal Fusion**: Combining multiple data modalities

---

## Project Structure

```
PPMI/
  README.md                                    # High-level overview
  work_log.md                                  # This file (detailed history)
  pyproject.toml                               # Python dependencies (uv)
  .venv/                                       # Virtual environment
  PPMI_Curated_Data_Cut_Public_20250321/      # Dataset
    20250310-Table 1.csv                       # Main data (15,316 rows x 181 cols)
    Data dictionary-Table 1.csv                # Variable definitions
    Information-Table 1.csv                    # Dataset metadata
  src/                                         # Source code modules
    data_loader.py                             # Data loading utilities
    data_preprocessing.py                      # Feature engineering
    plotting.py                                # Visualization functions
    metrics.py                                 # Evaluation metrics
    models.py                                  # ML model wrappers
    visualization_templates.py                 # High-level templates
  scripts/                                     # Executable analysis scripts
    run_model_comparison.py                    # Model comparison
    run_mseadlg_impact.py                      # Feature impact analysis
    run_visit_temporal.py                      # Temporal progression
    run_multimodal_integration.py              # Multi-modal analysis
  paper/                                       # Current work
    demos/                                     # Demo notebooks
    figures/                                   # Generated visualizations
  old_paper_writing/                           # Previous work (reference)
    main.tex                                   # Draft paper
    main.pdf                                   # Compiled paper
    figures/                                   # Previous visualizations
    task.md                                    # Task tracking
    COMPLETION_SUMMARY.md                      # Summary
    scripts/                                   # Original visualization scripts
```

---

## Technical Notes

### Data Processing
- **Missing Data**: Previous analysis used median imputation strategy
- **Class Balance**: Check cohort distribution in each analysis
- **Longitudinal Structure**: Each patient has multiple visits; account for within-subject correlation
- **Data Versioning**: This dataset is the March 21, 2025 public release

### Reproducibility Guidelines
1. Use random seeds for reproducibility
2. Document preprocessing steps
3. Save model configurations
4. Version control all scripts
5. Generate publication-quality figures (300 dpi, PDF + PNG)

### Python Environment
- **Python Version**: 3.13+
- **Package Manager**: uv
- **Dependencies**:
  - Data Processing: pandas, numpy, scipy
  - Machine Learning: scikit-learn, torch
  - Visualization: matplotlib, seaborn
  - Interactive: jupyter, ipython

---

## Progress Log

### November 2, 2025 - Project Restructuring
- Created work_log.md for detailed tracking
- Simplified README.md to high-level overview
- Restructured code: scripts/ → src/ with functional modules
- Renamed paper/notebooks/ → paper/demos/
- Refactored visualization scripts to use modular src/ functions
- Created multi-modal integration demos

### October 22, 2024 - Initial Paper Draft
- Completed draft paper targeting Journal of Movement Disorders
- Generated all publication figures
- Documented previous findings (RF 99.38% accuracy)
- Identified gaps for future work

---

## Next Steps

1. Run multi-modal integration demos
2. Explore NSD-ISS staging variables (March 2025 addition)
3. Investigate plasma biomarkers (ptau217, bd_tau)
4. Analyze prodromal cohort for early detection
5. Extend temporal analysis to all available visits (V04-V20)
6. Perform feature importance analysis across all 181 variables
7. Validate findings and prepare manuscript

---

## References

See `old_paper_writing/main.tex` for current bibliography (15 references, max 40 allowed for Journal of Movement Disorders).

---

## Publication Target

**Journal**: Journal of Movement Disorders (Original Article)
**Status**: Deep data mining phase, manuscript draft exists
**Word Limit**: Within journal requirements
**Figure Limit**: Following journal guidelines
