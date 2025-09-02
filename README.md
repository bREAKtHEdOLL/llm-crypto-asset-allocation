# llm-crypto-asset-allocation
This repo contains the data and code for my Master's Thesis *LLM-Driven Portfolio Management in Cryptocurrency Markets*. It covers everything from data collection to prompt construction and portfolio backtesting, showcasing how LLMs can be applied to crypto asset allocation. 

## Abstract
Recent advances in large language models (LLMs) have opened new opportunities for financial decision-making. Their ability to combine diverse data and reason across contexts makes them suitable for complex financial tasks. In this work, we investigate their role in dynamic asset allocation for cryptocurrency portfolios. Such markets are marked by high volatility, continuous trading, and diverse information sources. Building on insights from agent-based frameworks, we design a system that integrates market data, on-chain statistics, macroeconomic factors, and news summaries into structured prompts, which guide an LLM to generate hourly allocation scores. These scores are translated into portfolio weight and used to update the portfolio over time. To evaluate performance, we benchmark against naive strategies such as random and uniform allocation, as well as classical baselines including momentum trading. Experiments across bullish, bearish, and sideways regimes show that our approach achieves up to six times the return compared to baseline methods, while also achieving the lowest volatility across most benchmarks and cutting max drawdowns by more than 75% during bearish periods relative to uniform allocation baselines. Our findings highlight the potential of LLM-based agents to reason across heterogeneous information and adapt allocation strategies to shifting market conditions.

## Repository Structure
- `data_pipeline/` – Data collection and preprocessing
  - `coindesk_price_volume/` – Raw price and volume data from CoinDesk
  - `technical_indicators/` – Computation of TA features (MA, MACD, BB, etc.)
  - `formatting_for_prompting/` – Converting signals into textual descriptions
  - `final_merge/` – Merging market, on-chain, technical features, and news data together

- `trading_pipeline/` – Prompt construction, model inference, portfolio simulation, and evaluation process
  - `prompts/` – Hourly prompts used in experiments (bullish, bearish, sideways)
  - `model/` – Querying the LLM, parsing responses, updating portfolios
  - `evaluation/` – Evaluation metrics and visualization of performance
