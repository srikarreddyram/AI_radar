# 🧠 AI Infrastructure Intelligence Dataset (AIID)

![Total Events](badges/total_events.svg)
![Last Updated](badges/last_updated.svg)

> An automated data collection and intelligence platform tracking the AI infrastructure ecosystem.
> **Last checked: {{ last_checked }}**

---

## 📊 Dataset Stats

| Metric | Value |
|--------|-------|
| **Total Events** | {{ total_events }} |
| **Events (7 days)** | {{ events_7d }} |
| **Events (30 days)** | {{ events_30d }} |

### Category Distribution

| Category | Count |
|----------|-------|
{% for cat, count in category_distribution.items() -%}
| {{ cat }} | {{ count }} |
{% endfor %}

### Top Companies

| Company | Events |
|---------|--------|
{% for company, count in top_companies.items() -%}
| {{ company }} | {{ count }} |
{% endfor %}

---

## 🔥 Latest Events

{% for event in latest_events -%}
### {{ event.title }}
- **Date**: {{ event.date }}
- **Category**: `{{ event.category }}`
- **Company**: {{ event.company or 'N/A' }}
- **Source**: [{{ event.source }}]({{ event.url }})
{% if event.summary %}- **Summary**: {{ event.summary }}{% endif %}

{% endfor %}

---

## 🏗️ How It Works

AIID runs **7 independent GitHub Actions workflows** daily:

| # | Workflow | Schedule (UTC) | Description |
|---|----------|----------------|-------------|
| 1 | 📥 Collect | 00:30 | Gather articles from RSS feeds & NewsAPI |
| 2 | 🏷️ Classify | 02:00 | Categorize into 9 event types |
| 3 | 🔍 Extract | 03:00 | Extract entities (companies, products, locations) |
| 4 | 📊 Aggregate | 06:00 | Rebuild analytics CSV files |
| 5 | 📈 Stats | 12:00 | Calculate metrics & generate badges |
| 6 | 📝 README | 03:00, 15:00 | Update this file with latest data |
| 7 | 📋 Report | Sun 09:00 | Generate weekly summary report |
| 8-12 | 📈 Stocks | 5x Daily | Track AI company stock prices & volume |

## 📁 Data Files

| File | Description |
|------|-------------|
| [`events/events_master.json`](events/events_master.json) | Complete event ledger (append-only) |
| [`aggregated/all_events.csv`](aggregated/all_events.csv) | All events as CSV |
| [`aggregated/ai_stocks.csv`](aggregated/ai_stocks.csv) | Daily stock tracking for AI companies |
| [`aggregated/model_releases.csv`](aggregated/model_releases.csv) | Model release events |
| [`aggregated/gpu_releases.csv`](aggregated/gpu_releases.csv) | GPU/hardware events |
| [`aggregated/funding_rounds.csv`](aggregated/funding_rounds.csv) | Funding events (with `$USD` amounts) |
| [`aggregated/datacenter_events.csv`](aggregated/datacenter_events.csv) | Datacenter events |
| [`aggregated/outages.csv`](aggregated/outages.csv) | Outage events |

## 📂 Event Categories

| Category | Description |
|----------|-------------|
| `MODEL_RELEASE` | Foundation model or fine-tune release |
| `GPU_RELEASE` | New chip or hardware SKU |
| `DATACENTER_EXPANSION` | New facility, investment, or capacity |
| `FUNDING_EVENT` | Venture round, acquisition, or investment |
| `SERVICE_UPDATE` | Cloud API or platform feature update |
| `OUTAGE` | Service degradation or incident |
| `RESEARCH_BREAKTHROUGH` | Notable research result |
| `POLICY_REGULATION` | Government or regulatory action |
| `OTHER` | Uncategorized |

---

## 🛠️ Technology Stack

- **Collection**: `feedparser` + `requests` (RSS & HTTP)
- **Classification**: Rule-based keyword matching (Phase 1)
- **Entity Extraction**: `spaCy` + regex
- **Storage**: Flat JSON/CSV in Git
- **Automation**: GitHub Actions (7 cron workflows)
- **Cost**: $0 — entirely free tier

---

> **Built to run forever, automatically.** 🚀
