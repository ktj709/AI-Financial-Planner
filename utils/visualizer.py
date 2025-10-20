
"""
Simple charting utility that creates a spending breakdown bar chart and saves to PNG.
Uses matplotlib (no fixed colors/style so it's portable) as required by project.
"""
import matplotlib.pyplot as plt
import pandas as pd
from pathlib import Path

def save_category_breakdown(df: pd.DataFrame, out_path: str = "spending_breakdown.png"):
    """Aggregate by category and save a bar chart to out_path."""
    agg = df.groupby("category")["amount"].sum().abs().sort_values(ascending=False)
    plt.figure(figsize=(8,5))
    agg.plot(kind="bar")
    plt.title("Spending by Category (absolute values)")
    plt.xlabel("Category")
    plt.ylabel("Total Amount")
    Path(out_path).parent.mkdir(parents=True, exist_ok=True)
    plt.tight_layout()
    plt.savefig(out_path)
    plt.close()
    return out_path

def save_timeseries(df: pd.DataFrame, out_path: str = "spending_timeseries.png"):
    """Daily spending timeseries (sum per date)."""
    df["date"] = pd.to_datetime(df["date"])
    agg = df.groupby("date")["amount"].sum().abs().sort_index()
    plt.figure(figsize=(10,4))
    agg.plot()
    plt.title("Daily Spending (absolute)")
    plt.xlabel("Date")
    plt.ylabel("Amount")
    plt.tight_layout()
    plt.savefig(out_path)
    plt.close()
    return out_path
