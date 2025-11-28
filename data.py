"""
Data Verification Script
Verifies the local healthcare diabetes dataset exists and displays basic info
"""
import os
import pandas as pd

def verify_dataset():
    """Verify the local diabetes dataset exists and show basic info"""
    dataset_path = "Healthcare-Diabetes.csv"
    
    if not os.path.exists(dataset_path):
        print(f"✗ Dataset not found: {dataset_path}")
        print("Please ensure 'Healthcare-Diabetes.csv' is in the project directory.")
        return False
    
    print(f"✓ Dataset found: {dataset_path}")
    
    # Load and display basic info
    try:
        df = pd.read_csv(dataset_path)
        print(f"\n📊 Dataset Information:")
        print(f"   Rows: {len(df)}")
        print(f"   Columns: {len(df.columns)}")
        print(f"   Features: {', '.join(df.columns.tolist())}")
        print(f"\n✓ Dataset is ready to use!")
        return True
    except Exception as e:
        print(f"✗ Error reading dataset: {e}")
        return False

if __name__ == "__main__":
    verify_dataset()
