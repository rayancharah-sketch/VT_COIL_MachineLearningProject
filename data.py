"""
Data Download Script
Downloads the healthcare diabetes dataset from Kaggle

LLM ATTRIBUTION:
Dataset selection and Kaggle API usage determined by students.
GitHub Copilot assisted with implementing Kaggle API authentication and download logic.
Used LLM for learning Kaggle API and debugging authentication issues.
Code was reviewed, reformatted, and edited by LLM for readability.
Final code was reviewed and edited for accuracy by students.
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
