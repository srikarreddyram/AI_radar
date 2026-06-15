#!/usr/bin/env python3
"""
AIID — Aggregation Script (WF4)
Rebuilds all CSV analytics files from events_master.json.
Always produces a commit via snapshot timestamp.
Output: aggregated/*.csv + snapshots/YYYY-MM-DD_snapshot.json
"""

import csv
import json
import logging
from datetime import datetime, timezone
from pathlib import Path
from collections import Counter

BASE_DIR = Path(__file__).resolve().parent.parent
EVENTS_FILE = BASE_DIR / "events" / "events_master.json"
AGGREGATED_DIR = BASE_DIR / "aggregated"
SNAPSHOTS_DIR = BASE_DIR / "snapshots"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
log = logging.getLogger("aggregate")

TODAY = datetime.now(timezone.utc).strftime("%Y-%m-%d")
NOW_ISO = datetime.now(timezone.utc).isoformat()

# ---------------------------------------------------------------------------
# CSV field definitions per category
# ---------------------------------------------------------------------------

BASE_FIELDS = [
    "event_id", "date", "category", "company", "product",
    "location", "source", "url", "summary", "title",
]

CATEGORY_CSV_MAP = {
    "all_events": {
        "filter": None,
        "fields": BASE_FIELDS + ["funding_usd", "hardware_name"],
    },
    "model_releases": {
        "filter": "MODEL_RELEASE",
        "fields": BASE_FIELDS,
    },
    "gpu_releases": {
        "filter": "GPU_RELEASE",
        "fields": BASE_FIELDS + ["hardware_name"],
    },
    "funding_rounds": {
        "filter": "FUNDING_EVENT",
        "fields": BASE_FIELDS + ["funding_usd"],
    },
    "datacenter_events": {
        "filter": "DATACENTER_EXPANSION",
        "fields": BASE_FIELDS,
    },
    "outages": {
        "filter": "OUTAGE",
        "fields": BASE_FIELDS,
    },
}


def write_csv(events: list[dict], filename: str, fields: list[str], filter_cat: str | None):
    """Write filtered events to a CSV file."""
    if filter_cat:
        filtered = [e for e in events if e.get("category") == filter_cat]
    else:
        filtered = events

    filepath = AGGREGATED_DIR / f"{filename}.csv"
    with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        for event in sorted(filtered, key=lambda e: e.get("date", ""), reverse=True):
            writer.writerow(event)

    log.info("  %s: %d rows", filename, len(filtered))
    return len(filtered)


def main():
    log.info("=== AIID Aggregation — %s ===", TODAY)

    # Load events
    if EVENTS_FILE.exists():
        with open(EVENTS_FILE) as f:
            events = json.load(f)
    else:
        events = []
        log.info("No events_master.json found — creating empty aggregations")

    log.info("Total events in ledger: %d", len(events))

    # Ensure output directories exist
    AGGREGATED_DIR.mkdir(parents=True, exist_ok=True)
    SNAPSHOTS_DIR.mkdir(parents=True, exist_ok=True)

    # Generate all CSVs
    counts = {}
    for csv_name, config in CATEGORY_CSV_MAP.items():
        count = write_csv(events, csv_name, config["fields"], config["filter"])
        counts[csv_name] = count

    # Generate snapshot
    category_dist = Counter(e.get("category", "OTHER") for e in events)
    company_dist = Counter(e.get("company", "Unknown") for e in events)

    snapshot = {
        "snapshot_date": TODAY,
        "generated_at": NOW_ISO,
        "total_events": len(events),
        "category_distribution": dict(category_dist.most_common()),
        "top_companies": dict(company_dist.most_common(20)),
        "csv_row_counts": counts,
    }

    snapshot_path = SNAPSHOTS_DIR / f"{TODAY}_snapshot.json"
    with open(snapshot_path, "w") as f:
        json.dump(snapshot, f, indent=2, ensure_ascii=False)

    log.info("Snapshot saved to %s", snapshot_path)
    log.info("📊 aggregated datasets updated (%d total events)", len(events))
    print(f"TOTAL_EVENTS={len(events)}")


if __name__ == "__main__":
    main()
