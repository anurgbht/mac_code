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
TRANSACTIONS = HERE / "processed" / "transactions.csv"
IST = ZoneInfo("Asia/Kolkata")

# Palette (validated dataviz defaults). Gain/loss always also carries a +/- sign.
GAIN, LOSS, NEUTRAL = "#0ca30c", "#d03b3b", "#898781"
SERIES = "#2a78d6"
COST_LINE = "#eb6834"
# Event markers (categorical slots, fixed per event type)
EVENT_STYLE = {
    "BUY": dict(color="#6250d6", symbol="triangle-up", size=13, label="Buy"),
    "SELL": dict(color="#e87ba4", symbol="triangle-down", size=13, label="Sell"),
    "DIVIDEND": dict(color="#1baf7a", symbol="circle", size=8, label="Dividend"),
    "SHARE_ADJUSTMENT": dict(color="#eda100", symbol="diamond", size=10, label="Split / bonus"),
    "DEMERGER_IN": dict(color="#eda100", symbol="star", size=12, label="Demerger"),
    "DEMERGER_OUT": dict(color="#eda100", symbol="star", size=12, label="Demerger"),
}

st.set_page_config(page_title="Portfolio Monitor", page_icon="📈", layout="wide",
                   initial_sidebar_state="collapsed")


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
def fetch_history(ticker: str, period: str | None = None, start: str | None = None) -> pd.Series:
    when = {"start": start} if start else {"period": period}
    h = yf.download(ticker, interval="1d", progress=False, auto_adjust=False, **when)
    return _by_ticker(h, [ticker], "Close")[ticker].dropna()


