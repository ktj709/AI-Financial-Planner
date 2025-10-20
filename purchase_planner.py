
"""
Big Purchase Planner:
- Simple linear projection forecasting for savings goal using past monthly savings trend
- Suggests monthly saving needed to reach target in desired months
"""
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from datetime import datetime
import calendar

class PurchasePlanner:
    def __init__(self, transactions: pd.DataFrame, current_balance: float = 0.0):
        self.transactions = transactions.copy()
        self.current_balance = current_balance

    def monthly_savings_series(self):
        df = self.transactions.copy()
        df["date"] = pd.to_datetime(df["date"])
        df["month"] = df["date"].dt.to_period("M")
        # define savings as negative amounts (income credits) minus spending (positive)
        monthly_net = df.groupby("month")["amount"].sum()
        # treat negative as net positive savings when incomes dominate
        return monthly_net.rename_axis("month").reset_index()

    def forecast_required_savings(self, target_amount: float, months: int = 12):
        """
        Compute required monthly saving to reach target from current_balance in 'months'.
        Also uses a linear model on past monthly net to show projection (simple).
        """
        series = self.monthly_savings_series()
        if series.shape[0] < 2:
            # fallback simple division
            needed = max(0.0, (target_amount - self.current_balance) / months)
            return {"monthly_needed": float(round(needed,2)), "method": "simple_division"}

        # prepare data for regression
        series = series.sort_values("month")
        # x as integer index
        x = np.arange(len(series)).reshape(-1,1)
        y = -series["amount"].values  # invert sign: positive is savings
        model = LinearRegression().fit(x, y)
        # predicted monthly saving next month
        next_idx = np.array([[len(series)]])
        predicted_next = float(model.predict(next_idx)[0])
        # required monthly to hit target
        remaining = max(0.0, target_amount - self.current_balance)
        monthly_needed = remaining / months
        return {
            "monthly_needed": float(round(monthly_needed,2)),
            "predicted_next_month_saving": float(round(predicted_next,2)),
            "model_coef": float(model.coef_[0]),
            "method": "linear_regression_on_monthly_net"
        }
