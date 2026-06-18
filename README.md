# 🧠 AI Infrastructure Intelligence Dataset (AIID)

![Total Events](badges/total_events.svg)
![Last Updated](badges/last_updated.svg)

> An automated data collection and intelligence platform tracking the AI infrastructure ecosystem.
> **Last checked: 2026-06-18 at 17:57 UTC**

---

## 📊 Dataset Stats

| Metric | Value |
|--------|-------|
| **Total Events** | 505 |
| **Events (7 days)** | 227 |
| **Events (30 days)** | 227 |

### Category Distribution

| Category | Count |
|----------|-------|
| OTHER | 266 |
| RESEARCH_BREAKTHROUGH | 81 |
| MODEL_RELEASE | 68 |
| FUNDING_EVENT | 31 |
| GPU_RELEASE | 24 |
| DATACENTER_EXPANSION | 13 |
| POLICY_REGULATION | 10 |
| OUTAGE | 10 |
| SERVICE_UPDATE | 2 |


### Top Companies

| Company | Events |
|---------|--------|
| Intel | 39 |
| NVIDIA | 27 |
| OpenAI | 24 |
| Amazon | 24 |
| AI | 22 |
| Anthropic | 19 |
| Modal | 14 |
| Microsoft | 14 |
| Google | 10 |
| Meta | 10 |


---

## 🔥 Latest Events

### ElevenLabs now lets authors create and publish audiobooks on its own platform
- **Date**: Wed, 26 Fe
- **Category**: `FUNDING_EVENT`
- **Company**: N/A
- **Source**: [TechCrunch AI](https://techcrunch.com/2025/02/25/elevenlabs-is-now-letting-authors-create-and-publish-audiobooks-on-its-own-platform/)
- **Summary**: Voice AI company ElevenLabs is now letting authors publish AI-generated audiobooks on its own Reader app, TechCrunch has learned and the company confirmed. The announcement comes days after the company partnered with Spotify for AI-narrated audiobooks.

### Harvard dropouts to launch ‘always on’ AI smart glasses that listen and record every conversation
- **Date**: Wed, 20 Au
- **Category**: `POLICY_REGULATION`
- **Company**: Meta
- **Source**: [TechCrunch AI](https://techcrunch.com/2025/08/20/harvard-dropouts-to-launch-always-on-ai-smart-glasses-that-listen-and-record-every-conversation/)
- **Summary**: After developing a facial-recognition app for Meta’s Ray-Ban glasses and doxing random people, two former Harvard students are now launching a startup that makes smart glasses with an always-on microphone.

### Meta to add 100MW of solar power from US gear
- **Date**: Wed, 20 Au
- **Category**: `DATACENTER_EXPANSION`
- **Company**: Meta
- **Source**: [TechCrunch AI](https://techcrunch.com/2025/08/20/meta-to-add-100-mw-of-solar-power-from-u-s-gear/)
- **Summary**: The social media company is adding another tranche of solar to power a new AI data center in South Carolina.

### New in Amazon Bedrock AgentCore: Build agents with broader knowledge and continuous learning
- **Date**: Wed, 17 Ju
- **Category**: `OTHER`
- **Company**: Amazon
- **Source**: [AWS ML Blog](https://aws.amazon.com/blogs/machine-learning/new-in-amazon-bedrock-agentcore-build-agents-with-broader-knowledge-and-continuous-learning/)
- **Summary**: Today we're introducing new capabilities on Amazon Bedrock AgentCore, the platform to build, connect, and optimize agents. In this post, we cover how these capabilities close each gap: connecting agents to organizational, web, and paid knowledge; helping teams find and fix what's going wrong in p...

### Beyond Parallel Sampling: Diverse Query Initialization for Agentic Search
- **Date**: Wed, 17 Ju
- **Category**: `RESEARCH_BREAKTHROUGH`
- **Company**: AWS
- **Source**: [arXiv cs.AI](https://arxiv.org/abs/2606.17209)
- **Summary**: arXiv:2606.17209v1 Announce Type: new 
Abstract: Test-time scaling for agentic search typically increases depth (i.e., more turns and tokens per trajectory) or breadth (i.e., more parallel rollouts). Here we focus on breadth scaling, showing that standard parallel sampling yields diminishing retu...



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