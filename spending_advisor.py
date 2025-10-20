
"""
Daily Spending Advisor agent:
- Categorizes expenses (we have category column already; in a real scenario we'd infer),
- Identifies unusual spending (simple z-score on category totals),
- Produces visualizations (via utils.visualizer).
"""
import pandas as pd
import numpy as np
from scipy import stats
from utils.visualizer import save_category_breakdown, save_timeseries

class SpendingAdvisor:
    def __init__(self, transactions: pd.DataFrame):
        self.transactions = transactions.copy()

    def category_breakdown(self):
        return self.transactions.groupby("category")["amount"].sum()

    def unusual_spending(self, z_thresh=2.0):
        # Aggregate absolute spending per category and find z-score
        agg = self.transactions.groupby("category")["amount"].sum().abs()
        if len(agg) < 2:
            return []
        z = np.abs(stats.zscore(agg))
        outliers = agg.index[z > z_thresh].tolist()
        return outliers

    def generate_visuals(self, out_dir="./outputs"):
        cat_img = save_category_breakdown(self.transactions, f"{out_dir}/spending_breakdown.png")
        ts_img = save_timeseries(self.transactions, f"{out_dir}/spending_timeseries.png")
        return {"category_chart": cat_img, "timeseries_chart": ts_img}

    def summary(self, top_n=5):
        agg = self.transactions.groupby("category")["amount"].sum().abs().sort_values(ascending=False)
        return agg.head(top_n).to_dict()
