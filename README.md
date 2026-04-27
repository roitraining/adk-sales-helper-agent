# Sales Proposal Engine

A multi-agent AI assistant that prepares sales teams for prospect meetings. Given basic information about the seller and the prospect, it autonomously researches the prospect, then generates a personalized email and a browser-ready slide presentation — all in one conversation.

Built with [Google ADK](https://google.github.io/adk-docs/) and deployed to [Vertex AI Agent Engine](https://cloud.google.com/vertex-ai/generative-ai/docs/agent-engine/overview).

---

## What It Does

Start a conversation with the agent in Gemini Enterprise (or the Agent Engine Playground). It will ask you for:

- Your company name, description, and what you're selling
- The prospect's company name and website

Then it goes to work automatically:

1. Researches the prospect using live Google Search
2. Summarizes findings into a structured prospect brief
3. Writes a personalized introductory email
4. Builds a 6-slide HTML presentation (uploaded to Cloud Storage, browser-ready)
5. Generates a one-page executive summary leave-behind (also uploaded to Cloud Storage)
6. Delivers everything in a single formatted response with links

---

## Project Structure

```
sales-helper-agent/
├── app/
│   ├── agent.py                  # Root agent — gathers seller & prospect info
│   ├── agent_engine_app.py       # Agent Engine deployment wrapper
│   ├── config.py                 # Central config (env vars, model names, buckets)
│   ├── agents/
│   │   ├── pipeline.py           # Orchestrates the full agent pipeline
│   │   ├── research.py           # Prospects research via Google Search
│   │   ├── writer.py             # Synthesizes research into a structured prospect brief
│   │   ├── critique.py           # Quality-gates the brief; loops if it doesn't pass
│   │   ├── email_agent.py        # Writes personalized intro email
│   │   ├── presentation_agent.py # Generates HTML slide deck + uploads to GCS
│   │   ├── exec_summary_agent.py # Generates HTML executive summary + uploads to GCS
│   │   └── output_agent.py       # Assembles and delivers final results
│   └── tools/
│       ├── sales_info.py         # Saves seller/prospect info to session state
│       ├── context.py            # Reads session state for agents
│       └── gcs_upload.py         # Uploads HTML presentations to GCS
├── deployment/                   # Terraform infrastructure
├── notebooks/                    # Testing and evaluation notebooks
├── tests/                        # Unit, integration, and load tests
├── Makefile                      # Development commands
└── pyproject.toml                # Project dependencies
```

---

## Requirements

- **uv** — Python package manager — [Install](https://docs.astral.sh/uv/getting-started/installation/)
- **Google Cloud SDK** — [Install](https://cloud.google.com/sdk/docs/install)
- **A GCP project** with Vertex AI and Cloud Storage enabled
- **Two GCS buckets** — one for generated presentation assets, one for logs
- **ADC credentials** — run `gcloud auth application-default login`

---

## Quick Start

```bash
make install && make playground
```

Then open the local playground, select the `app` folder, and start a conversation.

---

## Configuration

All settings are in `app/config.py` and read from environment variables:

| Variable | Default | Description |
|---|---|---|
| `GOOGLE_CLOUD_PROJECT` | _(required)_ | GCP project ID |
| `GOOGLE_CLOUD_LOCATION` | `us-east4` | Vertex AI region |
| `ASSETS_BUCKET_NAME` | `tmp-adk-test-assets` | GCS bucket for generated presentations and executive summaries |
| `LOGS_BUCKET_NAME` | `tmp-adk-test-logs` | GCS bucket for ADK session artifacts |
| `CURRENT_MODEL` | _(see below)_ | Selects which model all agents use; defaults to `LITE_MODEL_NAME` |
| `PRO_MODEL_NAME` | `gemini-3.1-pro-preview` | Full-quality model (reserved for production) |
| `FAST_MODEL_NAME` | `gemini-3.1-flash-preview` | Fast, cost-effective model |
| `LITE_MODEL_NAME` | `gemini-3.1-flash-lite-preview` | Lightweight model used by default (lower latency and cost) |

Set these in your shell or a `.env` file before running locally.

---

## Commands

| Command | Description |
|---|---|
| `make install` | Install dependencies |
| `make playground` | Launch local dev environment (auto-reloads on save) |
| `make deploy` | Deploy to Vertex AI Agent Engine |
| `make register-gemini-enterprise` | Register deployed agent with Gemini Enterprise |
| `make test` | Run unit and integration tests |
| `make eval` | Run agent evaluation |
| `make setup-dev-env` | Provision GCP resources with Terraform |

---

## Deployment

```bash
gcloud config set project <your-project-id>
make deploy
```

The deploy script automatically passes `ASSETS_BUCKET_NAME` and `LOGS_BUCKET_NAME` as environment variables to the deployed agent. `GOOGLE_CLOUD_PROJECT` and `GOOGLE_CLOUD_LOCATION` are injected automatically by Agent Engine.

After deploying, register with Gemini Enterprise:

```bash
make register-gemini-enterprise
```

---

## Observability

Built-in telemetry exports to Cloud Trace, BigQuery, and Cloud Logging.
See the [observability guide](https://googlecloudplatform.github.io/agent-starter-pack/guide/observability) for queries and dashboards.

---

## Agent Flow

```
User
 │
 │  "I need to prep for a sales call with [Prospect]..."
 │
 ▼
┌─────────────────────────────────────────────────────┐
│ 1. Gather Info                                      │
│    Asks for seller info, prospect name & website    │
└─────────────────────┬───────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────┐
│ 2. Research Prospect                                │
│    Runs targeted Google searches on the prospect    │
└─────────────────────┬───────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────┐
│ 3. Summarize Research                               │
│    Distills findings into a structured brief        │
└─────────────────────┬───────────────────────────────┘
                      │
          ┌───────────┴───────────┐
          │   runs in parallel    │
          ▼                       ▼
┌──────────────────┐   ┌──────────────────────────────┐
│ 4. Write Email   │   │ 5. Build Presentation        │
│                  │   │    Generate HTML slide deck   │
│  Personalized    │   │    Upload to Cloud Storage    │
│  outreach email  │   └──────────────┬───────────────┘
│  ready to send   │                  │
└──────────────────┘                  ▼
          └───────────┬───────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────┐
│ 6. Deliver Results                                  │
│    📧 Email draft                                   │
│    📊 Presentation link (browser-ready)             │
└─────────────────────────────────────────────────────┘
                      │
                      ▼
                    User
```

