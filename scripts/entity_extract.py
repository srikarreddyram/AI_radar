#!/usr/bin/env python3
"""
AIID — Entity Extraction Script (WF3)
Extracts companies, products, locations, funding amounts, and hardware names
from classified articles using spaCy NER + regex patterns.
Input:  data/processed/YYYY-MM-DD_classified.json
Output: Appends structured events to events/events_master.json
"""

import json
import re
import uuid
import logging
from datetime import datetime, timezone
from pathlib import Path

try:
    import spacy
    NLP = spacy.load("en_core_web_sm")
except Exception:
    NLP = None

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PROCESSED = BASE_DIR / "data" / "processed"
EVENTS_FILE = BASE_DIR / "events" / "events_master.json"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
log = logging.getLogger("entity_extract")

TODAY = datetime.now(timezone.utc).strftime("%Y-%m-%d")

# ---------------------------------------------------------------------------
# Known entity lists for regex-based extraction
# ---------------------------------------------------------------------------

KNOWN_COMPANIES = [
    "OpenAI", "Anthropic", "Google", "Google DeepMind", "DeepMind",
    "NVIDIA", "AMD", "Intel", "Microsoft", "Amazon", "AWS", "Meta",
    "Apple", "Tesla", "Mistral", "Cohere", "Stability AI", "Hugging Face",
    "xAI", "Inflection", "Databricks", "Snowflake", "Cerebras",
    "Scale AI", "Perplexity", "Character.AI", "Midjourney", "Runway",
    "Groq", "SambaNova", "Together AI", "Anyscale", "Modal",
    "CoreWeave", "Lambda", "Crusoe", "Applied Digital",
]

KNOWN_MODELS = [
    "GPT-4", "GPT-4o", "GPT-5", "GPT-4.5",
    "Claude", "Claude 3", "Claude 3.5", "Claude 4",
    "Gemini", "Gemini 2", "Gemini Ultra", "Gemini Pro", "Gemini Flash",
    "Llama", "Llama 3", "Llama 4", "Code Llama",
    "Mistral", "Mixtral", "Mistral Large",
    "Command R", "Command R+",
    "Stable Diffusion", "DALL-E", "DALL-E 3", "Midjourney",
    "Phi-3", "Phi-4", "Qwen", "DeepSeek",
    "PaLM", "PaLM 2",
]

KNOWN_HARDWARE = [
    "H100", "H200", "B200", "B100", "B300", "GB200", "GB300",
    "A100", "A800", "L40", "L40S",
    "Blackwell", "Blackwell Ultra", "Hopper", "Grace Hopper",
    "TPU v5", "TPU v5e", "TPU v6", "Trillium",
    "MI300", "MI300X", "MI350",
    "Gaudi 3", "Trainium", "Trainium2", "Inferentia",
]

# ---------------------------------------------------------------------------
# Extraction functions
# ---------------------------------------------------------------------------

MONEY_RE = re.compile(
    r"\$\s*([\d,.]+)\s*(million|billion|M|B|mn|bn|m|b)",
    re.IGNORECASE,
)


def extract_funding_usd(text: str) -> int | None:
    """Extract dollar amount from text, normalize to USD integer."""
    match = MONEY_RE.search(text)
    if not match:
        return None
    amount_str = match.group(1).replace(",", "")
    try:
        amount = float(amount_str)
    except ValueError:
        return None
    multiplier_str = match.group(2).lower()
    if multiplier_str in ("billion", "b", "bn"):
        return int(amount * 1_000_000_000)
    elif multiplier_str in ("million", "m", "mn"):
        return int(amount * 1_000_000)
    return int(amount)


def extract_company(title: str, text: str) -> str:
    """Extract primary company name from text."""
    combined = f"{title} {text}"

    # Try known companies first (longest match)
    for company in sorted(KNOWN_COMPANIES, key=len, reverse=True):
        if company.lower() in combined.lower():
            return company

    # Fall back to spaCy NER
    if NLP:
        doc = NLP(combined[:1000])  # limit input length
        orgs = [ent.text for ent in doc.ents if ent.label_ == "ORG"]
        if orgs:
            return orgs[0]

    return ""


def extract_product(title: str, text: str) -> str:
    """Extract product/model name."""
    combined = f"{title} {text}"
    for model in sorted(KNOWN_MODELS, key=len, reverse=True):
        if model.lower() in combined.lower():
            return model
    return ""


def extract_hardware(title: str, text: str) -> str:
    """Extract hardware/chip name."""
    combined = f"{title} {text}"
    for hw in sorted(KNOWN_HARDWARE, key=len, reverse=True):
        if hw.lower() in combined.lower():
            return hw
    return ""


def extract_location(title: str, text: str) -> str:
    """Extract geographic location using spaCy GPE entity."""
    if not NLP:
        return ""
    combined = f"{title} {text}"
    doc = NLP(combined[:1000])
    gpes = [ent.text for ent in doc.ents if ent.label_ == "GPE"]
    return gpes[0] if gpes else ""


def generate_summary(article: dict) -> str:
    """Generate a 2-3 sentence summary from article text."""
    text = article.get("article_text", "")
    title = article.get("title", "")

    if not text:
        return title

    # Simple extractive: first 2 sentences
    sentences = re.split(r'(?<=[.!?])\s+', text.strip())
    summary_sentences = sentences[:2]
    summary = " ".join(summary_sentences)

    # Cap at 300 chars
    if len(summary) > 300:
        summary = summary[:297] + "..."

    return summary or title


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    log.info("=== AIID Entity Extraction — %s ===", TODAY)

    classified_path = DATA_PROCESSED / f"{TODAY}_classified.json"
    if not classified_path.exists():
        # Fallback to latest classified file
        classified_files = sorted(DATA_PROCESSED.glob("*_classified.json"))
        if not classified_files:
            log.info("No classified files found — nothing to extract")
            print("EVENT_COUNT=0")
            return
        classified_path = classified_files[-1]
        log.info("Falling back to: %s", classified_path)

    with open(classified_path) as f:
        articles = json.load(f)

    log.info("Processing %d classified articles", len(articles))

    # Load existing events for dedup
    if EVENTS_FILE.exists():
        with open(EVENTS_FILE) as f:
            existing_events = json.load(f)
    else:
        existing_events = []

    existing_urls = {e.get("url") for e in existing_events}

    new_events = []
    for article in articles:
        url = article.get("url", "")
        if url in existing_urls:
            continue  # skip duplicates

        title = article.get("title", "")
        text = article.get("article_text", "")
        category = article.get("category", "OTHER")

        event = {
            "event_id": str(uuid.uuid4()),
            "title": title,
            "date": article.get("publication_date", TODAY)[:10] or TODAY,
            "category": category,
            "company": extract_company(title, text),
            "product": extract_product(title, text),
            "location": extract_location(title, text),
            "funding_usd": None,
            "hardware_name": "",
            "source": article.get("source", ""),
            "url": url,
            "summary": generate_summary(article),
            "extracted_date": TODAY,
        }

        # Category-specific enrichment
        if category == "FUNDING_EVENT":
            event["funding_usd"] = extract_funding_usd(f"{title} {text}")

        if category == "GPU_RELEASE":
            event["hardware_name"] = extract_hardware(title, text)

        new_events.append(event)

    # Append to master ledger
    all_events = existing_events + new_events
    EVENTS_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(EVENTS_FILE, "w") as f:
        json.dump(all_events, f, indent=2, ensure_ascii=False)

    log.info("Extracted %d new events (total: %d)", len(new_events), len(all_events))
    print(f"EVENT_COUNT={len(new_events)}")


if __name__ == "__main__":
    main()
