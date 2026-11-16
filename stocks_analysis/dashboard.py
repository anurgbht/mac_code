"""Part 2: live portfolio monitor.

Reads processed/portfolio.json (made by ingest.py) and shows, per stock, what the
price is doing right now and what that means for your holding. Prices come from
Yahoo Finance (NSE symbols -> SYMBOL.NS); they refresh automatically.

Run:  uv run streamlit run dashboard.py
"""

from __future__ import annotations

import json
import warnings
from datetime import datetime, time
from pathlib import Path
from zoneinfo import ZoneInfo

import pandas as pd
import plotly.graph_objects as go
import streamlit as st
import yfinance as yf

import ingest

warnings.filterwarnings("ignore", category=FutureWarning)

HERE = Path(__file__).resolve().parent
PORTFOLIO = HERE / "processed" / "portfolio.json"
IST = ZoneInfo("Asia/Kolkata")

# Palette (validated dataviz defaults). Gain/loss always also carries a +/- sign.
GAIN, LOSS, NEUTRAL = "#0ca30c", "#d03b3b", "#898781"
SERIES = "#2a78d6"
COST_LINE = "#eb6834"

st.set_page_config(page_title="Portfolio Monitor", page_icon="📈", layout="wide")


# ----------------------------------------------------------------------------- data
def yahoo_ticker(symbol: str, exchange: str) -> str:
    return f"{symbol}.BO" if exchange.upper() == "BSE" else f"{symbol}.NS"


@st.cache_data(show_spinner=False)
def load_portfolio(path: str, mtime: float) -> dict:  # mtime busts the cache when the file changes
    return json.loads(Path(path).read_text())


def _by_ticker(df: pd.DataFrame, tickers: list[str], field: str) -> pd.DataFrame:
    if isinstance(df.columns, pd.MultiIndex):
        return df[field].reindex(columns=tickers)
    return df[[field]].set_axis(tickers, axis=1)


