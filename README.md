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

## Quick Start

### 1. Inspect Dataset Quality

```bash
python src/data_loader.py
```

Generates `inspection_report.txt` with:
- Structure summary (bearing folders, file counts)
- Format detection (delimiters, headers, columns)
- Data quality flags (missing values, empty files, anomalies)

The inspector checks:
✅ **Structure** - Lists all bearing folders and operating conditions  
✅ **Format** - Detects delimiters, headers, column names  
✅ **Quality** - Counts rows, detects missing values, flags inconsistencies  
✅ **Anomalies** - Reports naming issues, format mismatches

### 2. Data Understanding (Notebook 01)

Open `notebooks/01_data_understanding.ipynb` to:
- Load bearing data files
- Visualize vibration signals over time
- Identify degradation trends
- Understand RUL distribution

### 3. Exploratory Data Analysis (Notebook 02)

Analyze patterns:
- Statistical summaries per bearing/condition
- Correlation between horizontal and vertical vibrations
- Degradation curves

### 4. Preprocessing & Features (Notebooks 03-04)

Clean and engineer:
- Normalize vibration signals
- Extract statistical features (RMS, kurtosis, entropy)
- Time-domain and frequency-domain analysis
- Create sliding windows for time-series modeling

### 5. Anomaly Detection (Notebook 05)

Identify degradation onset:
- Statistical methods for anomaly detection
- Degradation point identification
- Remaining useful life calculation

### 6. Model Training (Notebook 06)

Train models:
- Regression models (Random Forest, SVR, etc.)
- Deep learning (LSTM, CNN)
- Ensemble approaches

### 7. Evaluation (Notebook 07)

Compare models:
- RMSE, MAE metrics
- Prediction accuracy at different time horizons
- Cross-validation and generalization

## RUL Labeling Strategy

For each bearing:
1. Load files in chronological order
2. Identify failure point (last file or threshold)
3. For each file: RUL = Time to failure - Current time
4. Create labels for supervised learning

## Expected Results

- RUL predictions with competitive RMSE
- Early degradation detection
- Model robustness across operating conditions
- Generalization to unseen bearings

## Dependencies

To be installed:
```bash
pip install numpy pandas scikit-learn matplotlib seaborn
pip install tensorflow  # or torch for deep learning
```

Note: `data_loader.py` uses only Python stdlib for maximum portability.

## Workflow

```
Raw Data (FEMTO Dataset)
    ↓
[01] Data Understanding & Inspection
    ↓
[02] Exploratory Data Analysis
    ↓
[03] Preprocessing (normalize, clean)
    ↓
[04] Feature Extraction
    ↓
[05] Anomaly Detection
    ↓
[06] Model Training
    ↓
[07] Evaluation & Results
    ↓
Reports & Findings
```

## References

- Dataset: NASA Prognostics Data Repository
- Challenge: PHM 2012 Data Challenge (PRONOSTIA)
- Paper: Nectoux et al., "PRONOSTIA: An experimental platform for bearings accelerated degradation tests"

## Notes

- `src/data_loader.py` uses only Python stdlib (no external dependencies) for robust inspection
- All notebooks are self-contained and can run independently
- Results saved to `results/` for experiment tracking
- Use `inspection_report.txt` to validate data before modeling

---

**Project:** FEMTO-PHM RUL Prediction  
**Last Updated:** November 2024
