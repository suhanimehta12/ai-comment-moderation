# 🚀 Deployment Guide

## Step 1 — Push to GitHub

```bash
git init
git add .
git commit -m "Initial commit: AI Comment Moderation System"
gh repo create ai-comment-moderation --public --push
# OR
git remote add origin https://github.com/YOUR_USERNAME/ai-comment-moderation.git
git push -u origin main
```

---

## Step 2 — Deploy Backend on Render

1. Go to [render.com](https://render.com) → **New Web Service**
2. Connect your GitHub repo
3. Set these settings:

| Setting | Value |
|---|---|
| Root directory | `backend` |
| Runtime | Python 3.11 |
| Build command | `pip install -r requirements.txt` |
| Start command | `uvicorn main:app --host 0.0.0.0 --port 10000` |
| Instance type | Free |

4. Click **Create Web Service**
5. Wait ~3 minutes for the build
6. Copy your backend URL: `https://your-service.onrender.com`

---

## Step 3 — Deploy Frontend on Vercel

1. Go to [vercel.com](https://vercel.com) → **Add New Project**
2. Import your GitHub repo
3. Set **Root directory** to `frontend`
4. Add environment variable:

| Key | Value |
|---|---|
| `REACT_APP_API_URL` | `https://your-service.onrender.com` |

5. Click **Deploy**

---

## Step 4 — Connect Them

In `frontend/src/api.js`, ensure:

```js
const BASE_URL = process.env.REACT_APP_API_URL || "http://localhost:8000";
```

The `REACT_APP_API_URL` env var set in Vercel will be used automatically at build time.

---

## Common Errors

| Error | Fix |
|---|---|
| CORS error in browser | Check `allow_origins` in `main.py`; set to your Vercel URL |
| 503 Models not loaded | Wait ~30s for Render cold start; hit `/health` first |
| `ModuleNotFoundError: nltk` | Ensure `requirements.txt` is installed on Render |
| Frontend shows "Something went wrong" | Open DevTools → Network → check the response body |
| Render build fails | Check Python version; use `python-3.11.0` in `.python-version` |

---

## Upgrade Your Model

Replace the seed training data in `model.py` with a real dataset:

```python
# In model.py, replace SEED_DATA with a CSV-loaded dataset
import pandas as pd
df = pd.read_csv("data/comments.csv")   # columns: text, toxic, spam, sentiment
```

For better accuracy consider:
- [Jigsaw Toxic Comment dataset](https://www.kaggle.com/c/jigsaw-toxic-comment-classification-challenge)
- [Twitter Sentiment140](https://www.kaggle.com/datasets/kazanova/sentiment140)
