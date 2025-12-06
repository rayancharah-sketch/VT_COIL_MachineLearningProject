"""
Data Download Script
Downloads the healthcare diabetes dataset from Kaggle
"""
from kaggle.api.kaggle_api_extended import KaggleApi

def download_dataset():
    """Download the diabetes dataset from Kaggle"""
    # Initialize and authenticate Kaggle API
    api = KaggleApi()
    api.authenticate()
    
    # Download and unzip dataset
    api.dataset_download_files("nanditapore/healthcare-diabetes", path=".", unzip=True)
    print("✓ Downloaded dataset 'nanditapore/healthcare-diabetes' successfully")

if __name__ == "__main__":
    download_dataset()
