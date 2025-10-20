# app.py
"""
Streamlit Web Interface for the Multi-Agent AI Financial Planner
✅ Combines manual sidebar navigation + natural language query mode
✅ Uses same architecture and agents from the CLI version (main.py)
"""

import streamlit as st
import pandas as pd
from utils.data_generator import generate_transactions
from router_agent import RouterAgent
import os

# --- PAGE CONFIG ---
st.set_page_config(page_title="AI Financial Planner", layout="wide", page_icon="💰")

# --- SIMULATED LOGIN ---
st.sidebar.header("🔐 Simulated Login")
username = st.sidebar.text_input("Enter username", "demo_user")
login_btn = st.sidebar.button("Login / Reset Session")

if login_btn or "user" not in st.session_state:
    st.session_state["user"] = {"username": username, "balance": 2500.00}
    st.session_state["transactions"] = generate_transactions(300)
    st.session_state["router"] = RouterAgent(
        st.session_state["transactions"],
        user_balance=st.session_state["user"]["balance"]
    )
    st.success(f"Logged in as {username} (Simulated)")
    st.rerun()

user = st.session_state["user"]
router = st.session_state["router"]

# --- SIDEBAR NAVIGATION ---
st.sidebar.header("🧭 Navigation")
mode = st.sidebar.radio(
    "Choose a mode:",
    ["💬 Natural Query Mode", "📊 Spending Advisor", "🚗 Purchase Planner", "✈️ Trip Planner"],
    index=0
)

st.sidebar.markdown("---")
st.sidebar.info(f"Current Balance: **${user['balance']}**")

# --- TITLE ---
st.title("💰 Multi-Agent AI Financial Planner")
st.caption("Built according to the AI/ML Technical Assignment requirements.")

# --- NATURAL LANGUAGE MODE ---
if mode == "💬 Natural Query Mode":
    st.subheader("💬 Ask a Question (Natural Language)")
    query = st.text_input("e.g., 'Plan a 4-day NYC trip with a $2000 budget'")
    run_btn = st.button("Run Query 🚀")

    if run_btn and query.strip():
        kwargs = {}
        q_lower = query.lower()
        import re
        if any(word in q_lower for word in ["buy", "purchase", "car", "save"]):
            m = re.search(r"\$?(\d{3,}(?:\.\d{1,2})?)", q_lower.replace(",", ""))
            if m:
                kwargs["target_amount"] = float(m.group(1))
            m2 = re.search(r"(\d+)\s*(months|month|m)", q_lower)
            if m2:
                kwargs["months"] = int(m2.group(1))
        if "trip" in q_lower or "nyc" in q_lower:
            m = re.search(r"\$?(\d{2,5})", q_lower.replace(",", ""))
            if m:
                kwargs["budget"] = float(m.group(1))
            m2 = re.search(r"(\d+)\s*(day|days)", q_lower)
            if m2:
                kwargs["days"] = int(m2.group(1))
            kwargs["destination"] = "NYC" if "nyc" in q_lower else "Unknown"

        with st.spinner("Analyzing query using RouterAgent..."):
            response = router.handle(query, **kwargs)

        st.subheader("🧠 Agent Response")
        st.json(response)

        # Auto-display visuals
        if response["intent"] == "spending":
            st.markdown("### 📊 Visual Insights")
            visuals = response.get("visuals", {})
            for k, path in visuals.items():
                if os.path.exists(path):
                    st.image(path, caption=k)
        elif response["intent"] == "purchase":
            plan = response["plan"]
            st.metric("Monthly Needed", f"${plan['monthly_needed']}")
            st.metric("Predicted Next Month Saving", f"${plan['predicted_next_month_saving']}")
        elif response["intent"] == "trip":
            plan = response["plan"]
            st.markdown(f"### ✈️ Trip Plan for {plan['destination']}")
            st.json(plan["breakdown"])
            st.success("✅ Trip Feasible" if plan["feasible"] else "⚠️ Trip Not Feasible")

# --- MANUAL MODES ---
elif mode == "📊 Spending Advisor":
    st.header("📊 Daily Spending Advisor")
    st.write("Analyze your spending habits and visualize expense patterns.")

    advisor = router  # Router contains transactions
    df = st.session_state["transactions"]
    from spending_advisor import SpendingAdvisor
    agent = SpendingAdvisor(df)

    if st.button("Run Spending Analysis"):
        st.success("Running analysis...")
        result = {
            "summary": agent.summary(),
            "unusual": agent.unusual_spending(),
            "visuals": agent.generate_visuals("./outputs")
        }
        st.json(result)
        for name, path in result["visuals"].items():
            if os.path.exists(path):
                st.image(path, caption=name)

elif mode == "🚗 Purchase Planner":
    st.header("🚗 Big Purchase Planner")
    st.write("Forecast savings and plan for major purchases.")
    from purchase_planner import PurchasePlanner
    df = st.session_state["transactions"]
    agent = PurchasePlanner(df, current_balance=user["balance"])

    target = st.number_input("Target Purchase Amount ($):", 1000, 100000, 30000, step=1000)
    months = st.slider("Months to achieve goal:", 1, 36, 12)
    if st.button("Generate Plan"):
        plan = agent.forecast_required_savings(target, months)
        st.json(plan)
        st.metric("Monthly Needed", f"${plan['monthly_needed']}")
        st.metric("Predicted Next Month Saving", f"${plan['predicted_next_month_saving']}")

elif mode == "✈️ Trip Planner":
    st.header("✈️ Trip Planning Assistant")
    st.write("Plan optimized trips based on your current balance and budget.")
    from trip_planner import TripPlanner
    agent = TripPlanner(user["balance"])

    destination = st.text_input("Destination", "New York City")
    days = st.slider("Trip Duration (Days):", 1, 14, 4)
    budget = st.number_input("Total Trip Budget ($):", 500, 10000, 2000, step=100)
    if st.button("Generate Trip Plan"):
        plan = agent.simulate_travel_options(destination, days, budget)
        st.json(plan)
        st.success("✅ Trip Feasible" if plan["feasible"] else "⚠️ Not Feasible")

# --- SESSION HISTORY ---
with st.expander("🧩 View Router Session History"):
    st.write(router.session)
