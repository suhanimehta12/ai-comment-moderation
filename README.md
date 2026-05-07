🛡️ AI Comment Moderation System

A production-ready full-stack SaaS system that performs real-time toxicity detection, spam filtering, and sentiment analysis on social media comments using a machine learning NLP pipeline.

🚀 Live Demo

👉 Frontend: https://ai-comment-moderation-43h1.vercel.app/

👉 Backend API: https://ai-comment-moderation-1.onrender.com

📸 Preview
🧠 Moderation Dashboard

📊 Prediction Results

📈 Probability Breakdown

✨ Features
🧠 Toxicity Detection — Classifies comments as Toxic / Non-Toxic
🚫 Spam Detection — Filters spam vs legitimate comments
💬 Sentiment Analysis — Positive / Negative / Neutral classification
📊 Confidence Score — Probability-based prediction confidence
📈 Full Probability Breakdown — Class-wise scoring for transparency
🕓 History Log — Stores last 5 analyzed comments
⚡ Real-time API inference — Fast prediction via REST API
🧱 Tech Stack
Layer	Technology
ML / NLP	scikit-learn · TF-IDF · Logistic Regression
Backend	FastAPI · Uvicorn · Pydantic
Frontend	React · Fetch API · Tailwind CSS
Deployment	Render (Backend) · Vercel (Frontend)
📁 Project Structure
ai-comment-moderation/
│
├── backend/
│   ├── main.py              # FastAPI app
│   ├── model.py             # ML pipelines
│   ├── preprocess.py        # Text cleaning pipeline
│   ├── requirements.txt
│   └── models/              # Trained model files
│
├── frontend/
│   └── src/
│       ├── api.js           # API calls (Fetch)
│       ├── Dashboard.jsx    # SaaS UI dashboard
│       └── App.js
│
├── screenshots/
│   ├── dashboard-1.png
│   ├── dashboard-2.png
│   └── dashboard-3.png
│
├── README.md
└── deployment-guide.md
⚙️ Run Locally
🧠 Backend (FastAPI)
cd backend
pip install -r requirements.txt
uvicorn main:app --reload --port 8000

👉 API runs at:

http://localhost:8000
💻 Frontend (React)
cd frontend
npm install
npm start

👉 App runs at:

http://localhost:3000
🌐 API Endpoints
🔹 POST /moderate-comment

Request

{ "comment": "This is amazing!" }

Response

{
  "toxicity": "Non-Toxic",
  "spam": "Not Spam",
  "sentiment": "Positive",
  "confidence": 0.91
}
🔹 GET /health
{ "status": "ok", "models_loaded": true }
📊 Use Cases
📱 Social media moderation (Instagram, TikTok, X)
🎥 YouTube comment filtering
🛡️ Brand safety monitoring dashboards
🎧 Customer support ticket prioritization
🤖 AI content moderation pipelines


MIT © 2025
