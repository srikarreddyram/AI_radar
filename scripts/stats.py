#!/usr/bin/env python3
"""
AIID — Stats & Badges Script (WF5)
Calculates dataset statistics and generates SVG badges.
Always produces a commit via timestamp in stats JSON.
Output: badges/*.svg + snapshots/YYYY-MM-DD_stats.json
"""

import json
import logging
from datetime import datetime, timezone, timedelta
from pathlib import Path
from collections import Counter
from dateutil import parser as dateutil_parser

BASE_DIR = Path(__file__).resolve().parent.parent
EVENTS_FILE = BASE_DIR / "events" / "events_master.json"
BADGES_DIR = BASE_DIR / "badges"
SNAPSHOTS_DIR = BASE_DIR / "snapshots"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
log = logging.getLogger("stats")

TODAY = datetime.now(timezone.utc).strftime("%Y-%m-%d")
NOW_ISO = datetime.now(timezone.utc).isoformat()
NOW_DISPLAY = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

# ---------------------------------------------------------------------------
# SVG Badge Generation
# ---------------------------------------------------------------------------

BADGE_TEMPLATE = """<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="20">
  <linearGradient id="b" x2="0" y2="100%">
    <stop offset="0" stop-color="#bbb" stop-opacity=".1"/>
    <stop offset="1" stop-opacity=".1"/>
  </linearGradient>
  <clipPath id="a">
    <rect width="{width}" height="20" rx="3" fill="#fff"/>
  </clipPath>
  <g clip-path="url(#a)">
    <rect width="{label_width}" height="20" fill="#555"/>
    <rect x="{label_width}" width="{value_width}" height="20" fill="{color}"/>
    <rect width="{width}" height="20" fill="url(#b)"/>
  </g>
  <g fill="#fff" text-anchor="middle" font-family="DejaVu Sans,Verdana,Geneva,sans-serif" font-size="11">
    <text x="{label_x}" y="15" fill="#010101" fill-opacity=".3">{label}</text>
    <text x="{label_x}" y="14">{label}</text>
    <text x="{value_x}" y="15" fill="#010101" fill-opacity=".3">{value}</text>
    <text x="{value_x}" y="14">{value}</text>
  </g>
</svg>"""


def generate_badge(label: str, value: str, color: str, filename: str):
    """Generate a shields.io-style SVG badge."""
    label_width = max(len(label) * 7 + 10, 50)
    value_width = max(len(value) * 7 + 10, 40)
    width = label_width + value_width

    svg = BADGE_TEMPLATE.format(
        width=width,
        label_width=label_width,
        value_width=value_width,
        label_x=label_width // 2,
        value_x=label_width + value_width // 2,
        label=label,
        value=value,
        color=color,
    )

    badge_path = BADGES_DIR / filename
    with open(badge_path, "w") as f:
        f.write(svg)
    log.info("Badge: %s → %s", filename, value)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    log.info("=== AIID Stats — %s ===", TODAY)

    # Load events
    if EVENTS_FILE.exists():
        with open(EVENTS_FILE) as f:
            events = json.load(f)
    else:
        events = []

    total = len(events)
    log.info("Total events: %d", total)

    # Category distribution
    category_dist = Counter(e.get("category", "OTHER") for e in events)

    # Company distribution (top 10)
    company_dist = Counter(e.get("company", "") for e in events if e.get("company"))
    top_companies = dict(company_dist.most_common(10))

    # Rolling counts
    today_dt = datetime.now(timezone.utc).date()

    def parse_event_date(date_str: str):
        """Robustly parse dates in ISO-8601 or RFC-822 format."""
        try:
            return dateutil_parser.parse(date_str).date()
        except Exception:
            return None

    rolling_7d = 0
    rolling_30d = 0
    for e in events:
        d = parse_event_date(e.get("date", ""))
        if d is None:
            continue
        delta = (today_dt - d).days
        if 0 <= delta <= 7:
            rolling_7d += 1
        if 0 <= delta <= 30:
            rolling_30d += 1

    # Build stats object
    stats = {
        "generated_at": NOW_ISO,
        "date": TODAY,
        "total_events": total,
        "events_7d": rolling_7d,
        "events_30d": rolling_30d,
        "category_distribution": dict(category_dist.most_common()),
        "top_companies": top_companies,
    }

    # Write stats JSON
    SNAPSHOTS_DIR.mkdir(parents=True, exist_ok=True)
    stats_path = SNAPSHOTS_DIR / f"{TODAY}_stats.json"
    with open(stats_path, "w") as f:
        json.dump(stats, f, indent=2, ensure_ascii=False)
    log.info("Stats saved to %s", stats_path)

    # Generate badges
    BADGES_DIR.mkdir(parents=True, exist_ok=True)
    generate_badge("AIID Events", str(total), "#4c1", "total_events.svg")
    generate_badge("Last Updated", NOW_DISPLAY, "#007ec6", "last_updated.svg")

    log.info("📈 stats refreshed")
    print(f"TOTAL_EVENTS={total}")


if __name__ == "__main__":
    main()
