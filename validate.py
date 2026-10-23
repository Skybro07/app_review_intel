"""Step 3: measure tagging accuracy against YOUR hand labels.
  python validate.py sample   -> writes data/validation_sheet.csv (50 reviews, no model labels shown)
  (fill the 'my_theme' column using the theme names from tag_reviews.py, or 'Other')
  python validate.py score    -> prints agreement % and a confusion summary
"""
import sys
import pandas as pd

if len(sys.argv) != 2 or sys.argv[1] not in {"sample", "score"}:
    raise SystemExit("Usage: python validate.py [sample|score]")

if sys.argv[1] == "sample":
    df = pd.read_csv("data/reviews_tagged.csv").sample(50, random_state=1)
    out = df[["review_id", "app", "text"]].copy(); out["my_theme"] = ""
    out.to_csv("data/validation_sheet.csv", index=False)
    print("Label data/validation_sheet.csv, then run: python validate.py score")
else:
    mine = pd.read_csv("data/validation_sheet.csv")
    mine["my_theme"] = mine["my_theme"].fillna("").astype(str).str.strip()
    mine = mine[mine["my_theme"] != ""]
    if mine.empty:
        raise SystemExit(
            "No hand labels found. Fill in the 'my_theme' column in "
            "data/validation_sheet.csv, then run: python validate.py score"
        )

    model = pd.read_csv("data/reviews_tagged.csv")[["review_id", "theme"]]
    m = mine.merge(model, on="review_id")
    acc = (
        m["my_theme"].str.lower()
        == m["theme"].fillna("").astype(str).str.strip().str.lower()
    ).mean()
    print(f"Agreement on {len(m)} reviews: {acc:.0%}")
    print(pd.crosstab(m["my_theme"], m["theme"]))
