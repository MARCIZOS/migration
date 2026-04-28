"""Run portfolio analysis locally by calling the API handler directly.

This script constructs a small portfolio payload and invokes `create_portfolio`.
It prints JSON output or the full exception for debugging.
"""
import json
import traceback
import sys
import os

# Ensure workspace root is on sys.path so `app` package imports resolve.
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from app.models.portfolio import PortfolioRequest, Asset
from app.api.routes import create_portfolio


def run_and_print(name: str, assets: list[Asset]):
    print(f"\n--- Running analysis: {name} ---")
    payload = PortfolioRequest(assets=assets)
    try:
        result = create_portfolio(payload)
        # Print concise selected metrics
        metrics = result.get("metrics", {})
        div = result.get("diversification", {})
        stress = result.get("stress", {})
        clusters = result.get("clusters", {})
        print(json.dumps({
            "name": name,
            "metrics": metrics,
            "diversification": div,
            "stress": stress,
            "clusters": clusters,
        }, indent=2, default=str))
        return result
    except Exception:
        print("ERROR running analysis:")
        traceback.print_exc()
        raise


if __name__ == "__main__":
    # Current portfolio (baseline)
    baseline_assets = [Asset(ticker="AAPL", weight=0.5), Asset(ticker="MSFT", weight=0.5)]
    baseline = run_and_print("Baseline 50/50 AAPL-MSFT", baseline_assets)

    # Improved portfolio: introduce bonds, gold, and international equity to reduce cluster concentration
    improved_assets = [
        Asset(ticker="AAPL", weight=0.30),
        Asset(ticker="MSFT", weight=0.20),
        Asset(ticker="AGG", weight=0.30),
        Asset(ticker="GLD", weight=0.10),
        Asset(ticker="VEA", weight=0.10),
    ]
    improved = run_and_print("Improved diversified portfolio", improved_assets)

    print("\nCompleted both analyses.")
