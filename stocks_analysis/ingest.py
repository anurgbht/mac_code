"""Part 1: ingest broker "Equity Transaction History" Excel exports.

Each file in data/ holds the history of ONE stock. The broker export does not
name the stock, so the NSE symbol must be the filename prefix, e.g.
    BAJFINANCE_Transaction_History_6677164_2026-11-16.xlsx  ->  BAJFINANCE

Outputs (in processed/):
    transactions.csv  every trade / corporate action, normalised, one row each
    holdings.csv      one row per stock: open quantity, cost basis, dividends, realised P&L
    portfolio.json    the same holdings plus open lots and metadata (read by the dashboard)

Run:  uv run python ingest.py [--data-dir data] [--out-dir processed]
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path

import pandas as pd

HERE = Path(__file__).resolve().parent
HEADER_ROW = 3  # 0-based row holding "TXN TYPE | DATE | ..."

COLUMN_MAP = {
    "TXN TYPE": "txn_type",
    "DATE": "date",
    "EXCHANGE": "exchange",
    "ACTION": "action",
    "PRODUCT TYPE": "product",
    "QTY": "qty",
    "TXN PRICE": "price",
    "VALUE AT COST(Incl. addnl charges)": "value",
    "STT": "stt",
    "BROKERAGE": "brokerage",
    "ADDITIONAL CHARGES": "other_charges",
    "REMARKS": "remarks",
}

DIVIDEND_RE = re.compile(r"Dividend of Rs\.?\s*([\d.]+)", re.I)
SPLIT_RE = re.compile(r"(\d+)\s*:\s*(\d+)\s*Subdivision", re.I)
BONUS_RE = re.compile(r"(\d+)\s*:\s*(\d+)\s*Bonus", re.I)
CONSOLIDATION_RE = re.compile(r"(\d+)\s*:\s*(\d+)\s*Consolidation", re.I)


def symbol_from_filename(path: Path) -> str:
    stem = path.stem
    if "_Transaction_History" in stem:
        return stem.split("_Transaction_History")[0].upper()
    if "_" in stem:
        return stem.split("_")[0].upper()
    raise ValueError(
        f"{path.name}: can't tell which stock this is. Rename it to "
        f"'<NSE_SYMBOL>_Transaction_History_....xlsx'."
    )


def to_num(v) -> float:
    if v is None or (isinstance(v, float) and pd.isna(v)):
        return 0.0
    if isinstance(v, str):
        v = v.replace(",", "").strip()
        if v in ("", "-"):
            return 0.0
    return float(v)


def read_export(path: Path) -> pd.DataFrame:
    df = pd.read_excel(path, header=HEADER_ROW)
    df.columns = [str(c).strip() for c in df.columns]
    missing = set(COLUMN_MAP) - set(df.columns)
    if missing:
        raise ValueError(f"{path.name}: unexpected layout, missing columns {sorted(missing)}")
    df = df.rename(columns=COLUMN_MAP)[list(COLUMN_MAP.values())]
    df = df.dropna(subset=["txn_type", "date"])
    df["date"] = pd.to_datetime(df["date"], format="%d-%b-%Y")
    for c in ("qty", "price", "value", "stt", "brokerage", "other_charges"):
        df[c] = df[c].map(to_num)
    df["remarks"] = df["remarks"].astype("string").fillna("").str.strip()
    df["action"] = df["action"].fillna("").astype(str).str.strip().str.upper()
    df["exchange"] = df["exchange"].fillna("").astype(str).str.strip()
    df["symbol"] = symbol_from_filename(path)
    df["source_file"] = path.name
    return df


def classify(row: pd.Series) -> dict:
    """Turn one raw row into an event with an explicit kind."""
    base = {
        "symbol": row.symbol,
        "date": row.date.date().isoformat(),
        "exchange": row.exchange,
        "qty": row.qty,
        "price": row.price,
        "value": row.value,
        "charges": row.stt + row.brokerage + row.other_charges,
        "dividend_per_share": 0.0,
        "share_factor": 1.0,
        "remarks": row.remarks,
        "source_file": row.source_file,
    }
    if row.txn_type.strip().lower() == "trade":
        if row.action not in ("BUY", "SELL"):
            raise ValueError(f"{row.source_file}: unknown trade action {row.action!r}")
        return {**base, "kind": row.action}

    remarks = row.remarks
    divs = [float(x) for x in DIVIDEND_RE.findall(remarks)]
    factor = 1.0
    for a, b in SPLIT_RE.findall(remarks):  # "2:1 Subdivision" -> 1 old share becomes 2
        factor *= int(a) / int(b)
    for a, b in BONUS_RE.findall(remarks):  # "4:1 Bonus" -> 4 new for every 1 held
        factor *= (int(a) + int(b)) / int(b)
    for a, b in CONSOLIDATION_RE.findall(remarks):  # "1:10 Consolidation" -> 10 old become 1
        factor *= int(a) / int(b)

    if divs and factor == 1.0:
        return {**base, "kind": "DIVIDEND", "dividend_per_share": sum(divs)}
    if factor != 1.0 and not divs:
        return {**base, "kind": "SHARE_ADJUSTMENT", "share_factor": factor}
    return {**base, "kind": "UNHANDLED"}


@dataclass
class Position:
    symbol: str
    exchange: str = "NSE"
    lots: list[dict] = field(default_factory=list)  # FIFO: {date, qty, cost}
    dividends: float = 0.0
    realised_pnl: float = 0.0
    charges_paid: float = 0.0
    first_buy: str | None = None
    last_txn: str | None = None
    warnings: list[str] = field(default_factory=list)

    @property
    def qty(self) -> float:
        return sum(l["qty"] for l in self.lots)

    @property
    def invested(self) -> float:
        return sum(l["cost"] for l in self.lots)

    def apply(self, ev: dict) -> None:
        kind = ev["kind"]
        self.last_txn = ev["date"]
        if ev["exchange"]:
            self.exchange = ev["exchange"]
        if kind == "BUY":
            self.lots.append({"date": ev["date"], "qty": ev["qty"], "cost": ev["value"]})
            self.charges_paid += ev["charges"]
            self.first_buy = self.first_buy or ev["date"]
        elif kind == "SELL":
            self.charges_paid += ev["charges"]
            # TXN PRICE / VALUE are already net of charges (VALUE == QTY * TXN PRICE).
            proceeds = ev["value"] or ev["qty"] * ev["price"]
            remaining, cost_out = ev["qty"], 0.0
            while remaining > 1e-9:
                if not self.lots:
                    self.warnings.append(f"{ev['date']}: sold more shares than held")
                    break
                lot = self.lots[0]
                take = min(lot["qty"], remaining)
                unit = lot["cost"] / lot["qty"]
                cost_out += take * unit
                lot["qty"] -= take
                lot["cost"] -= take * unit
                remaining -= take
                if lot["qty"] <= 1e-9:
                    self.lots.pop(0)
            self.realised_pnl += proceeds - cost_out
        elif kind == "DIVIDEND":
            self.dividends += ev["value"] or ev["qty"] * ev["dividend_per_share"]
            if abs(ev["qty"] - self.qty) > 1e-6:
                self.warnings.append(
                    f"{ev['date']}: dividend paid on {ev['qty']:g} shares but {self.qty:g} held"
                )
        elif kind == "SHARE_ADJUSTMENT":
            before = self.qty
            for lot in self.lots:
                lot["qty"] *= ev["share_factor"]  # cost unchanged, so cost/share drops
            added = self.qty - before
            if abs(added - ev["qty"]) > 1e-6:
                self.warnings.append(
                    f"{ev['date']}: adjustment added {added:g} shares, broker says {ev['qty']:g}"
                )
        else:
            self.warnings.append(f"{ev['date']}: ignored corporate action: {ev['remarks']!r}")

    def summary(self) -> dict:
        qty = self.qty
        return {
            "symbol": self.symbol,
            "exchange": self.exchange,
            "qty": round(qty, 6),
            "invested": round(self.invested, 2),
            "avg_cost": round(self.invested / qty, 4) if qty else 0.0,
            "dividends": round(self.dividends, 2),
            "realised_pnl": round(self.realised_pnl, 2),
            "charges_paid": round(self.charges_paid, 2),
            "first_buy": self.first_buy,
            "last_txn": self.last_txn,
        }


KIND_ORDER = {"SHARE_ADJUSTMENT": 0, "DIVIDEND": 1, "UNHANDLED": 1, "BUY": 2, "SELL": 3}


def ingest(data_dir: Path, out_dir: Path) -> dict:
    files = sorted(p for p in data_dir.glob("*.xls*") if not p.name.startswith("~$"))
    if not files:
        raise SystemExit(f"No Excel files in {data_dir}")

    events = []
    for f in files:
        raw = read_export(f)
        events.extend(classify(r) for r in raw.itertuples(index=False))
        print(f"  read {f.name}: {len(raw)} rows")

    tx = pd.DataFrame(events)
    # Corporate actions on an ex-date apply to shares held before that day's trades.
    tx["_order"] = tx["kind"].map(KIND_ORDER)
    tx = tx.sort_values(["symbol", "date", "_order"]).drop(columns="_order").reset_index(drop=True)

    positions: dict[str, Position] = {}
    for ev in tx.to_dict("records"):
        positions.setdefault(ev["symbol"], Position(ev["symbol"])).apply(ev)

    holdings = [p.summary() for p in positions.values()]
    portfolio = {
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "source_files": [f.name for f in files],
        "holdings": [
            {**p.summary(),
             "lots": [{**l, "qty": round(l["qty"], 6), "cost": round(l["cost"], 2)} for l in p.lots],
             "warnings": p.warnings}
            for p in positions.values()
        ],
    }

    out_dir.mkdir(parents=True, exist_ok=True)
    tx[["symbol", "date", "kind", "exchange", "qty", "price", "value", "charges",
        "dividend_per_share", "share_factor", "remarks", "source_file"]].to_csv(
        out_dir / "transactions.csv", index=False)
    pd.DataFrame(holdings).to_csv(out_dir / "holdings.csv", index=False)
    (out_dir / "portfolio.json").write_text(json.dumps(portfolio, indent=2))

    for p in positions.values():
        for w in p.warnings:
            print(f"  WARNING {p.symbol}: {w}", file=sys.stderr)
    return portfolio


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--data-dir", type=Path, default=HERE / "data")
    ap.add_argument("--out-dir", type=Path, default=HERE / "processed")
    args = ap.parse_args()

    print(f"Ingesting {args.data_dir}")
    portfolio = ingest(args.data_dir, args.out_dir)
    df = pd.DataFrame(portfolio["holdings"]).drop(columns=["lots", "warnings"])
    with pd.option_context("display.width", 200, "display.max_columns", None):
        print(df.to_string(index=False))
    print(f"\nWrote transactions.csv, holdings.csv, portfolio.json to {args.out_dir}")


if __name__ == "__main__":
    main()
