import os
from data_pipeline import load_and_prepare, build_figures, generate_insights, generate_recommendations

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATASET_PATH = os.path.join(BASE_DIR, 'Dataset', 'Aadhar Enrolment Dataset.csv')

data = load_and_prepare(DATASET_PATH, state_filter='Maharashtra')
figs = build_figures(data)
insights = generate_insights(data)
recs = generate_recommendations(data)

print("Loaded rows:", len(data['df']))
print("Monthly points:", len(data['monthly']))
print("Districts:", data['df']['district'].nunique())
print("Pincodes:", data['df']['pincode'].nunique())
print("Insights summary keys:", list(insights.keys()))

# Optional: print some insight strings
for k, v in insights.items():
    print(f"\n[{k}]\nWhat: {v['what']}\nFindings: {v['findings']}\nWhy: {v['why']}")

print("\nPolicy Recommendations:")
for r in recs:
    print("-", r)
