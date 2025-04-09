import pandas as pd
import os
import re

# Directory where cleaned CSVs are stored (2014 – 2024)
DATA_DIR = r"C:\Users\footb\Desktop\Agriculture Forecasting\Datasets\Weather_Dataset\final"

# Expected schema
EXPECTED_COLS = {
    'District', 'Mandal', 'Date',
    'Rainfall (mm)', 'Min Humidity (%)', 'Max Humidity (%)'
}
EXPECTED_DTYPES = {
    'District': 'object',
    'Mandal': 'object',
    'Date': 'datetime64[ns]',
    'Rainfall (mm)': 'float64',
    'Min Humidity (%)': 'float64',
    'Max Humidity (%)': 'float64'
}

# === Main Analyzer Function ===
def analyze_file(filepath):
    try:
        df = pd.read_csv(filepath)
        df.columns = df.columns.str.strip()  # Remove accidental spaces

        # Extract year from filename using regex
        filename = os.path.basename(filepath)
        match = re.search(r'20\d{2}', filename)
        year = match.group() if match else 'Unknown'
        print(f"\n📘 Year: {year} | File: {filename} | Records: {len(df)}")

        # === 1. Column & Data Type Check ===
        print("\n📌 Column Types:")
        print(df.dtypes)

        unexpected_cols = set(df.columns) - EXPECTED_COLS
        if unexpected_cols:
            print(f"⚠️ Unexpected columns: {unexpected_cols}")

        missing_cols = EXPECTED_COLS - set(df.columns)
        if missing_cols:
            print(f"❌ Missing expected columns: {missing_cols}")

        # Check type mismatches
        mismatches = {
            col: (df[col].dtype, EXPECTED_DTYPES[col])
            for col in EXPECTED_COLS if col in df.columns and df[col].dtype != EXPECTED_DTYPES[col]
        }
        if mismatches:
            print("⚠️ Data type mismatches:")
            for col, (found, expected) in mismatches.items():
                print(f"   - {col}: found {found}, expected {expected}")

        # === 2. Date Validation ===
        if 'Date' in df.columns:
            df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
            invalid_dates = df['Date'].isna().sum()
            if invalid_dates > 0:
                print(f"⚠️ Invalid dates found: {invalid_dates}")

            # Date coverage check
            expected_days = 366 if year == '2020' else 365
            unique_dates = df['Date'].nunique()
            if unique_dates < expected_days * 0.9:
                print(f"⚠️ Incomplete date coverage: only {unique_dates} unique dates")

        # === 3. Missing Values ===
        print("\n🧼 Missing Values:")
        na_counts = df.isna().sum()
        has_missing = na_counts[na_counts > 0]
        if not has_missing.empty:
            total = len(df)
            print("Column (Count / %):")
            for col, count in has_missing.items():
                pct = (count / total) * 100
                print(f"  - {col}: {count} ({pct:.2f}%)")
        else:
            print("✅ No missing values")

        # === 4. Row Count Validation ===
        min_expected = 33 * 200 * (366 if year == '2020' else 365)
        if len(df) < min_expected * 0.9:
            print(f"⚠️ Row count low: {len(df)} (Expected ~{min_expected})")

        # === 5. Sample Preview ===
        print("\n🔍 Sample Records:")
        print(df.head(3))

    except Exception as e:
        print(f"❌ Error analyzing {filepath}: {e}")

# === Batch Run Over All Files ===
for year in range(2014, 2025):
    file = f"final_daily_rainfall_{year}.csv"
    full_path = os.path.join(DATA_DIR, file)
    if os.path.exists(full_path):
        analyze_file(full_path)
    else:
        print(f"❌ Missing: {file}")

