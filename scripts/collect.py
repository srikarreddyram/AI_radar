#!/usr/bin/env python3
"""
AIID — Data Collection Script (WF1)
Collects AI infrastructure news from RSS feeds and NewsAPI.
Outputs: data/raw/YYYY-MM-DD.json
"""

import json
import os
import sys
import hashlib
import random
import glob
import logging
from datetime import datetime, timezone
from pathlib import Path

import feedparser
import requests

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_RAW = BASE_DIR / "data" / "raw"
DATA_PROCESSED = BASE_DIR / "data" / "processed"
EVENTS_MASTER = BASE_DIR / "events" / "events_master.json"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
log = logging.getLogger("collect")

TODAY = datetime.now(timezone.utc).strftime("%Y-%m-%d")

# RSS feed sources — company blogs, news outlets, research
RSS_FEEDS = {
    # Company blogs
    "OpenAI Blog": "https://openai.com/blog/rss.xml",
    "Anthropic Blog": "https://www.anthropic.com/news/rss",
    "Google DeepMind": "https://deepmind.google/blog/rss.xml",
    "NVIDIA Blog": "https://blogs.nvidia.com/feed/",
    "AWS ML Blog": "https://aws.amazon.com/blogs/machine-learning/feed/",
    "Azure AI Blog": "https://azure.microsoft.com/en-us/blog/tag/ai/feed/",
    "Meta AI Blog": "https://ai.meta.com/blog/rss/",
    # News outlets
    "TechCrunch AI": "https://techcrunch.com/tag/artificial-intelligence/feed/",
    "VentureBeat AI": "https://venturebeat.com/category/ai/feed/",
    "The Verge AI": "https://www.theverge.com/rss/ai-artificial-intelligence/index.xml",
    # Research feeds
    "arXiv cs.AI": "https://rss.arxiv.org/rss/cs.AI",
    "arXiv cs.LG": "https://rss.arxiv.org/rss/cs.LG",
    "Papers With Code": "https://paperswithcode.com/latest/feed",
}

NEWSAPI_BASE = "https://newsapi.org/v2/everything"
NEWSAPI_KEYWORDS = (
    '("AI model" OR "GPU" OR "datacenter" OR "data center" OR "AI funding" '
    'OR "artificial intelligence" OR "large language model" OR "LLM" '
    'OR "NVIDIA" OR "OpenAI" OR "Anthropic" OR "Google DeepMind")'
)

REQUEST_TIMEOUT = 15  # seconds per HTTP request
MAX_RUNTIME_SECONDS = 450  # 7.5 minutes hard ceiling


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def article_id(url: str) -> str:
    """Deterministic ID from URL for deduplication."""
    return hashlib.sha256(url.encode()).hexdigest()[:16]


def safe_get(url: str, **kwargs) -> requests.Response | None:
    """GET with timeout and error swallowing."""
    try:
        resp = requests.get(url, timeout=REQUEST_TIMEOUT, **kwargs)
        resp.raise_for_status()
        return resp
    except Exception as exc:
        log.warning("HTTP error for %s: %s", url, exc)
        return None


# ---------------------------------------------------------------------------
# RSS collection
# ---------------------------------------------------------------------------

def collect_rss() -> list[dict]:
    """Parse all RSS feeds and return normalized articles."""
    articles = []
    for source_name, feed_url in RSS_FEEDS.items():
        log.info("Fetching RSS: %s", source_name)
        try:
            feed = feedparser.parse(feed_url)
            for entry in feed.entries[:20]:  # cap per feed
                pub_date = ""
                if hasattr(entry, "published"):
                    pub_date = entry.published
                elif hasattr(entry, "updated"):
                    pub_date = entry.updated

                url = getattr(entry, "link", "")
                if not url:
                    continue

                articles.append({
                    "id": article_id(url),
                    "title": getattr(entry, "title", ""),
                    "source": source_name,
                    "publication_date": pub_date,
                    "url": url,
                    "article_text": getattr(entry, "summary", ""),
                })
        except Exception as exc:
            log.warning("Failed to parse feed %s: %s", source_name, exc)
    return articles


# ---------------------------------------------------------------------------
# NewsAPI collection
# ---------------------------------------------------------------------------

def collect_newsapi() -> list[dict]:
    """Fetch articles from NewsAPI free tier."""
    api_key = os.environ.get("NEWS_API_KEY", "")
    if not api_key:
        log.info("NEWS_API_KEY not set — skipping NewsAPI collection")
        return []

    params = {
        "q": NEWSAPI_KEYWORDS,
        "language": "en",
        "sortBy": "publishedAt",
        "pageSize": 50,
        "apiKey": api_key,
    }

    articles = []
    resp = safe_get(NEWSAPI_BASE, params=params)
    if resp is None:
        return articles

    data = resp.json()
    for item in data.get("articles", []):
        url = item.get("url", "")
        if not url:
            continue
        articles.append({
            "id": article_id(url),
            "title": item.get("title", ""),
            "source": item.get("source", {}).get("name", "NewsAPI"),
            "publication_date": item.get("publishedAt", ""),
            "url": url,
            "article_text": item.get("content", "") or item.get("description", ""),
        })
    log.info("NewsAPI returned %d articles", len(articles))
    return articles


# ---------------------------------------------------------------------------
# Deduplication
# ---------------------------------------------------------------------------

def deduplicate(articles: list[dict]) -> list[dict]:
    """Remove duplicates by article id (URL hash)."""
    seen = set()
    unique = []
    for art in articles:
        if art["id"] not in seen:
            seen.add(art["id"])
            unique.append(art)
    return unique


# ---------------------------------------------------------------------------
# No-news fallback: reprocessing historical articles
# ---------------------------------------------------------------------------

def reprocess_historical() -> list[dict]:
    """Pick 30 random historical raw articles and return them for reprocessing."""
    raw_files = sorted(glob.glob(str(DATA_RAW / "*.json")))
    if not raw_files:
        log.info("No historical data to reprocess")
        return []

    all_articles = []
    for fpath in raw_files:
        try:
            with open(fpath) as f:
                all_articles.extend(json.load(f))
        except Exception:
            continue

    if not all_articles:
        return []

    sample_size = min(30, len(all_articles))
    sampled = random.sample(all_articles, sample_size)
    for art in sampled:
        art["reprocessed"] = True
        art["reprocessed_date"] = TODAY
    log.info("♻️ reprocessed %d historical articles", sample_size)
    return sampled


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    log.info("=== AIID Collection — %s ===", TODAY)

    # Collect from all sources
    rss_articles = collect_rss()
    log.info("RSS collected: %d articles", len(rss_articles))

    newsapi_articles = collect_newsapi()
    log.info("NewsAPI collected: %d articles", len(newsapi_articles))

    all_articles = deduplicate(rss_articles + newsapi_articles)
    log.info("After dedup: %d unique articles", len(all_articles))

    # No-news fallback
    if len(all_articles) == 0:
        log.info("Zero new articles — running reprocessing fallback")
        all_articles = reprocess_historical()

    # Write output
    DATA_RAW.mkdir(parents=True, exist_ok=True)
    output_path = DATA_RAW / f"{TODAY}.json"
    with open(output_path, "w") as f:
        json.dump(all_articles, f, indent=2, ensure_ascii=False)

    log.info("Wrote %d articles to %s", len(all_articles), output_path)

    # Print count for commit message
    print(f"ARTICLE_COUNT={len(all_articles)}")


if __name__ == "__main__":
    main()
