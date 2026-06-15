# AI Infrastructure Intelligence Dataset (AIID)
## Product Requirements & Architecture Document v2.0

| Metric | Target |
|--------|--------|
| **Commits/day** | 5–9 |
| **Workflows** | 7 |
| **Commits/year** | 2000+ |
| **Cost** | $0 |

> Version 2.0 · June 2026 · srikarreddyram

---

## 1. Executive Summary

AIID is an automated data collection and intelligence platform that continuously gathers, classifies, structures, and archives developments in the AI infrastructure ecosystem — then commits that work to GitHub on a strict schedule, generating **5–9 real commits every single day**.

The pipeline collects from multiple public sources and transforms unstructured news into structured datasets covering:
- Foundation model releases
- AI startup funding events
- Datacenter expansions and investments
- GPU and hardware launches
- AI cloud service updates
- Outages and incidents
- Major research breakthroughs

**Core goal**: A continuously growing, machine-readable dataset that supports trend analysis, dashboards, predictive analytics, research, and ML forecasting — while keeping the GitHub contribution graph green every single day, automatically, forever.

---

## 2. Problem Statement

Current AI industry information exists in fragmented sources: company blogs, news websites, research portals, product announcements, and social media. There is no centralized structured dataset recording the evolution of AI infrastructure over time.

Researchers and engineers manually aggregate information about model releases, datacenter investments, hardware launches, funding trends, and AI outages. AIID automates all of this — and generates proof-of-work on GitHub as a side effect.

---

## 3. Goals

### 3.1 Primary Goals
- Automatically collect AI infrastructure news daily.
- Convert unstructured text into structured, queryable records.
- Maintain a permanently growing historical dataset (append-only).
- Generate 5–9 GitHub commits per day via 7 independent workflows.
- Enable analytics, dashboards, and forecasting on the accumulated data.

### 3.2 Secondary Goals
- Build a reusable, modular ETL architecture.
- Support LLM-based classification (Phase 2).
- Create datasets suitable for ML training and research.
- Demonstrate data engineering and MLOps skills publicly on GitHub.

---

## 4. GitHub Contribution Strategy

The single most important architectural decision in AIID is splitting the pipeline into **7 independent GitHub Actions workflows**, each with its own schedule and its own commit.

### 4.1 The 7 Workflows

| Workflow | Script | Cron (UTC) | Commit message | Always runs? |
|----------|--------|------------|----------------|--------------|
| WF1 | `collect.py` | 00:30 UTC | 📥 raw collection: YYYY-MM-DD (N articles) | No* |
| WF2 | `classify.py` | 02:00 UTC | 🏷️ classified: N/M articles | No* |
| WF3 | `entity_extract.py` | 03:00 UTC | 🔍 entities extracted: N events | No* |
| WF4 | `aggregate.py` | 06:00 UTC | 📊 aggregated datasets updated (N total) | Yes |
| WF5 | `stats.py` | 12:00 UTC | 📈 stats refreshed | Yes |
| WF6 | `readme_update.py` | 18:00 UTC | 📝 README: daily summary updated | Yes |
| WF7 | `weekly_report.py` | Sun 09:00 | 📋 weekly report: W## YYYY | Yes |

\* On no-news days, WF1–3 run enrichment passes on historical data instead.

### 4.2 The No-News Problem — Solved

Five guaranteed content generators:
1. **Reprocessing** — Re-classify 30 random historical articles with updated rules.
2. **Derived metrics** — Recalculate rolling 7-day event counts, leaderboards, breakdowns.
3. **Trend snapshots** — Save daily snapshot to `snapshots/YYYY-MM-DD_snapshot.json`.
4. **Enrichment passes** — Fill blank fields in old events.
5. **README heartbeat** — Always updates `Last checked: DATE at 18:00 UTC`.

---

## 5. Functional Requirements

### FR1 — Daily Data Collection
Sources collected at 00:30 UTC daily:
- **RSS feeds**: OpenAI, Anthropic, DeepMind, NVIDIA, AWS, Azure, arXiv cs.AI + cs.LG
- **News APIs**: NewsAPI free tier (100 req/day), TechCrunch, VentureBeat, The Verge
- **Output**: `data/raw/YYYY-MM-DD.json`

### FR2 — Article Normalization
Schema: `title`, `source`, `publication_date`, `url`, `article_text`

### FR3 — Event Classification (9-category taxonomy)

| Category | Description |
|----------|-------------|
| `MODEL_RELEASE` | Foundation model or fine-tune release |
| `GPU_RELEASE` | New chip or hardware SKU announcement |
| `DATACENTER_EXPANSION` | New facility, investment, or capacity |
| `FUNDING_EVENT` | Venture round, acquisition, strategic investment |
| `SERVICE_UPDATE` | Cloud API or platform feature update |
| `OUTAGE` | Service degradation or incident |
| `RESEARCH_BREAKTHROUGH` | Peer-reviewed or notable research |
| `POLICY_REGULATION` | Government or regulatory action |
| `OTHER` | Does not fit above categories |

- **Phase 1**: Rule-based keyword matching
- **Phase 2**: LLM-based classification via Claude API

