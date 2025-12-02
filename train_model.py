"""
Neural Network Model Training Script
Builds, trains, and evaluates a neural network for diabetes risk prediction
"""
import numpy as np
import pandas as pd
from tensorflow import keras
from tensorflow.keras import layers
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score, confusion_matrix, classification_report
import matplotlib.pyplot as plt
import joblib
import os

from preprocess import load_and_preprocess_data

def build_model(input_dim):
    """
    Build a simple feedforward neural network
    
    Args:
        input_dim: Number of input features
    
    Returns:
        Compiled Keras model
    """
    model = keras.Sequential([
        # Input layer
        layers.Dense(32, activation='relu', input_dim=input_dim, name='hidden_layer_1'),
        layers.Dropout(0.3),
        
        # Hidden layer
        layers.Dense(16, activation='relu', name='hidden_layer_2'),
        layers.Dropout(0.2),

        # Hidden layer
        layers.Dense(8, activation='relu', name='hidden_layer_3'),
        layers.Dropout(0.2),
        
        # Output layer
        layers.Dense(1, activation='sigmoid', name='output_layer')
    ])
    
    # Compile model
    model.compile(
        optimizer='adam',
        loss='binary_crossentropy',
        metrics=['accuracy', keras.metrics.Precision(), keras.metrics.Recall()]
    )
    
    return model

def train_model(X_train, y_train, X_test, y_test, epochs=100, batch_size=32):
    """
    Train the neural network model
    
    Args:
        X_train, y_train: Training data
        X_test, y_test: Testing data
        epochs: Number of training epochs
        batch_size: Batch size for training
    
    Returns:
        Trained model and training history
    """
    print("\nBuilding model...")
    model = build_model(X_train.shape[1])
    print(model.summary())
    
    # Early stopping to prevent overfitting
    early_stopping = keras.callbacks.EarlyStopping(
        monitor='val_loss',
        patience=10,
        restore_best_weights=True
    )
    
    print("\nTraining model...")
    history = model.fit(
        X_train, y_train,
        validation_data=(X_test, y_test),
        epochs=epochs,
        batch_size=batch_size,
        callbacks=[early_stopping],
        verbose=1
    )
    
    return model, history

def evaluate_model(model, X_test, y_test):
    """
    Evaluate model performance with various metrics
    
    Args:
        model: Trained Keras model
        X_test, y_test: Test data
    
    Returns:
        Dictionary of evaluation metrics
    """
    print("\n" + "="*60)
    print("MODEL EVALUATION")
    print("="*60)
    
    # Get predictions
    y_pred_proba = model.predict(X_test, verbose=0)
    y_pred = (y_pred_proba > 0.5).astype(int).flatten()
    
    # Calculate metrics
    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred, zero_division=0)
    recall = recall_score(y_test, y_pred, zero_division=0)
    f1 = f1_score(y_test, y_pred, zero_division=0)
    roc_auc = roc_auc_score(y_test, y_pred_proba)
    
    print(f"\nAccuracy:  {accuracy:.4f}")
    print(f"Precision: {precision:.4f}")
    print(f"Recall:    {recall:.4f}")
    print(f"F1-Score:  {f1:.4f}")
    print(f"ROC-AUC:   {roc_auc:.4f}")
    
    print(f"\nConfusion Matrix:")
    print(confusion_matrix(y_test, y_pred))
    
    print(f"\nClassification Report:")
    print(classification_report(y_test, y_pred, target_names=['No Diabetes', 'Diabetes']))
    
    metrics = {
        'accuracy': accuracy,
        'precision': precision,
        'recall': recall,
        'f1_score': f1,
        'roc_auc': roc_auc
    }
    
    return metrics

def plot_training_history(history):
    """Plot training history"""
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    
    # Plot accuracy
    axes[0].plot(history.history['accuracy'], label='Train Accuracy')
    axes[0].plot(history.history['val_accuracy'], label='Val Accuracy')
    axes[0].set_title('Model Accuracy')
    axes[0].set_xlabel('Epoch')
    axes[0].set_ylabel('Accuracy')
    axes[0].legend()
    axes[0].grid(True)
    
    # Plot loss
    axes[1].plot(history.history['loss'], label='Train Loss')
    axes[1].plot(history.history['val_loss'], label='Val Loss')
    axes[1].set_title('Model Loss')
    axes[1].set_xlabel('Epoch')
    axes[1].set_ylabel('Loss')
    axes[1].legend()
    axes[1].grid(True)
    
    plt.tight_layout()
    plt.savefig('models/training_history.png', dpi=150, bbox_inches='tight')
    print("\n✓ Training history plot saved to models/training_history.png")
    plt.close()

def calculate_feature_importance(model, X_test, y_test, feature_names):
    """
    Calculate feature importance using permutation importance approximation
    
    Args:
        model: Trained model
        X_test: Test data
        feature_names: List of feature names
    
    Returns:
        Dictionary mapping feature names to importance scores
    """
    print("\nCalculating feature importance...")
    
    # Get baseline predictions
    baseline_pred = model.predict(X_test, verbose=0)
    baseline_loss = keras.losses.binary_crossentropy(
        np.concatenate([y_test.values, 1 - y_test.values], axis=0).reshape(-1, 2),
        np.concatenate([baseline_pred, 1 - baseline_pred], axis=1)
    ).numpy().mean()
    
    importance_scores = {}
    
    for i, feature in enumerate(feature_names):
        # Permute feature
        X_permuted = X_test.copy()
        X_permuted[:, i] = np.random.permutation(X_permuted[:, i])
        
        # Get predictions with permuted feature
        permuted_pred = model.predict(X_permuted, verbose=0)
        permuted_loss = keras.losses.binary_crossentropy(
            np.concatenate([y_test.values, 1 - y_test.values], axis=0).reshape(-1, 2),
            np.concatenate([permuted_pred, 1 - permuted_pred], axis=1)
        ).numpy().mean()
        
        # Importance is the increase in loss
        importance_scores[feature] = max(0, permuted_loss - baseline_loss)
    
    # Normalize importance scores
    total_importance = sum(importance_scores.values())
    if total_importance > 0:
        importance_scores = {k: v/total_importance for k, v in importance_scores.items()}
    
    # Save importance scores
    joblib.dump(importance_scores, 'models/feature_importance.pkl')
    print("✓ Feature importance saved to models/feature_importance.pkl")
    
    return importance_scores

if __name__ == "__main__":
    # Load and preprocess data
    X_train, X_test, y_train, y_test, scaler, feature_names = load_and_preprocess_data()
    
    # Train model
    model, history = train_model(X_train, y_train, X_test, y_test)
    
    # Evaluate model
    metrics = evaluate_model(model, X_test, y_test)
    
    # Plot training history
    plot_training_history(history)
    
    # Calculate feature importance
    importance = calculate_feature_importance(model, X_test, y_test, feature_names)
    
    print("\nFeature Importance:")
    for feature, score in sorted(importance.items(), key=lambda x: x[1], reverse=True):
        print(f"  {feature}: {score:.4f}")
    
    # Save model
    os.makedirs('models', exist_ok=True)
    model.save('models/diabetes_model.h5')
    print("\n✓ Model saved to models/diabetes_model.h5")
    
    # Save metrics
    joblib.dump(metrics, 'models/metrics.pkl')
    print("✓ Metrics saved to models/metrics.pkl")
    
    print("\n" + "="*60)
    print("✓ MODEL TRAINING COMPLETED SUCCESSFULLY!")
    print("="*60)
