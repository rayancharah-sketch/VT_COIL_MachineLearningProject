// JavaScript for Diabetes Risk Predictor

/*
LLM ATTRIBUTION:
Frontend interaction logic implemented with GitHub Copilot assistance.
Students designed AJAX workflow and UI updates, Copilot helped with async/await syntax and DOM manipulation.
Used LLM for learning JavaScript async/await, debugging AJAX calls, and testing frontend interactions.
Code was reviewed, reformatted, and edited by LLM for readability.
Final code was reviewed and edited for accuracy by students.
*/

document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('predictionForm');
    
    if (form) {
        form.addEventListener('submit', handleFormSubmit);
    }
});

async function handleFormSubmit(event) {
    event.preventDefault();
    
    // Get form data
    const formData = new FormData(event.target);
    const data = {};
    
    for (let [key, value] of formData.entries()) {
        data[key] = parseFloat(value);
    }
    
    // Show loading state
    const submitBtn = event.target.querySelector('button[type="submit"]');
    const originalBtnText = submitBtn.innerHTML;
    submitBtn.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span>Analyzing...';
    submitBtn.disabled = true;
    
    try {
        // Make prediction request
        const response = await fetch('/predict', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data)
        });
        
        const result = await response.json();
        
        if (result.success) {
            displayResults(result);
        } else {
            showError(result.error || 'An error occurred during prediction.');
        }
    } catch (error) {
        showError('Failed to connect to the server. Please try again.');
        console.error('Error:', error);
    } finally {
        // Restore button state
        submitBtn.innerHTML = originalBtnText;
        submitBtn.disabled = false;
    }
}

function displayResults(result) {
    const resultsSection = document.getElementById('resultsSection');
    const riskAlert = document.getElementById('riskAlert');
    const riskTitle = document.getElementById('riskTitle');
    const riskMessage = document.getElementById('riskMessage');
    const confidenceScore = document.getElementById('confidenceScore');
    const topFeaturesList = document.getElementById('topFeaturesList');
    const explanationText = document.getElementById('explanationText');
    
    // Set risk level styling
    riskAlert.className = 'alert';
    if (result.risk_level === 'Low') {
        riskAlert.classList.add('alert-success');
    } else if (result.risk_level === 'Moderate') {
        riskAlert.classList.add('alert-warning');
    } else {
        riskAlert.classList.add('alert-danger');
    }
    
    // Update risk information
    riskTitle.textContent = `${result.risk_level} Risk Detected`;
    riskMessage.textContent = result.prediction === 1 
        ? 'The model indicates a positive diabetes risk based on your health metrics.'
        : 'The model indicates a lower diabetes risk based on your health metrics.';
    confidenceScore.textContent = result.confidence;
    
    // Display top contributing features
    topFeaturesList.innerHTML = '';
    if (result.top_features && result.top_features.length > 0) {
        result.top_features.forEach(feature => {
            const li = document.createElement('li');
            li.className = 'list-group-item d-flex justify-content-between align-items-center';
            li.innerHTML = `
                <span><strong>${feature.name.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase())}:</strong> ${feature.value}</span>
                <span class="badge bg-primary rounded-pill">${feature.importance}</span>
            `;
            topFeaturesList.appendChild(li);
        });
    } else {
        topFeaturesList.innerHTML = '<li class="list-group-item">No feature importance data available.</li>';
    }
    
    // Display explanation
    explanationText.textContent = result.explanation;
    
    // Show results section with animation
    resultsSection.style.display = 'block';
    resultsSection.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

function showError(message) {
    const resultsSection = document.getElementById('resultsSection');
    resultsSection.innerHTML = `
        <div class="alert alert-danger" role="alert">
            <h5 class="alert-heading">Error</h5>
            <p>${message}</p>
        </div>
    `;
    resultsSection.style.display = 'block';
}

function fillSampleData() {
    // Sample data for quick testing
    const sampleData = {
        'Pregnancies': 3,
        'Glucose': 148,
        'BloodPressure': 72,
        'SkinThickness': 35,
        'Insulin': 0,
        'BMI': 33.6,
        'DiabetesPedigreeFunction': 0.627,
        'Age': 50
    };
    
    // Fill form with sample data
    for (let [key, value] of Object.entries(sampleData)) {
        const input = document.getElementById(key);
        if (input) {
            input.value = value;
        }
    }
    
    // Show notification
    const alert = document.createElement('div');
    alert.className = 'alert alert-info alert-dismissible fade show mt-3';
    alert.innerHTML = `
        Sample data loaded! Click "Predict Diabetes Risk" to see results.
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    const form = document.getElementById('predictionForm');
    form.insertBefore(alert, form.firstChild);
    
    // Auto-dismiss after 3 seconds
    setTimeout(() => {
        alert.remove();
    }, 3000);
}
