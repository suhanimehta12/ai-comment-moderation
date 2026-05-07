"""
preprocess.py
-------------
Text cleaning and normalization for the comment moderation pipeline.
Adapted from nlp-text-classifier/src/preprocess.py.
"""

import re
import string
import nltk

for resource in ["punkt", "stopwords", "wordnet", "punkt_tab"]:
    nltk.download(resource, quiet=True)

from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize

STOP_WORDS = set(stopwords.words("english"))
lemmatizer = WordNetLemmatizer()

# Words that are meaningful for toxicity/sentiment — keep them even if stopwords
KEEP_WORDS = {"not", "no", "never", "nothing", "nobody", "nowhere", "nor",
              "neither", "against", "hate", "love", "good", "bad"}
STOP_WORDS -= KEEP_WORDS


def clean_text(text: str) -> str:
    """
    Normalize a raw comment string:
      1. Lowercase
      2. Remove URLs, mentions, hashtags
      3. Remove punctuation & digits
      4. Tokenize → remove stopwords → lemmatize
    """
    if not isinstance(text, str) or not text.strip():
        return ""

    text = text.lower()
    text = re.sub(r"http\S+|www\.\S+", "", text)
    text = re.sub(r"[@#]\w+", "", text)
    text = text.translate(str.maketrans("", "", string.punctuation + string.digits))

    tokens = word_tokenize(text)
    tokens = [
        lemmatizer.lemmatize(tok)
        for tok in tokens
        if tok not in STOP_WORDS and len(tok) > 1
    ]

    return " ".join(tokens)
