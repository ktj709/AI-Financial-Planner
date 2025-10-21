💰AI Financial Planner

Multi-Agent Intelligent Financial Assistant
(Built with Gemini 2.0 Flash LLM, Streamlit, and Machine Learning)

🧠 Overview

The AI Financial Planner is a multi-agent intelligent system designed to assist users in understanding and managing their personal finances through data-driven insights and natural language queries.

It combines Machine Learning, LLMs (Gemini 2.0 Flash), and multi-agent orchestration to perform:

Spending analysis and visualization

Purchase goal forecasting

Trip planning and feasibility simulation

The system offers two modes:

🖥️ Streamlit Web App — interactive dashboard

💬 CLI Interface — quick command-line mode

🚀 Features
| Feature                            | Description                                                                                |
| ---------------------------------- | ------------------------------------------------------------------------------------------ |
| 💬 **Natural Language Query Mode** | Ask finance-related questions in plain English (via Gemini 2.0 Flash or keyword fallback). |
| 🧾 **Spending Advisor**            | Analyzes spending patterns, categories, and detects unusual expenses.                      |
| 🚗 **Purchase Planner**            | Uses Linear Regression to forecast future savings and plan for big purchases.              |
| ✈️ **Trip Planner**                | Simulates travel cost breakdown and checks trip feasibility.                               |
| 📊 **Interactive Charts**          | Generates spending breakdown and time-series visuals.                                      |
| 🔐 **Secure Config**               | `.env` file stores all API keys (Gemini, Sentry).                                          |
| 🧩 **Modular Agents**              | Each financial domain handled by an independent agent module.                              |
| 🧠 **LLM Integration**             | Gemini 2.0 Flash used for intent classification and reasoning.                             |
| 🪶 **Monitoring**                  | Sentry SDK for error tracking and session transparency.                                    |

🏗️ Architecture Overview
Core Components

RouterAgent → Orchestrates flow between agents and classifies user intent.

SpendingAdvisor → Analyzes expenses, identifies anomalies, generates visuals.

PurchasePlanner → Runs ML model (Linear Regression) to forecast savings.

TripPlanner → Generates simulated travel cost breakdown.

Gemini Client → Connects to Gemini 2.0 Flash for natural language understanding.

Visualizer → Creates charts using Matplotlib.

🧩 File Structure

AI_Financial_Planner/
│
├── main.py                  # CLI entry point
├── app.py                   # Streamlit web app
├── router_agent.py          # Core orchestrator
│
├── spending_advisor.py      # Spending analysis module
├── purchase_planner.py      # Savings forecasting module
├── trip_planner.py          # Trip planning module
│
├── utils/
│   ├── gemini_client.py     # Gemini 2.0 Flash API wrapper
│   ├── data_generator.py    # Synthetic data generator (Faker)
│   └── visualizer.py        # Chart generation utilities
│
├── sentry_setup.py          # Monitoring setup
├── .env                     # API keys (GEMINI_API_KEY, SENTRY_DSN)
├── requirements.txt         # Dependencies
└── Architecture_Documentation.md  # Architecture explanation

⚙️ Installation & Setup
1️⃣ Clone the Repository

git clone https://github.com/your-username/ai-financial-planner.git
cd ai-financial-planner

2️⃣ Install Requirements

pip install -r requirements.txt

3️⃣ Create .env File

GEMINI_API_KEY=your_gemini_api_key_here
SENTRY_DSN=your_sentry_dsn_here

4️⃣ Run the App
💬 CLI Mode:
python main.py --user demo

🖥️ Streamlit Web App:
streamlit run app.py

🧠 Example Queries (Natural Language)
| Query                                                 | Agent           |
| ----------------------------------------------------- | --------------- |
| “Show me my spending breakdown for the last 30 days.” | SpendingAdvisor |
| “List unusual spending patterns this week.”           | SpendingAdvisor |
| “Help me save for a $10,000 bike in 8 months.”        | PurchasePlanner |
| “I want to buy a $30,000 car next year.”              | PurchasePlanner |
| “Plan a 4-day NYC trip with a $2000 budget.”          | TripPlanner     |
| “Can I afford a weekend trip to Goa under $1000?”     | TripPlanner     |

📈 Machine Learning Logic

Algorithm: Linear Regression (scikit-learn)

Used In: PurchasePlanner

Purpose: Predict next-month savings and recommend monthly saving goals.

Input Data: Synthetic transaction dataset generated via Faker.

Outputs:

monthly_needed → Required savings per month.

predicted_next_month_saving → Forecasted ML output.

model_coef → Trend slope.

🧭 Monitoring & Logging

Sentry SDK captures errors and agent-level reasoning trails.

RouterAgent.session keeps all queries, intents, and outcomes for transparency.

🧩 Agents Interaction Flow

User Query
   │
   ▼
RouterAgent (LLM + Heuristic Classification)
   ├── SpendingAdvisor → Charts + Expense Summary
   ├── PurchasePlanner → ML Forecast + Saving Strategy
   └── TripPlanner → Travel Simulation + Feasibility
   │
   ▼
Streamlit / CLI Output (Visuals + JSON Insights)

🧰 Dependencies

python-dotenv
requests
pandas
numpy
matplotlib
scikit-learn
streamlit
rich
faker
PyMuPDF
beautifulsoup4
python-dateutil
scipy
sentry-sdk
tqdm


Install via:
pip install -r requirements.txt


📊 Example Outputs
1️⃣ Spending Breakdown
{
  "intent": "spending",
  "summary": {"salary": 143478.05, "rent": 50136.03, "groceries": 6271.77},
  "unusual": ["salary"],
  "visuals": {
    "category_chart": "./outputs/spending_breakdown.png",
    "timeseries_chart": "./outputs/spending_timeseries.png"
  }
}


2️⃣ Purchase Forecast
{
  "intent": "purchase",
  "plan": {
    "monthly_needed": 937.5,
    "predicted_next_month_saving": 18300.67,
    "model_coef": 2093.84
  }
}

🧠 LLM Integration (Gemini 2.0 Flash)

The RouterAgent calls utils/gemini_client.py, which:

Reads API key from .env

Sends classification prompt to Gemini

Returns an intent label: spending, purchase, trip, or other

If the API fails, fallback keyword-based classification ensures offline usability.

🧩 Future Enhancements

Real financial data API (e.g., Plaid)

Voice-based financial assistant

Advanced ML forecasting (Prophet/ARIMA)

Multi-user persistent accounts

Expense trend recommendations

📚 Credits

LLM: Gemini 2.0 Flash

Frameworks: Streamlit, scikit-learn

Visualization: Matplotlib

Monitoring: Sentry

Data Simulation: Faker

✅ Summary

This system demonstrates a modular, intelligent, and explainable AI architecture that aligns with all functional and technical requirements from the assignment PDF.
It blends LLMs, ML forecasting, visualization, and financial simulation into a cohesive end-to-end solution.
