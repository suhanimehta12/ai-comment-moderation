# 🛡️ AI Comment Moderation System

A production-ready SaaS tool that classifies social media comments in real time — detecting **toxicity**, **spam**, and **sentiment** using your existing NLP pipeline.

---

## 🚀 Features

| Feature | Details |
|---|---|
| Toxicity Detection | Toxic / Non-Toxic |
| Spam Detection | Spam / Not Spam |
| Sentiment Analysis | Positive / Negative / Neutral |
| Confidence Score | Per-prediction probability |
| Probability Breakdown | Full class scores per task |
| History Log | Last 5 analyzed comments |

---

## 🧱 Tech Stack

| Layer | Technology |
|---|---|
| ML / NLP | scikit-learn · TF-IDF · Logistic Regression |
| Backend | FastAPI · Pydantic · Uvicorn |
| Frontend | React · Fetch API |
| Deployment | Render (backend) · Vercel (frontend) |

---

## 📁 Project Structure

```
ai-comment-moderation/
├── backend/
│   ├── main.py           # FastAPI app + routes
│   ├── model.py          # Multi-task sklearn pipelines
│   ├── preprocess.py     # Text cleaning (from your NLP classifier)
│   ├── requirements.txt
│   └── models/           # Auto-created; holds .joblib file
│
├── frontend/
│   └── src/
│       ├── api.js         # Fetch API integration
│       ├── Dashboard.jsx  # Full SaaS dashboard UI
│       └── App.js
│
├── README.md
└── deployment-guide.md
```

---

## ⚡ Run Locally

### Backend

```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

The first run trains models on seed data and saves them to `backend/models/`.
Subsequent runs load the saved model — startup is instant.

### Frontend

```bash
# Create React app scaffolding (if you haven't already)
npx create-react-app frontend
cp -r frontend/src/* frontend/src/

cd frontend
npm install
npm start
```

Open [http://localhost:3000](http://localhost:3000).

---

## 🌐 API

### `POST /moderate-comment`

**Request**
```json
{ "comment": "This is amazing!" }
```

**Response**
```json
{
  "comment": "This is amazing!",
  "toxicity": "Non-Toxic",
  "spam": "Not Spam",
  "sentiment": "Positive",
  "confidence": 0.91,
  "all_scores": {
    "toxicity":  { "Non-Toxic": 0.91, "Toxic": 0.09 },
    "spam":      { "Not Spam": 0.88, "Spam": 0.12 },
    "sentiment": { "Positive": 0.85, "Negative": 0.07, "Neutral": 0.08 }
  }
}
```

### `GET /health`
```json
{ "status": "ok", "models_loaded": true }
```

---

## 📊 Use Cases

- **Instagram / TikTok moderation** — auto-flag toxic comments before they go live
- **YouTube comment filtering** — remove spam and hate speech at scale  
- **Brand safety dashboards** — monitor brand sentiment across platforms
- **Customer support triage** — route negative sentiment tickets to priority queues

---

## 🏆 Skills Demonstrated

✔ NLP / ML model integration (sklearn pipelines)  
✔ FastAPI REST API design  
✔ React SaaS dashboard  
✔ Fetch API (no Axios)  
✔ Full-stack deployment  
✔ Real-world product thinking  
