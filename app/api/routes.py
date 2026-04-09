"""API routes for portfolio operations."""

from fastapi import APIRouter, HTTPException, status

from app.models.portfolio import PortfolioRequest
from app.services.ai_service import generate_portfolio_explanation
from app.services.clustering_service import perform_clustering
from app.services.correlation_service import (
    compute_correlation_matrix,
    get_high_correlation_pairs,
)
from app.services.data_service import calculate_returns, get_historical_prices
from app.services.diversification_service import (
    calculate_cluster_concentration,
    calculate_diversification_score,
    calculate_enb,
)
from app.services.portfolio_service import validate_portfolio
from app.services.risk_service import (
    calculate_cvar,
    calculate_drawdown,
    calculate_portfolio_returns,
    calculate_var,
    calculate_volatility,
)
from app.services.stress_service import (
    apply_correlation_stress,
    apply_joint_stress,
)

router = APIRouter()


@router.post("/portfolio")
def create_portfolio(portfolio: PortfolioRequest) -> dict[str, object]:
    """Accept and validate a portfolio payload."""
    try:
        validated = validate_portfolio(portfolio)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc

    tickers = [asset.ticker for asset in validated.assets]
    weights = [asset.weight for asset in validated.assets]
    weights_map = {asset.ticker: asset.weight for asset in validated.assets}

    try:
        price_df = get_historical_prices(tickers)
        returns_df = calculate_returns(price_df)
        corr_matrix = compute_correlation_matrix(returns_df)
        high_corr_pairs = get_high_correlation_pairs(corr_matrix, threshold=0.7)
        clusters = perform_clustering(corr_matrix)
        portfolio_returns = calculate_portfolio_returns(returns_df, weights)
        volatility = calculate_volatility(portfolio_returns)
        var_95 = calculate_var(portfolio_returns, confidence=0.95)
        cvar_95 = calculate_cvar(portfolio_returns, confidence=0.95)
        max_drawdown = calculate_drawdown(portfolio_returns)
        stressed_corr_matrix = apply_correlation_stress(corr_matrix)
        stressed_returns_df = apply_joint_stress(returns_df, stressed_corr_matrix)
        stressed_portfolio_returns = calculate_portfolio_returns(stressed_returns_df, weights)
        stressed_var_95 = calculate_var(stressed_portfolio_returns, confidence=0.95)
        stressed_cvar_95 = calculate_cvar(stressed_portfolio_returns, confidence=0.95)
        enb = calculate_enb(weights)
        cluster_concentration = calculate_cluster_concentration(clusters, weights_map)
        diversification_score = calculate_diversification_score(enb, len(tickers))
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc
    except RuntimeError as exc:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=str(exc),
        ) from exc

    print("Price data preview:")
    print(price_df.head().to_string())
    print("Returns data preview:")
    print(returns_df.head().to_string())
    print("Correlation matrix preview:")
    print(corr_matrix.head().to_string())
    print("Distance matrix preview:")
    print((1.0 - corr_matrix).head().to_string())
    print("High correlation pairs:")
    print(high_corr_pairs)
    print("Cluster assignments:")
    print(clusters)
    print("Portfolio returns head:")
    print(portfolio_returns.head().to_string())
    print("Volatility:")
    print(volatility)
    print("VaR 95:")
    print(var_95)
    print("CVaR 95:")
    print(cvar_95)
    print("Max drawdown:")
    print(max_drawdown)
    print("Stressed returns head:")
    print(stressed_returns_df.head().to_string())
    print("Normal vs stressed VaR/CVaR:")
    print(
        {
            "normal_var": var_95,
            "stressed_var": stressed_var_95,
            "normal_cvar": cvar_95,
            "stressed_cvar": stressed_cvar_95,
        }
    )
    print("ENB value:")
    print(enb)
    print("Cluster weights:")
    print(cluster_concentration)

    llm_input = {
        "volatility": volatility,
        "var": var_95,
        "cvar": cvar_95,
        "max_drawdown": max_drawdown,
        "clusters": {str(cluster_id): members for cluster_id, members in clusters.items()},
        "enb": enb,
        "diversification_score": diversification_score,
        "stress": {
            "normal_var": var_95,
            "stressed_var": stressed_var_95,
            "normal_cvar": cvar_95,
            "stressed_cvar": stressed_cvar_95,
        },
    }
    ai_explanation = generate_portfolio_explanation(llm_input)
    print("Input sent to Groq:")
    print(llm_input)
    print("Raw Groq LLM response:")
    print(ai_explanation)

    return {
        "message": "Analysis complete",
        "metrics": {
            "volatility": round(volatility, 6),
            "var": round(var_95, 6),
            "cvar": round(cvar_95, 6),
            "max_drawdown": round(max_drawdown, 6),
        },
        "clusters": {str(cluster_id): members for cluster_id, members in clusters.items()},
        "high_correlation_pairs": high_corr_pairs,
        "correlation_matrix": corr_matrix.to_dict(),
        "assets": [{"ticker": ticker, "weight": weight} for ticker, weight in weights_map.items()],
        "diversification": {
            "enb": round(enb, 6),
            "diversification_score": round(diversification_score, 6),
            "cluster_concentration": cluster_concentration,
        },
        "stress": {
            "normal_var": round(var_95, 6),
            "stressed_var": round(stressed_var_95, 6),
            "normal_cvar": round(cvar_95, 6),
            "stressed_cvar": round(stressed_cvar_95, 6),
        },
        "ai_explanation": ai_explanation,
    }
