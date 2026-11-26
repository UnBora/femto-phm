import os
import sys
import pickle
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
from scipy import signal, stats
from sklearn.preprocessing import StandardScaler, RobustScaler, MinMaxScaler

sys.path.insert(0, '../src')
from data_loader import FEMTOInspector

sns.set_style('whitegrid')
plt.rcParams['figure.figsize'] = (14, 6)

print("✓ Libraries imported")


def load_bearing_data(bearing_path):
    """
    Load all CSV files from a bearing condition folder.
    """
    bearing_path = Path(bearing_path)
    csv_files = sorted(bearing_path.glob('*.csv'))
    
    data_frames = []
    for csv_file in csv_files:
        try:
            df = pd.read_csv(csv_file)
            df['file_index'] = len(data_frames)
            data_frames.append(df)
        except Exception as e:
            print(f"Error loading {csv_file}: {e}")
    
    return data_frames

data_root = Path("../data/raw")
learning_set_path = data_root / "Learning_set"

# Load all bearing conditions
all_bearings = {}
bearing_names = sorted(os.listdir(learning_set_path))

for bearing_name in bearing_names:
    bearing_path = learning_set_path / bearing_name
    if bearing_path.is_dir():
        all_bearings[bearing_name] = load_bearing_data(bearing_path)

print(f"✓ Loaded {len(all_bearings)} bearing conditions")
print(f"Total files: {sum(len(data) for data in all_bearings.values())}")




# Inspect sample bearing
sample_bearing = all_bearings['Bearing1_1']
sample_data = pd.concat(sample_bearing, ignore_index=True)

print("\n=== Data Quality Report (Bearing1_1) ===")
print(f"\nShape: {sample_data.shape}")
print(f"\nData Types:\n{sample_data.dtypes}")
print(f"\nMissing Values:\n{sample_data.isnull().sum()}")
print(f"\nBasic Statistics:\n{sample_data[['Horizontal_vibration', 'Vertical_vibration']].describe()}")
print(f"\nValue Ranges:")
print(f"  Horizontal: [{sample_data['Horizontal_vibration'].min():.4f}, {sample_data['Horizontal_vibration'].max():.4f}]")
print(f"  Vertical: [{sample_data['Vertical_vibration'].min():.4f}, {sample_data['Vertical_vibration'].max():.4f}]")





# Inspect sample bearing
def check_missing_values(bearing_dict):
    """
    Check for missing values across all bearings.
    """
    missing_report = []
    
    for bearing_name, bearing_data in bearing_dict.items():
        combined = pd.concat(bearing_data, ignore_index=True)
        total_rows = len(combined)
        
        for col in combined.columns:
            missing_count = combined[col].isnull().sum()
            if missing_count > 0:
                missing_pct = (missing_count / total_rows) * 100
                missing_report.append({
                    'Bearing': bearing_name,
                    'Column': col,
                    'Missing': missing_count,
                    'Percentage': missing_pct
                })
    
    return pd.DataFrame(missing_report)

missing_df = check_missing_values(all_bearings)

if len(missing_df) > 0:
    print("\n=== Missing Values Found ===")
    print(missing_df.to_string())
else:
    print("✓ No missing values detected in dataset")







def detect_outliers_zscore(data, threshold=4):
    """
    Detect outliers using Z-score method.
    threshold=4 is very conservative (99.99% of data under normal distribution)
    """
    z_scores = np.abs(stats.zscore(data))
    return z_scores > threshold

def detect_outliers_iqr(data, multiplier=3.0):
    """
    Detect outliers using IQR method.
    multiplier=3.0 is aggressive (only severe outliers)
    """
    Q1 = np.percentile(data, 25)
    Q3 = np.percentile(data, 75)
    IQR = Q3 - Q1
    
    lower_bound = Q1 - multiplier * IQR
    upper_bound = Q3 + multiplier * IQR
    
    return (data < lower_bound) | (data > upper_bound)

# Check outliers in sample bearing
h_signal = sample_data['Horizontal_vibration'].values
v_signal = sample_data['Vertical_vibration'].values

outliers_z_h = detect_outliers_zscore(h_signal, threshold=4)
outliers_iqr_h = detect_outliers_iqr(h_signal, multiplier=3.0)

print("\n=== Outlier Detection Results (Bearing1_1 Horizontal) ===")
print(f"Z-score (threshold=4): {outliers_z_h.sum()} outliers ({100*outliers_z_h.sum()/len(h_signal):.2f}%)")
print(f"IQR (multiplier=3.0): {outliers_iqr_h.sum()} outliers ({100*outliers_iqr_h.sum()/len(h_signal):.2f}%)")

# Visualize
# fig, axes = plt.subplots(1, 2, figsize=(14, 5))
# fig.suptitle('Outlier Detection - Z-score vs IQR Method', fontsize=13, fontweight='bold')

