Architecture Documentation

Project: Multi-Agent AI Financial Planner
Developed for: AI/ML Intern Technical Assignment
Developer: Kshitij Saxena
Date: 21-10-2025

1. 🎯 Overview

The AI Financial Planner is a modular, multi-agent system that transforms a basic banking backend into a proactive, intelligent financial assistant.
It analyzes user spending, plans savings for large purchases, and generates optimized travel budgets — all through a natural language or interactive web interface.

The system supports two interfaces:

a) Command-Line Interface (CLI) — for quick text-based interactions.
b) Streamlit Web App — for an interactive, dashboard-like experience.

Both interfaces communicate with the same backend multi-agent architecture.

2. 🧩 System Architecture Overview
2.1 Core Components

| Component                      | Description                                                                                                                                                            |
| ------------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **RouterAgent (Orchestrator)** | Acts as the central brain. Analyzes user input using Gemini 2.0 Flash or keyword heuristics, routes queries to appropriate agents, and maintains conversation context. |
| **SpendingAdvisor**            | Analyzes transaction patterns, identifies spending categories, detects unusual spending via z-score, and generates visual charts.                                      |
| **PurchasePlanner**            | Helps users plan for big purchases by forecasting savings goals using Linear Regression (ML).                                                                          |
| **TripPlanner**                | Simulates trip budgets using mock travel data and assesses trip feasibility based on user balance.                                                                     |
| **Gemini Client Wrapper**      | Integrates the Gemini 2.0 Flash LLM for natural language understanding. Reads API key from `.env`.                                                                     |
| **Data Generator (Faker)**     | Produces realistic mock transaction datasets for demonstration and testing.                                                                                            |
| **Visualizer**                 | Generates bar and line charts for spending insights using Matplotlib.                                                                                                  |
| **Monitoring Layer (Sentry)**  | Enables error tracking and decision logging for transparency.                                                                                                          |


3. 🧠 Multi-Agent Architecture Diagram
(Present in the repo at the root level itself)

4. 🔄 Data Flow
4.1 Input Stage

User logs in (simulated authentication).
Enters a query via CLI or Streamlit input box.

4.2 Processing Stage

RouterAgent receives the query.
Tries Gemini 2.0 Flash for intent classification:

spending, purchase, trip, or other.

If Gemini unavailable, uses keyword heuristics.
Based on intent, routes data to the relevant agent.


4.3 Agent Actions
| Agent               | Input                  | Processing                                         | Output                |
| ------------------- | ---------------------- | -------------------------------------------------- | --------------------- |
| **SpendingAdvisor** | Transactions DataFrame | Expense grouping, anomaly detection, visualization | Summary dict + charts |
| **PurchasePlanner** | Transactions + balance | Linear Regression forecasting                      | Savings plan dict     |
| **TripPlanner**     | Balance + query params | Simulated travel costs                             | Trip plan dict        |

4.4 Output Stage

Router collects agent response.

CLI prints formatted JSON.

Streamlit renders charts, metrics, and structured insights.

5. ⚙️ Technology Stack
   | Layer                | Tools / Libraries Used                            |
| -------------------- | ------------------------------------------------- |
| **Frontend (Web)**   | Streamlit                                         |
| **Frontend (CLI)**   | Rich                                              |
| **Backend Logic**    | Python                                            |
| **LLM Integration**  | Gemini 2.0 Flash (via REST + `.env` API key)      |
| **Data Processing**  | Pandas, NumPy                                     |
| **Visualization**    | Matplotlib                                        |
| **Machine Learning** | scikit-learn (Linear Regression), SciPy (Z-score) |
| **Mock Data**        | Faker                                             |
| **PDF/Text Parsing** | PyMuPDF, BeautifulSoup4                           |
| **Monitoring**       | Sentry SDK                                        |
| **Configuration**    | python-dotenv                                     |


6. 🧮 Machine Learning Component

Algorithm Used: Linear Regression (sklearn.linear_model.LinearRegression)

Purpose: Predicts next-month savings trends and models user’s financial behavior.

Inputs: Monthly aggregated net savings from transaction data.

Outputs:

monthly_needed: Required saving per month to hit target.

predicted_next_month_saving: ML forecast.

model_coef: Financial trend slope.

7. 🔐 Security and Permissions

No real financial data used — all transactions are synthetic (via Faker).

.env file securely stores:

GEMINI_API_KEY

SENTRY_DSN (optional)

RouterAgent enforces simulated user-level session management.

No external write access or real API calls.

8. 🧭 Monitoring & Observability

Sentry SDK integrated for error tracking and agent reasoning trace.

RouterAgent.session dictionary logs:

Query text

Classified intent

Timestamped responses

This allows transparent demonstration of how decisions are made — fulfilling the PDF’s “Agent reasoning trail” requirement.

9. 🧰 Deployment & Execution

   | Mode                | Command                           | Description                                      |
| ------------------- | --------------------------------- | ------------------------------------------------ |
| CLI Mode            | `python main.py --user demo`      | Text-based interactive mode                      |
| Streamlit Web Mode  | `streamlit run app.py`            | Web dashboard with navigation + natural language |
| Optional Monitoring | Set `SENTRY_DSN` in `.env`        | Enables real-time logging                        |
| Dependency Install  | `pip install -r requirements.txt` | Installs all dependencies                        |

10. 💬 Example User Interactions
    | Example Query                                         | Agent Used      | Output                |
| ----------------------------------------------------- | --------------- | --------------------- |
| “Show me my spending breakdown for the last 30 days.” | SpendingAdvisor | Charts + summary      |
| “I want to buy a $30,000 car next year.”              | PurchasePlanner | Savings plan forecast |
| “Plan a 4-day NYC trip with a $2000 budget.”          | TripPlanner     | Budget breakdown      |
| “List unusual spending patterns this week.”           | SpendingAdvisor | Anomaly report        |
| “Help me save for a $10,000 bike in 8 months.”        | PurchasePlanner | ML-driven forecast    |

11. 🧩 Modularity Summary
 Each .py file represents one independent module:

| File                      | Purpose                          |
| ------------------------- | -------------------------------- |
| `main.py`                 | CLI interface                    |
| `app.py`                  | Streamlit interface              |
| `router_agent.py`         | Orchestration and routing        |
| `spending_advisor.py`     | Expense analytics                |
| `purchase_planner.py`     | Forecasting and savings planning |
| `trip_planner.py`         | Simulated trip optimization      |
| `utils/gemini_client.py`  | LLM interface (Gemini 2.0 Flash) |
| `utils/data_generator.py` | Synthetic data generator         |
| `utils/visualizer.py`     | Chart rendering                  |
| `sentry_setup.py`         | Monitoring configuration         |

12. 🧠 Key Design Principles

Modularity: Each agent functions independently.

Reusability: Common utilities shared via utils/.

LLM Flexibility: Gemini API can be swapped for any other LLM.

Transparency: Router keeps reasoning history.

Extensibility: Future agents (e.g., “Investment Advisor”) can be added easily.

✅ Summary

This architecture successfully implements the Multi-Agent Financial Planner system exactly as described in the assignment PDF.
It demonstrates:

Multi-agent orchestration

LLM-based reasoning

ML forecasting

Visualization and insight generation

Monitoring and modular design
