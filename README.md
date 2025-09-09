# HarmWatch — Adverse Societal Impact of Social Media (Beginner Starter Kit)

A super-simple tool to:
- load a CSV of social posts,
- clean the text,
- classify into impact categories (cyberbullying, hate speech, misinformation, scam/phishing, privacy risk, mental health risk, hacking/exploit, neutral),
- visualize counts and trends,
- export CSV/HTML,
- optionally save to local SQLite (not required to use).

## 1) Install
```bash
python -m venv .venv        # or: python3 -m venv .venv
# Windows
.venv\Scripts\activate
# macOS/Linux
# source .venv/bin/activate
pip install -r requirements.txt
```

If NLTK stopwords are missing later, run:
```python
import nltk; nltk.download('stopwords')
```

## 2) Run locally
```bash
streamlit run app/app.py
```

## 3) Upload sample data
Use: `data/sample_posts.csv` (has columns: platform, date, author_id, url, text).

## 4) Deploy (Streamlit Community Cloud)
1. Create GitHub account and install **GitHub Desktop**.
2. New repository → choose this folder → Publish to GitHub (Public).
3. On Streamlit Cloud → New app → pick your repo → app path `app/app.py` → Deploy.
