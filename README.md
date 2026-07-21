# 🧠 AI Infrastructure Intelligence Dataset (AIID)

![Total Events](badges/total_events.svg)
![Last Updated](badges/last_updated.svg)

> An automated data collection and intelligence platform tracking the AI infrastructure ecosystem.
> **Last checked: 2026-07-21 at 16:24 UTC**

---

## 📊 Dataset Stats

| Metric | Value |
|--------|-------|
| **Total Events** | 4801 |
| **Events (7 days)** | 723 |
| **Events (30 days)** | 3011 |

### Category Distribution

| Category | Count |
|----------|-------|
| OTHER | 2897 |
| MODEL_RELEASE | 569 |
| RESEARCH_BREAKTHROUGH | 546 |
| FUNDING_EVENT | 278 |
| GPU_RELEASE | 265 |
| DATACENTER_EXPANSION | 100 |
| POLICY_REGULATION | 71 |
| OUTAGE | 59 |
| SERVICE_UPDATE | 16 |


### Top Companies

| Company | Events |
|---------|--------|
| Intel | 437 |
| NVIDIA | 245 |
| AI | 230 |
| OpenAI | 207 |
| Anthropic | 182 |
| Amazon | 129 |
| Meta | 79 |
| Modal | 72 |
| Microsoft | 69 |
| Google | 68 |


---

## 🔥 Latest Events

### ElevenLabs now lets authors create and publish audiobooks on its own platform
- **Date**: Wed, 26 Fe
- **Category**: `FUNDING_EVENT`
- **Company**: N/A
- **Source**: [TechCrunch AI](https://techcrunch.com/2025/02/25/elevenlabs-is-now-letting-authors-create-and-publish-audiobooks-on-its-own-platform/)
- **Summary**: Voice AI company ElevenLabs is now letting authors publish AI-generated audiobooks on its own Reader app, TechCrunch has learned and the company confirmed. The announcement comes days after the company partnered with Spotify for AI-narrated audiobooks.

### NVIDIA and AWS Collaborate to Bring AI to Production at Scale
- **Date**: Wed, 24 Ju
- **Category**: `GPU_RELEASE`
- **Company**: NVIDIA
- **Source**: [NVIDIA Blog](https://blogs.nvidia.com/blog/nvidia-aws-ai-production-scale/)
- **Summary**: Building AI systems at scale is demanding, requiring low-latency inference, fast vector search, strong GPU price-performance and infrastructure that can grow without multiplying operational complexity. NVIDIA’s latest work with Amazon Web Services (AWS) addresses each of those constraints.

### RIFT-Bench: Dynamic Red-teaming For Agentic AI Systems
- **Date**: Wed, 24 Ju
- **Category**: `MODEL_RELEASE`
- **Company**: RIFT-Bench: Dynamic Red-teaming
- **Source**: [arXiv cs.AI](https://arxiv.org/abs/2606.23927)
- **Summary**: arXiv:2606.23927v1 Announce Type: new 
Abstract: Agentic AI systems powered by large language models (LLMs) are rapidly evolving into autonomous decision-making systems, exposing attack vectors beyond those of traditional LLM vulnerabilities. Existing security evaluations are often tied to specif...

### Neuro-Symbolic Drive: Rule-Grounded Faithful Reasoning for Driving VLAs
- **Date**: Wed, 24 Ju
- **Category**: `RESEARCH_BREAKTHROUGH`
- **Company**: CoT
- **Source**: [arXiv cs.AI](https://arxiv.org/abs/2606.23938)
- **Summary**: arXiv:2606.23938v1 Announce Type: new 
Abstract: Driving VLA models incorporating Chain-of-Thought (CoT) reasoning are attractive because they leverage pretrained VLM representations and expose intermediate decisions in natural language, yet current rationales often lack the step-by-step decision...

### Critique of Agent Model
- **Date**: Wed, 24 Ju
- **Category**: `MODEL_RELEASE`
- **Company**: Large Language Model
- **Source**: [arXiv cs.AI](https://arxiv.org/abs/2606.23991)
- **Summary**: arXiv:2606.23991v1 Announce Type: new 
Abstract: What is an agent? What constitutes agency?



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