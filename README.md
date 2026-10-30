# ScamShield AI
### A Real-Time, Explainable and Adaptive Multimodal Scam & Phishing Detection System

ScamShield AI is a machine-learning-based application designed to identify suspicious SMS messages and phishing URLs. It combines text classification, URL analysis, and explainable warning indicators to help users assess potential online threats.

## Key Features

- **SMS Scam Detection:** Classifies messages as spam or legitimate using Natural Language Processing.
- **Phishing URL Detection:** Examines URL-based features to identify potentially malicious links.
- **Combined Scan:** Combines message and URL risk scores to provide an overall assessment.
- **Explainable Warnings:** Displays suspicious indicators that may have influenced the result.
- **Risk Classification:** Categorizes results into Low Risk, Uncertain, and High Risk.
- **Scan History:** Maintains records of previous scans.
- **Analytics Dashboard:** Presents scan statistics and visual summaries.
- **User Feedback:** Collects feedback for review and future model improvement.

## Technologies Used

| Component | Technologies |
|---|---|
| Programming Language | Python |
| Frontend and Dashboard | Streamlit |
| Machine Learning | Scikit-learn |
| Text Processing | TF-IDF |
| SMS Classification | Logistic Regression |
| URL Classification | Random Forest |
| Data Processing | Pandas, NumPy |
| URL Feature Extraction | tldextract |
| Database | SQLite |
| Model Persistence | Joblib |
| Visualization | Matplotlib, Seaborn |

## System Architecture

1. **Input:** User submits an SMS message, URL, or both.
2. **Text Analysis:** The SMS model processes message text using TF-IDF features and Logistic Regression.
3. **URL Analysis:** The URL module extracts lexical and domain-related features and uses a Random Forest classifier.
4. **Risk Assessment:** The detector combines the available model risk scores.
5. **Explanation:** The system displays relevant warning indicators.
6. **Output:** The dashboard displays the prediction, risk score, and risk category.

## Model Evaluation

The models were evaluated using separate training, validation, and test datasets.

### SMS Classification

- Algorithm: Logistic Regression
- Feature extraction: TF-IDF
- Test accuracy: **97.29%**
- Spam precision: **85%**
- Spam recall: **96%**
- Spam F1-score: **90%**

### URL Classification

- Algorithm: Random Forest
- Features: 12 lexical and domain-related URL features
- Test accuracy: **99.25%**
- Phishing precision: **99.18%**
- Phishing recall: **97.59%**

*These results are from the project's selected test datasets and do not guarantee the same performance on real-world messages or URLs.*

## Project Structure

```text
ScamShieldAI/
│
├── app.py
├── requirements.txt
│
├── data/
│   ├── SMSSpamCollection
│   ├── phishing_urls.csv
│   ├── train.csv
│   ├── validation.csv
│   ├── test.csv
│   └── URL training and testing files
│
├── models/
│   ├── text_model.pkl
│   └── url_model.pkl
│
└── src/
    ├── database.py
    ├── hybrid_detector.py
    ├── train_text_model.py
    ├── train_url_model.py
    ├── evaluate_text_model.py
    ├── evaluate_url_model.py
    ├── extract_url_features.py
    ├── prepare_url_data.py
    ├── baseline_text_model.py
    ├── logistic_text_model.py
    └── inspect_url_dataset.py
```
## Working of the Project

ScamShield AI follows a multi-stage detection process to identify suspicious messages and phishing URLs.

### 1. User Input

The user interacts with the Streamlit dashboard and selects one of three scanning options:

- **Message Scan:** Enter an SMS or text message.
- **URL Scan:** Enter a website URL.
- **Combined Scan:** Submit both a message and a URL for analysis.

### 2. SMS Detection Process

When a message is submitted:

1. The input message is passed to the trained text classification pipeline.
2. TF-IDF converts the message into numerical features based on word importance.
3. The Logistic Regression model analyses these features.
4. The model generates a spam risk score.
5. A threshold of 0.40 is used to classify the message as spam or legitimate.
6. The system displays the prediction and relevant warning indicators.

### 3. Phishing URL Detection Process

When a URL is submitted:

1. The URL is passed to the URL feature extraction module.
2. The system extracts 12 features, including:
   - URL length
   - Domain length
   - Number of dots and hyphens
   - Number of special characters and digits
   - Number of subdomains
   - HTTPS indicator
   - IP address indicator
   - Suspicious keyword count
   - Path length
   - Brand impersonation indicator
3. The extracted features are passed to the trained Random Forest model.
4. The model generates a phishing risk score.
5. A threshold of 0.50 is used to classify the URL.
6. The system displays the prediction and detected warning indicators.

### 4. Combined Risk Assessment

In Combined Scan mode, the system analyses the message and URL separately.

- The SMS model produces a message risk score.
- The URL model produces a URL risk score.
- The higher of the two available scores is selected as the overall risk score.

This approach ensures that a high-risk signal from either detector is reflected in the combined assessment.

### 5. Risk Level Classification

The overall risk score is converted into one of three categories:

| Risk Score | Risk Level |
|---|---|
| Below 40% | Low Risk |
| 40% to below 70% | Uncertain |
| 70% and above | High Risk |

### 6. Explainable Warning Indicators

Along with the prediction, the system displays warning indicators to help users understand suspicious characteristics.

Examples include:
- Suspicious words or phrases in a message.
- Multiple subdomains in a URL.
- Suspicious keywords such as login, verify, or account.
- A possible mismatch between a brand name and the registered domain.

These indicators are heuristic explanations and do not prove that a message or website is malicious.

### 7. Database and Feedback Management

- Every completed scan is stored in an SQLite database.
- Scan records include the input, prediction, risk score, risk level, warning indicators, and timestamp.
- Users can view previous scans through the Scan History page.
- The Analytics page presents visual summaries of scan activity and detected threats.
- Users can submit feedback about predictions.
- Submitted feedback is stored with a Pending review status and can be reviewed before being considered for future model improvements.

**Important:** User feedback does not automatically retrain or modify the existing machine-learning models.
## Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/abarnamohan2005-art/ScamShieldAI.git
```

### 2. Navigate to the project folder

```bash
cd ScamShieldAI
```

### 3. Create a virtual environment

```bash
python -m venv .venv
```

### 4. Activate the environment

**Windows PowerShell:**

```powershell
.venv\Scripts\Activate.ps1
```

### 5. Install dependencies

```bash
pip install -r requirements.txt
```

### 6. Run the application

```bash
streamlit run app.py
```

The application will open in your browser.

## Limitations

- SMS detection is trained using a general SMS spam dataset and may not identify every type of scam.
- URL detection relies on extracted URL features rather than live website inspection or threat-intelligence services.
- Brand impersonation detection uses a limited configured list of trusted domains.
- Risk scores are model outputs and should not be interpreted as guaranteed probabilities.
- A low-risk result does not guarantee that a message or URL is safe.

## Future Enhancements

- Expand training datasets with more diverse scam and phishing examples.
- Integrate trusted, regularly updated threat-intelligence sources.
- Improve explainability and risk-score calibration.
- Introduce a controlled feedback-review workflow for future model updates.
- Explore additional modalities and adaptive detection techniques.

## Disclaimer

ScamShield AI is an educational and research-oriented threat-assessment tool. Its predictions are intended to support user awareness and should not replace independent verification or professional cybersecurity solutions.

## Author

**Abarna Mohan**

GitHub: [abarnamohan2005-art](https://github.com/abarnamohan2005-art)
