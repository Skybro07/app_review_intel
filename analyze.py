"""Step 4: charts + prioritized recommendations."""
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("data/reviews_tagged.csv", parse_dates=["date"])
neg = df[df["sentiment"] == "negative"]

# 1. Theme share of negative reviews by app
share = pd.crosstab(neg["theme"], neg["app"], normalize="columns") * 100
share.plot(kind="barh", figsize=(9, 5)); plt.xlabel("% of negative reviews"); plt.title("What users complain about, by app")
plt.tight_layout(); plt.savefig("outputs/theme_share_by_app.png", dpi=150); plt.close()

# 2. Monthly negative-review rate
df["month"] = df["date"].dt.to_period("M").astype(str)
trend = df.groupby("month")["sentiment"].apply(lambda s: (s == "negative").mean() * 100)
trend.plot(marker="o", figsize=(9, 4)); plt.ylabel("% negative"); plt.title("Negative review rate over time")
plt.tight_layout(); plt.savefig("outputs/sentiment_trend.png", dpi=150); plt.close()

# 3. Priority = volume x average severity (negative reviews only)
pr = neg.groupby("theme").agg(volume=("text", "count"), avg_severity=("severity", "mean"))
pr["priority_score"] = pr["volume"] * pr["avg_severity"]
pr = pr.sort_values("priority_score", ascending=False)
pr.to_csv("outputs/priority_table.csv")
pr["priority_score"].plot(kind="barh", figsize=(8, 4)).invert_yaxis(); plt.title("Fix-first priority (volume x severity)")
plt.tight_layout(); plt.savefig("outputs/priority.png", dpi=150); plt.close()

# 4. Recommendations draft with real example complaints
lines = ["# Recommendations (draft - edit with your own judgment)\n"]
for theme in [t for t in pr.index if t != "Other"][:3]:
    row = pr.loc[theme]
    lines.append(f"## {theme}: {int(row.volume)} negative reviews, avg severity {row.avg_severity:.1f}")
    for t in neg[neg["theme"] == theme].sort_values("severity", ascending=False)["text"].head(3):
        lines.append(f'- "{t[:160]}"')
    lines.append("- **Proposed fix:** (write your recommendation + the metric you'd track)\n")
open("outputs/recommendations.md", "w").write("\n".join(lines))
print(pr); print("Saved charts + recommendations.md in outputs/")

