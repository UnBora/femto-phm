# FEMTO-PHM: Remaining Useful Life Prediction for Bearings

Predictive maintenance and health management (PHM) system for bearing remaining useful life (RUL) estimation using the NASA FEMTO (PRONOSTIA) bearing dataset.

## Project Structure

```
femto-phm/
│
├── data/
│   ├── raw/                    # Raw FEMTO bearing dataset
│   │   ├── Learning_set/       # Training bearings (4 bearings × 3 conditions)
│   │   ├── Test_set/           # Test bearings (3 bearings × 2 conditions)
│   │   └── Full_Test_Set/      # Full test set
│   ├── interim/                # Intermediate processed data
│   └── processed/              # Final processed data for modeling
│
├── notebooks/
│   ├── 01_data_understanding.ipynb    # Initial dataset inspection & exploration
│   ├── 02_eda.ipynb                   # Exploratory data analysis
│   ├── 03_preprocessing.ipynb         # Data cleaning & normalization
│   ├── 04_feature_extraction.ipynb    # Feature engineering for RUL
│   ├── 05_anomaly_detection.ipynb     # Anomaly & degradation detection
│   ├── 06_model_training.ipynb        # Model training (ML/DL approaches)
│   └── 07_evaluation.ipynb            # Model evaluation & results
│
├── src/
│   ├── __init__.py
│   ├── data_loader.py          # Dataset inspection & loading
│   ├── preprocessing.py        # Data cleaning & normalization
│   ├── features.py             # Feature extraction & engineering
│   ├── models/                 # Model implementations
│   │   └── __init__.py
│   └── evaluation.py           # Evaluation metrics & visualization
│
├── results/
│   ├── figures/                # Plots, visualizations, graphs
│   ├── metrics/                # Performance metrics, results
│   └── models/                 # Trained model files
│
├── literature_review/          # Papers, references, notes
│
├── reports/                    # Final reports, findings
│
├── inspection_report.txt       # Dataset structure & quality report
├── README.md                   # This file
└── .gitignore
```

## Dataset: NASA FEMTO Bearing

**Learning Set:** 4 bearings run to failure under 3 different operating conditions
- Bearing1_1, Bearing1_2, Bearing1_3
- Bearing2_1, Bearing2_2, Bearing2_3
- Bearing3_1, Bearing3_2, Bearing3_3
- Bearing4_1, Bearing4_2, Bearing4_3

**Test Set:** 3 bearings under 2 operating conditions
- Bearing1_1, Bearing1_2
- Bearing2_1, Bearing2_2
- Bearing3_1, Bearing3_2

**Data Format:**
- Multiple CSV files per bearing condition (chronological sequence)
- Columns: Horizontal vibration, Vertical vibration, Timestamp
- Sampling rate: 10 kHz
- Each file contains vibration snapshots over successive time intervals

## Installation & Setup

### Environment Setup

```bash
cd /home/bora-un/Desktop/femto-phm

# Option 1: User-level installation (fastest)
python3 -m pip install --user -r requirements.txt

# Option 2: Virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Option 3: Run setup script
bash setup.sh
```

**Dependencies:** numpy, pandas, matplotlib, seaborn, scikit-learn, scipy, jupyter, ipython

See `SETUP.md` for detailed troubleshooting and alternatives.

---

## Workflow & Notebooks

### Complete Analysis Pipeline

```
Raw Data (FEMTO Dataset)
    ↓
[01] Data Understanding & Inspection
    ↓
[02] Exploratory Data Analysis
    ↓
[03] Preprocessing & Normalization
    ↓
[04] Feature Extraction & Engineering
    ↓
[05] Anomaly Detection & Degradation Onset
    ↓
[06] Model Training (ML & DL approaches)
    ↓
[07] Evaluation & Results Analysis
    ↓
Reports & Findings
```

---

## Detailed Notebook Descriptions

