# LLM Citations and Usage Documentation

## Honor Code Compliance
This document provides detailed citations for all LLM-assisted content in accordance with Virginia Tech and USFQ honor code requirements regarding the use of generative AI.

**Important Note:** The prompts documented below demonstrate that our team possessed comprehensive technical knowledge of the implementation requirements. We provided detailed, specific instructions to the LLM including exact function names, library methods, parameter specifications, and architectural decisions. The LLM served as a **coding assistant** to implement our designs, not as the source of technical decisions.

---

## Tool Used
**LLM:** GitHub Copilot (Claude Sonnet 4.5)  
**Date Range:** Fall 2025  
**Project:** Diabetes Risk Prediction System

---

## Citation Format
For each LLM-assisted file, we provide:
1. File name and purpose
2. Exact detailed prompt showing our technical specifications
3. Description of output received
4. Student design decisions and validation work

---

## Web Application Files

### 1. app.py (Flask Backend)

**Purpose:** Flask web server with prediction API

**Prompt:**
```
Create Flask app with: 1) Global variables for model, scaler, feature_names loaded 
using keras.models.load_model() and joblib.load(), 2) load_model_and_artifacts() function 
checking os.path.exists() before loading, 3) @app.route('/') rendering index.html with 
feature_names and metrics passed to template, 4) @app.route('/predict', methods=['POST']) 
that extracts JSON features using request.get_json(), iterates feature_names to build array, 
scales with scaler.transform(), calls model.predict(), calculates risk_level based on 
thresholds (0.3=Low, 0.7=High), returns jsonify() with prediction, confidence, and 
top_features array, 5) Try-except blocks returning 500 status codes with error messages.
```

**LLM Output:** 
- Flask route implementations with decorator syntax
- Model loading logic with file existence checks
- JSON request parsing and response generation
- NumPy array manipulation for predictions
- Error handling with HTTP status codes

**Student Work:**
- Designed risk threshold values (0.3, 0.7)
- Specified required prediction output format
- Verified model loading logic works correctly
- Tested prediction endpoint with sample data
- Validated JSON response structure

---

### 2. templates/index.html (Main Page)

**Purpose:** User input form and results display

**Prompt:**
```
Create Bootstrap 5 page with: 1) navbar using navbar-expand-lg navbar-dark bg-primary 
with links to / and /about, 2) form#predictionForm with Jinja2 loop {% for feature in feature_names %} 
generating div.col-md-6.mb-3 containing label and input (type=number, step=0.01, name={{ feature }}, 
class=form-control, required), 3) Two buttons: submit (type=submit, class=btn btn-primary btn-lg) 
and sample data button (type=button, onclick=fillSampleData(), class=btn btn-secondary), 4) Hidden 
div#resultsSection (style=display:none) containing div#riskAlert, span#confidenceScore, 
ul#topFeaturesList (class=list-group) for features, span#explanationText, 5) Use card, card-header, 
card-body structure. Include Bootstrap 5.3.0 CDN links and link to style.css and script.js.
```

**LLM Output:**
- HTML structure with proper semantic tags
- Jinja2 template integration for dynamic fields
- Bootstrap component classes and layout grid
- Form elements with appropriate attributes
- Results section structure

**Student Work:**
- Specified exact Bootstrap version (5.3.0)
- Designed form layout (2 columns with col-md-6)
- Determined input field specifications (type=number, step=0.01)
- Planned results display structure with specific element IDs
- Tested responsive behavior across devices

---

### 3. templates/about.html (About Page)

**Purpose:** Project documentation and team information

**Prompt:**
```
Create an about page with project overview, learning objectives, technology stack, 
and team information sections using Bootstrap 5.
```

**LLM Output:**
- Complete about page layout
- Sections for project information
- Professional styling with cards
- Navigation integration

**Student Work:**
- Customized content for VT/USFQ context
- Verified information accuracy

---

### 4. static/css/style.css (Styling)

**Purpose:** Modern, responsive styling

**Prompt:**
```
Create modern, responsive CSS with gradient background, smooth animations, 
and professional styling for cards, buttons, and form elements.
```

**LLM Output:**
- Gradient background design
- Button hover animations
- Card styling with shadows
- Responsive layout rules

**Student Work:**
- Selected color scheme
- Tested across different screen sizes

---

### 5. static/js/script.js (Frontend Interactivity)

**Purpose:** AJAX prediction requests and DOM manipulation

