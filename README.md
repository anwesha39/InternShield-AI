# 🛡️ InternShield AI
### AI-Powered Job and Internship Scam Detection System

**InternShield AI** is a machine-learning-powered web application designed to help students and job seekers identify potentially fraudulent job and internship opportunities.

Users can submit a job description and receive an automated screening result, including a machine learning prediction, suspicious warning indicators, risk assessment, and safety recommendations.

🌐 **Live Website:** https://intern-shield-ai-beta.vercel.app/

🔗 **Backend API:** https://internshield-ai-6yxa.onrender.com

📖 **API Documentation:** https://internshield-ai-6yxa.onrender.com/docs

---

## 🚀 Key Features

- **AI-Based Detection:** Uses a trained machine learning model to classify job descriptions.
- **Risk Assessment:** Displays Lower Risk, Suspicious, or High Risk results.
- **Warning Indicators:** Identifies patterns such as registration fees, guaranteed selection, unrealistic earnings, and urgency pressure.
- **Safety Recommendations:** Provides guidance based on the screening results.
- **Interactive Web Interface:** Built with React and designed for a responsive user experience.
- **REST API:** Connects the frontend to a Python FastAPI backend.

## 🧠 Machine Learning Methodology

The project uses Natural Language Processing (NLP) and supervised machine learning.

**Workflow:**

1. Dataset collection
2. Exploratory Data Analysis (EDA)
3. Data preprocessing and text cleaning
4. Text feature extraction using TF-IDF
5. Training and evaluation of machine learning models
6. Model selection and integration with FastAPI
7. Frontend and backend deployment

**Selected Model:** Linear Support Vector Classifier (LinearSVC)

**Other evaluated model:** Logistic Regression

**Evaluation metrics:**
- Accuracy
- Precision
- Recall
- F1-Score
- ROC-AUC
- PR-AUC
- Confusion Matrix

## 🛠️ Technology Stack

| Category | Technologies |
|---|---|
| Frontend | React.js, Vite, CSS |
| Backend | Python, FastAPI |
| Machine Learning | Scikit-learn, LinearSVC |
| NLP | TF-IDF Vectorization |
| Data Processing | Pandas, NumPy |
| Model Storage | Joblib |
| Deployment | Vercel, Render |
| Version Control | Git, GitHub |

## 📁 Project Structure

```text
InternShield-AI/
│
├── backend/
│   ├── eda.py
│   ├── feature_extraction.py
│   ├── main.py
│   ├── preprocess.py
│   ├── train_models.py
│   └── requirements.txt
│
├── dataset/
│   └── fake_job_postings.csv
│
├── documentation/
│
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── assets/
│   │   ├── App.jsx
│   │   ├── App.css
│   │   ├── index.css
│   │   └── main.jsx
│   ├── package.json
│   └── vite.config.js
│
├── models/
│   ├── all_models.joblib
│   ├── best_model.joblib
│   └── tfidf_vectorizer.joblib
│
├── reports/
│
└── .gitignore
```

## ⚙️ Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/anwesha39/InternShield-AI.git
cd InternShield-AI
```

### 2. Set up the Python backend

```bash
cd backend
python -m venv .venv
```

Activate the virtual environment on Windows:

```powershell
.venv\Scripts\Activate.ps1
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Start the backend from the project root:

```bash
uvicorn backend.main:app --host 127.0.0.1 --port 8000
```

Backend API: http://127.0.0.1:8000

API documentation: http://127.0.0.1:8000/docs

### 3. Set up the React frontend

Open another terminal:

```bash
cd frontend
npm install
npm run dev
```

Frontend: http://localhost:5173

Make sure the frontend API configuration points to your local FastAPI backend when running locally.

## 🌐 Deployment

- **Frontend:** Vercel
- **Backend:** Render

The deployed frontend communicates with the deployed FastAPI backend.

## ⚠️ Disclaimer

InternShield AI is an automated screening tool. Its predictions and warning indicators do not prove that a job offer is fraudulent or genuine.

Users should independently verify employers, recruiters, payment requests, and job offers before sharing personal information or making payments.

## 🔮 Future Improvements

- PDF and offer-letter text extraction
- Improved fraud detection using larger and more diverse datasets
- Explainable AI for prediction transparency
- More advanced NLP techniques
- User feedback and reporting system
- Enhanced model evaluation on real-world job advertisements

## 👩‍💻 Project Author

**Anwesha Barman**

BCA – Artificial Intelligence and Data Science

GitHub: https://github.com/anwesha39

LinkedIn: http://linkedin.com/in/anwesha-barman-210185315/

---

⭐ If you find this project interesting, consider giving the repository a star!
