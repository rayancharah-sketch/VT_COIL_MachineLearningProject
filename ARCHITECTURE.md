# System Architecture Diagram

## 📊 Complete Data Flow

```
┌─────────────────────────────────────────────────────────────────────────┐
│                        DIABETES RISK PREDICTOR                           │
│                      Full-Stack ML Application                           │
└─────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────┐
│ PHASE 1: DATA ACQUISITION & PREPARATION                                 │
└─────────────────────────────────────────────────────────────────────────┘

    data.py
    ───────────►  Kaggle API  ───────────►  healthcare-diabetes.csv
                  (Download)                 (Raw Dataset)
                     │
                     ▼
    preprocess.py
    ───────────►  pandas/sklearn  ────────►  Processed Data
                  • Handle missing values      • X_train (scaled)
                  • Feature scaling            • X_test (scaled)
                  • Train/test split           • y_train
                  • Save scaler                • y_test
                     │
                     ▼
                  models/
                  • scaler.pkl
                  • feature_names.pkl


┌─────────────────────────────────────────────────────────────────────────┐
│ PHASE 2: MODEL TRAINING & EVALUATION                                    │
└─────────────────────────────────────────────────────────────────────────┘

    train_model.py
    ───────────►  TensorFlow/Keras  ─────►  Neural Network
                  Build Model:               Architecture:
                  • Input Layer              ┌────────────────┐
                  • Dense(16) + ReLU        │ Input Features │
                  • Dropout(0.3)            └────────┬───────┘
                  • Dense(8) + ReLU                  │
                  • Dropout(0.2)             ┌───────▼────────┐
                  • Dense(1) + Sigmoid      │ Dense (16, ReLU)│
                                             │ Dropout (30%)   │
                  Train:                     └───────┬────────┘
                  • 50 epochs                        │
                  • Binary crossentropy      ┌───────▼────────┐
                  • Adam optimizer          │ Dense (8, ReLU) │
                  • Early stopping          │ Dropout (20%)   │
                     │                       └───────┬────────┘
                     ▼                               │
                  Evaluate:                  ┌───────▼────────┐
                  • Accuracy                 │ Output (Sigmoid)│
                  • Precision                └────────────────┘
                  • Recall
                  • F1-Score
                  • ROC-AUC
                     │
                     ▼
                  models/
                  • diabetes_model.h5
                  • feature_importance.pkl
                  • metrics.pkl
                  • training_history.png


┌─────────────────────────────────────────────────────────────────────────┐
│ PHASE 3: WEB APPLICATION & DEPLOYMENT                                   │
└─────────────────────────────────────────────────────────────────────────┘

    ┌──────────────────────┐
    │    Web Browser       │
    │   http://localhost   │
    │        :5000         │
    └──────────┬───────────┘
               │
    ┌──────────▼───────────────────────────────────────────────────────┐
    │                    FRONTEND (HTML/CSS/JS)                        │
    ├──────────────────────────────────────────────────────────────────┤
    │  templates/index.html                                            │
    │  • User Input Form (BMI, Glucose, Age, etc.)                    │
    │  • Sample Data Button                                            │
    │  • Results Display Section                                       │
    │                                                                   │
    │  templates/about.html                                            │
    │  • Project Documentation                                         │
    │  • Team Information                                              │
    │  • Technology Stack                                              │
    │                                                                   │
    │  static/css/style.css                                            │
    │  • Modern Gradient Design                                        │
    │  • Responsive Layout                                             │
    │  • Animations                                                    │
    │                                                                   │
    │  static/js/script.js                                             │
    │  • Form Submission Handler                                       │
    │  • AJAX Prediction Request                                       │
    │  • Results Display Logic                                         │
    └───────────────────────────┬──────────────────────────────────────┘
                                │ HTTP POST /predict
                                │ {feature1: value1, ...}
                                ▼
    ┌────────────────────────────────────────────────────────────────┐
    │                  BACKEND (Flask API)                            │
    ├────────────────────────────────────────────────────────────────┤
    │  app.py                                                         │
    │                                                                  │
    │  Route: GET /                                                   │
    │  └─► Render index.html with feature names                      │
    │                                                                  │
    │  Route: POST /predict                                           │
    │  └─► 1. Receive user input (JSON)                              │
    │      2. Load model & scaler                                     │
    │      3. Scale input features                                    │
    │      4. Make prediction                                         │
    │      5. Calculate risk level                                    │
    │      6. Get feature importance                                  │
    │      7. Generate explanation                                    │
    │      8. Return JSON response                                    │
    │                                                                  │
    │  Route: GET /about                                              │
    │  └─► Render about.html                                         │
    └─────────────────────────┬──────────────────────────────────────┘
                              │
              ┌───────────────┴───────────────┐
              ▼                               ▼
    ┌─────────────────┐           ┌──────────────────┐
    │ ML Model Engine │           │ Explainability   │
    ├─────────────────┤           │ Engine           │
    │ • Load model.h5 │           ├──────────────────┤
    │ • Load scaler   │           │ • Feature ranks  │
    │ • Predict proba │           │ • Explanations   │
    │ • Risk level    │           │ • Recommendations│
    └─────────────────┘           └──────────────────┘
              │                               │
              └───────────────┬───────────────┘
                              ▼
                    JSON Response
                    {
                      "success": true,
                      "risk_level": "High",
                      "probability": 0.85,
                      "confidence": "85.0%",
                      "top_features": [...],
                      "explanation": "...",
                      "disclaimer": "..."
                    }
                              │
                              ▼
                    ┌────────────────────┐
                    │ User sees results: │
                    │ • Risk level badge │
                    │ • Key factors      │
                    │ • AI explanations  │
                    │ • Recommendations  │
                    └────────────────────┘


┌─────────────────────────────────────────────────────────────────────────┐
│ TECHNOLOGY STACK SUMMARY                                                 │
└─────────────────────────────────────────────────────────────────────────┘

Backend:
  • Python 3.12
  • TensorFlow 2.15 (Neural Network)
  • scikit-learn 1.3 (Preprocessing)
  • Flask 3.0 (Web Framework)
  • pandas/NumPy (Data Handling)

Frontend:
  • HTML5
  • CSS3 (with custom styling)
  • JavaScript (ES6+)
  • Bootstrap 5.3

Data:
  • Kaggle API (Dataset Download)
  • CSV Format (Input Data)
  • joblib (Model Persistence)

DevOps:
  • Git (Version Control)
  • pip (Package Management)


┌─────────────────────────────────────────────────────────────────────────┐
│ FILE STRUCTURE                                                           │
└─────────────────────────────────────────────────────────────────────────┘

VT_COIL_MachineLearningProject/
│
├── 📄 Core Python Scripts
│   ├── data.py              ← Downloads dataset
│   ├── preprocess.py        ← Cleans & prepares data
│   ├── train_model.py       ← Trains neural network
│   └── app.py               ← Flask web server
│
├── 🌐 Web Interface
│   ├── templates/
│   │   ├── index.html       ← Main prediction page
│   │   └── about.html       ← Documentation page
│   │
│   └── static/
│       ├── css/
│       │   └── style.css    ← Custom styles
│       └── js/
│           └── script.js    ← Frontend logic
│
├── 🧠 Trained Models & Artifacts
│   └── models/
│       ├── diabetes_model.h5          ← Trained NN
│       ├── scaler.pkl                 ← Feature scaler
│       ├── feature_names.pkl          ← Feature list
│       ├── feature_importance.pkl     ← Importance scores
│       ├── metrics.pkl                ← Performance metrics
│       └── training_history.png       ← Training curves
│
├── 📚 Documentation
│   ├── README.md            ← Main documentation
│   ├── PROJECT_SUMMARY.md   ← Implementation summary
│   ├── QUICK_REFERENCE.md   ← Quick commands guide
│   └── ARCHITECTURE.md      ← This file
│
├── 🔧 Configuration
│   ├── requirements.txt     ← Python dependencies
│   ├── .gitignore          ← Git exclusions
│   ├── run_project.py      ← Automated setup
│   └── check_setup.py      ← Health check
│
└── 📓 Optional
    └── notebooks/           ← Jupyter notebooks


┌─────────────────────────────────────────────────────────────────────────┐
│ USER JOURNEY                                                             │
└─────────────────────────────────────────────────────────────────────────┘

1. User visits http://localhost:5000
   └─► Sees professional landing page with gradient background

2. User fills health metrics form:
   • Pregnancies, Glucose, Blood Pressure, etc.
   OR clicks "Use Sample Data" button

3. User clicks "Predict Diabetes Risk"
   └─► JavaScript sends AJAX POST request

4. Flask backend processes request:
   a) Validates input
   b) Scales features using saved scaler
   c) Runs prediction through neural network
   d) Calculates risk level (Low/Moderate/High)
   e) Gets top contributing features
   f) Generates human-readable explanation

5. User sees results:
   ┌──────────────────────────────────────┐
   │  🚨 High Risk Detected                │
   │  Confidence: 85.0%                    │
   │                                       │
   │  🔍 Key Contributing Factors:         │
   │  • Glucose: 148 (56.2% importance)   │
   │  • BMI: 33.6 (24.1% importance)      │
   │  • Age: 50 (12.8% importance)        │
   │                                       │
   │  💡 AI Health Assistant:              │
   │  Your glucose level (148) is          │
   │  elevated. Consider discussing this   │
   │  with a healthcare professional...    │
   │                                       │
   │  ⚠️ Disclaimer: Educational only      │
   └──────────────────────────────────────┘

6. User can:
   • Try different inputs
   • Read detailed explanations
   • View About page for more info


┌─────────────────────────────────────────────────────────────────────────┐
│ DEPLOYMENT WORKFLOW                                                      │
└─────────────────────────────────────────────────────────────────────────┘

Local Development:
  python run_project.py
  └─► Automated: Install → Download → Train → Deploy

Manual Steps:
  1. pip install -r requirements.txt
  2. python data.py
  3. python train_model.py
  4. python app.py
  5. Open browser: http://127.0.0.1:5000


Future Cloud Deployment (Optional):
  • Heroku: Free tier available
  • AWS: EC2 or Elastic Beanstalk
  • Google Cloud: App Engine
  • Azure: App Service


┌─────────────────────────────────────────────────────────────────────────┐
│ LEARNING OUTCOMES MAPPED TO COMPONENTS                                   │
└─────────────────────────────────────────────────────────────────────────┘

Objective 1: Neural Networks Understanding
  ├─► train_model.py - Architecture implementation
  ├─► models/diabetes_model.h5 - Trained weights
  └─► Feature importance calculation

Objective 2: Python ML Experience
  ├─► TensorFlow/Keras - Deep learning
  ├─► scikit-learn - Preprocessing & metrics
  ├─► pandas - Data manipulation
  └─► NumPy - Numerical computing

Objective 3: AI in Healthcare
  ├─► Diabetes prediction use case
  ├─► Explainable AI (feature importance)
  ├─► Medical disclaimers
  └─► Ethical considerations


═══════════════════════════════════════════════════════════════════════════
                        END OF ARCHITECTURE DIAGRAM
═══════════════════════════════════════════════════════════════════════════
```
