# Fintech App Review Intelligence

> Turning 600+ unstructured Google Play reviews of India's top fintech apps into a prioritized list of what product teams should fix first.


## Problem
Product teams at Indian fintech apps receive thousands of Play Store reviews. They are noisy, unstructured, and hard to turn into decisions. **Which issues hurt users most, and how do competing apps compare?**

## What this project does
1. **Scrapes** real Google Play reviews for PhonePe, Paytm, Google Pay and Groww.
2. **Tags** each review with a **theme**, **sentiment** and **severity** (1 = minor, 2 = annoying, 3 = critical such as money loss, fraud or no account access).
3. **Validates** the tagging against a hand-labelled sample of 50 reviews.
4. **Prioritizes** issues using `priority = volume x average severity`.
5. **Serves** an interactive Streamlit dashboard with app and sentiment filters.

## Dataset
| Item | Value |
|---|---|
| Source | Google Play Store (India, English) |
| Apps | PhonePe, Paytm, Google Pay, Groww |
| Reviews analysed | 609 (after removing duplicates and very short reviews) |
| Theme categories | 12: Payment failure, Login / KYC, Customer support, App performance / bugs, Fees / charges, Fraud / security, UI / UX, Feature requests, Investment / trading, App availability / compatibility, General experience, Other |

## Key results
| Metric | Result |
|---|---|
| Average rating (all 4 apps) | **3.46 / 5** |
| Average severity | **1.71 / 3** |
| Highest rated apps | Paytm and PhonePe (about 3.9) |
| Lowest rated app | Google Pay (about 3.2); Groww about 3.4 |
| Tagging agreement with manual labels (50 reviews) | **__%** |

**Priority table (all sentiments, from the dashboard):**
| Theme | Reviews | Avg severity | Priority |
|---|---|---|---|
| Other | 161 | 1.68 | 271 |
| General experience | 177 | 1.23 | 218 |
| App performance / bugs | 48 | 2.42 | 116 |

**Top 3 pain points (negative reviews only, run `python analyze.py`):**
1. __ : __ negative reviews, avg severity __
2. __ : __ negative reviews, avg severity __
3. __ : __ negative reviews, avg severity __

### Insights
- Paytm and PhonePe earn noticeably higher average ratings than Google Pay, so Google Pay has the most room to win back users.
- **App performance / bugs** has the highest average severity among the large themes (2.42 vs 1.23 for general feedback). Fewer reviews, but each one is more serious.
- Over half of all reviews fall into the broad "General experience" and "Other" buckets. Most users leave short, generic feedback, and the actionable signal sits in a smaller set of detailed reviews.
- __ (add one insight from the negative-only view, e.g. which app has the most payment-failure complaints)

## Recommendations
| Priority | Issue | Proposed fix | Metric to track |
|---|---|---|---|
| 1 | __ | __ | __ |
| 2 | __ | __ | __ |
| 3 | __ | __ | __ |

## Product thinking
- **Stakeholder:** Product manager for payments reliability, plus the customer support lead.
- **North-star metric:** payment success rate; supporting metrics are app crash-free sessions, support ticket resolution time and Play Store rating.
- **Experiment:** ship the top fix to 10% of users, compare payment success rate and 1-star review share against the control group over 2 weeks, then roll out if the lift holds.

## Run it yourself
```bash
pip install -r requirements.txt
python scrape_reviews.py
export ANTHROPIC_API_KEY=...        # optional: or use `keywords` mode for a free baseline
python tag_reviews.py llm           # or: python tag_reviews.py keywords
python validate.py sample           # label data/validation_sheet.csv by hand
python validate.py score
python analyze.py
streamlit run app.py
```
After changing theme rules, rerun `python tag_reviews.py keywords` to refresh all rows. LLM mode reuses cached labels and applies the keyword rules only to reviews cached as `Other`.

## Project structure
| File | Purpose |
|---|---|
| `scrape_reviews.py` | Downloads reviews from Google Play |
| `tag_reviews.py` | Theme, sentiment and severity tagging (keyword rules or LLM) |
| `validate.py` | Builds a 50-review labelling sheet and scores agreement |
| `analyze.py` | Charts, priority table and recommendations draft |
| `app.py` | Streamlit dashboard |

## Limitations
- Play Store only; sample is the newest reviews per app, so it reflects recent sentiment rather than all-time.
- Reviews skew negative and short; many cannot be assigned a specific theme.
- Tagging can be wrong on sarcasm and mixed reviews. Agreement was measured on a 50-review sample only.
- Severity is a rule-based or LLM judgment, not a measured business impact.

## Tech stack
Python, pandas, matplotlib, Streamlit, google-play-scraper

