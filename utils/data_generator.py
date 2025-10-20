
"""
Generate mock transactions & user profile data using Faker (as required by the PDF).
Output is a pandas DataFrame of transactions (date, amount, merchant, category).
"""
from faker import Faker
import pandas as pd
import random
from datetime import datetime, timedelta

fake = Faker()

CATEGORIES = ["groceries", "dining", "transport", "entertainment", "utilities", "salary", "rent", "shopping"]

def generate_transactions(n: int = 500, start_date: str = None):
    """Generate n mock transactions over the past ~6 months by default."""
    if start_date:
        start = datetime.fromisoformat(start_date)
    else:
        start = datetime.now() - timedelta(days=180)

    rows = []
    for _ in range(n):
        days_offset = random.randint(0, 180)
        date = (start + timedelta(days=days_offset)).date().isoformat()
        category = random.choices(CATEGORIES, weights=[15,12,10,8,6,10,12,7])[0]
        merchant = fake.company() if random.random() > 0.2 else fake.first_name() + " Shop"
        amount = round(random.uniform(3.0, 200.0), 2)
        # salary and rent larger amounts and occasional negative (income)
        if category == "salary":
            amount = round(random.uniform(1500, 5000), 2) * -1  # negative to indicate credit
        if category == "rent":
            amount = round(random.uniform(400, 2000), 2)
        rows.append({"date": date, "amount": amount, "merchant": merchant, "category": category})
    df = pd.DataFrame(rows)
    return df
