"""
Flask Web Application for Diabetes Risk Prediction
Provides a web interface for users to input health metrics and receive risk predictions
"""
from flask import Flask, render_template, request, jsonify
import numpy as np
import joblib
from tensorflow import keras
import os

app = Flask(__name__)

# Load model and preprocessing artifacts
MODEL_PATH = 'models/diabetes_model.h5'
SCALER_PATH = 'models/scaler.pkl'
FEATURE_NAMES_PATH = 'models/feature_names.pkl'
FEATURE_IMPORTANCE_PATH = 'models/feature_importance.pkl'
METRICS_PATH = 'models/metrics.pkl'

# Global variables for loaded objects
model = None
scaler = None
feature_names = None
feature_importance = None
metrics = None

def load_model_and_artifacts():
    """Load trained model and preprocessing artifacts"""
    global model, scaler, feature_names, feature_importance, metrics
    
    if os.path.exists(MODEL_PATH):
        model = keras.models.load_model(MODEL_PATH)
        print("✓ Model loaded successfully")
    else:
        print("⚠ Model not found. Please train the model first.")
    
    if os.path.exists(SCALER_PATH):
        scaler = joblib.load(SCALER_PATH)
        print("✓ Scaler loaded successfully")
    
    if os.path.exists(FEATURE_NAMES_PATH):
        feature_names = joblib.load(FEATURE_NAMES_PATH)
        print("✓ Feature names loaded successfully")
    
    if os.path.exists(FEATURE_IMPORTANCE_PATH):
        feature_importance = joblib.load(FEATURE_IMPORTANCE_PATH)
        print("✓ Feature importance loaded successfully")
    
    if os.path.exists(METRICS_PATH):
        metrics = joblib.load(METRICS_PATH)
        print("✓ Metrics loaded successfully")

@app.route('/')
def home():
    """Render the home page"""
    return render_template('index.html', 
                         feature_names=feature_names,
                         metrics=metrics)

@app.route('/predict', methods=['POST'])
def predict():
    """Handle prediction requests"""
    try:
        if model is None or scaler is None or feature_names is None:
            return jsonify({
                'error': 'Model not loaded. Please train the model first.',
                'success': False
            }), 500
        
        # Get input data from request
        data = request.get_json()
        
        # Extract features in the correct order
        features = []
        feature_values = {}
        for feature in feature_names:
            value = float(data.get(feature, 0))
            features.append(value)
            feature_values[feature] = value
        
        # Convert to numpy array and reshape
        features_array = np.array(features).reshape(1, -1)
        
        # Scale features
        features_scaled = scaler.transform(features_array)
        
        # Make prediction
        prediction_proba = model.predict(features_scaled, verbose=0)[0][0]
        prediction = int(prediction_proba > 0.5)
        
        # Determine risk level
        if prediction_proba < 0.3:
            risk_level = "Low"
            risk_color = "success"
        elif prediction_proba < 0.7:
            risk_level = "Moderate"
            risk_color = "warning"
        else:
            risk_level = "High"
            risk_color = "danger"
        
        # Get top contributing features
        top_features = []
        if feature_importance:
            sorted_features = sorted(feature_importance.items(), 
                                   key=lambda x: x[1], 
                                   reverse=True)[:3]
            for feat, importance in sorted_features:
                top_features.append({
                    'name': feat,
                    'value': feature_values.get(feat, 'N/A'),
                    'importance': f"{importance*100:.1f}%"
                })
        
        # Generate explanation
        explanation = generate_explanation(prediction_proba, top_features, feature_values)
        
        # Prepare response
        response = {
            'success': True,
            'prediction': prediction,
            'probability': float(prediction_proba),
            'risk_level': risk_level,
            'risk_color': risk_color,
            'confidence': f"{prediction_proba*100:.1f}%",
            'top_features': top_features,
            'explanation': explanation,
            'disclaimer': 'This prediction is for educational purposes only and should not replace professional medical advice.'
        }
        
        return jsonify(response)
    
    except Exception as e:
        return jsonify({
            'error': str(e),
            'success': False
        }), 400

def generate_explanation(probability, top_features, feature_values):
    """
    Generate human-readable explanation for the prediction
    
    Args:
        probability: Prediction probability
        top_features: List of top contributing features
        feature_values: Dictionary of all feature values
    
    Returns:
        String explanation
    """
    explanations = []
    
    if probability < 0.3:
        explanations.append("Your diabetes risk appears to be low based on the provided information.")
    elif probability < 0.7:
        explanations.append("You have a moderate risk of diabetes. Consider monitoring your health metrics.")
    else:
        explanations.append("Your diabetes risk is elevated. We strongly recommend consulting with a healthcare professional.")
    
    # Add feature-specific insights
    if top_features:
        explanations.append("\n\nKey factors influencing this assessment:")
        for feature in top_features:
            feature_name = feature['name'].lower()
            feature_val = feature['value']
            
            if 'glucose' in feature_name and isinstance(feature_val, (int, float)):
                if feature_val > 140:
                    explanations.append(f"• Your glucose level ({feature_val}) is elevated.")
                elif feature_val > 100:
                    explanations.append(f"• Your glucose level ({feature_val}) is in the pre-diabetic range.")
            
            elif 'bmi' in feature_name and isinstance(feature_val, (int, float)):
                if feature_val > 30:
                    explanations.append(f"• Your BMI ({feature_val:.1f}) indicates obesity, a risk factor for diabetes.")
                elif feature_val > 25:
                    explanations.append(f"• Your BMI ({feature_val:.1f}) is in the overweight range.")
            
            elif 'age' in feature_name and isinstance(feature_val, (int, float)):
                if feature_val > 45:
                    explanations.append(f"• Age ({feature_val}) is a risk factor for type 2 diabetes.")
            
            elif 'blood' in feature_name or 'pressure' in feature_name:
                if isinstance(feature_val, (int, float)) and feature_val > 140:
                    explanations.append(f"• Your blood pressure ({feature_val}) is elevated.")
    
    explanations.append("\n\nRecommendations:")
    explanations.append("• Schedule regular check-ups with your healthcare provider")
    explanations.append("• Maintain a healthy diet and exercise routine")
    explanations.append("• Monitor your blood glucose levels regularly")
    
    return " ".join(explanations)

@app.route('/about')
def about():
    """Render the about page"""
    return render_template('about.html')

if __name__ == '__main__':
    print("="*60)
    print("DIABETES RISK PREDICTION WEB APP")
    print("="*60)
    
    # Load model and artifacts
    load_model_and_artifacts()
    
    if model is None:
        print("\n⚠ WARNING: Model not found!")
        print("Please run 'python train_model.py' first to train the model.")
        print("\nStarting server anyway for demonstration...")
    
    print("\n✓ Starting Flask server...")
    print("✓ Open http://127.0.0.1:5000 in your browser")
    print("\nPress CTRL+C to stop the server\n")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
