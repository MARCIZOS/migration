"""AI explanation service powered by Groq."""

import json
import os

from groq import Groq

DEFAULT_GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.1-8b-instant")
REQUEST_TIMEOUT_SECONDS = 20


def _build_prompt(data: dict) -> str:
    """Build a concise structured prompt for risk explanation."""
    return (
        "You are a financial risk analyst.\n"
        "Explain the portfolio risk in simple terms for a non-technical investor.\n"
        "Include: diversification quality, risk concentration, stress vulnerability, and downside risk.\n"
        "Avoid technical jargon and keep the explanation practical and concise (120-180 words).\n\n"
        f"Portfolio analysis data:\n{json.dumps(data, indent=2)}"
    )


def generate_portfolio_explanation(data: dict) -> str:
    """Generate human-readable explanation using Groq chat completion API."""
    api_key = os.getenv("GROQ_API_KEY")
    
    if not api_key:
        print("[WARN] GROQ_API_KEY not found in environment variables")
        return (
            "AI explanation unavailable: GROQ_API_KEY is not configured. "
            "Set the key in .env file to enable generated insights."
        )

    try:
        print(f"[OK] Groq API Key found (length: {len(api_key)} chars)")
        print(f"[OK] Using model: {DEFAULT_GROQ_MODEL}")
        
        client = Groq(api_key=api_key, timeout=REQUEST_TIMEOUT_SECONDS)
        
        print("[OK] Groq client initialized")
        print("[OK] Calling Groq API...")
        
        response = client.chat.completions.create(
            model=DEFAULT_GROQ_MODEL,
            messages=[
                {"role": "system", "content": "You produce clear and accurate financial explanations."},
                {"role": "user", "content": _build_prompt(data)},
            ],
            temperature=0.2,
        )
        
        print("[OK] Groq API response received")
        
        content = response.choices[0].message.content
        if not content:
            print("[WARN] WARNING: Empty response from Groq model")
            return "AI explanation unavailable: empty response from Groq model."
        
        print(f"[OK] AI explanation generated ({len(content)} chars)")
        return content.strip()
        
    except TimeoutError as exc:
        error_msg = f"AI explanation unavailable: Groq API timeout ({REQUEST_TIMEOUT_SECONDS}s)"
        print(f"[ERR] {error_msg}")
        return error_msg
    except Exception as exc:
        error_msg = f"AI explanation unavailable due to Groq API error: {str(exc)}"
        print(f"[ERR] {error_msg}")
        return error_msg
