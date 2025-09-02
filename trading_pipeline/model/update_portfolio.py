def update_portfolio(current_portfolio: dict, scores: dict, prices: dict, max_buy_ratio: float=0.1, sell_strength: float = 0.25) -> dict:
    """
    Update the portfolio allocation based on model scores and current prices.

    Args:
        current_portfolio (dict): Holdings in units, e.g. {"BTC": 0.3, "ETH": 1.2, ...}
        scores (dict): Model-generated allocation scores in [-1.0, 1.0] per token
        prices (dict): Current token prices in USD per unit
        max_buy_ratio (float): Max% of total portfolio value to reallocate this hour (buy tokens) (每小时可以用来买入的资金最多是总资产的10%)
        sell_strength (float): Percentage of holdings to sell per unit of negative score
    
    Returns:
        dict: Updated portfolio (new quantites per asset)
    """
    updated_portfolio = current_portfolio.copy()
    tokens = ["BTC", "ETH", "SOL", "DOGE", "USDT"]

    # 1. Reduce holdings for negative scores (if we hold any)
    for token, score in scores.items():
        if token == ["USDT"]:
            continue   
        if score < 0 and updated_portfolio[token] > 0:
            sell_ratio = sell_strength * abs(score)   # Calculate how much to sell based on score and sell_strength
            quantity_to_sell = updated_portfolio[token] * sell_ratio    # Sell a portion of that token
            updated_portfolio[token] -= quantity_to_sell    # Reduce holdings for sold token
            updated_portfolio["USDT"] += (quantity_to_sell * prices[token]) / prices["USDT"]  # Add USDT from sale

    # 2. Compute total current portfolio value (in USD)
    total_current_value = sum(updated_portfolio[token] * prices[token] for token in tokens)

    # 3. Compute max USD capital to buy this hour
    max_capital_to_buy = total_current_value * max_buy_ratio    # ***

    # 4. Positive scores -> buy new capital proportianlly
    positive_scores = {token: score for token, score in scores.items() if score > 0}
    total_score_positive = sum(positive_scores.values())

    if total_score_positive > 0:
        weights = {token: score / total_score_positive for token, score in positive_scores.items()}
        target_usd_allocation = {token: max_capital_to_buy * weight for token, weight in weights.items()}
        total_needed_usdt_value = sum(target_usd_allocation.values())
        available_usdt_value = updated_portfolio["USDT"] * prices["USDT"]

        # Scale = 1.o if enough USDT, otherwise scale down proportionally
        scale = min(1.0, available_usdt_value / total_needed_usdt_value) if total_needed_usdt_value > 0 else 0.0

        for token, target_value in target_usd_allocation.items():
            adjusted_target_value = target_value * scale
            units_to_buy = adjusted_target_value / prices[token]  # Purchase assets (using USDT)
            updated_portfolio[token] += units_to_buy    
            updated_portfolio["USDT"] -= adjusted_target_value / prices["USDT"]    # Deduct USDT used for purchase
            updated_portfolio["USDT"] = max(updated_portfolio["USDT"], 0)    # Ensure USDT doesn't go negative
    
    return updated_portfolio