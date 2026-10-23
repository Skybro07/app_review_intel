# Fintech App Review Intelligence

**Problem:** Product teams at Indian fintech apps drown in unstructured Play Store reviews. Which issues should be fixed first?

**Approach:** Scrape ~2,400 Google Play reviews (PhonePe, Paytm, Google Pay, Groww) -> LLM tags theme/sentiment/severity -> validate on 50 hand-labelled reviews -> rank issues by volume x severity -> recommendations.

## Run
```
pip install -r requirements.txt
python scrape_reviews.py
export ANTHROPIC_API_KEY=...        # or use `keywords` mode for a free baseline
python tag_reviews.py llm
python validate.py sample           # label data/validation_sheet.csv by hand
python validate.py score
python analyze.py
streamlit run app.py
```

The theme rules include **General experience** for broad app praise or criticism,
**Feature requests**, **Investment / trading**, and
**App availability / compatibility**. After changing theme rules, rerun
`python tag_reviews.py keywords` to refresh all rows in
`data/reviews_tagged.csv`. LLM mode reuses cached labels and applies the keyword
rules only to reviews cached as `Other`; use keywords mode to apply changed
rules consistently to the full dataset.

## Results
_(fill in: agreement %, top 3 pain points, per-app differences)_

## Limitations
Reviews skew negative; Play Store only; sample is the newest N reviews per app; LLM tags can be wrong on sarcasm/mixed reviews.

## Product thinking
_(fill in: stakeholder, metric to track e.g. payment success rate / support CSAT, experiment to validate your top fix)_
