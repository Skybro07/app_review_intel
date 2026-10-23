"""Step 2: tag each review with theme, sentiment, severity.
Usage:  python tag_reviews.py llm        (needs ANTHROPIC_API_KEY, best quality)
        python tag_reviews.py keywords   (free, offline baseline)
"""
import os, sys, json, re
import pandas as pd

THEMES = {
    "Payment failure": ["payment fail", "failed payment", "money deducted", "deducted", "pending", "refund", "stuck", "not received", "declined", "transaction", "upi", "money not sending", "unable to send", "not able to send", "payment not sent", "can't pay", "cannot pay"],
    "Login / KYC": ["login", "log in", "otp", "kyc", "verification", "verify", "blocked", "sign in", "password", "aadhaar", "pan card"],
    "Customer support": ["support", "customer care", "customer service", "complaint", "no response", "helpline", "ticket", "chatbot"],
    "App performance / bugs": ["crash", "slow", "hang", "bug", "lag", "not working", "error", "loading", "glitch", "freez", "not opening", "not open", "can't open", "cannot open", "doesn't open", "does not open"],
    "Fees / charges": ["fee", "charge", "commission", "convenience", "brokerage", "hidden", "cashback", "reward"],
    "Fraud / security": ["fraud", "scam", "hacked", "unauthorized", "phishing", "spam", "cheat", "stolen"],
    "UI / UX": ["ui", "interface", "design", "user friendly", "easy to use", "confusing", "layout", "navigation"],
    "Feature requests": ["feature", "features", "add option", "new option", "please add", "should add", "want to add", "wish", "suggestion", "suggest", "request", "bring back", "missing option"],
    "Investment / trading": ["investment", "investing", "invest", "trading", "trade", "stocks", "stock market", "shares", "mutual fund", "sip", "etf", "ipo", "demat", "portfolio", "f&o", "market movements"],
    "App availability / compatibility": ["download", "install", "update", "updated", "compatible", "compatibility", "not supported", "device", "android version", "country", "region", "available in", "not available"],
    "General experience": ["good", "great", "nice", "excellent", "love", "wonderful", "useful", "best", "awesome", "amazing", "fantastic", "super", "satisfied", "happy", "thank", "thanks", "bad", "worst", "poor", "useless", "disappoint", "terrible"],
}
CRITICAL = ["fraud", "scam", "hacked", "unauthorized", "stolen", "money deducted", "lost money", "cheat"]

def sentiment_from_rating(r):
    return "negative" if r <= 2 else "neutral" if r == 3 else "positive"

def classify_theme(text):
    scores = {theme: sum(keyword in text for keyword in keywords) for theme, keywords in THEMES.items()}
    best = max(scores, key=scores.get)
    return best if scores[best] > 0 else "Other"

def tag_keywords(df):
    themes, sev = [], []
    for text, rating in zip(df["text"].str.lower(), df["rating"]):
        themes.append(classify_theme(text))
        if rating == 1 or any(c in text for c in CRITICAL): sev.append(3)
        elif rating <= 3: sev.append(2)
        else: sev.append(1)
    df["theme"], df["severity"] = themes, sev
    df["sentiment"] = df["rating"].apply(sentiment_from_rating)
    return df

PROMPT = """You are classifying Google Play reviews of Indian fintech apps.
For each review return: theme (one of {themes} or "Other"), sentiment (positive/neutral/negative),
severity (1=minor, 2=annoying, 3=critical: money loss, fraud, cannot access account).
Return ONLY a JSON list like [{{"id": "12", "theme": "...", "sentiment": "...", "severity": 1}}].
Reviews:
{reviews}"""

def tag_llm(df, model="claude-haiku-5-5", batch=15):
    import anthropic
    client = anthropic.Anthropic()
    cache_path = "data/llm_cache.json"
    cache = json.load(open(cache_path)) if os.path.exists(cache_path) else {}
    for i in range(0, len(df), batch):
        chunk = df.iloc[i:i + batch]
        todo = chunk[~chunk["review_id"].astype(str).isin(cache)]
        if todo.empty: continue
        body = "\n".join(f'{{"id": "{r.review_id}", "text": {json.dumps(r.text[:400])}}}' for r in todo.itertuples())
        msg = client.messages.create(model=model, max_tokens=2000, messages=[
            {"role": "user", "content": PROMPT.format(themes=list(THEMES), reviews=body)}])
        try:
            items = json.loads(re.search(r"\[.*\]", msg.content[0].text, re.S).group(0))
            for it in items: cache[str(it["id"])] = it
        except Exception as e:
            print("batch", i, "failed to parse:", e)
        json.dump(cache, open(cache_path, "w"))
        print(f"{min(i + batch, len(df))}/{len(df)} done")
    df["theme"] = df["review_id"].astype(str).map(lambda x: cache.get(x, {}).get("theme", "Other"))
    other = df["theme"].eq("Other")
    df.loc[other, "theme"] = df.loc[other, "text"].str.lower().apply(classify_theme)
    df["sentiment"] = df["review_id"].astype(str).map(lambda x: cache.get(x, {}).get("sentiment", None))
    df["severity"] = df["review_id"].astype(str).map(lambda x: cache.get(x, {}).get("severity", 2))
    df["sentiment"] = df["sentiment"].fillna(df["rating"].apply(sentiment_from_rating))
    return df

if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "keywords"
    df = pd.read_csv("data/reviews_raw.csv")
    df = tag_llm(df) if mode == "llm" else tag_keywords(df)
    df.to_csv("data/reviews_tagged.csv", index=False)
    print("Saved data/reviews_tagged.csv  (mode:", mode + ")")
