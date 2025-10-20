
"""
Router / Orchestrator:
- Analyzes the user's plain text query and routes to the correct agent(s).
- For LLM-based intent classification it uses the gemini client wrapper.
- Keeps a minimal context (session dict) shared between agents.
"""
from utils.gemini_client import call_gemini
from spending_advisor import SpendingAdvisor
from purchase_planner import PurchasePlanner
from trip_planner import TripPlanner
import pandas as pd

class RouterAgent:
    def __init__(self, transactions: pd.DataFrame, user_balance: float = 0.0, session_id: str = "session"):
        self.transactions = transactions
        self.user_balance = user_balance
        self.session = {"id": session_id, "history": []}

    def classify_intent(self, query: str) -> str:
        """
        Use a brief prompt to Gemini to classify into intent categories:
        'spending', 'purchase', 'trip', or 'other'.
        """
        prompt = f"""
You are an intent classifier. Classify the user query into one of:
spending, purchase, trip, other.
Return only the single word label.

Query: \"{query}\"
"""
        try:
            resp = call_gemini(prompt, max_tokens=32)
            if not resp:
                raise RuntimeError("Empty response from Gemini")
            label = resp.strip().lower().split()[0]
            if label in ("spending", "purchase", "trip", "other"):
                return label
            return "other"
        except Exception:
            # fallback heuristic
            q = query.lower()
            if any(w in q for w in [
                "spend", "spending", "spent", "expense", "expenses",
                "breakdown", "report", "category", "categories", "analysis"
            ]):
                return "spending"
            if any(w in q for w in ["buy", "car", "purchase", "save", "saving"]):
                return "purchase"
            if any(w in q for w in ["trip", "flight", "hotel", "nyc", "plan"]):
                return "trip"
            return "other"

    def handle(self, query: str, **kwargs):
        label = self.classify_intent(query)
        self.session["history"].append({"query": query, "intent": label})
        if label == "spending":
            advisor = SpendingAdvisor(self.transactions)
            return {
                "intent": "spending",
                "summary": advisor.summary(),
                "unusual": advisor.unusual_spending(),
                "visuals": advisor.generate_visuals(out_dir=kwargs.get("out_dir","./outputs"))
            }
        elif label == "purchase":
            planner = PurchasePlanner(self.transactions, current_balance=self.user_balance)
            # expecting e.g. "I want to buy a $30000 car in 12 months"
            # simple parse:
            target = kwargs.get("target_amount", kwargs.get("amount", 0.0))
            months = kwargs.get("months", 12)
            return {"intent": "purchase", "plan": planner.forecast_required_savings(target, months)}
        elif label == "trip":
            trip = TripPlanner(self.user_balance)
            dest = kwargs.get("destination", "Unknown")
            days = kwargs.get("days", 3)
            budget = kwargs.get("budget", 1000.0)
            return {"intent": "trip", "plan": trip.simulate_travel_options(dest, days, budget)}
        else:
            return {"intent": "other", "message": "I could not determine the intent precisely."}