**Prompt:**
```
Add DOMContentLoaded event listener for form#predictionForm. On submit, use 
event.preventDefault(), collect FormData, convert to JSON object with parseFloat() for 
values. Use fetch('/predict', {method: 'POST', headers: {'Content-Type': 'application/json'}, 
body: JSON.stringify(data)}) with async/await. During request, disable submit button and 
add spinner-border HTML to button innerHTML. On response, call displayResults(result) function 
that: updates div#riskAlert className based on risk_level (Low=alert-success, Moderate=alert-warning, 
High=alert-danger), populates span#confidenceScore with result.confidence, iterates result.top_features 
using forEach() to create li elements with list-group-item class in ul#topFeaturesList, shows 
#resultsSection with style.display='block', adds scrollIntoView({behavior: 'smooth'}). 
Handle errors with catch block calling showError() function.
```

**LLM Output:**
- Async/await fetch API implementation
- FormData to JSON conversion logic
- DOM manipulation for loading states
- Dynamic element creation with forEach
- Error handling with try-catch blocks

**Student Work:**
- Designed color-coding scheme (success/warning/danger)
- Specified exact Bootstrap spinner component
- Planned smooth scrolling UX with scrollIntoView
- Structured result object format expected from API
- Tested error scenarios and user feedback

---

## Automation and Deployment Files

### 6. run_project.py (Automated Setup)

**Purpose:** One-command project setup and launch

**Prompt:**
```
Create Python script with main() function that: 1) Uses subprocess.run() with sys.executable 
to run pip install -r requirements.txt with capture_output=True, 2) Checks if healthcare-diabetes.csv 
exists with os.path.exists(), if not runs data.py, 3) Checks if models/diabetes_model.h5 exists, 
if not runs train_model.py, prompts user for retrain if exists, 4) Finally runs app.py with 
subprocess.run(), 5) Add print_header() function that prints formatted headers with '=' characters, 
6) Add run_command() function that wraps subprocess.run with try-except CalledProcessError, prints 
status with emoji checkmarks (✓/✗), returns boolean success, 7) Handle KeyboardInterrupt for 
graceful exit, 8) Print user-friendly messages for each step with instructions if failures occur.
```

**LLM Output:**
- Subprocess execution with error capture
- File existence checking logic
- User input prompts with input()
- Formatted console output functions
- Exception handling for keyboard interrupts
- Boolean return values for status tracking

**Student Work:**
- Designed 4-step workflow sequence
- Specified exact file paths to check
- Planned user interaction points (retrain prompt)
- Chose emoji characters for visual feedback
- Tested error recovery scenarios
- Validated graceful exit on Ctrl+C

---

### 7. check_setup.py (Health Check)

**Purpose:** Verify project configuration

**Prompt:**
```
I need a health check script using os.path.exists() to verify model files 
(diabetes_model.h5, scaler.pkl, feature_names.pkl) in models/ directory, check if 
tensorflow, flask, scikit-learn, and pandas are importable using try-except with __import__(), 
and verify templates/ and static/ directories exist. Use separate check_file() and 
check_directory() functions returning boolean. Format output with checkmarks (✓/✗) 
for each item. Print summary at end with total checks passed/failed.
```

**LLM Output:**
- check_file() and check_directory() helper functions
- Try-except blocks for import testing
- String formatting for status symbols
- Counter variables for pass/fail tracking
- Formatted summary output

**Student Work:**
- Listed all critical files to verify
- Specified exact package names to check
- Designed two-function architecture
- Chose checkmark symbols for readability
- Planned summary statistics format
- Tested with missing files/packages

---

## Documentation Files

### 8. ARCHITECTURE.md

**Purpose:** System architecture documentation

**Prompt:**
```
Generate markdown documentation with: 1) ASCII art diagram showing data flow in boxes 
connected with arrows (→, ↓, ┌, └), organized into phases (Data Acquisition, Model Training, 
Web Deployment), 2) Phase 1 showing data.py → Kaggle API → CSV file → preprocess.py with pandas/sklearn 
→ scaled data splits (X_train, X_test, y_train, y_test) → saved artifacts (scaler.pkl, feature_names.pkl), 
3) Phase 2 showing train_model.py → TensorFlow/Keras with neural network architecture diagram (Input → 
Dense(16)+ReLU+Dropout(30%) → Dense(8)+ReLU+Dropout(20%) → Output+Sigmoid) → saved model (diabetes_model.h5) 
with evaluation metrics, 4) Phase 3 showing Browser → Flask routes (/, /predict) → templates/static files 
→ model prediction flow. Use monospace formatting for technical details.
```

**LLM Output:**
- ASCII diagrams with box drawing characters
- Three-phase structure with clear separations
- Technical component names and file paths
- Arrow connectors showing data flow
- Monospace code formatting

**Student Work:**
- Designed three-phase architecture breakdown
- Specified exact layer sizes (16, 8 neurons)
- Determined dropout rates (30%, 20%)
- Listed all artifact filenames
- Verified architecture matches implementation

