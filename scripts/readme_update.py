#!/usr/bin/env python3
"""
AIID — README Update Script (WF6)
Auto-generates README.md from Jinja2 template with live stats.
Always produces a commit via heartbeat timestamp.
Output: README.md (overwritten)
"""

import json
import logging
from datetime import datetime, timezone
from pathlib import Path

from jinja2 import Environment, FileSystemLoader

BASE_DIR = Path(__file__).resolve().parent.parent
EVENTS_FILE = BASE_DIR / "events" / "events_master.json"
TEMPLATE_DIR = BASE_DIR / "scripts" / "templates"
README_PATH = BASE_DIR / "README.md"
SNAPSHOTS_DIR = BASE_DIR / "snapshots"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
log = logging.getLogger("readme_update")

TODAY = datetime.now(timezone.utc).strftime("%Y-%m-%d")
NOW_DISPLAY = datetime.now(timezone.utc).strftime("%Y-%m-%d at %H:%M UTC")


def load_latest_stats() -> dict:
    """Load the most recent stats snapshot."""
    stats_files = sorted(SNAPSHOTS_DIR.glob("*_stats.json"))
    if stats_files:
        with open(stats_files[-1]) as f:
            return json.load(f)
    return {
        "total_events": 0,
        "events_7d": 0,
        "events_30d": 0,
        "category_distribution": {},
        "top_companies": {},
    }


def load_latest_events(n: int = 5) -> list[dict]:
    """Load the N most recent events."""
    if EVENTS_FILE.exists():
        with open(EVENTS_FILE) as f:
            events = json.load(f)
        # Sort by date descending
        events.sort(key=lambda e: e.get("date", ""), reverse=True)
        return events[:n]
    return []


def main():
    log.info("=== AIID README Update — %s ===", TODAY)

    stats = load_latest_stats()
    latest_events = load_latest_events(5)

    # Render template
    env = Environment(loader=FileSystemLoader(str(TEMPLATE_DIR)))
    template = env.get_template("readme_template.md")

    readme_content = template.render(
        last_checked=NOW_DISPLAY,
        today=TODAY,
        total_events=stats.get("total_events", 0),
        events_7d=stats.get("events_7d", 0),
        events_30d=stats.get("events_30d", 0),
        category_distribution=stats.get("category_distribution", {}),
        top_companies=stats.get("top_companies", {}),
        latest_events=latest_events,
    )

    with open(README_PATH, "w") as f:
        f.write(readme_content)

    log.info("README.md updated (Last checked: %s)", NOW_DISPLAY)
    log.info("📝 README: daily summary updated")


if __name__ == "__main__":
    main()
