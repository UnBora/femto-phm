# FEMTO-PHM Environment Setup Guide

## Quick Start

### Option 1: User-Level Installation (No sudo needed)
```bash
cd /home/bora-un/Desktop/femto-phm
python3 -m pip install --user -r requirements.txt
```

### Option 2: Virtual Environment (Recommended)
```bash
cd /home/bora-un/Desktop/femto-phm

# Create virtual environment
python3 -m venv venv

# Activate it
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Option 3: Run Setup Script
```bash
cd /home/bora-un/Desktop/femto-phm
bash setup.sh
```

---

## Troubleshooting

### Error: "No module named pip"
**Solution:** Install pip first
```bash
# Option A: Using ensurepip
python3 -m ensurepip --user --upgrade

# Option B: Using apt (Linux)
# Contact system admin or use Option 1/2 above
```

### Error: "No module named venv"
**Solution:** Skip venv and use user-level installation (Option 1)
```bash
python3 -m pip install --user -r requirements.txt
```

### After Installation: "ModuleNotFoundError"
If you used `--user` flag, Python should find packages. If not:
```bash
# Check where packages were installed
python3 -m pip show numpy

# Verify installation
python3 -c "import numpy; print(numpy.__version__)"
```

---

## Verifying Installation

Run this to check all dependencies:
```bash
python3 << EOF
import sys
packages = ['numpy', 'pandas', 'matplotlib', 'seaborn', 'sklearn', 'scipy', 'jupyter', 'IPython']
print(f"Python {sys.version}")
print("\nChecking packages:")
for pkg in packages:
    try:
        __import__(pkg)
        print(f"✓ {pkg}")
    except ImportError:
        print(f"✗ {pkg} - NOT INSTALLED")
EOF
```

---

## Running Jupyter Notebook

### Method 1: Local Jupyter
```bash
cd /home/bora-un/Desktop/femto-phm
jupyter notebook
```
Then open: `http://localhost:8888`

### Method 2: VSCode with Python extension
1. Open VSCode
2. Open folder: `/home/bora-un/Desktop/femto-phm`
3. Click "Select Kernel" → Choose Python 3
4. Open `notebooks/01_data_understanding.ipynb`

### Method 3: Jupyter Lab (if installed)
```bash
jupyter lab
```

---

## Alternative: Direct Python Script

If Jupyter doesn't work, run the notebook as a script:
```bash
cd /home/bora-un/Desktop/femto-phm
python3 -c "
import sys
sys.path.insert(0, 'src')
exec(open('notebooks/01_data_understanding.ipynb').read())
"
```

---

## Package Versions

| Package | Version | Purpose |
|---------|---------|---------|
| numpy | 1.24.3 | Numerical computing |
| pandas | 2.0.3 | Data manipulation |
| matplotlib | 3.7.2 | Plotting |
| seaborn | 0.12.2 | Statistical visualizations |
| scikit-learn | 1.3.0 | Machine learning |
| scipy | 1.11.2 | Scientific computing |
| jupyter | 1.0.0 | Notebooks |
| ipython | 8.14.0 | Interactive shell |

---

## If All Else Fails

Use Python without dependencies (basic analysis):
```bash
cd /home/bora-un/Desktop/femto-phm
python3 src/data_loader.py
```

This runs the dataset inspector using only Python stdlib (no imports needed).

---

## Next Steps

After installing dependencies:
1. Run Jupyter: `jupyter notebook`
2. Open: `notebooks/01_data_understanding.ipynb`
3. Run all cells to explore the dataset
4. Check output plots in `results/figures/`

