"""FOR TESTING ONLY. Generates FAKE reviews so you can check the pipeline runs. Never report results from this."""
import random, pandas as pd
random.seed(0)
T = ["Payment failed and money deducted, refund still pending", "OTP never arrives, cannot login", "KYC verification keeps failing",
     "Customer care gives no response to my complaint", "App crashes and is very slow", "Hidden charges and convenience fee are unfair",
     "Got a scam call after using this, unauthorized transaction", "UI is confusing, hard navigation", "Great app, easy to use and fast",
     "Love the cashback rewards, smooth experience"]
rows = [{"review_id": str(i), "app": random.choice(["PhonePe", "Paytm", "Google Pay", "Groww"]),
         "rating": random.choice([1, 1, 2, 3, 4, 5]), "text": random.choice(T) + " please fix",
         "date": pd.Timestamp("2025-06-01") + pd.Timedelta(days=random.randint(0, 300))} for i in range(400)]
pd.DataFrame(rows).to_csv("data/reviews_raw.csv", index=False)