@st.cache_data(show_spinner=False)
def load_transactions(path: str, mtime: float) -> pd.DataFrame:
    return pd.read_csv(path, parse_dates=["date"])


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
    labels = [label_fmt(v) for v in d[value]]
    fig = go.Figure(go.Bar(
        x=d[value], y=d["Stock"], orientation="h",
        marker=dict(color=[GAIN if v >= 0 else LOSS for v in d[value]], cornerradius=4),
        text=labels, textposition="none", hovertemplate="%{y}: %{text}<extra></extra>",
    ))
    # Value label sits on the far side of the zero line from its bar, so it never
    # collides with the bar or with the stock name, however narrow the chart gets.
    for stock, v, lab in zip(d["Stock"], d[value], labels):
        fig.add_annotation(x=0, y=stock, text=lab, showarrow=False, font=dict(size=11),
                           xanchor="right" if v >= 0 else "left", xshift=-4 if v >= 0 else 4)
    lo, hi = min(d[value].min(), 0), max(d[value].max(), 0)
    pad = (hi - lo) * 0.35 or 1  # room for the labels on the empty side of zero
    fig.update_layout(
        title=dict(text=title, font=dict(size=14)), height=60 + 44 * len(d),
        margin=dict(l=10, r=10, t=40, b=10), bargap=0.35, showlegend=False,
        xaxis=dict(zeroline=True, zerolinecolor="#c3c2b7", showgrid=False, showticklabels=False,
                   range=[min(lo, -pad), max(hi, pad)]),
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
    df["ltp"] = df["ltp"].astype(float)
    df["prev_close"] = df["prev_close"].astype(float)
    no_price = df["ltp"].isna()
    if no_price.any():
        # Unlisted holdings / bad symbols: value at cost and keep them out of today's move,
        # so they don't distort the portfolio totals.
        df.loc[no_price, "ltp"] = df.loc[no_price, "avg_cost"]
        df.loc[no_price, "prev_close"] = df.loc[no_price, "avg_cost"]
        st.info(f"No market price for {', '.join(df[no_price].symbol)} (unlisted, or check the "
                "symbol in the filename). Valued at cost and marked with * below.")
        df.loc[no_price, "symbol"] = df.loc[no_price, "symbol"] + " *"
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
        styled, hide_index=True, width="stretch", height=35 * (len(table) + 1) + 3,  # no inner scroll
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
d1, d2 = st.columns([2, 2])
sym = d1.selectbox("Stock", holdings.symbol.tolist(), label_visibility="collapsed")
RANGES = ["Since 1st buy", "1mo", "6mo", "1y", "2y", "5y"]
period = d2.segmented_control("Range", RANGES, default=RANGES[0], label_visibility="collapsed") or RANGES[0]
h = holdings.set_index("symbol").loc[sym]
if period == RANGES[0]:
    hist = fetch_history(h.ticker, start=(pd.Timestamp(h.first_buy) - pd.Timedelta(days=30)).date().isoformat())
else:
    hist = fetch_history(h.ticker, period=period)

tx = load_transactions(str(TRANSACTIONS), TRANSACTIONS.stat().st_mtime) if TRANSACTIONS.exists() else pd.DataFrame()
if tx.empty:
    ev = pd.DataFrame(columns=["date", "kind"])
else:
    if "related_symbol" not in tx:
        tx["related_symbol"] = ""
    ev = tx[tx.symbol == sym].copy()
    ev.loc[ev.kind == "DEMERGER", "kind"] = "DEMERGER_IN"  # shares received from a parent
    spun_off = tx[(tx.kind == "DEMERGER") & (tx.related_symbol == sym)].assign(kind="DEMERGER_OUT")
    ev = pd.concat([ev, spun_off], ignore_index=True)
hist.index = pd.to_datetime(hist.index).tz_localize(None)
ev = (ev[(ev.date >= hist.index[0] - pd.Timedelta(days=60)) & (ev.date <= hist.index[-1])]
      if not hist.empty else ev.iloc[0:0])

# Yahoo prices are split-adjusted, so scale the per-share price of each past trade by
# every split/bonus that happened after it, to place it on the same scale as the chart.
adjustments = tx[(tx.symbol == sym) & (tx.kind == "SHARE_ADJUSTMENT")] if not tx.empty else pd.DataFrame()


def later_factor(d: pd.Timestamp) -> float:
    return float(adjustments.loc[adjustments.date > d, "share_factor"].prod()) if len(adjustments) else 1.0


def short_remark(r: str) -> str:
    import re
    return re.sub(r"\s*(applied )?on Ex-Date:\s*\S+", "", str(r)).strip()


def event_hover(kind: str, g: pd.DataFrame) -> str:
    d = g.date.iloc[0]
    if kind in ("BUY", "SELL"):
        qty = g.qty.sum()
        px = (g.qty * g.price).sum() / qty
        verb = "Bought" if kind == "BUY" else "Sold"
        f = later_factor(d)
        adj = f"<br>= ₹{px / f:,.2f} split-adjusted ({qty * f:g} shares today)" if f != 1 else ""
        return f"<b>{verb} {qty:g} @ ₹{px:,.2f}</b>{adj}"
    if kind == "DIVIDEND":
        return (f"<b>Dividend ₹{g.dividend_per_share.sum():g}/share</b>"
                f"<br>₹{g.value.sum():,.0f} received on {g.qty.iloc[0]:g} shares")
    if kind == "DEMERGER_IN":
        r = g.iloc[0]
        return (f"<b>Received {r.qty:g} shares via demerger from {r.related_symbol}</b>"
                f"<br>Cost carried over ₹{r.value:,.2f} (₹{r.price:,.2f}/share)")
    if kind == "DEMERGER_OUT":
        r = g.iloc[0]
        return (f"<b>Demerged {r.symbol}: received {r.qty:g} shares</b>"
                f"<br>₹{r.value:,.2f} of your cost moved to {r.symbol}")
    return f"<b>{' + '.join(short_remark(r) for r in g.remarks)}</b><br>×{g.share_factor.prod():g} shares"


fig = go.Figure()
fig.add_trace(go.Scatter(x=hist.index, y=hist.values, mode="lines", name=sym, showlegend=False,
                         line=dict(color=SERIES, width=2), hovertemplate="₹%{y:,.2f}<extra></extra>"))
fig.add_hline(y=h.avg_cost, line=dict(color=COST_LINE, width=2, dash="dash"),
              annotation_text=f"Your avg cost ₹{h.avg_cost:,.2f}", annotation_position="top left")

span_days = max((hist.index[-1] - hist.index[0]).days, 1) if not hist.empty else 1
for kind, style in EVENT_STYLE.items():
    rows = ev[ev.kind == kind]
    if rows.empty:
        continue
    groups = [g for _, g in rows.groupby("date")]
    dates = [g.date.iloc[0] for g in groups]
    # A demerged stock may list weeks after the ex-date: pin those markers to its first price.
    prices = [float(hist.asof(d)) if d >= hist.index[0] else float(hist.iloc[0]) for d in dates]
    prices = [float(hist.iloc[0]) if pd.isna(p) else p for p in prices]
    fig.add_trace(go.Scatter(
        x=dates, y=prices, mode="markers", name=style["label"],
        marker=dict(color=style["color"], symbol=style["symbol"], size=style["size"],
                    line=dict(color="rgba(0,0,0,0.6)", width=1)),
        text=[event_hover(kind, g) for g in groups], hovertemplate="%{text}<extra></extra>",
    ))
    if kind in ("BUY", "SELL"):  # trades: always-visible vertical marker + label
        last_label = None
        for d in dates:
            fig.add_vline(x=d, line=dict(color=style["color"], width=1.5, dash="dot"), opacity=0.8)
            # skip the text label when it would collide with the previous one
            if last_label is None or (d - last_label).days > span_days * 0.05:
                fig.add_annotation(x=d, y=1, yref="paper", text=style["label"], showarrow=False,
                                   yanchor="bottom", font=dict(color=style["color"], size=11))
                last_label = d

fig.update_layout(height=420, margin=dict(l=10, r=10, t=30, b=10), hovermode="x unified",
                  legend=dict(orientation="h", yanchor="top", y=-0.08, x=0),
                  yaxis=dict(tickprefix="₹", gridcolor="rgba(137,135,129,0.2)"),
                  xaxis=dict(showgrid=False, hoverformat="%d %b %Y"))
st.plotly_chart(fig, width="stretch", config={"displayModeBar": False})
st.caption("Purchases are dotted lines. Hover the dots for dividends and splits. Click a legend item to hide it. "
           "Yahoo adjusts prices for splits and bonuses, and your average cost is adjusted the same way, "
           "so the lines are comparable.")

lots = next(x for x in portfolio["holdings"] if x["symbol"] == sym)["lots"]
with st.expander(f"Open lots for {sym} (FIFO, cost includes charges)"):
    st.dataframe(pd.DataFrame(lots).assign(cost_per_share=lambda d: (d.cost / d.qty).round(2)),
                 hide_index=True, width="stretch")

st.caption(f"Portfolio built {portfolio['generated_at']} from {len(portfolio['source_files'])} file(s). "
           "Prices from Yahoo Finance; may be delayed.")
