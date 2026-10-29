"""Dashboard: streamlit run app.py"""
import pandas as pd
import streamlit as st

st.set_page_config(page_title="Fintech App Review Intelligence", layout="wide")
df = pd.read_csv("data/reviews_tagged.csv")
st.title("Fintech App Review Intelligence")

apps = st.sidebar.multiselect("Apps", sorted(df["app"].unique()), default=sorted(df["app"].unique()))
sent = st.sidebar.multiselect("Sentiment", ["negative", "neutral", "positive"], default=["negative"])
f = df[df["app"].isin(apps) & df["sentiment"].isin(sent)]

c1, c2, c3 = st.columns(3)
c1.metric("Reviews", len(f)); c2.metric("Avg rating", f"{f['rating'].mean():.2f}"); c3.metric("Avg severity", f"{f['severity'].mean():.2f}")

left, right = st.columns(2)
left.subheader("Themes"); left.bar_chart(f["theme"].value_counts())
right.subheader("Average rating by app")
right.bar_chart(f.groupby("app")["rating"].mean())

st.subheader("Priority (volume x severity)")
pr = f.groupby("theme").agg(volume=("text", "count"), avg_severity=("severity", "mean"))
pr["priority"] = pr["volume"] * pr["avg_severity"]
st.dataframe(pr.sort_values("priority", ascending=False))
st.subheader("Example reviews")
st.dataframe(f.sort_values("severity", ascending=False)[["app", "rating", "theme", "severity", "text"]].head(50))
