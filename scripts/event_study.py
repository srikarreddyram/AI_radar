#!/usr/bin/env python3
"""
AIID — Event Study Script (WF8)
Measures whether categorized news events for a company coincide with
abnormal next-trading-day moves in that company's tracked stock price.
Output: reports/event_study/YYYY-MM-DD.md
"""

from __future__ import annotations

import csv
import json
import logging
import re
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from statistics import mean

BASE_DIR = Path(__file__).resolve().parent.parent
EVENTS_FILE = BASE_DIR / "events" / "events_master.json"
STOCKS_FILE = BASE_DIR / "aggregated" / "ai_stocks.csv"
REPORTS_DIR = BASE_DIR / "reports" / "event_study"

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
log = logging.getLogger("event_study")

ISO_DATE = re.compile(r"^\d{4}-\d{2}-\d{2}$")

# Only companies with a tracked ticker (see scripts/stocks_tracker.py) are
# mapped here. Extend both together if you start tracking a new ticker.
COMPANY_TICKER = {
    "Intel": "INTC",
    "NVIDIA": "NVDA",
    "Amazon": "AMZN",
    "AWS": "AMZN",
    "Meta": "META",
    "Google": "GOOGL",
    "Google DeepMind": "GOOGL",
    "Microsoft": "MSFT",
    "Apple": "AAPL",
    "AMD": "AMD",
    "TSMC": "TSM",
    "Taiwan Semiconductor Manufacturing": "TSM",
}

# Below this many matched event days, flag the row as noise rather than signal.
MIN_EVENT_DAYS = 5


def event_date(e: dict) -> str | None:
    """Best available ISO date for an event: its own date, else collection date."""
    d = e.get("date", "")
    if ISO_DATE.match(d):
        return d
    ed = e.get("extracted_date", "")
    if ISO_DATE.match(ed):
        return ed
    return None


def load_daily_closes() -> dict[str, dict[str, float]]:
    """ticker -> {date: last recorded price that day}."""
    latest: dict[str, dict[str, tuple[str, float]]] = defaultdict(dict)
    with open(STOCKS_FILE) as f:
        for row in csv.DictReader(f):
            ticker, date, t = row["Ticker"], row["Date"], row["Time"]
            try:
                price = float(row["Price"])
            except (KeyError, ValueError):
                continue
            if not price:
                continue
            prev = latest[ticker].get(date)
            if prev is None or t > prev[0]:
                latest[ticker][date] = (t, price)
    return {tk: {d: p for d, (_, p) in days.items()} for tk, days in latest.items()}


def daily_returns(closes: dict[str, float]) -> dict[str, float]:
    """date -> pct return vs the prior date present in this ticker's series."""
    dates = sorted(closes)
    returns = {}
    for prev, cur in zip(dates, dates[1:]):
        p0, p1 = closes[prev], closes[cur]
        if p0:
            returns[cur] = (p1 - p0) / p0 * 100
    return returns


def next_trading_day(sorted_dates: list[str], d: str) -> str | None:
    for cand in sorted_dates:
        if cand > d:
            return cand
    return None


def main():
    with open(EVENTS_FILE) as f:
        events = json.load(f)
    all_closes = load_daily_closes()

    ticker_dates = {tk: sorted(closes) for tk, closes in all_closes.items()}
    ticker_returns = {tk: daily_returns(closes) for tk, closes in all_closes.items()}

    grouped: dict[tuple[str, str], list[str]] = defaultdict(list)
    for e in events:
        ticker = COMPANY_TICKER.get(e.get("company", ""))
        if not ticker or ticker not in ticker_returns:
            continue
        ed = event_date(e)
        if not ed:
            continue
        grouped[(ticker, e.get("category", "OTHER"))].append(ed)

    rows = []
    for (ticker, category), edates in grouped.items():
        dates = ticker_dates[ticker]
        returns = ticker_returns[ticker]
        baseline = list(returns.values())
        if not baseline:
            continue
        baseline_mean = mean(baseline)

        matched_returns = []
        for ed in edates:
            nd = next_trading_day(dates, ed)
            if nd and nd in returns:
                matched_returns.append(returns[nd])
        if not matched_returns:
            continue

        ev_mean = mean(matched_returns)
        rows.append({
            "ticker": ticker,
            "category": category,
            "n_events": len(edates),
            "n_matched": len(matched_returns),
            "event_avg_next_day_pct": round(ev_mean, 3),
            "baseline_avg_daily_pct": round(baseline_mean, 3),
            "delta_pct": round(ev_mean - baseline_mean, 3),
            "insufficient": len(matched_returns) < MIN_EVENT_DAYS,
        })

    rows.sort(key=lambda r: abs(r["delta_pct"]), reverse=True)

    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    report_path = REPORTS_DIR / f"{today}.md"

    lines = [
        f"# \U0001F4D0 AIID Event Study — {today}",
        "",
        "> Does a categorized news event for a company coincide with an abnormal move in "
        "its stock the next trading day, compared to that ticker's average daily move?",
        f"> Rows with fewer than {MIN_EVENT_DAYS} matched event days are flagged **low-n** "
        "— treat as noise, not signal.",
        "",
        "| Ticker | Category | Events | Matched | Avg next-day return (event) | "
        "Baseline avg daily return | Delta |",
        "|---|---|---|---|---|---|---|",
    ]
    for r in rows:
        flag = " ⚠️ low-n" if r["insufficient"] else ""
        lines.append(
            f"| {r['ticker']} | {r['category']} | {r['n_events']} | {r['n_matched']}{flag} "
            f"| {r['event_avg_next_day_pct']}% | {r['baseline_avg_daily_pct']}% | {r['delta_pct']:+.3f}% |"
        )
    if not rows:
        lines.append("| _no matched company/category pairs yet_ | | | | | | |")

    report_path.write_text("\n".join(lines) + "\n")
    log.info("Wrote %s (%d rows)", report_path, len(rows))
    print(f"ROW_COUNT={len(rows)}")


if __name__ == "__main__":
    main()
