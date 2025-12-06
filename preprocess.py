"""
Data Preprocessing Pipeline
Handles data loading, cleaning, feature engineering, and train/test split

LLM ATTRIBUTION:
Preprocessing strategy (scaling, train-test split) designed by students.
GitHub Copilot assisted with print statements for data exploration and debugging output.
Used LLM for learning pandas and scikit-learn best practices for data preprocessing.
Code was reviewed, reformatted, and edited by LLM for readability.
Final code was reviewed and edited for accuracy by students.
"""
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import joblib
import os

def load_and_preprocess_data(dataset_path='healthcare-diabetes.csv'):
    """
    Load and preprocess the diabetes dataset
    
    Args:
        dataset_path: Path to the CSV file
    
    Returns:
        X_train, X_test, y_train, y_test, scaler, feature_names
    """
    print("Loading dataset...")
    df = pd.read_csv(dataset_path)
    
    print(f"Dataset shape: {df.shape}")
    print(f"\nColumns: {df.columns.tolist()}")
    print(f"\nFirst few rows:\n{df.head()}")
    print(f"\nData types:\n{df.dtypes}")
    print(f"\nMissing values:\n{df.isnull().sum()}")
    print(f"\nDataset statistics:\n{df.describe()}")
    
    # Handle missing values
    print("\nHandling missing values...")
    # For numeric columns, fill with median
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    for col in numeric_cols:
        if df[col].isnull().sum() > 0:
            df[col].fillna(df[col].median(), inplace=True)
    
    # Identify target column (commonly 'Outcome', 'Diabetes', or similar)
    target_candidates = ['Outcome', 'diabetes', 'Diabetes', 'target', 'label']
    target_col = None
    for candidate in target_candidates:
        if candidate in df.columns:
            target_col = candidate
            break
    
    if target_col is None:
        # If no standard target found, assume last column is target
        target_col = df.columns[-1]
        print(f"⚠ No standard target column found, using '{target_col}'")
    
    print(f"Target column: {target_col}")
    print(f"Class distribution:\n{df[target_col].value_counts()}")
    
    # Separate features and target
    X = df.drop(columns=[target_col])
    y = df[target_col]
    
    # Keep only numeric features
    X = X.select_dtypes(include=[np.number])
    feature_names = X.columns.tolist()
    
    print(f"\nFeatures used: {feature_names}")
    print(f"Number of features: {len(feature_names)}")
    
    # Split data into train and test sets (80/20)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    print(f"\nTrain set size: {len(X_train)}")
    print(f"Test set size: {len(X_test)}")
    
    # Feature scaling using StandardScaler
    print("\nScaling features...")
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # Save the scaler
    os.makedirs('models', exist_ok=True)
    joblib.dump(scaler, 'models/scaler.pkl')
    print("✓ Scaler saved to models/scaler.pkl")
    
    # Save feature names
    joblib.dump(feature_names, 'models/feature_names.pkl')
    print("✓ Feature names saved to models/feature_names.pkl")
    
    return X_train_scaled, X_test_scaled, y_train, y_test, scaler, feature_names

if __name__ == "__main__":
    # Run preprocessing
    X_train, X_test, y_train, y_test, scaler, features = load_and_preprocess_data()
    print("\n✓ Data preprocessing completed successfully!")
    print(f"Training samples: {X_train.shape}")
    print(f"Testing samples: {X_test.shape}")