### [01] Data Understanding
**Goal:** Understand dataset structure and raw data characteristics  
**Input:** Raw CSV files in `data/raw/`  
**Process:**
- Inspect dataset using `src/data_loader.py`
- Load bearing data chronologically
- Visualize vibration signals across bearing lifespan
- Track degradation progression (RMS, kurtosis)
- Compare bearings across operating conditions
- Extract statistical features

**Key Outputs:**
- Dataset structure validation
- Vibration signal plots (early, middle, late stages)
- RMS degradation curves
- Cross-bearing comparisons
- Feature evolution analysis
- Summary statistics table

**Insights:**
- 4 bearings × 3 conditions = 12 scenarios in Learning set
- Bearing lifespan varies by operating stress
- Clear RMS and kurtosis increase indicates degradation
- Both horizontal and vertical vibrations informative

---

### [02] Exploratory Data Analysis
**Goal:** Deep statistical analysis and pattern discovery  
**Input:** Loaded bearing data from Notebook 01  
**Process:**
- Calculate statistical features per file (RMS, Kurtosis, Crest Factor, Std Dev)
- Analyze signal distributions (normal vs heavy-tailed)
- Create Q-Q plots to assess deviation from normality
- Track feature evolution over bearing lifespan
- Plot degradation curves for all 12 bearings
- Calculate feature correlations (heatmap)
- Analyze horizontal vs vertical vibration relationships
- Study operating condition effects on degradation
- Perform frequency-domain analysis (Power Spectral Density)

**Features Analyzed:**
- **RMS**: Root Mean Square (energy indicator)
- **Kurtosis**: Peakedness (impulsiveness, bearing spalls)
- **Crest Factor**: Peak to RMS ratio (impact severity)
- **Skewness**: Distribution asymmetry
- **Standard Deviation**: Signal variability

**Key Outputs:**
- Distribution analysis plots (histograms + Q-Q plots)
- Degradation curves for all bearings
- Feature correlation matrix heatmap
- H vs V vibration comparison
- Operating condition effects visualization
- Power spectral density plots
- Statistical summary tables (CSV)
- EDA summary report

**Key Findings:**
1. **Degradation Pattern**: Monotonic increase in RMS/Kurtosis over time
2. **Operating Conditions**: Condition 1 (normal) → longest lifespan; Condition 3 (high stress) → shortest
3. **Feature Correlations**: 
   - H and V RMS: moderate-to-strong correlation
   - Kurtosis and RMS: strong correlation (both increase with degradation)
   - Crest Factor: Independent indicator of impact severity
4. **Distribution Shift**: Healthy bearings ≈ normal; Degraded bearings → heavy-tailed
5. **Frequency Content**: Low frequencies dominate; spalls create high-frequency energy peaks

**Why This Matters:**
- Guides feature selection for modeling
- Validates assumption of degradation trends
- Identifies which features are most predictive
- Shows operating condition affects degradation rate
- Informs whether to use H, V, or both vibrations

---

### [03] Preprocessing & Normalization
**Goal:** Clean, standardize, and prepare data for feature extraction  
**Input:** Raw bearing data with identified statistics  
**Process:**
- Handle missing values (interpolation, removal)
- Detect and remove outliers (statistical methods)
- Normalize signals to zero mean and unit variance
- Apply bandpass filtering (remove noise, extract relevant frequencies)
- Detrend signals if needed
- Create consistent time-series windows across all bearings
- Split data into train/validation/test sets

**Normalization Methods:**
- **Z-score normalization**: (x - mean) / std
- **Min-Max scaling**: (x - min) / (max - min)
- **Robust scaling**: For outlier-resistant normalization

**Expected Outputs:**
- Cleaned bearing datasets
- Normalization parameters (saved for test set)
- Preprocessed data in `data/interim/`
- Quality metrics (before/after comparisons)

---

