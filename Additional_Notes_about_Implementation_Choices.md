🧩 Additional Notes about Implementation Choices
1️⃣ Modular Multi-Agent Design

Each financial function — spending analysis, purchase planning, and trip simulation — was encapsulated in a dedicated agent class.
This promotes loose coupling and high cohesion, allowing independent testing, debugging, and future scalability (e.g., adding an “Investment Advisor” agent).

2️⃣ Gemini 2.0 Flash Integration

Used for intent classification to make the system conversational and context-aware.

Integrated through a minimal wrapper (utils/gemini_client.py) with .env-based key management.

A keyword-based fallback was added to ensure full offline functionality, keeping the app robust even without an API connection.

Reasoning: The assignment emphasized LLM usage but required reliability in demo environments, hence the hybrid (LLM + heuristic) design.

3️⃣ Streamlit + CLI Dual Interface

CLI (main.py) satisfies the “Command-Line Agent System” requirement in the PDF.

Streamlit App (app.py) demonstrates improved user experience and visualization for real-world usability.

Reasoning: Having both allows the project to meet academic evaluation requirements while also looking industry-ready.

4️⃣ Synthetic Transaction Data via Faker

Since real financial APIs were not part of the scope, synthetic data generation ensures:

Consistent, privacy-safe test data.

Realistic category and amount distributions for ML models.

Reasoning: Enables deterministic testing while fulfilling the “data ingestion” and “analytics” criteria.

5️⃣ Machine Learning Forecasting

Implemented Linear Regression to predict savings trends based on historical synthetic data.

Outputs include slope (model_coef), predicted next-month savings, and recommended monthly savings.

Reasoning: Linear Regression aligns with the PDF’s requirement of “ML-based pattern analysis and forecasting,” while keeping computational complexity minimal for demo.

6️⃣ Visualizations with Matplotlib

Used matplotlib for category breakdown and spending trends.

Simple static charts ensure compatibility with both CLI and Streamlit.

Charts saved under /outputs for persistence.

Reasoning: Matches “financial visualization” deliverable and works offline.

7️⃣ Monitoring with Sentry

Integrated Sentry SDK for logging and debugging agent actions.
This fulfills the requirement for system observability and allows better traceability of user sessions.

8️⃣ Environment & Dependencies

No venv was used as per project requirement.
Dependencies were consolidated in requirements.txt and configured to be lightweight and compatible across Python 3.10–3.13.

9️⃣ Design Principle

“Explainable AI” — every numerical output (forecast, anomaly, feasibility) is directly derived from visible computations, not hidden heuristics.

Reasoning: Helps meet the “transparency and explainability” expectation from the assignment.

🔟 Overall Design Choice

The entire system was built to simulate a production-ready AI planner while remaining academic-evaluation friendly:

Clear separation of logic and presentation.

Easy reproducibility on any local machine.

Self-contained — no external financial APIs required.
