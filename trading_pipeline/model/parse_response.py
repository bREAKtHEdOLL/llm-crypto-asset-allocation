import re

def parse_model_response(response_text: str) -> dict:
    """
    Extracts allocation scores for 5 tokens from LLM-generated text.

    Args: 
        response_text
    
    Returns: 
        A DICTIONARY with allocation scores for each token.
        e.g. {"BTC": 0.6, "ETH": -0.2, "SOL": 0.0, "DOGE": 0.1, "USDT": -0.5}
        Any missing asset will default to 0.0 (neutral signal).
    """
    assets = ["BTC", "ETH", "SOL", "DOGE", "USDT"]
    scores = {}

    # Regex pattern: Matches lines like "BTC: +0.5" or "DOGE : -0.3" or "ETH:+1.0"
    pattern = r"(\bBTC|\bETH|\bSOL|\bDOGE|\bUSDT)\s*:\s*([-+]?[0-9]+(?:\.[0-9]+)?)"

    matches = re.findall(pattern, response_text)  # 返回的是list of tuples: e.g. [('BTC', '+0.8'), ('ETH', '-0.1'), ('DOGE', '0.0')]...

    for asset, score_str in matches:
        try:
            scores[asset] = float(score_str)
        except ValueError:
            continue
    
    # Fill in 0.0 for any asset not mentioned in the response
    for asset in assets:
        if asset not in scores:
            scores[asset] = 0.0
    
    return scores