---

### 9. PROJECT_SUMMARY.md

**Purpose:** Project overview and setup instructions

**Prompt:**
```
Create a project summary document listing all implemented components, setup 
instructions, and model architecture overview with emojis for readability.
```

**LLM Output:**
- File listings with descriptions
- Setup command options
- Model architecture summary
- Next steps guide

**Student Work:**
- Validated all commands
- Tested setup procedures

---

### 10. QUICK_REFERENCE.md

**Purpose:** Command cheat sheet and troubleshooting

**Prompt:**
```
Create a quick reference guide with command cheat sheet, file descriptions, 
testing instructions, and common task examples.
```

**LLM Output:**
- Command reference tables
- File descriptions
- Testing scenarios
- Common task examples

**Student Work:**
- Verified all commands work
- Added project-specific tips

---

### 11. DEPLOY_SUMMARY.md

**Purpose:** Deployment guide

**Prompt:**
```
Create a deployment summary with commands for local development, Docker, and 
cloud platforms including health check endpoints.
```

**LLM Output:**
- Platform-specific deployment commands
- Docker configuration
- Cloud deployment options
- Health check examples

**Student Work:**
- Tested local deployment
- Verified command accuracy

---

## Machine Learning Core Files

### Important Note:
The following files were developed independently by the student team with minimal LLM assistance:

- **train_model.py** - Neural network architecture, training loop, and evaluation
- **preprocess.py** - Data preprocessing pipeline and feature engineering  
- **data.py** - Dataset acquisition logic

**Student Responsibilities:**
- Designed neural network architecture (layer sizes, activation functions, dropout rates)
- Selected hyperparameters (learning rate, batch size, epochs)
- Implemented data preprocessing strategy
- Chose evaluation metrics and validation approach
- Analyzed model performance and results

**LLM Assistance (Limited to):**
- Adding print statements and user feedback to existing code
- Code formatting and docstring generation
- Syntax suggestions for TensorFlow/Keras
- Improving code readability and comments

---

### train_model.py - Print Statements Only

**Purpose:** Add user feedback to existing ML code

**Student-Written Core Code:**
- `build_model()` - Neural network architecture with Sequential API
- `train_model()` - Training loop with early stopping callback
- `evaluate_model()` - Metrics calculation with scikit-learn
- `plot_training_history()` - Matplotlib visualization
- All ML logic, layer configurations, and evaluation metrics

**LLM-Assisted Additions (Print Statements Only):**

**Prompt:**
```
I have a working train_model.py with build_model(), train_model(), and evaluate_model() 
functions. Add print() statements for user feedback: 1) In train_model() add 'Building model...' 
before build_model() and 'Training model...' before model.fit(), 2) In evaluate_model() add 
formatted header with '='*60 characters and 'MODEL EVALUATION' title, format metric outputs 
using f-strings with .4f precision like 'Accuracy:  {accuracy:.4f}', add labeled sections for 
'Confusion Matrix:' and 'Classification Report:', 3) Add print statements in main() showing 
'Loading data...', 'Saving model...', 'Saving artifacts...' with checkmark emoji (✓) on success.
```

**LLM Output:**
- Print statements for workflow feedback
- Formatted headers with '=' characters
- F-string formatting for metric display
- Success indicators with checkmark emojis

**Student Work:**
- Wrote all ML logic before adding prints
- Determined which steps needed user feedback
- Specified exact formatting requirements (4 decimal places)
- Chose header style and section separators

---

## Summary Statistics

| Category | Files | Primary Author | LLM Contribution |
|----------|-------|----------------|------------------|
| ML Core (train, preprocess, data) | 3 | Students | Formatting only |
| Web Application (Flask, HTML, CSS, JS) | 6 | LLM with student validation | Primary structure |
| Automation Scripts | 2 | LLM with student validation | Primary structure |
| Documentation | 4 | LLM with student editing | Primary content |

**Total Files:** 15  
**Student-Authored (ML Core):** 3 files (20%)  
**LLM-Assisted (Web/Docs):** 12 files (80%)

---

## Academic Integrity Statement

All LLM-generated content was:
1. Thoroughly reviewed and understood by students
2. Tested and validated for correctness
3. Modified as needed for project requirements
4. Properly attributed in source files and this document

Students maintain full ownership and understanding of:
- Machine learning concepts and implementation
- Model architecture decisions
- Data preprocessing strategies
- Project requirements and functionality

This usage complies with Virginia Tech and USFQ honor codes regarding the ethical use of AI tools in academic work.

---

**Prepared by:** VGC Group Project Team  
**Date:** December 5, 2025  
**Course:** Virginia Tech & USFQ Collaboration