### [04] Feature Extraction & Engineering
**Goal:** Extract comprehensive features for RUL prediction  
**Input:** Preprocessed bearing data  
**Process:**
- **Time-domain features** (per file/window):
  - RMS, Mean, Std Dev, Min, Max, Range
  - Kurtosis, Skewness, Crest Factor
  - Peak value, Zero crossings
  - Histogram features (bin statistics)
  
- **Frequency-domain features**:
  - Power Spectral Density (PSD) peaks
  - Frequency bands (0-5kHz, 5-10kHz, etc.)
  - Spectral entropy
  - Frequency centroid
  
- **Time-frequency features**:
  - Wavelet coefficients
  - Short-Time Fourier Transform (STFT)
  
- **Temporal features** (across files):
  - Feature trends (slope, acceleration)
  - Rolling statistics (mean, std over windows)
  - Degradation indicators

**Sliding Window Approach:**
- Create overlapping windows from consecutive files
- Each window = one training sample with target RUL
- Captures temporal dependencies

**Expected Outputs:**
- Comprehensive feature matrix (N samples × M features)
- Feature importance rankings
- Feature selection results (redundancy removal)
- Processed data in `data/processed/`
- Feature extraction pipeline (for test set)

**Why Multiple Features:**
- Single features (e.g., RMS alone) insufficient
- Different features capture different aspects of degradation
- Redundancy removal improves model efficiency
- Ensemble models benefit from diverse features

---

### [05] Anomaly Detection & Degradation Onset
**Goal:** Identify when bearing degradation begins and characterize failure progression  
**Input:** Engineered features from Notebook 04  
**Process:**
- Establish baseline (early-stage bearing statistics)
- Detect anomalies using:
  - Statistical methods (Z-score, IQR)
  - Isolation Forest
  - Local Outlier Factor (LOF)
  - Mahalanobis distance
- Identify degradation onset (first anomaly)
- Classify bearing health states:
  - **Healthy**: Normal operation
  - **Degrading**: Anomalies detected
  - **Severe**: High-severity anomalies
- Calculate time-to-failure from each point

**Expected Outputs:**
- Anomaly scores for each file
- Degradation onset timestamps
- Health state classifications
- RUL labels for supervised learning
- Anomaly detection plots

---

### [06] Model Training
**Goal:** Build and train RUL prediction models  
**Input:** Engineered features + RUL labels from Notebook 05  
**Process:**

**Machine Learning Models:**
- **Linear Models**: Linear/Ridge/Lasso regression
- **Tree Models**: Random Forest, Gradient Boosting, XGBoost
- **Support Vector Machines**: SVR (epsilon regression)
- **Ensemble Methods**: Voting, Stacking

**Deep Learning Models:**
- **LSTM (Long Short-Term Memory)**: Sequence learning
- **CNN**: Feature extraction from time-series
- **CNN-LSTM**: Hybrid approach

**Training Strategy:**
- Cross-validation (K-fold)
- Hyperparameter tuning (grid search, random search)
- Early stopping (overfitting prevention)
- Class balancing (if needed)
- Condition-aware training (separate models per condition?)

**Expected Outputs:**
- Trained model files in `results/models/`
- Training curves (loss, metrics)
- Cross-validation results
- Hyperparameter configurations
- Model performance on validation set

---

### [07] Evaluation & Results
**Goal:** Assess model performance and compare approaches  
**Input:** Trained models from Notebook 06  
**Process:**
- **Evaluation Metrics:**
  - RMSE (Root Mean Squared Error)
  - MAE (Mean Absolute Error)
  - MAPE (Mean Absolute Percentage Error)
  - R² score
  - Score function: (mean RUL error, scores at different time horizons)

- **Detailed Analysis:**
  - Per-bearing performance
  - Per-condition performance
  - Generalization across unseen bearings
  - Prediction at different RUL windows (early vs late)
  - Confidence intervals

- **Visualizations:**
  - Actual vs Predicted plots
  - Residual analysis
  - Model comparison bar charts
  - Confusion matrices (if classification)

