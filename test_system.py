"""
Test script to verify ARAIA system with different portfolio examples.
Run this from the migration directory after backend is running.
"""

import json
import requests
import sys

BACKEND_URL = "http://127.0.0.1:8000/portfolio"

# Test portfolios
TEST_PORTFOLIOS = {
    "us_stocks": {
        "name": "US Tech Portfolio",
        "assets": [
            {"ticker": "AAPL", "weight": 0.3},
            {"ticker": "MSFT", "weight": 0.3},
            {"ticker": "GOOGL", "weight": 0.2},
            {"ticker": "NVDA", "weight": 0.2},
        ],
    },
    "indian_stocks": {
        "name": "Indian Banking Sector",
        "assets": [
            {"ticker": "HDFC.NS", "weight": 0.4},
            {"ticker": "ICICI.NS", "weight": 0.3},
            {"ticker": "AXIS.NS", "weight": 0.3},
        ],
    },
    "mixed_portfolio": {
        "name": "Mixed Global Portfolio",
        "assets": [
            {"ticker": "AAPL", "weight": 0.25},
            {"ticker": "MSFT", "weight": 0.25},
            {"ticker": "TCS.NS", "weight": 0.25},
            {"ticker": "INFY.NS", "weight": 0.25},
        ],
    },
}


def test_portfolio(portfolio_name: str, portfolio_data: dict):
    """Test a portfolio against the backend."""
    print(f"\n{'='*70}")
    print(f"Testing: {portfolio_data['name']}")
    print(f"Portfolio: {portfolio_name}")
    print(f"{'='*70}")

    payload = {"assets": portfolio_data["assets"]}

    print(f"\n📤 Sending request to {BACKEND_URL}")
    print(f"📊 Portfolio composition:")
    for asset in portfolio_data["assets"]:
        print(f"   • {asset['ticker']}: {asset['weight']:.1%}")

    try:
        response = requests.post(BACKEND_URL, json=payload, timeout=60)

        if response.status_code == 200:
            data = response.json()
            print(f"\n✅ API Response Received (HTTP 200)")

            # Extract and display metrics
            metrics = data.get("metrics", {})
            diversification = data.get("diversification", {})
            stress = data.get("stress", {})
            clusters = data.get("clusters", {})

            print(f"\n📈 Risk Metrics:")
            print(f"   Volatility:     {metrics.get('volatility', 0):.2%}")
            print(f"   VaR (95%):      {metrics.get('var', 0):.6f}")
            print(f"   CVaR (95%):     {metrics.get('cvar', 0):.6f}")
            print(f"   Max Drawdown:   {metrics.get('max_drawdown', 0):.2%}")

            print(f"\n🎯 Diversification:")
            print(f"   ENB:                    {diversification.get('enb', 0):.2f}")
            print(f"   Diversification Score:  {diversification.get('diversification_score', 0):.4f}")

            print(f"\n⚠️ Stress Test (Normal vs Stressed):")
            print(f"   VaR:  {stress.get('normal_var', 0):.6f} → {stress.get('stressed_var', 0):.6f}")
            print(f"   CVaR: {stress.get('normal_cvar', 0):.6f} → {stress.get('stressed_cvar', 0):.6f}")

            print(f"\n🔗 Clusters ({len(clusters)} found):")
            for cluster_id, tickers in clusters.items():
                print(f"   Cluster {cluster_id}: {', '.join(tickers)}")

            high_corr = data.get("high_correlation_pairs", [])
            if high_corr:
                print(f"\n🔥 High Correlation Pairs (> 0.7):")
                for ticker_a, ticker_b, corr in high_corr:
                    print(f"   {ticker_a} ↔ {ticker_b}: {corr:.4f}")

            ai_msg = data.get("ai_explanation", "")
            if ai_msg and "unavailable" not in ai_msg.lower():
                print(f"\n🤖 AI Insights:")
                print(f"   {ai_msg[:150]}...")
            else:
                print(f"\n📌 AI Insights: Not available (check Groq API key)")

            print(f"\n✅ All metrics calculated successfully!")
            return True

        else:
            print(f"\n❌ API Error (HTTP {response.status_code})")
            print(f"   Response: {response.json().get('detail', response.text)}")
            return False

    except requests.exceptions.ConnectionError:
        print(f"\n❌ Connection Error: Cannot reach backend at {BACKEND_URL}")
        print(f"   Make sure uvicorn is running: uvicorn app.main:app --reload")
        return False

    except requests.exceptions.Timeout:
        print(f"\n❌ Timeout: Backend took too long to respond")
        return False

    except Exception as exc:
        print(f"\n❌ Unexpected Error: {exc}")
        return False


def main():
    """Run all tests."""
    print("\n" + "=" * 70)
    print("🧪 ARAIA System Test Suite")
    print("=" * 70)
    print(f"Backend URL: {BACKEND_URL}")
    print(f"Test Cases: {len(TEST_PORTFOLIOS)}")

    results = {}

    for portfolio_key, portfolio_data in TEST_PORTFOLIOS.items():
        success = test_portfolio(portfolio_key, portfolio_data)
        results[portfolio_key] = success

    # Summary
    print(f"\n\n{'='*70}")
    print("📊 Test Summary")
    print(f"{'='*70}")

    passed = sum(1 for v in results.values() if v)
    total = len(results)

    for name, success in results.items():
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status}: {TEST_PORTFOLIOS[name]['name']}")

    print(f"\nTotal: {passed}/{total} tests passed")

    if passed == total:
        print("\n🎉 System is working correctly!")
        return 0
    else:
        print("\n⚠️ Some tests failed. Check backend logs.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
