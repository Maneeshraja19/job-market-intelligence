import pandas as pd
import os

RAW_DATA_DIR = "data/raw"

def summarize_raw_data():
    """Print a quick summary of all CSV files in the raw data folder."""
    files = [f for f in os.listdir(RAW_DATA_DIR) if f.endswith('.csv')]
    
    if not files:
        print("No CSV files found in data/raw/")
        return
    
    for file in files:
        path = os.path.join(RAW_DATA_DIR, file)
        df = pd.read_csv(path)
        print(f"\n{file}")
        print(f"  Rows: {len(df)}")
        print(f"  Columns: {list(df.columns)}")

if __name__ == "__main__":
    summarize_raw_data()