# # Z-score
# axes[0].scatter(range(len(h_signal)), h_signal, alpha=0.5, s=5, label='Normal', color='steelblue')
# axes[0].scatter(np.where(outliers_z_h)[0], h_signal[outliers_z_h], color='red', s=20, label='Outliers', marker='x')
# axes[0].set_title('Z-score Method (threshold=4)', fontsize=11)
# axes[0].set_xlabel('Sample Index')
# axes[0].set_ylabel('Horizontal Vibration')
# axes[0].legend()
# axes[0].grid(True, alpha=0.3)

# # IQR
# axes[1].scatter(range(len(h_signal)), h_signal, alpha=0.5, s=5, label='Normal', color='steelblue')
# axes[1].scatter(np.where(outliers_iqr_h)[0], h_signal[outliers_iqr_h], color='red', s=20, label='Outliers', marker='x')
# axes[1].set_title('IQR Method (multiplier=3.0)', fontsize=11)
# axes[1].set_xlabel('Sample Index')
# axes[1].set_ylabel('Horizontal Vibration')
# axes[1].legend()
# axes[1].grid(True, alpha=0.3)

# plt.tight_layout()
# plt.savefig('../results/figures/03_outlier_detection.png', dpi=300, bbox_inches='tight')
# plt.show()

# print("\n✓ Saved to results/figures/03_outlier_detection.png")




# # Decision: Proceed without outlier removal
# # (Extreme values are legitimate bearing degradation)
# print("Decision: Keep all values (extreme values = bearing degradation)")
# print("Proceeding to normalization...")



# # Visualize different normalization methods
# sample_signal = sample_data['Horizontal_vibration'].values[:5000]  # First 5000 samples

# # Apply different scalers
# z_scaler = StandardScaler()
# minmax_scaler = MinMaxScaler()
# robust_scaler = RobustScaler()

# z_normalized = z_scaler.fit_transform(sample_signal.reshape(-1, 1)).flatten()
# minmax_normalized = minmax_scaler.fit_transform(sample_signal.reshape(-1, 1)).flatten()
# robust_normalized = robust_scaler.fit_transform(sample_signal.reshape(-1, 1)).flatten()

# # Compare
# fig, axes = plt.subplots(2, 2, figsize=(14, 8))
# fig.suptitle('Normalization Methods Comparison', fontsize=13, fontweight='bold')

# # Original
# axes[0, 0].hist(sample_signal, bins=50, color='steelblue', alpha=0.7, edgecolor='black')
# axes[0, 0].set_title(f'Original (Mean={np.mean(sample_signal):.2f}, Std={np.std(sample_signal):.2f})', fontsize=11)
# axes[0, 0].set_ylabel('Frequency')
# axes[0, 0].grid(True, alpha=0.3)

# # Z-score
# axes[0, 1].hist(z_normalized, bins=50, color='coral', alpha=0.7, edgecolor='black')
# axes[0, 1].set_title(f'Z-score (Mean={np.mean(z_normalized):.2f}, Std={np.std(z_normalized):.2f})', fontsize=11)
# axes[0, 1].set_ylabel('Frequency')
# axes[0, 1].grid(True, alpha=0.3)

# # Min-Max
# axes[1, 0].hist(minmax_normalized, bins=50, color='green', alpha=0.7, edgecolor='black')
# axes[1, 0].set_title(f'Min-Max (Min={np.min(minmax_normalized):.2f}, Max={np.max(minmax_normalized):.2f})', fontsize=11)
# axes[1, 0].set_xlabel('Value')
# axes[1, 0].set_ylabel('Frequency')
# axes[1, 0].grid(True, alpha=0.3)

# # Robust
# axes[1, 1].hist(robust_normalized, bins=50, color='purple', alpha=0.7, edgecolor='black')
# axes[1, 1].set_title(f'Robust (Median-based)', fontsize=11)
# axes[1, 1].set_xlabel('Value')
# axes[1, 1].set_ylabel('Frequency')
# axes[1, 1].grid(True, alpha=0.3)

# plt.tight_layout()
# plt.savefig('../results/figures/03_normalization_methods.png', dpi=300, bbox_inches='tight')
# plt.show()

# print("✓ Saved to results/figures/03_normalization_methods.png")
# print("\nRecommendation: Use Z-score (StandardScaler) for this dataset")





def apply_butterworth_filter(signal_data, fs=10000, lowcut=0.1, highcut=5000, order=4):
    """
    Apply Butterworth bandpass filter.
    fs: Sampling frequency (Hz)
    lowcut, highcut: Frequency band
    order: Filter order (higher = steeper cutoff)
    """
    nyquist = fs / 2
    low = lowcut / nyquist
    high = highcut / nyquist
    
    # Ensure frequencies are valid
    low = max(low, 0.0001)
    high = min(high, 0.9999)
    
    b, a = signal.butter(order, [low, high], btype='band')
    filtered = signal.filtfilt(b, a, signal_data)
    
    return filtered

