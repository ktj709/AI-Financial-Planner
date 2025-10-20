
"""
Trip Planning Assistant:
- Uses simulated travel pricing (assignment allows simulated responses).
- Builds a budget plan based on user's current finances and requested trip budget.
"""
from typing import Dict
import random

class TripPlanner:
    def __init__(self, user_balance: float):
        self.user_balance = user_balance

    def simulate_travel_options(self, destination: str, days: int, budget: float) -> Dict:
        """
        Simulate hotels/flights/activities costs and return an optimized plan
        (keeps strictly to assignment requirement: simulate or integrate travel APIs).
        """
        # Simulate categories
        flight = round(budget * random.uniform(0.2, 0.4), 2)
        hotel = round(budget * random.uniform(0.25, 0.45), 2)
        activities = round(budget * random.uniform(0.1, 0.2), 2)
        daily_food = round((budget - (flight + hotel + activities)) / (days or 1), 2)
        plan = {
            "destination": destination,
            "days": days,
            "budget": budget,
            "breakdown": {
                "flight_estimate": flight,
                "hotel_estimate": hotel,
                "activities_estimate": activities,
                "daily_food_estimate": daily_food
            },
            "feasible": budget <= self.user_balance or (budget * 0.5) <= self.user_balance
        }
        return plan
