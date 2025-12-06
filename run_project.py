"""
Quick Setup and Run Script
Automates the entire project setup and execution
"""
import os
import sys
import subprocess

def print_header(text):
    """Print a formatted header"""
    print("\n" + "="*60)
    print(f"  {text}")
    print("="*60 + "\n")

def run_command(description, command, check=True):
    """Run a command and handle errors"""
    print(f"⏳ {description}...")
    try:
        result = subprocess.run(command, shell=True, check=check, 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✓ {description} completed successfully")
            if result.stdout:
                print(result.stdout)
            return True
        else:
            print(f"⚠ {description} finished with warnings")
            if result.stderr:
                print(result.stderr)
            return False
    except subprocess.CalledProcessError as e:
        print(f"❌ Error during {description}")
        print(f"Error message: {e.stderr}")
        return False

def main():
    """Main setup and run workflow"""
    print_header("DIABETES RISK PREDICTOR - SETUP & RUN")
    
    # Check if Python is available
    print("🔍 Checking Python installation...")
    try:
        import sys
        print(f"✓ Python {sys.version} found")
    except:
        print("❌ Python not found. Please install Python 3.8 or higher.")
        sys.exit(1)
    
    # Step 1: Install dependencies
    print_header("STEP 1: Installing Dependencies")
    if not run_command("Installing Python packages", 
                       f"{sys.executable} -m pip install -r requirements.txt"):
        print("⚠ Some packages may not have installed. Continuing anyway...")
    
    # Step 2: Download dataset
    print_header("STEP 2: Downloading Dataset")
    if os.path.exists("healthcare-diabetes.csv"):
        print("✓ Dataset already exists, skipping download")
    else:
        if not run_command("Downloading dataset from Kaggle", 
                          f"{sys.executable} data.py", check=False):
            print("\n⚠ Dataset download failed!")
            print("Please ensure:")
            print("  1. You have a Kaggle account")
            print("  2. Your kaggle.json file is in C:\\Users\\<YourName>\\.kaggle\\")
            print("  3. You've accepted the dataset's terms on Kaggle.com")
            response = input("\nWould you like to continue anyway? (y/n): ")
            if response.lower() != 'y':
                sys.exit(1)
    
    # Step 3: Train model
    print_header("STEP 3: Training Neural Network Model")
    if os.path.exists("models/diabetes_model.h5"):
        response = input("Model already exists. Retrain? (y/n): ")
        if response.lower() != 'y':
            print("✓ Using existing model")
        else:
            run_command("Training model", f"{sys.executable} train_model.py")
    else:
        if not run_command("Training model", f"{sys.executable} train_model.py", check=False):
            print("\n⚠ Model training failed!")
            print("The web app will still start, but predictions won't work.")
            response = input("\nWould you like to start the web app anyway? (y/n): ")
            if response.lower() != 'y':
                sys.exit(1)
    
    # Step 4: Launch web application
    print_header("STEP 4: Starting Web Application")
    print("\n🚀 Launching Flask web server...")
    print("📱 Open your browser and navigate to: http://127.0.0.1:5000")
    print("⌨️  Press CTRL+C to stop the server\n")
    
    try:
        subprocess.run(f"{sys.executable} app.py", shell=True)
    except KeyboardInterrupt:
        print("\n\n✓ Server stopped")
        print("Thank you for using the Diabetes Risk Predictor!")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠ Setup interrupted by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ An unexpected error occurred: {e}")
        sys.exit(1)