# Apply filter to sample
filtered_signal = apply_butterworth_filter(sample_signal, fs=10000, lowcut=0.1, highcut=5000)

# Compare original vs filtered
fig, axes = plt.subplots(3, 1, figsize=(14, 8))
fig.suptitle('Signal Filtering: Original vs Filtered', fontsize=13, fontweight='bold')

# Time domain comparison
time_range = slice(0, 1000)  # First 1000 samples
axes[0].plot(sample_signal[time_range], linewidth=1, label='Original', alpha=0.7, color='steelblue')
axes[0].plot(filtered_signal[time_range], linewidth=1, label='Filtered', alpha=0.7, color='coral')
axes[0].set_title('Time Domain (First 1000 Samples)', fontsize=11)
axes[0].set_ylabel('Amplitude')
axes[0].legend()
axes[0].grid(True, alpha=0.3)

# Distribution comparison
axes[1].hist(sample_signal, bins=50, alpha=0.6, label='Original', color='steelblue', edgecolor='black')
axes[1].hist(filtered_signal, bins=50, alpha=0.6, label='Filtered', color='coral', edgecolor='black')
axes[1].set_title('Amplitude Distribution', fontsize=11)
axes[1].set_xlabel('Amplitude')
axes[1].set_ylabel('Frequency')
axes[1].legend()
axes[1].grid(True, alpha=0.3)

# Statistics comparison
stats_text = f"""Original Signal:
  Mean: {np.mean(sample_signal):.4f}
  Std: {np.std(sample_signal):.4f}
  RMS: {np.sqrt(np.mean(sample_signal**2)):.4f}

Filtered Signal:
  Mean: {np.mean(filtered_signal):.4f}
  Std: {np.std(filtered_signal):.4f}
  RMS: {np.sqrt(np.mean(filtered_signal**2)):.4f}
"""
axes[2].text(0.1, 0.5, stats_text, fontsize=11, family='monospace',
            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5),
            verticalalignment='center', transform=axes[2].transAxes)
axes[2].axis('off')

plt.tight_layout()
plt.savefig('../results/figures/03_signal_filtering.png', dpi=300, bbox_inches='tight')
plt.show()

print("✓ Saved to results/figures/03_signal_filtering.png")










def preprocess_bearing_data(bearing_data, scaler=None, fit_scaler=True):
    """
    Complete preprocessing pipeline for bearing data.
    
    Parameters:
    -----------
    bearing_data : list of DataFrames
        List of raw CSV dataframes for a bearing condition
    scaler : sklearn scaler object
        Pre-fitted scaler (from training data)
    fit_scaler : bool
        Whether to fit scaler on this data
    
    Returns:
    --------
    processed_data : list of DataFrames
        Preprocessed bearing data
    scaler : fitted scaler object
    """
    processed_data = []
    all_signals = []
    
    # Step 1: Extract and filter signals
    for df in bearing_data:
        df_copy = df.copy()
        
        # Remove any missing values
        df_copy = df_copy.dropna()
        
        # Apply Butterworth filter
        h_filtered = apply_butterworth_filter(df_copy['Horizontal_vibration'].values)
        v_filtered = apply_butterworth_filter(df_copy['Vertical_vibration'].values)
        
        df_copy['Horizontal_vibration'] = h_filtered
        df_copy['Vertical_vibration'] = v_filtered
        
        processed_data.append(df_copy)
        all_signals.extend(h_filtered)
        all_signals.extend(v_filtered)
    
    # Step 2: Fit or use scaler
    all_signals = np.array(all_signals).reshape(-1, 1)
    
    if fit_scaler:
        scaler = StandardScaler()
        scaler.fit(all_signals)


    if len(all_signals) == 0:
            raise ValueError("No signal samples collected after filtering; check input DataFrames and filter.")

    # Step 3: Apply normalization
    for df in processed_data:
        h_normalized = scaler.transform(df['Horizontal_vibration'].values.reshape(-1, 1)).flatten()
        v_normalized = scaler.transform(df['Vertical_vibration'].values.reshape(-1, 1)).flatten()
        
        df['Horizontal_vibration'] = h_normalized
        df['Vertical_vibration'] = v_normalized
    
    return processed_data, scaler

print("✓ Preprocessing pipeline defined")







# Preprocess all bearing conditions
preprocessed_bearings = {}
scalers = {}

for bearing_name, bearing_data in all_bearings.items():
    processed, scaler = preprocess_bearing_data(bearing_data, fit_scaler=True)
    preprocessed_bearings[bearing_name] = processed
    scalers[bearing_name] = scaler

print(f"✓ Preprocessed {len(preprocessed_bearings)} bearing conditions")
print("✓ Scalers saved for test set application")