# Race Engineer — RAG Assistant for varunsani.vercel.app

A self-updating Retrieval-Augmented Generation (RAG) chatbot embedded directly in [Varun Sani's portfolio](https://varunsani.vercel.app/). It answers visitor questions using only Varun's own portfolio, resume, research paper, GitHub projects, and referenced external links — never from the LLM's general knowledge — and every substantive answer carries a citation chip that scrolls straight to the source section.

## Table of contents

- [Architecture at a glance](#architecture-at-a-glance)
- [Repository layout](#repository-layout)
- [How the self-updating pipeline works](#how-the-self-updating-pipeline-works)
- [Retrieval strategy](#retrieval-strategy)
- [Persona](#persona)
- [Tech stack](#tech-stack)
- [API](#api)
- [Local development](#local-development)
- [Deployment](#deployment)
- [Evaluation](#evaluation)
- [Design guarantees](#design-guarantees)

## Architecture at a glance

```
┌────────────────────┐      GitHub Actions       ┌──────────────────────┐
│  portfolio-site/    │  ───(scrape + reindex)──▶ │  backend/content/     │
│  index.html         │                            │  portfolio.md, links │
│  (Vercel, static)   │◀──── widget calls /chat ── │  .json               │
└─────────┬───────────┘                            └──────────┬───────────┘
          │ fetch()                                            │ embed
          ▼                                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│                    FastAPI backend (Railway, Docker)                    │
│  routers/chat.py → services/rag_pipeline.py                            │
│     ├─ retriever.py   → hybrid vector + BM25 search, MMR, compression  │
│     ├─ embedder.py    → sentence-transformers embeddings               │
│     ├─ generator.py   → Groq LLM call with the Race Engineer persona   │
│     └─ memory.py      → Redis-backed conversation history (6h TTL)     │
│  Postgres + pgvector  → knowledge_base table, zero-downtime reindex    │
└────────────────────────────────────────────────────────────────────────┘
```

## Repository layout

```
backend/                       FastAPI RAG service (retrieval, generation, memory)
├── app/
│   ├── main.py                 App factory, CORS, rate-limit handler
│   ├── config.py                Pydantic settings (env-driven)
│   ├── db/connection.py         Postgres/pgvector pool + init
│   ├── models/schemas.py        Request/response + knowledge chunk schemas
│   ├── routers/chat.py          POST /chat, GET /health
│   └── services/
│       ├── embedder.py          Embedding generation
│       ├── retriever.py         Hybrid search, MMR, contextual compression
│       ├── generator.py         Groq LLM call + persona system prompt
│       ├── memory.py            Redis conversation history
│       └── rag_pipeline.py      Orchestrates retrieval → generation → citations
├── scripts/
│   ├── scrape_portfolio.py      Scrapes the live site into content/portfolio.md
│   ├── index_knowledge.py       Embeds + zero-downtime swap into Postgres
│   ├── verify_index.py          Sanity-checks the index after a build
│   └── evaluate.py              Ad hoc quality/latency check against a live URL
├── content/
│   ├── portfolio.md             Scraped portfolio content (source of truth)
│   └── links.json               External links referenced by the portfolio
├── requirements.txt
├── Dockerfile
└── .env.example

portfolio-site/
└── index.html                   The real portfolio — widget CSS/JS already inlined, deploy as-is

.github/workflows/
├── deploy-portfolio.yml         Waits for Vercel's deploy, then triggers scrape-and-reindex
├── scrape-and-reindex.yml       Re-scrapes the live site every 6h; commits only on real changes
├── reindex.yml                  Re-embeds + zero-downtime swap; also runs daily as a safety net
└── deploy.yml                   Backend deploy workflow

DEPLOYMENT.md                    Full step-by-step production setup
```

**`portfolio-site/index.html` is the real, deployable portfolio.** The widget's CSS is inlined in `<head>` and its JS is inlined right before `</body>`, deferred with `setTimeout(init, 1200)` after `window.onload` so it never competes with the page's own load or Lighthouse timing. There is nothing else to wire up — this single file is the whole static site. Before deploying, set the inlined placeholder to the real backend URL:

```html
window.RACE_ENGINEER_API_URL = "https://<your-backend-url>";
```

## How the self-updating pipeline works

The bot's knowledge stays in sync with the live portfolio with no manual reindexing:

1. **`deploy-portfolio.yml`** runs whenever `portfolio-site/index.html` changes. Vercel's own Git integration deploys the change independently (no token or CLI step needed — see `DEPLOYMENT.md` §5); this workflow just waits ~45s for that deploy to land, then triggers `scrape-and-reindex.yml` immediately, rather than waiting for the next scheduled run.
2. **`scrape-and-reindex.yml`** also runs on a 6-hour cron as a safety net for live-site changes made outside of a push (e.g. edits made directly in the Vercel dashboard). It re-scrapes `https://varunsani.vercel.app`, and only commits `backend/content/portfolio.md` / `links.json` back to the repo **if the text actually changed**.
3. That commit touches `backend/content/**`, which triggers **`reindex.yml`**: it re-embeds everything (including a fresh pull of the resume from Google Drive) and performs a **zero-downtime swap** into Postgres — new vectors are built and verified while the old ones stay live and queryable, then the swap flips atomically. See the comment block at the top of `backend/scripts/index_knowledge.py` for the exact sequence.
4. Citations always point at `#anchor` links on the live site, so once new content is live at those anchors, citation chips keep scrolling to the right place.
5. **Resume updates run on a separate clock.** A Drive-only resume edit never touches git, so nothing above fires for it — `reindex.yml` also runs on its own once-a-day schedule as a safety net, so a resume change surfaces within ~24h even with zero portfolio changes. Trigger **Run workflow** on `reindex.yml` for an instant pickup instead.

You can also trigger **Run workflow** on `scrape-and-reindex.yml` manually from the Actions tab at any time.

## Retrieval strategy

Retrieval is not plain cosine similarity — it's a small pipeline tuned for a narrow, factual knowledge base:

- **Hybrid search** — vector similarity (weighted 0.7) blended with BM25 keyword score (weighted 0.3), so exact figures like "85% accuracy" or "RMSE" survive embedding fuzz.
- **MMR (Maximum Marginal Relevance) re-ranking** (λ = 0.7) removes near-duplicate chunks — e.g. a project described in both the portfolio and the resume.
- **Contextual compression** trims each retrieved chunk down to its most query-relevant sentences before it reaches the LLM, keeping the prompt small and signal-dense.
- A **similarity threshold** (0.3 by default) means an out-of-scope question returns "no data" instead of a hallucinated answer.
- `top_k` defaults to 5 retrieved chunks per query; all of the above are tunable via environment variables (see `app/config.py`).

## Persona

The system prompt (in `backend/app/services/generator.py`) gives the bot a "Race Engineer" voice: mostly a sharp, professional briefing in plain sentences with no corporate filler, with F1 language showing up as an occasional word choice rather than a metaphor in every sentence. Tune the ratio there if it drifts too far either way.

## Tech stack

| Layer | Choice |
|---|---|
| API framework | FastAPI + Uvicorn |
| LLM | Groq (`openai/gpt-oss-120b` by default, configurable via `GROQ_MODEL`) |
| Embeddings | sentence-transformers |
| Vector store | PostgreSQL + `pgvector` |
| Keyword search | rank-bm25 |
| Session memory | Redis (last 10 turns, 6h TTL) |
| Rate limiting | slowapi (30 requests/minute/IP) |
| Resume parsing | pdfplumber / pypdf |
| Hosting | Railway (backend, Docker) + Vercel (static portfolio site) |
| CI/CD | GitHub Actions (scrape, reindex, deploy triggers) |

## API

```
POST /chat
  { "message": "<string, 1-1000 chars>", "session_id": "<string, 1-128 chars>" }
  → { "answer": "<string>", "citations": [{ "text", "url", "anchor" }], "latency_ms": <int> }

GET /health
  → { "status": "ok", "vectors_indexed": <int> }
```

CORS is locked to `frontend_origin_prod` (plus `localhost:3000` / `localhost:5500` for local dev) in `app/main.py`. Rate-limit responses return HTTP 429 with an in-persona message.

## Local development

```bash
cd backend
cp .env.example .env   # fill in DATABASE_URL, REDIS_URL, GROQ_API_KEY
pip install -r requirements.txt
python scripts/scrape_portfolio.py     # refresh content/portfolio.md
python scripts/index_knowledge.py      # build the vector index
uvicorn app.main:app --reload
```

Then open `portfolio-site/index.html` directly, or serve it with any static file server — the widget's CSS/JS are already inlined, so there's nothing extra to link. Just make sure the inlined `window.RACE_ENGINEER_API_URL` points at `http://localhost:8000` while developing.

## Deployment

Full step-by-step instructions — provisioning Railway (Postgres + `pgvector`, Redis), setting environment variables and GitHub Secrets, connecting Vercel to Git, running the first index, and confirming the self-updating loop end to end — live in **[DEPLOYMENT.md](./DEPLOYMENT.md)**.

Two things only you can configure before deploying:

1. **Groq API key** — sign up at [console.groq.com](https://console.groq.com) (free tier) and grab a key.
2. **Railway project** — one Postgres service with the `vector` extension available, and one Redis service.

The resume is not a manual step: `index_knowledge.py` fetches it fresh from Google Drive (`RESUME_URL`) on every reindex run, so updating the resume on Drive is enough — nothing to re-commit. The Drive file's sharing setting must be **"Anyone with the link can view"**; a restricted file will 404 or redirect to a login page for the CI runner, same as it would for a logged-out visitor. The fetch handles Drive's virus-scan interstitial for larger files, and falls back to the last successfully-downloaded copy (cached at `backend/content/resume.pdf`, gitignored) if a given run's download fails, so a single bad network blip doesn't take resume content out of the index. Section splitting is by detected font size/weight rather than a hardcoded list of header words, so renaming or adding resume sections needs no code change.

## Evaluation

```bash
python backend/scripts/evaluate.py --url https://<your-deployed-backend>
```

Runs a fixed set of test questions against a live deployment and prints each question, the answer, its citations, and latency — enough to eyeball faithfulness and relevance before wiring up full RAGAS-style metrics (optional; see the docstring in `evaluate.py`).

## Design guarantees

- Never answers from the LLM's general knowledge about Varun — only from retrieved context.
- Every substantive answer carries at least one citation chip.
- Citation clicks scroll to the exact `#anchor`, not just the top of the page.
- The widget loads lazily after the page is interactive — it never touches Lighthouse's TTI.
- Conversation history persists per session (last 10 turns, Redis, 6h TTL).
- Reindexing is zero-downtime: pending → verify → atomic swap → delete old.
- Rate limited to 30 requests/minute/IP, with an in-persona 429 message.
- All secrets live in environment variables / GitHub Secrets — never in code.
- CORS is locked to `https://varunsani.vercel.app` in production.