### FR4 — Entity Extraction
Extract: `company`, `product`, `location`, `funding_value`, `hardware_name`

### FR5 — Structured Dataset Creation

| Field | Type | Description |
|-------|------|-------------|
| `event_id` | string | UUID |
| `date` | string | ISO date |
| `category` | enum | One of 9 categories |
| `company` | string | Primary company |
| `product` | string | Nullable |
| `location` | string | Nullable |
| `funding_usd` | integer | Nullable |
| `source` | string | Publication name |
| `url` | string | Canonical URL |
| `summary` | string | 2–3 sentences |

### FR6 — Append-Only Event Ledger
All events appended to `events/events_master.json`. No deletions ever.

### FR7 — Daily GitHub Automation
Fully unattended commits and pushes.

### FR8 — Analytics Dataset Generation
CSVs in `aggregated/`: `all_events.csv`, `model_releases.csv`, `gpu_releases.csv`, `funding_rounds.csv`, `datacenter_events.csv`, `outages.csv`

---

## 6. Repository Structure

```
ai-infrastructure-intelligence/
├── .github/workflows/
│   ├── collect.yml
│   ├── classify.yml
│   ├── entity_extract.yml
│   ├── aggregate.yml
│   ├── stats.yml
│   ├── readme_update.yml
│   └── weekly_report.yml
├── data/
│   ├── raw/            ← one JSON per day
│   └── processed/      ← classified JSON per day
├── events/
│   └── events_master.json
├── aggregated/         ← 6 CSV files
├── reports/weekly/
├── snapshots/
├── badges/
├── scripts/
│   ├── collect.py
│   ├── classify.py
│   ├── entity_extract.py
│   ├── aggregate.py
│   ├── stats.py
│   └── readme_update.py
├── requirements.txt
└── README.md
```

---

## 7. Technology Stack

| Layer | Tool | Why |
|-------|------|-----|
| Collection | `feedparser`, `requests` | Zero-cost RSS + HTTP |
| Classification (MVP) | Keyword rules | No API cost |
| Classification (V2) | Claude API | High accuracy |
| Entity extraction | `spaCy` + regex | Free, fast |
| Storage | Flat JSON/CSV in Git | $0 database |
| Automation | GitHub Actions | Free 2,000 min/month |
| Dashboard (Phase 2) | GitHub Pages + Chart.js | Free hosting |
| News source | NewsAPI free tier | 100 req/day |
| Reports | Jinja2 | Markdown templating |

---

## 8. Data Sources

### 8.1 Company Blogs (RSS)
- OpenAI, Anthropic, Google DeepMind, NVIDIA, AWS, Azure, Meta AI

### 8.2 News Feeds
- TechCrunch AI, VentureBeat AI, The Verge AI, NewsAPI.org

### 8.3 Research Feeds
- arXiv cs.AI, arXiv cs.LG, Papers With Code

---

## 9. Data Models

### 9.1 Base Event
`event_id`, `title`, `source`, `date`, `category`, `company`, `product`, `location`, `summary`, `url`

### 9.2 Funding Event (extends base)
`startup`, `amount_usd`, `round_type`, `investors`

### 9.3 Datacenter Event (extends base)
`company`, `location`, `capacity_mw`, `investment_usd`

### 9.4 Model Release (extends base)
`company`, `model_name`, `model_type`, `release_date`, `open_source`

---

## 10. Non-Functional Requirements

| Requirement | Target |
|-------------|--------|
| Reliability | 95%+ workflow success rate |
| Commits | 5–9/day (min 4 guaranteed) |
| Annual | 365+ green days |
| Scale | 100K+ records |
| Cost | $0 total |
| Automation | 100% unattended |

---

## 11. Phase Roadmap

### Phase 1 — MVP (Week 1–2) ← **CURRENT**
- Repository structure + all scripts + all 7 workflows + deploy

### Phase 2 — LLM Upgrade (Week 3–4)
- Claude API classification + confidence scores + GitHub Pages dashboard

### Phase 3 — Reports (Month 2)
- Jinja2 weekly reports + README top-5 daily + monthly rollups

### Phase 4 — Analytics (Month 3)
- Streamlit dashboard + forecasting + semantic search

---

## 12. Success Metrics

| Metric | Target |
|--------|--------|
| Daily execution | 95%+ workflow success |
| Dataset growth | 100+ events/month |
| Commits | 5+/day, 4 guaranteed |
| Annual streak | 365 green squares |
| Maintenance | Zero after deploy |

---

## 13. Implementation Notes

### 13.1 Commit Pattern
`checkout → run script → git add -A → git diff --staged --quiet || git commit → git push`

### 13.2 Free Tier Budget
7 workflows × 30 days = 210 runs × ~5 min = ~1,050 min (under 2,000 limit)

### 13.3 Rate Limits
NewsAPI: 100 req/day. Exponential backoff → fallback to RSS-only.

### 13.4 Secrets
`NEWS_API_KEY` and `CLAUDE_API_KEY` (Phase 2) as GitHub repo secrets. Never committed.

---

> **AIID PRD v2.0 · Built to run forever, automatically.**
