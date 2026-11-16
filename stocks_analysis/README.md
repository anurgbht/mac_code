# Stocks analysis

Two steps, both run with [uv](https://docs.astral.sh/uv/):

1. **Ingest:** reads every broker export in `data/` and writes `processed/transactions.csv`,
   `processed/holdings.csv` and `processed/portfolio.json`. Handles buys, sells (FIFO),
   dividends, splits, bonuses and consolidations.

   ```bash
   uv run python ingest.py
   ```

2. **Monitor:** a live dashboard with NSE prices via Yahoo Finance (auto-refreshes).

   ```bash
   uv run streamlit run dashboard.py
   ```

The broker export doesn't name the stock, so each file's name must start with its NSE symbol:
`BAJFINANCE_Transaction_History_6677164_2026-11-16.xlsx`. To add a stock, drop its export into `data/`
and re-run ingest (or click **Re-ingest** in the dashboard sidebar).
