
"""
CLI entrypoint that ties everything together.
Follows the PDF: command-line interface with simulated user authentication and
routing to three agents via the RouterAgent.
"""
import argparse
import pandas as pd
from utils.data_generator import generate_transactions
from router_agent import RouterAgent
from rich import print as rprint
from rich.prompt import Prompt

def simulate_login(username: str):
    # Simulated login as allowed by the assignment
    return {"username": username, "user_id": f"user_{username}", "balance": 2500.00}

def main():
    parser = argparse.ArgumentParser(description="Multi-Agent AI Financial Planner CLI (assignment)")
    parser.add_argument("--user", type=str, default="demo", help="username (simulated auth)")
    args = parser.parse_args()

    user = simulate_login(args.user)
    rprint(f"[bold green]Logged in as:[/bold green] {user['username']} (simulated)")

    # Create mock transactions as required by the assignment
    df = generate_transactions(n=300)
    router = RouterAgent(df, user_balance=user["balance"])

    while True:
        query = Prompt.ask("\nEnter your question (or 'exit' to quit)")
        if query.strip().lower() in ("exit", "quit"):
            rprint("[bold yellow]Goodbye![/bold yellow]")
            break

        # Simple CLI parse to extract optional parameters for purchase/trip
        # Keep parsing minimal to remain within PDF scope:
        kwargs = {}
        if "buy" in query.lower() or "car" in query.lower() or "purchase" in query.lower():
            # try to find a number in query
            import re
            m = re.search(r"\$?(\d{3,}(?:\.\d{1,2})?)", query.replace(",", ""))
            if m:
                kwargs["target_amount"] = float(m.group(1))
            m2 = re.search(r"(\d+)\s*(months|month|m)", query)
            if m2:
                kwargs["months"] = int(m2.group(1))
        if "trip" in query.lower() or "nyc" in query.lower():
            # basic extraction
            import re
            m = re.search(r"\$?(\d{2,5})", query.replace(",", ""))
            if m:
                kwargs["budget"] = float(m.group(1))
            m2 = re.search(r"(\d+)\s*(day|days)", query)
            if m2:
                kwargs["days"] = int(m2.group(1))
            kwargs["destination"] = "NYC" if "nyc" in query.lower() else "Unknown"

        # route the query
        resp = router.handle(query, **kwargs)
        rprint("[bold cyan]Response:[/bold cyan]")
        rprint(resp)

if __name__ == "__main__":
    main()