@st.cache_data(ttl=20, show_spinner=False)
def fetch_quotes(tickers: tuple[str, ...]) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Returns (quotes, intraday). quotes: ltp, prev_close, day_high, day_low, as_of per ticker."""
    t = list(tickers)
    daily = yf.download(t, period="7d", interval="1d", progress=False, auto_adjust=False, threads=True)
    intra = yf.download(t, period="1d", interval="5m", progress=False, auto_adjust=False, threads=True)
    closes = _by_ticker(daily, t, "Close")
    highs, lows = _by_ticker(daily, t, "High"), _by_ticker(daily, t, "Low")
    iclose = _by_ticker(intra, t, "Close") if not intra.empty else pd.DataFrame(columns=t)

    rows = {}
    for tk in t:
        c = closes[tk].dropna()
        if c.empty:
            rows[tk] = {}
            continue
        ic = iclose[tk].dropna() if tk in iclose else pd.Series(dtype=float)
        ltp = float(ic.iloc[-1]) if not ic.empty else float(c.iloc[-1])
        as_of = ic.index[-1] if not ic.empty else c.index[-1]
        rows[tk] = {
            "ltp": ltp,
            "prev_close": float(c.iloc[-2]) if len(c) > 1 else float("nan"),
            "day_high": float(highs[tk].dropna().iloc[-1]),
            "day_low": float(lows[tk].dropna().iloc[-1]),
            "as_of": pd.Timestamp(as_of).tz_convert(IST) if pd.Timestamp(as_of).tzinfo else pd.Timestamp(as_of),
        }
    return pd.DataFrame(rows).T, iclose


@st.cache_data(ttl=3600, show_spinner=False)
def fetch_history(ticker: str, period: str) -> pd.Series:
    h = yf.download(ticker, period=period, interval="1d", progress=False, auto_adjust=False)
    return _by_ticker(h, [ticker], "Close")[ticker].dropna()


def market_status(now: datetime) -> tuple[bool, str]:
    is_open = now.weekday() < 5 and time(9, 15) <= now.time() <= time(15, 30)
    return is_open, ("NSE open" if is_open else "NSE closed · showing last traded prices")


# ----------------------------------------------------------------------------- formatting
def inr(x: float, signed: bool = False) -> str:
    if pd.isna(x):
        return "—"
    sign = ("+" if x > 0 else "−" if x < 0 else "") if signed else ("−" if x < 0 else "")
    return f"{sign}₹{abs(x):,.0f}"


def inr_short(x: float, signed: bool = False) -> str:
    """Compact Indian units for headline tiles: ₹4.26L, ₹1.2Cr."""
    a = abs(x)
    body = (f"{a / 1e7:.2f}Cr" if a >= 1e7 else f"{a / 1e5:.2f}L" if a >= 1e5
            else f"{a / 1e3:.1f}K" if a >= 1e4 else f"{a:,.0f}")
    sign = ("+" if x > 0 else "−" if x < 0 else "") if signed else ("−" if x < 0 else "")
    return f"{sign}₹{body}"


def pct(x: float) -> str:
    if pd.isna(x):
        return "—"
    return f"{'+' if x > 0 else '−' if x < 0 else ''}{abs(x):.2f}%"


def polarity_color(v):
    if pd.isna(v) or v == 0:
        return f"color: {NEUTRAL}"
    return f"color: {GAIN if v > 0 else LOSS}; font-weight: 600"


def diverging_bar(df: pd.DataFrame, value: str, label_fmt, title: str) -> go.Figure:
    d = df.sort_values(value)
    lo, hi = min(d[value].min(), 0), max(d[value].max(), 0)
    pad = (hi - lo) * 0.3 or 1  # room for the outside labels on both sides
    fig = go.Figure(go.Bar(
        x=d[value], y=d["Stock"], orientation="h",
        marker=dict(color=[GAIN if v >= 0 else LOSS for v in d[value]], cornerradius=4),
        text=[label_fmt(v) for v in d[value]], textposition="outside", cliponaxis=False,
        hovertemplate="%{y}: %{text}<extra></extra>",
    ))
    fig.update_layout(
        title=dict(text=title, font=dict(size=14)), height=60 + 44 * len(d),
        margin=dict(l=10, r=60, t=40, b=10), bargap=0.35, showlegend=False,
        xaxis=dict(zeroline=True, zerolinecolor="#c3c2b7", showgrid=False, showticklabels=False,
                   range=[lo - (pad if lo < 0 else 0), hi + (pad if hi > 0 else 0)]),
        yaxis=dict(showgrid=False, ticksuffix="  "),
    )
    return fig


# ----------------------------------------------------------------------------- sidebar
with st.sidebar:
    st.header("Settings")
    refresh = st.select_slider("Refresh every", options=[15, 30, 60, 120, 300], value=60,
                               format_func=lambda s: f"{s}s" if s < 60 else f"{s // 60} min")
    if st.button("Re-ingest data folder", width="stretch"):
        with st.spinner("Reading Excel files…"):
            ingest.ingest(HERE / "data", HERE / "processed")
        st.success("Portfolio rebuilt")
    st.caption("Add a broker export to `data/` named `<NSE_SYMBOL>_Transaction_History_….xlsx`, "
               "then re-ingest.")

if not PORTFOLIO.exists():
    st.warning("No processed portfolio yet. Run `uv run python ingest.py` or use **Re-ingest** in the sidebar.")
    st.stop()

portfolio = load_portfolio(str(PORTFOLIO), PORTFOLIO.stat().st_mtime)
holdings = pd.DataFrame([h for h in portfolio["holdings"] if h["qty"] > 0])
if holdings.empty:
    st.info("No open positions in the portfolio.")
    st.stop()
holdings["ticker"] = [yahoo_ticker(s, e) for s, e in zip(holdings.symbol, holdings.exchange)]

for h in portfolio["holdings"]:
    for w in h.get("warnings", []):
        st.sidebar.warning(f"{h['symbol']}: {w}")

st.title("Portfolio monitor")


# ----------------------------------------------------------------------------- live section
@st.fragment(run_every=refresh)
def live() -> None:
    now = datetime.now(IST)
    is_open, status = market_status(now)
    try:
        quotes, intraday = fetch_quotes(tuple(holdings.ticker))
    except Exception as e:  # network / Yahoo hiccup: keep the page alive and retry next tick
        st.error(f"Couldn't fetch prices: {e}")
        return

    df = holdings.join(quotes, on="ticker")
    missing = df[df["ltp"].isna()].symbol.tolist()
    if missing:
        st.warning(f"No price data for: {', '.join(missing)} — check the symbol in the filename.")
    df["ltp"] = df["ltp"].astype(float)
    df["prev_close"] = df["prev_close"].astype(float)
    df["value"] = df.qty * df.ltp
    df["day_chg_pct"] = (df.ltp / df.prev_close - 1) * 100
    df["day_pnl"] = df.qty * (df.ltp - df.prev_close)
    df["unreal"] = df.value - df.invested
    df["unreal_pct"] = df.unreal / df.invested * 100
    df["total_ret"] = df.unreal + df.dividends + df.realised_pnl
    df["weight"] = df.value / df.value.sum() * 100

    as_of = pd.to_datetime(df["as_of"].dropna()).max()
    dot = "🟢" if is_open else "⚪"
    st.caption(f"{dot} {status} · prices as of {as_of:%d %b %Y, %H:%M} IST · "
               f"refreshed {now:%H:%M:%S} · next refresh in {refresh}s")

    # KPI row
    invested, value = df.invested.sum(), df.value.sum()
    unreal, day = value - invested, df.day_pnl.sum()
    prev_value = (df.qty * df.prev_close).sum()
    divs = df.dividends.sum()
    k = st.columns(5)
    k[0].metric("Current value", inr_short(value), help=inr(value))
    k[1].metric("Invested", inr_short(invested), help=inr(invested))
    k[2].metric("Unrealised P&L", inr_short(unreal, True), f"{unreal / invested * 100:+.2f}%", help=inr(unreal, True))
    k[3].metric("Today", inr_short(day, True), f"{day / prev_value * 100:+.2f}%", help=inr(day, True))
    k[4].metric("Dividends", inr_short(divs), f"Total {pct((unreal + divs) / invested * 100)}",
                delta_color="off", help="Total return = unrealised P&L + dividends, on cost")

    # Holdings table
    spark = {tk: intraday[tk].dropna().round(2).tolist() if tk in intraday else []
             for tk in df.ticker}
    table = pd.DataFrame({
        "Stock": df.symbol,
        "Today": [spark[t] for t in df.ticker],
        "LTP": df.ltp,
        "Day %": df.day_chg_pct,
        "Day P&L": df.day_pnl,
        "Qty": df.qty,
        "Avg cost": df.avg_cost,
        "Invested": df.invested,
        "Value": df.value,
        "P&L": df.unreal,
        "P&L %": df.unreal_pct,
        "Dividends": df.dividends,
        "Weight %": df.weight,
    }).sort_values("Value", ascending=False)

    styled = (table.style
              .map(polarity_color, subset=["Day %", "Day P&L", "P&L", "P&L %"])
              .format({"LTP": "₹{:,.2f}", "Avg cost": "₹{:,.2f}", "Qty": "{:,.0f}",
                       "Day %": pct, "P&L %": pct, "Weight %": "{:.1f}%",
                       "Day P&L": lambda v: inr(v, True), "P&L": lambda v: inr(v, True),
                       "Invested": inr, "Value": inr, "Dividends": inr}))
    st.dataframe(
        styled, hide_index=True, width="stretch",
        column_config={"Today": st.column_config.LineChartColumn("Today", width="small")},
    )

    # Charts
    chart_df = df.rename(columns={"symbol": "Stock"})
    c1, c2 = st.columns(2)
    c1.plotly_chart(diverging_bar(chart_df, "day_chg_pct", pct, "Today's move"),
                    width="stretch", config={"displayModeBar": False})
    c2.plotly_chart(diverging_bar(chart_df, "unreal_pct", pct, "Unrealised return on cost"),
                    width="stretch", config={"displayModeBar": False})


live()


# ----------------------------------------------------------------------------- stock detail
st.subheader("Stock detail")
d1, d2 = st.columns([3, 1])
sym = d1.selectbox("Stock", holdings.symbol.tolist(), label_visibility="collapsed")
period = d2.segmented_control("Range", ["1mo", "6mo", "1y", "2y", "5y"], default="1y",
                              label_visibility="collapsed") or "1y"
h = holdings.set_index("symbol").loc[sym]
hist = fetch_history(h.ticker, period)

fig = go.Figure()
fig.add_trace(go.Scatter(x=hist.index, y=hist.values, mode="lines", name=sym,
                         line=dict(color=SERIES, width=2),
                         hovertemplate="%{x|%d %b %Y}<br>₹%{y:,.2f}<extra></extra>"))
fig.add_hline(y=h.avg_cost, line=dict(color=COST_LINE, width=2, dash="dash"),
              annotation_text=f"Your avg cost ₹{h.avg_cost:,.2f}", annotation_position="top left")
fig.update_layout(height=380, margin=dict(l=10, r=10, t=10, b=10), hovermode="x unified",
                  showlegend=False, yaxis=dict(tickprefix="₹", gridcolor="rgba(137,135,129,0.2)"),
                  xaxis=dict(showgrid=False))
st.plotly_chart(fig, width="stretch", config={"displayModeBar": False})
st.caption("Prices are adjusted by Yahoo for splits and bonuses, and so is your average cost, "
           "so the two lines are comparable.")

lots = next(x for x in portfolio["holdings"] if x["symbol"] == sym)["lots"]
with st.expander(f"Open lots for {sym} (FIFO, cost includes charges)"):
    st.dataframe(pd.DataFrame(lots).assign(cost_per_share=lambda d: (d.cost / d.qty).round(2)),
                 hide_index=True, width="stretch")

st.caption(f"Portfolio built {portfolio['generated_at']} from {len(portfolio['source_files'])} file(s). "
           "Prices from Yahoo Finance; may be delayed.")
