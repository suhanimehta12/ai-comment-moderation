"""
model.py
--------
Multi-task comment moderation model.

Three lightweight sklearn pipelines, each trained on the same data:
  • toxicity  : Toxic / Non-Toxic
  • spam      : Spam / Not Spam
  • sentiment : Positive / Negative / Neutral

If a pre-trained model file is found at MODEL_PATH it is loaded;
otherwise the models are trained on synthetic seed data and saved.
"""

import os
import joblib
import numpy as np
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction.text import TfidfVectorizer
from preprocess import clean_text

MODEL_PATH = os.path.join(os.path.dirname(__file__), "models", "moderation_model.joblib")

# ---------------------------------------------------------------------------
# Seed training data (used when no pre-trained model is present)
# ---------------------------------------------------------------------------

SEED_DATA = {
    "toxicity": {
        "texts": [
            # Toxic
            "You are an idiot and should be ashamed",
            "I hate you so much you disgusting person",
            "Go kill yourself nobody likes you",
            "This is absolute garbage content",
            "What a stupid moron you are",
            "You don't deserve to live",
            "Pathetic loser get out of here",
            "This person is trash and worthless",
            "I will destroy you online",
            "Terrible human being die already",
            # Non-Toxic
            "This is such a great video thank you",
            "Amazing content keep it up",
            "I really enjoyed watching this",
            "Great job on the explanation",
            "Could you make more videos like this",
            "Really helpful information appreciate it",
            "Love the energy in this video",
            "This made my day so much better",
            "Fantastic work as always",
            "So well produced and informative",
        ],
        "labels": ["Toxic"] * 10 + ["Non-Toxic"] * 10,
    },
    "spam": {
        "texts": [
            # Spam
            "Check out my channel for free giveaways click link in bio",
            "Buy followers now only 5 dollars visit mysite.com",
            "FREE MONEY click here limited time offer",
            "Sub4sub anyone? subscribe to me I subscribe back",
            "Visit my profile for exclusive deals discount code",
            "Make 1000 dollars a day working from home click now",
            "I gained 10k followers using this trick linktr.ee",
            "Promo code SAVE50 for 50% off check my bio",
            "First 100 subs get free gift hurry up",
            "Follow me back I follow everyone guaranteed",
            # Not Spam
            "This is really interesting content",
            "I disagree with the point made at minute 5",
            "Can you explain the second part again",
            "The editing on this video is impressive",
            "I shared this with my friends they loved it",
            "What software did you use for this",
            "This topic needs more coverage",
            "My favorite video this week",
            "Thank you for the tutorial it worked",
            "Looking forward to the next episode",
        ],
        "labels": ["Spam"] * 10 + ["Not Spam"] * 10,
    },
    "sentiment": {
        "texts": [
            # Positive
            "This is absolutely wonderful I love it",
            "Best video I have seen all year incredible",
            "So happy I found this channel amazing",
            "This made me smile thank you so much",
            "Brilliant content keep up the great work",
            "Fantastic explanation really helped me",
            # Negative
            "This is the worst thing I have ever seen",
            "Completely useless waste of my time",
            "Terrible quality very disappointed",
            "Horrible experience do not recommend",
            "Very bad video nothing explained properly",
            "I hated every minute of this content",
            # Neutral
            "I watched this video yesterday",
            "The video is about machine learning basics",
            "This covers the topic of text classification",
            "The channel posts every Tuesday",
            "There are ten minutes of content here",
            "The speaker mentions three main points",
        ],
        "labels": ["Positive"] * 6 + ["Negative"] * 6 + ["Neutral"] * 6,
    },
}


def _build_pipeline() -> Pipeline:
    return Pipeline([
        ("tfidf", TfidfVectorizer(
            max_features=5000,
            ngram_range=(1, 2),
            min_df=1,
            sublinear_tf=True,
        )),
        ("clf", LogisticRegression(max_iter=1000, C=3.0, solver="lbfgs")),
    ])


def _train_all() -> dict:
    models = {}
    for task, data in SEED_DATA.items():
        cleaned = [clean_text(t) for t in data["texts"]]
        pipe = _build_pipeline()
        pipe.fit(cleaned, data["labels"])
        models[task] = pipe
        print(f"[model] Trained '{task}' pipeline on {len(cleaned)} samples")
    return models


def load_or_train_model() -> dict:
    """Return {'toxicity': pipe, 'spam': pipe, 'sentiment': pipe}."""
    if os.path.exists(MODEL_PATH):
        print(f"[model] Loading from {MODEL_PATH}")
        return joblib.load(MODEL_PATH)

    print("[model] No saved model found — training on seed data...")
    models = _train_all()
    os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)
    joblib.dump(models, MODEL_PATH)
    print(f"[model] Saved → {MODEL_PATH}")
    return models


def predict_comment(comment: str, models: dict) -> dict:
    """Run all three pipelines and return a unified moderation result."""
    clean = clean_text(comment)

    if not clean.strip():
        return {
            "comment": comment,
            "toxicity": "Non-Toxic",
            "spam": "Not Spam",
            "sentiment": "Neutral",
            "confidence": 1.0,
            "all_scores": {},
        }

    results = {}
    all_scores = {}

    for task, pipe in models.items():
        probs = pipe.predict_proba([clean])[0]
        classes = pipe.classes_
        prob_map = {str(c): round(float(p), 4) for c, p in zip(classes, probs)}
        label = classes[np.argmax(probs)]
        confidence = float(np.max(probs))
        results[task] = {"label": label, "confidence": confidence, "probs": prob_map}
        all_scores[task] = prob_map

    # Overall confidence = average of the three top-class probabilities
    avg_conf = round(
        sum(r["confidence"] for r in results.values()) / len(results), 4
    )

    return {
        "comment": comment,
        "toxicity": results["toxicity"]["label"],
        "spam": results["spam"]["label"],
        "sentiment": results["sentiment"]["label"],
        "confidence": avg_conf,
        "all_scores": all_scores,
    }
