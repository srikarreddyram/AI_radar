# 🧠 AI Infrastructure Intelligence Dataset (AIID)

![Total Events](badges/total_events.svg)
![Last Updated](badges/last_updated.svg)

> An automated data collection and intelligence platform tracking the AI infrastructure ecosystem.
> **Last checked: 2026-08-14 at 15:54 UTC**

---

## 📊 Dataset Stats

| Metric | Value |
|--------|-------|
| **Total Events** | 8065 |
| **Events (7 days)** | 675 |
| **Events (30 days)** | 3048 |

### Category Distribution

| Category | Count |
|----------|-------|
| OTHER | 4869 |
| MODEL_RELEASE | 953 |
| RESEARCH_BREAKTHROUGH | 929 |
| FUNDING_EVENT | 470 |
| GPU_RELEASE | 394 |
| DATACENTER_EXPANSION | 206 |
| OUTAGE | 115 |
| POLICY_REGULATION | 105 |
| SERVICE_UPDATE | 24 |


### Top Companies

| Company | Events |
|---------|--------|
| Intel | 682 |
| NVIDIA | 396 |
| AI | 389 |
| OpenAI | 347 |
| Anthropic | 296 |
| Amazon | 199 |
| Meta | 144 |
| Google | 125 |
| Microsoft | 119 |
| Modal | 115 |


---

## 🔥 Latest Events

### Do Models Fake Alignment Without Clear Consequences?
- **Date**: Wed, 29 Ju
- **Category**: `RESEARCH_BREAKTHROUGH`
- **Company**: Sheshadri et al.
- **Source**: [arXiv cs.AI](https://arxiv.org/abs/2607.24758)
- **Summary**: arXiv:2607.24758v1 Announce Type: new 
Abstract: Large language models are capable of recognizing evaluation contexts and altering their behavior to reflect evaluator expectations rather than typical deployment behaviors, a phenomenon known as alignment faking. The reasons why models fake alignme...

### Beyond Memory: A Templated Substrate for Heterogeneous Collaborative Knowledge Work with LLM Agents
- **Date**: Wed, 29 Ju
- **Category**: `MODEL_RELEASE`
- **Company**: Karpathy
- **Source**: [arXiv cs.AI](https://arxiv.org/abs/2607.24759)
- **Summary**: arXiv:2607.24759v1 Announce Type: new 
Abstract: Research projects, educational efforts, and adjacent knowledge work accumulate findings, decisions, and reasoning that future collaborators rarely recover. The parts most useful to that work, including dead ends and walked-back claims, are routinel...

### Kernel Forge: An Agent Harness for LLM-based Generation and Optimization of CUDA Kernels
- **Date**: Wed, 29 Ju
- **Category**: `GPU_RELEASE`
- **Company**: NVIDIA
- **Source**: [arXiv cs.AI](https://arxiv.org/abs/2607.24762)
- **Summary**: arXiv:2607.24762v1 Announce Type: new 
Abstract: Machine learning models are increasingly embedded in everyday software, and most of their runtime is spent in a small set of compute kernels such as matrix multiplication, convolution, and normalization. Optimizing these kernels is one of the most ...

### CaRE Compute-aware Remasking Evaluation Protocol for Masked Diffusion Language Models
- **Date**: Wed, 29 Ju
- **Category**: `RESEARCH_BREAKTHROUGH`
- **Company**: CaRE
- **Source**: [arXiv cs.AI](https://arxiv.org/abs/2607.24763)
- **Summary**: arXiv:2607.24763v1 Announce Type: new 
Abstract: Masked diffusion language models (MDLMs) are advancing rapidly, yet the evaluation standards needed to reliably interpret their progress have not kept pace. Despite MDLMs becoming competitive with autoregressive language models, seven recent remask...

### GrocLM: Grocery Category Recommendation in E-Commerce with Large Language Models
- **Date**: Wed, 29 Ju
- **Category**: `RESEARCH_BREAKTHROUGH`
- **Company**: GROCLM
- **Source**: [arXiv cs.AI](https://arxiv.org/abs/2607.24764)
- **Summary**: arXiv:2607.24764v1 Announce Type: new 
Abstract: The rapid growth of online grocery shopping requires recommendation systems that capture cyclical purchasing behavior and diverse user intents. Traditional item-level methods face scalability and accuracy challenges, motivating category-level recom...



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