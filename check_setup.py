"""
Project Health Check
Verifies that all required files and dependencies are in place

LLM ATTRIBUTION:
Verification logic designed by students, implemented with GitHub Copilot assistance.
Copilot helped structure the check functions and format status output.
Used LLM for debugging file path issues and testing verification logic.
Code was reviewed, reformatted, and edited by LLM for readability.
Final code was reviewed and edited for accuracy by students.
"""
import os
import sys

def check_file(filepath, description):
    """Check if a file exists"""
    exists = os.path.exists(filepath)
    status = "✓" if exists else "✗"
    print(f"{status} {description}: {filepath}")
    return exists

def check_directory(dirpath, description):
    """Check if a directory exists"""
    exists = os.path.isdir(dirpath)
    status = "✓" if exists else "✗"
    print(f"{status} {description}: {dirpath}")
    return exists

def check_python_package(package_name):
    """Check if a Python package is installed"""
    try:
        if package_name == 'kaggle':
            # Special handling for kaggle package
            import kaggle
            print(f"✓ {package_name}")
            return True
        else:
            __import__(package_name.split('==')[0].replace('-', '_'))
            print(f"✓ {package_name}")
            return True
    except ImportError:
        print(f"✗ {package_name}")
        return False
    except Exception:
        # For kaggle API, the import might fail if credentials missing
        # but package is installed
        print(f"⚠ {package_name} (installed but needs configuration)")
        return True

def main():
    print("="*60)
    print("  DIABETES RISK PREDICTOR - PROJECT HEALTH CHECK")
    print("="*60)
    
    # Check Python version
    print("\n📌 Python Version:")
    print(f"   {sys.version}")
    if sys.version_info < (3, 8):
        print("⚠  Warning: Python 3.8+ recommended")
    
    # Check project structure
    print("\n📂 Project Structure:")
    all_files = True
    
    files_to_check = [
        ("data.py", "Dataset download script"),
        ("preprocess.py", "Data preprocessing"),
        ("train_model.py", "Model training"),
        ("app.py", "Flask web application"),
        ("run_project.py", "Automated setup script"),
        ("requirements.txt", "Dependencies list"),
        ("README.md", "Documentation"),
        ("QUICK_REFERENCE.md", "Quick reference guide"),
        (".gitignore", "Git ignore file"),
    ]
    
    for filepath, description in files_to_check:
        if not check_file(filepath, description):
            all_files = False
    
    print("\n📁 Directories:")
    dirs_to_check = [
        ("models", "Model storage"),
        ("templates", "HTML templates"),
        ("static/css", "Stylesheets"),
        ("static/js", "JavaScript files"),
        ("notebooks", "Jupyter notebooks"),
    ]
    
    for dirpath, description in dirs_to_check:
        if not check_directory(dirpath, description):
            all_files = False
    
    print("\n📄 Template Files:")
    template_files = [
        ("templates/index.html", "Main page"),
        ("templates/about.html", "About page"),
    ]
    
    for filepath, description in template_files:
        if not check_file(filepath, description):
            all_files = False
    
    print("\n🎨 Static Files:")
    static_files = [
        ("static/css/style.css", "Main stylesheet"),
        ("static/js/script.js", "Main JavaScript"),
    ]
    
    for filepath, description in static_files:
        if not check_file(filepath, description):
            all_files = False
    
    # Check Python packages
    print("\n📦 Python Packages:")
    packages_to_check = [
        "tensorflow",
        "sklearn",
        "pandas",
        "numpy",
        "matplotlib",
        "seaborn",
        "flask",
        "joblib",
        "kaggle",
    ]
    
    all_packages = True
    for package in packages_to_check:
        if not check_python_package(package):
            all_packages = False
    
    # Check optional files/artifacts
    print("\n🔍 Training Artifacts (created after training):")
    artifacts = [
        ("healthcare-diabetes.csv", "Dataset"),
        ("models/diabetes_model.h5", "Trained model"),
        ("models/scaler.pkl", "Feature scaler"),
        ("models/feature_names.pkl", "Feature names"),
        ("models/feature_importance.pkl", "Feature importance"),
    ]
    
    artifacts_exist = 0
    for filepath, description in artifacts:
        if check_file(filepath, description):
            artifacts_exist += 1
    
    # Check Kaggle API
    print("\n🔑 Kaggle API Configuration:")
    kaggle_path = os.path.expanduser("~/.kaggle/kaggle.json")
    windows_kaggle_path = os.path.expanduser("~\\.kaggle\\kaggle.json")
    
    if os.path.exists(kaggle_path) or os.path.exists(windows_kaggle_path):
        print("✓ Kaggle API credentials found")
    else:
        print("✗ Kaggle API credentials NOT found")
        print("  → Download from https://www.kaggle.com/account")
        print(f"  → Place in: {windows_kaggle_path}")
    
    # Summary
    print("\n" + "="*60)
    print("  SUMMARY")
    print("="*60)
    
    if all_files and all_packages:
        print("✅ All required files and packages are in place!")
        if artifacts_exist == len(artifacts):
            print("✅ All training artifacts found - ready to run!")
            print("\n🚀 Next step: python app.py")
        else:
            print("⚠  Training artifacts missing - need to train model")
            print("\n🚀 Next steps:")
            print("   1. python data.py       (download dataset)")
            print("   2. python train_model.py (train model)")
            print("   3. python app.py        (run web app)")
    else:
        if not all_files:
            print("❌ Some project files are missing")
        if not all_packages:
            print("❌ Some Python packages are not installed")
            print("\n🔧 Fix: pip install -r requirements.txt")
    
    print("\n💡 Tip: Run 'python run_project.py' for automated setup")
    print("="*60)

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n❌ Error during health check: {e}")
        sys.exit(1)
