"""Step 1: download real Google Play reviews (run on your own machine)."""
import pandas as pd
from google_play_scraper import reviews, Sort

APPS = {
    "PhonePe": "com.phonepe.app",
    "Paytm": "net.one97.paytm",
    "Google Pay": "com.google.android.apps.nbu.paisa.user",
    "Groww": "com.nextbillion.groww",
}
PER_APP = 600  # ~2,400 reviews total

rows = []
for name, app_id in APPS.items():
    res, _ = reviews(app_id, lang="en", country="in", sort=Sort.NEWEST, count=PER_APP)
    for r in res:
        rows.append({"app": name, "rating": r["score"], "text": r["content"], "date": r["at"]})
    print(name, len(res), "reviews")

df = pd.DataFrame(rows).drop_duplicates(subset=["app", "text"])
df = df[df["text"].str.split().str.len() >= 4].reset_index(drop=True)
df.insert(0, "review_id", df.index.astype(str))
df.to_csv("data/reviews_raw.csv", index=False)
print("Saved", len(df), "reviews -> data/reviews_raw.csv")
