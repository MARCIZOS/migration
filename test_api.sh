#!/bin/bash

echo "=== TESTING PDMS API ENDPOINTS ==="
echo ""

echo "1️⃣ Testing Portfolio Analysis Endpoint"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

RESPONSE=$(curl -s -X POST http://127.0.0.1:8001/portfolio \
  -H "Content-Type: application/json" \
  -d '{
    "assets": [
      {"ticker": "AAPL", "weight": 0.4},
      {"ticker": "MSFT", "weight": 0.3},
      {"ticker": "GOOGL", "weight": 0.3}
    ]
  }')

echo "$RESPONSE" | python -m json.tool 2>/dev/null | head -80

if echo "$RESPONSE" | grep -q "metrics"; then
  echo ""
  echo "✅ Portfolio endpoint: SUCCESS - metrics returned"
else
  echo ""
  echo "❌ Portfolio endpoint: FAILED - no metrics"
fi

echo ""
echo "2️⃣ Testing Stock Data Retrieval"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Testing if yfinance can fetch data for AAPL..."
python -c "
import yfinance as yf
try:
    ticker = yf.Ticker('AAPL')
    hist = ticker.history(period='1d')
    if len(hist) > 0:
        print('✅ yfinance: SUCCESS - data retrieved')
        print(f'   Latest close price: ${hist[\"Close\"].iloc[-1]:.2f}')
    else:
        print('❌ yfinance: FAILED - no data')
except Exception as e:
    print(f'❌ yfinance: ERROR - {str(e)[:100]}')
" 2>/dev/null

echo ""
echo "3️⃣ Testing Clustering & Correlation"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
if echo "$RESPONSE" | grep -q "clusters"; then
  echo "✅ Clustering: SUCCESS - cluster data present"
  CLUSTERS=$(echo "$RESPONSE" | python -c "import sys, json; data=json.load(sys.stdin); print(json.dumps(data.get('clusters', {}), indent=2))" 2>/dev/null | head -10)
  echo "   Clusters: $CLUSTERS"
else
  echo "❌ Clustering: FAILED - no cluster data"
fi

echo ""
echo "4️⃣ Testing Risk Metrics Calculation"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
if echo "$RESPONSE" | python -c "import sys, json; data=json.load(sys.stdin); print('✅ Risk Metrics: SUCCESS' if data.get('metrics', {}).get('volatility') else '❌ Risk: FAILED')" 2>/dev/null; then
  echo "$RESPONSE" | python -c "
import sys, json
data = json.load(sys.stdin)
metrics = data.get('metrics', {})
print(f'   Volatility: {metrics.get(\"volatility\", 0):.4%}')
print(f'   VaR (95%): {metrics.get(\"var\", 0):.6f}')
print(f'   CVaR (95%): {metrics.get(\"cvar\", 0):.6f}')
print(f'   Max Drawdown: {metrics.get(\"max_drawdown\", 0):.4%}')
" 2>/dev/null
fi

echo ""
echo "5️⃣ Testing Diversification Metrics"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
if echo "$RESPONSE" | grep -q "diversification"; then
  echo "✅ Diversification: SUCCESS"
  echo "$RESPONSE" | python -c "
import sys, json
data = json.load(sys.stdin)
div = data.get('diversification', {})
print(f'   ENB: {div.get(\"enb\", 0):.2f}')
print(f'   Diversification Score: {div.get(\"diversification_score\", 0):.4f}')
" 2>/dev/null
else
  echo "❌ Diversification: FAILED"
fi

echo ""
echo "6️⃣ Testing Stress Test"
echo "━━━━━━━━━━━━━━━━━━━━"
if echo "$RESPONSE" | grep -q "stressed_var"; then
  echo "✅ Stress Test: SUCCESS"
  echo "$RESPONSE" | python -c "
import sys, json
data = json.load(sys.stdin)
stress = data.get('stress', {})
print(f'   Normal VaR: {stress.get(\"normal_var\", 0):.6f}')
print(f'   Stressed VaR: {stress.get(\"stressed_var\", 0):.6f}')
print(f'   Impact: {(stress.get(\"stressed_var\", 0) - stress.get(\"normal_var\", 0)) / max(stress.get(\"normal_var\", 1), 0.0001):.2%}')
" 2>/dev/null
else
  echo "❌ Stress Test: FAILED"
fi

echo ""
echo "7️⃣ Testing High Correlation Detection"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
if echo "$RESPONSE" | grep -q "high_correlation_pairs"; then
  PAIRS=$(echo "$RESPONSE" | python -c "import sys, json; data=json.load(sys.stdin); print(len(data.get('high_correlation_pairs', [])))" 2>/dev/null)
  echo "✅ High Correlation: SUCCESS - $PAIRS pairs found"
else
  echo "ℹ️  High Correlation: No pairs with correlation > 0.7"
fi

echo ""
echo "8️⃣ Testing AI Explanation Service"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
if echo "$RESPONSE" | grep -q "ai_explanation"; then
  AI_MSG=$(echo "$RESPONSE" | python -c "import sys, json; data=json.load(sys.stdin); msg=data.get('ai_explanation', ''); print(msg[:60]+'...' if len(msg)>60 else msg)" 2>/dev/null)
  if [[ "$AI_MSG" == *"unavailable"* ]]; then
    echo "ℹ️  AI Explanation: API key not configured (expected if GROQ_API_KEY not set)"
  else
    echo "✅ AI Explanation: SUCCESS"
    echo "   Message: $AI_MSG"
  fi
else
  echo "❌ AI Explanation: FAILED"
fi

echo ""
echo "═════════════════════════════════════"
echo "✅ API TESTING COMPLETE"
echo "═════════════════════════════════════"

