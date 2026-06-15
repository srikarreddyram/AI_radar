#!/usr/bin/env python3
"""
AIID — Weekly Report Script (WF7)
Generates a weekly summary report in Markdown.
Runs every Sunday at 09:00 UTC.
Output: reports/weekly/YYYY-WNN.md
"""

import json
import logging
from datetime import datetime, timezone, timedelta
from pathlib import Path
from collections import Counter

from jinja2 import Environment, FileSystemLoader

BASE_DIR = Path(__file__).resolve().parent.parent
EVENTS_FILE = BASE_DIR / "events" / "events_master.json"
TEMPLATE_DIR = BASE_DIR / "scripts" / "templates"
REPORTS_DIR = BASE_DIR / "reports" / "weekly"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
log = logging.getLogger("weekly_report")

NOW = datetime.now(timezone.utc)
TODAY = NOW.strftime("%Y-%m-%d")
YEAR = NOW.strftime("%Y")
WEEK_NUM = NOW.strftime("%W")
WEEK_LABEL = f"{YEAR}-W{WEEK_NUM}"


def get_week_events(events: list[dict]) -> list[dict]:
    """Filter events from the last 7 days."""
    cutoff = (NOW - timedelta(days=7)).date()
    week_events = []
    for e in events:
        try:
            event_date = datetime.strptime(e.get("date", "")[:10], "%Y-%m-%d").date()
            if event_date >= cutoff:
                week_events.append(e)
        except (ValueError, TypeError):
            continue
    return week_events


def main():
    log.info("=== AIID Weekly Report — %s ===", WEEK_LABEL)

    # Load events
    if EVENTS_FILE.exists():
        with open(EVENTS_FILE) as f:
            all_events = json.load(f)
    else:
        all_events = []

    week_events = get_week_events(all_events)
    log.info("Events this week: %d (total: %d)", len(week_events), len(all_events))

    # Calculate stats
    category_dist = Counter(e.get("category", "OTHER") for e in week_events)
    company_dist = Counter(e.get("company", "") for e in week_events if e.get("company"))
    top_companies = dict(company_dist.most_common(10))

    # Total funding this week
    total_funding = sum(
        e.get("funding_usd", 0) or 0
        for e in week_events
        if e.get("category") == "FUNDING_EVENT"
    )

    # Generate report
    env = Environment(loader=FileSystemLoader(str(TEMPLATE_DIR)))
    template = env.get_template("weekly_report_template.md")

    report_content = template.render(
        week_label=WEEK_LABEL,
        generated_at=NOW.strftime("%Y-%m-%d %H:%M UTC"),
        total_events_all=len(all_events),
        week_event_count=len(week_events),
        category_distribution=dict(category_dist.most_common()),
        top_companies=top_companies,
        total_funding=total_funding,
        top_events=week_events[:10],
    )

    # Write report
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    report_path = REPORTS_DIR / f"{WEEK_LABEL}.md"
    with open(report_path, "w") as f:
        f.write(report_content)

    log.info("📋 weekly report: %s", WEEK_LABEL)
    log.info("Report saved to %s", report_path)


if __name__ == "__main__":
    main()
