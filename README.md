# 🏥 Diabetes Risk Prediction System

A machine learning web application that predicts diabetes risk using neural networks. Built with TensorFlow/Keras and Flask.

## 👥 Team Members
- **Rayan Charah** - 906695619
- **Ifzaal Ahamed Imdad** - 906718090
- **Jhonatan Quiroga** - 00330058

## 📚 Learning Objectives
1. Understand how neural networks classify medical data
2. Gain practical experience with Python ML libraries (TensorFlow, scikit-learn)
3. Explore AI applications in healthcare and analyze their potential impact
4. Develop full-stack ML applications with web interfaces

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Local dataset: `Healthcare-Diabetes.csv` (included in repository)

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/rayancharah-sketch/VT_COIL_MachineLearningProject.git
cd VT_COIL_MachineLearningProject
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Verify the dataset** (optional)
```bash
python data.py
```
The dataset `Healthcare-Diabetes.csv` should already be in the project directory.

4. **Train the model**
```bash
python train_model.py
```

5. **Run the web application**
```bash
python app.py
```

6. **Open your browser**
   - Navigate to: `http://127.0.0.1:5000`

## 📁 Project Structure

```
VT_COIL_MachineLearningProject/
│
├── data.py                 # Dataset download script
├── preprocess.py           # Data preprocessing pipeline
├── train_model.py          # Model training and evaluation
├── app.py                  # Flask web application
│
├── models/                 # Saved models and artifacts
│   ├── diabetes_model.h5   # Trained neural network
│   ├── scaler.pkl          # Feature scaler
│   ├── feature_names.pkl   # Feature names list
│   ├── feature_importance.pkl  # Feature importance scores
│   └── training_history.png    # Training visualization
│
├── templates/              # HTML templates
│   ├── index.html          # Main prediction page
│   └── about.html          # About/documentation page
│
├── static/                 # Static assets
│   ├── css/
│   │   └── style.css       # Custom styles
│   └── js/
│       └── script.js       # Frontend JavaScript
│
├── notebooks/              # Jupyter notebooks (optional)
├── requirements.txt        # Python dependencies
└── README.md              # This file
```

## 🧠 Model Architecture

**Neural Network Specifications:**
- **Framework:** TensorFlow/Keras
- **Type:** Feedforward Neural Network
- **Architecture:**
  - Input Layer: Variable (based on dataset features)
  - Hidden Layer 1: 16 neurons, ReLU activation, 30% dropout
  - Hidden Layer 2: 8 neurons, ReLU activation, 20% dropout
  - Output Layer: 1 neuron, Sigmoid activation
- **Loss Function:** Binary Crossentropy
- **Optimizer:** Adam
- **Training:** 80/20 train-test split, early stopping

## 📊 Dataset

**Source:** Local CSV File - Healthcare-Diabetes.csv  
**Included:** Yes, in the project repository

The dataset contains various health indicators including:
- Glucose levels
- Blood pressure
- BMI (Body Mass Index)
- Age
- Insulin levels
- And other diabetes risk factors

## 🎯 Features

### Core Features
✅ Neural network-based diabetes risk prediction  
✅ Data preprocessing with StandardScaler normalization  
✅ Train/test evaluation with multiple metrics  
✅ Feature importance calculation  
✅ Web interface for easy predictions  

### Web Application
✅ User-friendly form for health metric input  
✅ Real-time risk prediction (Low/Moderate/High)  
✅ Confidence scores and probability estimates  
✅ Top contributing factors visualization  
✅ AI health assistant explanations  
✅ Medical disclaimers and safety information  

### Explainability
✅ Feature importance ranking  
✅ Human-readable explanations  
✅ Health recommendations based on risk factors  
✅ Transparent prediction process  

## 📈 Model Performance

The model is evaluated using:
- **Accuracy** - Overall prediction correctness
- **Precision** - True positive rate
- **Recall** - Sensitivity to positive cases
- **F1-Score** - Harmonic mean of precision and recall
- **ROC-AUC** - Area under the ROC curve

Performance metrics are displayed in the web interface footer after training.

## 🔧 Usage Examples

### Training a New Model
```bash
python train_model.py
```

### Making Predictions via CLI
```python
from tensorflow import keras
import joblib
import numpy as np

# Load model and scaler
model = keras.models.load_model('models/diabetes_model.h5')
scaler = joblib.load('models/scaler.pkl')

# Sample input
sample_data = np.array([[3, 148, 72, 35, 0, 33.6, 0.627, 50]])
scaled_data = scaler.transform(sample_data)

# Predict
prediction = model.predict(scaled_data)
print(f"Diabetes risk probability: {prediction[0][0]:.2%}")
```

### Running the Web App
```bash
python app.py
```
Then visit `http://127.0.0.1:5000` in your browser.

## ⚠️ Important Disclaimers

**Medical Disclaimer:**  
This application is for **EDUCATIONAL PURPOSES ONLY**. It is NOT a medical diagnostic tool and should never be used as a substitute for professional medical advice, diagnosis, or treatment. Always consult with qualified healthcare professionals regarding any medical condition or health concerns.

**Data Privacy:**  
This application does not store or transmit user health data. All predictions are performed locally and are not saved.

## 🤖 AI & LLM Usage

This project follows ethical AI guidelines set by Virginia Tech and USFQ. Large Language Models (LLMs) were consulted for:
- Brainstorming model architectures
- Debugging assistance and error explanations
- Code structure and best practices
- Visualization ideas and explainability features

**LLMs Used:** ChatGPT-4, GitHub Copilot

All AI-generated code was thoroughly reviewed, tested, and modified by the team.

## 📚 References

1. **Chinta, S. V., Wang, Z., Palikhe, A., Zhang, X., Kashif, A., Smith, M. A., & Zhang, W. (2025).** AI-driven healthcare: A review on ensuring. National Tsing Hua University.

2. **Koski, E., & Murphy, J. (2021).** AI in Healthcare. New York: IBM.

3. **Saraswat, D., Bhattacharya, P., Verma, A., Prasad, V. K., Tanwar, S., Sharma, G., & Sharma, R. (2022).** Explainable AI for Healthcare 5.0: Opportunities. IEEE Access.

4. **Kaggle Dataset:** nanditapore/healthcare-diabetes  
   https://www.kaggle.com/datasets/nanditapore/healthcare-diabetes

5. **scikit-learn Documentation**  
   https://scikit-learn.org/stable/modules/classification.html

6. **TensorFlow/Keras Documentation**  
   https://www.tensorflow.org/guide/keras

## 🛠️ Technologies Used

**Machine Learning:**
- TensorFlow 2.15.0
- Keras (TensorFlow backend)
- scikit-learn 1.3.2
- pandas 2.1.4
- NumPy 1.26.2

**Visualization:**
- Matplotlib 3.8.2
- Seaborn 0.13.0

**Web Framework:**
- Flask 3.0.0
- Bootstrap 5.3.0

**Other:**
- joblib 1.3.2

## 🐛 Troubleshooting

### Issue: "Model not found"
**Solution:** Run `python train_model.py` first to train and save the model.

### Issue: "Dataset not found"
**Solution:** Ensure `Healthcare-Diabetes.csv` is in the project root directory. The file should be included in the repository.

### Issue: Port 5000 already in use
**Solution:** Edit `app.py` and change the port number:
```python
app.run(debug=True, host='0.0.0.0', port=5001)  # Use a different port
```

## 📝 License

This project is for educational purposes as part of the VGC Group Project for Virginia Tech and USFQ courses.

## 📧 Contact

For questions or feedback, please contact any team member through the course channels.

---

**Virginia Tech & USFQ | 2025**