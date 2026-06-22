# Smart Wallet Guardian 💳

Smart Wallet Guardian is an AI-powered fraud detection prototype designed to protect digital wallet users from suspicious transactions.


## 🚀 Features

- Real-time fraud risk scoring
- Decision output: APPROVE / FLAG / BLOCK
- Explainable reasons for each transaction
- Streamlit frontend for user interaction
- FastAPI backend for risk scoring API
- Machine learning model integration


## 🏗️ System Architecture

User → Frontend (Streamlit) → Backend API (FastAPI) → Fraud Engine → Output

 

## 🧠 Technologies Used

- Python
- Streamlit (Frontend)
- FastAPI (Backend)
- Scikit-learn (Machine Learning)
- Joblib (Model handling)


## ▶️ How to Run

### 1. Install dependencies
pip install -r requirements.txt

### 2. Start backend
uvicorn api:app --reload

### 3. Start frontend
streamlit run app.py


## 🎯 Demo

The system allows users to:
- Input transaction details
- Analyze fraud risk instantly
- View decision and explanation


## 💡 Business Idea

This solution can be offered as an API service for:
- Digital wallet providers
- Banks
- Fintech platforms


## 👥 Team

- Frontend Developer (NAHVINDREN)
- Backend Developer (HARESH)
- ML Engineer (NANCY & KAVI PRIYA)
- Business & Presentation Lead (NANCY & KAVI PRIYA)
