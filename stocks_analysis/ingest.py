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
# "1:10 Demerger of ITCLTDEQ to ITCHOTELSEQ" -> 1 new share for every 10 parent shares
DEMERGER_RE = re.compile(r"(\d+)\s*:\s*(\d+)\s*Demerger of\s+(\S+)\s+to\s+(\S+)", re.I)

# The broker names a demerger's parent by an internal code, not its NSE symbol. The
# parent is normally found automatically (the holding whose quantity matches the
# demerger ratio); add an entry here only if that fails, e.g. {"ITCLTDEQ": "ITC"}.
DEMERGER_PARENT_OVERRIDES: dict[str, str] = {}


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
    df["action"] = df["action"].astype("string").fillna("").str.strip().str.upper()
    df["exchange"] = df["exchange"].astype("string").fillna("").str.strip()
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
        "related_symbol": "",
        "source_file": row.source_file,
    }
    # "Trade" = exchange trade; "Manual" = e.g. IPO allotment, also carrying BUY/SELL.
    if row.action in ("BUY", "SELL"):
        return {**base, "kind": row.action}
    if row.txn_type.strip().lower() in ("trade", "manual"):
        raise ValueError(f"{row.source_file}: unknown {row.txn_type} action {row.action!r}")

    remarks = row.remarks
    if m := DEMERGER_RE.search(remarks):
        a, b, parent_code, _ = m.groups()
        # VALUE is the cost the broker carries over from the parent to these shares.
        return {**base, "kind": "DEMERGER", "share_factor": int(a) / int(b),
                "related_symbol": parent_code}
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
    exchanges: set[str] = field(default_factory=set)
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
            self.exchanges.add(ev["exchange"])
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

    def receive_demerger(self, ev: dict, parent: str) -> None:
        self.last_txn = ev["date"]
        self.lots.append({"date": ev["date"], "qty": ev["qty"], "cost": ev["value"],
                          "via": f"demerger from {parent}"})
        self.first_buy = self.first_buy or ev["date"]

    def give_up_cost(self, amount: float, date: str, child: str) -> None:
        """Move `amount` of cost basis to a demerged company, pro rata across lots."""
        invested = self.invested
        if amount > invested + 1e-6:
            self.warnings.append(f"{date}: demerger to {child} carries more cost than held")
            amount = invested
        keep = 1 - amount / invested if invested else 1
        for lot in self.lots:
            lot["cost"] *= keep

    def summary(self) -> dict:
        qty = self.qty
        return {
            "symbol": self.symbol,
            # Quote on NSE whenever the stock has any NSE activity; BSE only if BSE-only.
            "exchange": "NSE" if "NSE" in self.exchanges or not self.exchanges else sorted(self.exchanges)[0],
            "qty": round(qty, 6),
            "invested": round(self.invested, 2),
            "avg_cost": round(self.invested / qty, 4) if qty else 0.0,
            "dividends": round(self.dividends, 2),
            "realised_pnl": round(self.realised_pnl, 2),
            "charges_paid": round(self.charges_paid, 2),
            "first_buy": self.first_buy,
            "last_txn": self.last_txn,
        }


def find_demerger_parent(ev: dict, positions: dict) -> str | None:
    code = ev["related_symbol"]
    if code in DEMERGER_PARENT_OVERRIDES:
        return DEMERGER_PARENT_OVERRIDES[code]
    matches = [s for s, p in positions.items()
               if s != ev["symbol"] and p.qty > 0 and abs(p.qty * ev["share_factor"] - ev["qty"]) < 1e-6]
    if len(matches) > 1:  # several holdings fit the ratio: prefer one whose name is in the code
        named = [s for s in matches if code.upper().startswith(s.replace("-", "")[:3])]
        matches = named if len(named) == 1 else matches
    return matches[0] if len(matches) == 1 else None


KIND_ORDER = {"SHARE_ADJUSTMENT": 0, "DEMERGER": 0, "DIVIDEND": 1, "UNHANDLED": 1, "BUY": 2, "SELL": 3}


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

    # A holding split across NSE and BSE gets one dividend row per exchange; merge
    # them so each payout is checked against the full position.
    demerger_parents: dict[tuple[str, str], str] = {}
    merged: list[dict] = []
    for ev in tx.to_dict("records"):
        prev = merged[-1] if merged else None
        if (prev and ev["kind"] == prev["kind"] == "DIVIDEND"
                and (ev["symbol"], ev["date"], ev["dividend_per_share"])
                == (prev["symbol"], prev["date"], prev["dividend_per_share"])):
            merged[-1] = {**prev, "qty": prev["qty"] + ev["qty"], "value": prev["value"] + ev["value"]}
        else:
            merged.append(ev)

    # Demergers move shares and cost between stocks, so replay every stock's events
    # together in date order rather than one stock at a time.
    merged.sort(key=lambda e: (e["date"], KIND_ORDER[e["kind"]]))
    positions: dict[str, Position] = {}
    for ev in merged:
        pos = positions.setdefault(ev["symbol"], Position(ev["symbol"]))
        if ev["kind"] != "DEMERGER":
            pos.apply(ev)
            continue
        parent = find_demerger_parent(ev, positions)
        if parent is None:
            pos.warnings.append(f"{ev['date']}: couldn't find the parent of this demerger "
                                f"({ev['remarks']!r}); add it to DEMERGER_PARENT_OVERRIDES")
            pos.receive_demerger(ev, "unknown parent")
            continue
        positions[parent].give_up_cost(ev["value"], ev["date"], ev["symbol"])
        pos.receive_demerger(ev, parent)
        demerger_parents[(ev["symbol"], ev["date"])] = parent
    tx["related_symbol"] = [
        demerger_parents.get((s, d), r) for s, d, r in zip(tx.symbol, tx.date, tx.related_symbol)]

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
        "dividend_per_share", "share_factor", "related_symbol", "remarks", "source_file"]].to_csv(
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
