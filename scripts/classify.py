#!/usr/bin/env python3
"""
AIID — Classification Script (WF2)
Rule-based keyword classification of collected articles into 9 categories.
Input:  data/raw/YYYY-MM-DD.json
Output: data/processed/YYYY-MM-DD_classified.json
"""

import json
import re
import logging
from datetime import datetime, timezone
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_RAW = BASE_DIR / "data" / "raw"
DATA_PROCESSED = BASE_DIR / "data" / "processed"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
log = logging.getLogger("classify")

TODAY = datetime.now(timezone.utc).strftime("%Y-%m-%d")

# ---------------------------------------------------------------------------
# Keyword rules — order matters (first match wins)
# ---------------------------------------------------------------------------

CATEGORY_RULES: list[tuple[str, list[str]]] = [
    ("OUTAGE", [
        r"\boutage\b", r"\bdowntime\b", r"\bincident\b", r"\bdegraded\b",
        r"\bservice disruption\b", r"\boffline\b", r"\bdown for\b",
    ]),
    ("FUNDING_EVENT", [
        r"\braises\b", r"\braised\b", r"\bfunding\b", r"\bseries [a-e]\b",
        r"\bseed round\b", r"\binvestment\b", r"\bacquisition\b",
        r"\bacquires\b", r"\bacquired\b", r"\bvaluation\b", r"\bipo\b",
        r"\bventure\b", r"\b\$\d+.*(?:million|billion|M|B)\b",
    ]),
    ("GPU_RELEASE", [
        r"\bgpu\b", r"\bchip\b", r"\bblackwell\b", r"\bh100\b", r"\bh200\b",
        r"\bb200\b", r"\bb100\b", r"\ba100\b", r"\btpu\b", r"\bnpu\b",
        r"\bhardware launch\b", r"\bsilicon\b", r"\bprocessor\b",
        r"\baccelerator\b", r"\bgb200\b", r"\bgb300\b",
    ]),
    ("MODEL_RELEASE", [
        r"\blaunches model\b", r"\breleases model\b", r"\bopen.source model\b",
        r"\bgpt-\d\b", r"\bgpt\d\b", r"\bclaude\b", r"\bgemini\b",
        r"\bllama\b", r"\bmistral\b", r"\bcommand r\b", r"\bpalm\b",
        r"\bfoundation model\b", r"\blarge language model\b", r"\bllm\b",
        r"\bfine-tun\b", r"\bopen.weights\b", r"\bmodel card\b",
        r"\bbenchmark.* sota\b", r"\bstate.of.the.art\b",
        r"\bmultimodal model\b", r"\bdiffusion model\b",
    ]),
    ("DATACENTER_EXPANSION", [
        r"\bdatacenter\b", r"\bdata center\b", r"\bfacility\b",
        r"\bmegawatt\b", r"\b\d+ mw\b", r"\bcampus\b",
        r"\bhyperscale\b", r"\bcloud region\b", r"\bavailability zone\b",
    ]),
    ("SERVICE_UPDATE", [
        r"\bapi\b.*\b(?:update|launch|release|preview|ga)\b",
        r"\bplatform update\b", r"\bnew feature\b", r"\bgenerally available\b",
        r"\bpreview\b", r"\bsdk\b.*\b(?:release|update|launch)\b",
        r"\bcloud service\b",
    ]),
    ("RESEARCH_BREAKTHROUGH", [
        r"\bresearch paper\b", r"\bpeer.review\b", r"\bbenchmark\b",
        r"\barxiv\b", r"\bneurips\b", r"\bicml\b", r"\biclr\b",
        r"\bbreakthrough\b", r"\bnovel approach\b", r"\bsota\b",
        r"\bstate of the art\b", r"\bpaper\b.*\b(?:proposes|introduces)\b",
    ]),
    ("POLICY_REGULATION", [
        r"\bregulation\b", r"\bexecutive order\b", r"\bpolicy\b",
        r"\blegislation\b", r"\bban\b", r"\bcompliance\b",
        r"\bgovernment\b.*\bai\b", r"\beu ai act\b", r"\bsafety standards\b",
    ]),
]


def classify_article(title: str, text: str) -> str:
    """Return the first matching category, or OTHER."""
    combined = f"{title} {text}".lower()
    for category, patterns in CATEGORY_RULES:
        for pattern in patterns:
            if re.search(pattern, combined, re.IGNORECASE):
                return category
    return "OTHER"


def main():
    log.info("=== AIID Classification — %s ===", TODAY)

    raw_path = DATA_RAW / f"{TODAY}.json"
    if not raw_path.exists():
        log.warning("No raw data for today: %s", raw_path)
        # Try to classify any unprocessed historical files
        raw_files = sorted(DATA_RAW.glob("*.json"))
        if not raw_files:
            log.info("No raw files at all — nothing to classify")
            print("CLASSIFIED_COUNT=0")
            print("TOTAL_COUNT=0")
            return
        raw_path = raw_files[-1]
        log.info("Falling back to most recent raw file: %s", raw_path)

    with open(raw_path) as f:
        articles = json.load(f)

    log.info("Loaded %d articles from %s", len(articles), raw_path.name)

    classified_count = 0
    for article in articles:
        title = article.get("title", "")
        text = article.get("article_text", "")
        category = classify_article(title, text)
        article["category"] = category
        article["classification_method"] = "keyword_v1"
        article["classified_date"] = TODAY
        classified_count += 1

    # Write classified output
    DATA_PROCESSED.mkdir(parents=True, exist_ok=True)
    output_path = DATA_PROCESSED / f"{TODAY}_classified.json"
    with open(output_path, "w") as f:
        json.dump(articles, f, indent=2, ensure_ascii=False)

    # Category distribution
    from collections import Counter
    dist = Counter(a["category"] for a in articles)
    for cat, count in dist.most_common():
        log.info("  %s: %d", cat, count)

    log.info("Wrote %d classified articles to %s", len(articles), output_path)
    print(f"CLASSIFIED_COUNT={classified_count}")
    print(f"TOTAL_COUNT={len(articles)}")


if __name__ == "__main__":
    main()