**Expected Outputs:**
- Comprehensive evaluation report
- Comparison of all models
- Best model selection
- Performance metrics in `results/metrics/`
- Final plots in `results/figures/`
- Recommendations for deployment

---

## RUL Labeling Strategy

**Remaining Useful Life (RUL)** = Time remaining until bearing failure

### Definition:
- For each bearing: Identify failure point (last file or threshold)
- For each file at time t: RUL = Files remaining × Time per file
- RUL decreases from lifespan to 0

### Example:
- Bearing lifespan: 100 files (each = 1 hour)
- File 20: RUL = (100 - 20) × 1 = 80 hours remaining
- File 99: RUL = (100 - 99) × 1 = 1 hour remaining

### Why Important:
- Provides targets for supervised learning
- Enables regression models for prediction
- Allows comparison across different lifespans
- Critical for maintenance scheduling

---

## Outputs & Results Structure

### Generated During Analysis:

**`results/figures/`** - Visualizations
- `01_vibration_signals_progression.png` - Signal progression
- `01_rms_degradation.png` - RMS over time
- `01_cross_bearing_comparison.png` - Bearing comparisons
- `01_feature_evolution.png` - Feature trends
- `02_distribution_analysis.png` - Distribution shifts
- `02_degradation_curves_all.png` - All bearings
- `02_feature_correlation.png` - Correlation matrix
- `02_h_vs_v_analysis.png` - Horizontal vs Vertical
- `02_condition_effects.png` - Operating condition impact
- `02_frequency_analysis.png` - Power spectral density
- Plus: preprocessing, modeling, evaluation plots

**`results/metrics/`** - Statistical Reports
- `02_bearing_statistics.csv` - Overall statistics
- `02_condition_analysis.csv` - Condition analysis
- `02_eda_summary.txt` - EDA findings
- Plus: feature importance, evaluation metrics, predictions

**`results/models/`** - Trained Models
- `best_model.pkl` or `.h5` - Best performing model
- `model_config.json` - Architecture config
- `scaler.pkl` - Normalization parameters

---

## Key Performance Indicators

### Target Metrics:
- **RMSE**: < 100 hours for good prediction
- **MAE**: < 80 hours
- **R² Score**: > 0.8 (explains 80%+ variance)
- **Generalization**: Similar performance on unseen bearings

### Validation Strategy:
- Leave-one-bearing-out cross-validation
- Separate train/test on different bearings
- Per-condition performance tracking

---

## Expected Results

- RUL predictions with competitive accuracy
- Early degradation detection capability
- Model robustness across operating conditions
- Generalization to unseen bearings
- Deployment-ready models with performance metrics

---

## References

- **Dataset**: NASA Prognostics Data Repository (FEMTO/PRONOSTIA)
- **Challenge**: PHM 2012 Data Challenge
- **Paper**: Nectoux et al., "PRONOSTIA: An experimental platform for bearings accelerated degradation tests"
- **Domain**: Predictive Maintenance, Condition-Based Monitoring, RUL Estimation

---

## Notes & Best Practices

- **`src/data_loader.py`** uses only Python stdlib for maximum portability
- **All notebooks** are self-contained and can run independently
- **Results** automatically saved to `results/` for experiment tracking
- **Validation** of data quality using `inspection_report.txt` before modeling
- **Modularity**: Each notebook builds on previous outputs but can run standalone
- **Reproducibility**: All random seeds fixed, hyperparameters documented

## Troubleshooting

### Import Errors
```bash
# Verify installation
python3 -c "import numpy, pandas, matplotlib, seaborn, sklearn; print('✓ All OK')"
```

### Jupyter Not Found
```bash
python3 -m jupyter notebook
```

### Memory Issues
- Reduce number of files loaded at once
- Use chunking for large datasets
- See individual notebooks for memory optimization

---

**Project:** FEMTO-PHM RUL Prediction  
**Version:** 1.0  
**Last Updated:** November 2024  
**Status:** Notebooks 01-02 complete, 03-07 in development
