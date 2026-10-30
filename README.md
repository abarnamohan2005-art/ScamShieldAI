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
