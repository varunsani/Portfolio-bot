# Race Engineer — RAG assistant for varunsani.vercel.app

A self-updating RAG chatbot embedded in Varun Sani's portfolio. It answers
questions about Varun from his portfolio, resume, research paper, GitHub
projects, and the external links he references — nothing else, with
citations that scroll to the exact section.

## What's in this repo

```
backend/                FastAPI RAG service (retrieval, generation, memory)
portfolio-site/index.html   Your actual portfolio — widget CSS/JS already inlined, deploy as-is
.github/workflows/      CI/CD: auto-scrape, auto-reindex, auto-deploy (backend + portfolio)
```

**`portfolio-site/index.html` is your real portfolio file** with the
widget's CSS inlined in `<head>` and its JS inlined right before `</body>`,
deferred with `setTimeout(init, 1200)` after `window.onload` so it never
competes with the page's own load/Lighthouse timing. Before using it:
replace the placeholder in the inlined script —
`window.RACE_ENGINEER_API_URL = "https://your-app.railway.app"` — with your
real deployed backend URL. There's nothing else to copy in or wire up —
this single file is your whole deployable site.

## How the self-updating part works

You said you'll change the portfolio later and want the bot to pick that up
automatically — here's the loop that does it, with no manual reindexing:

1. **`deploy-portfolio.yml`** runs whenever `portfolio-site/index.html`
   changes: Vercel's own Git integration deploys the change on its own (no
   token or CLI step needed — see DEPLOYMENT.md §5), and this workflow just
   waits ~45s for that to land, then immediately triggers
   `scrape-and-reindex.yml` — no waiting for the next cron tick after you've
   actually edited the site.
2. **`scrape-and-reindex.yml`** also runs every 6 hours on its own (in case
   the live site changes some other way). It re-scrapes
   `https://varunsani.vercel.app` live, and only commits
   `backend/content/portfolio.md` / `links.json` back to the repo **if the
   text actually changed**.
3. That commit touches `backend/content/**`, which triggers **`reindex.yml`**:
   it re-embeds everything (including a fresh pull of your resume from
   Google Drive — see below) and does a zero-downtime swap into Postgres
   (old vectors stay live and queryable until the new batch is fully
   verified, then it flips atomically — see the comment block at the top of
   `backend/scripts/index_knowledge.py`).
4. Citations always point at `#anchor` links on the live site, so once the
   new content is live at those anchors, citation chips keep scrolling to
   the right place.
5. **Resume changes are on a separate clock.** A Drive-only resume edit
   never touches git, so nothing above triggers for it — `reindex.yml` also
   runs on its own once-a-day schedule as a safety net, so a resume update
   shows up within ~24h even with no portfolio change at all. Click **Run
   workflow** on `reindex.yml` for an instant pickup instead.

If you'd rather not wait, click **Run workflow** on `scrape-and-reindex.yml`
in the Actions tab any time.

## Retrieval strategy (why it's not just cosine similarity)

- **Hybrid search**: vector similarity (70%) + BM25 keyword score (30%),
  so exact figures like "85% accuracy" or "RMSE" aren't lost to embedding fuzz.
- **MMR (Maximum Marginal Relevance)** re-ranking removes near-duplicate
  chunks (e.g. a project described in both the portfolio and the resume).
- **Contextual compression** trims each retrieved chunk down to its most
  query-relevant sentences before it ever reaches the LLM, so the prompt
  stays small and signal-dense.
- A **similarity threshold** (0.3 by default) means an out-of-scope question
  returns "no data" instead of a hallucinated answer.

## Persona

95% of the voice is just a sharp, professional person giving a clear
briefing — plain sentences, no corporate filler. F1 language shows up as an
occasional word choice, never a full metaphor-per-sentence bit. See the
system prompt in `backend/app/services/generator.py` if you want to tune
the ratio further.

## Before you deploy — two things only you can do

1. **Groq API key**: sign up at console.groq.com (free tier) and grab a key.
2. **Railway project**: create one Postgres service (with the `vector`
   extension available — Railway's Postgres image supports it) and one Redis
   service.

Resume is no longer a manual step — `index_knowledge.py` fetches it fresh
from Google Drive (`RESUME_URL`) on every reindex run, so updating your
resume on Drive is enough; nothing to re-commit. Make sure that file's
sharing setting is **"Anyone with the link can view"** (the default for a
private/restricted file will 404 or redirect to a login page for the CI
runner, same as it would for any logged-out visitor). It handles Drive's
virus-scan interstitial for larger files, and falls back to the last
successfully-downloaded copy (cached at `backend/content/resume.pdf`,
gitignored) if a given run's download fails, so one bad network blip
doesn't take resume content out of the index. Section splitting is by
detected font size/weight, not a hardcoded list of header words — so
renaming or adding resume sections (Leadership, Volunteering, whatever)
needs no code change either.

Full step-by-step in [DEPLOYMENT.md](./DEPLOYMENT.md).

## Local development

```bash
cd backend
cp .env.example .env   # fill in DATABASE_URL, REDIS_URL, GROQ_API_KEY
pip install -r requirements.txt
python scripts/scrape_portfolio.py     # refresh content/portfolio.md
python scripts/index_knowledge.py      # build the vector index
uvicorn app.main:app --reload
```

Then open `portfolio-site/index.html` directly, or serve it with any static
server — the widget CSS/JS are already inlined, so nothing extra to link.
Just make sure the inlined `window.RACE_ENGINEER_API_URL` points at
`http://localhost:8000` while developing.

## Evaluation

```bash
python backend/scripts/evaluate.py --url https://your-app.railway.app
```

Prints each test question, the answer, citations, and latency, so you can
eyeball faithfulness/relevance before wiring up full RAGAS metrics (optional
— see the docstring in `evaluate.py`).

## Non-negotiables this build respects

- Never answers from the LLM's general knowledge about Varun — only retrieved context.
- Every substantive answer carries at least one citation chip.
- Citation clicks scroll to the exact `#anchor`, not just the top of the page.
- Widget loads lazily after the page is interactive — doesn't touch Lighthouse's TTI.
- Conversation history persists per session (last 10 turns, Redis, 6h TTL).
- Reindexing is zero-downtime (pending → verify → atomic swap → delete old).
- Rate limited: 30 requests/minute/IP, F1-flavoured 429 message.
- All secrets live in environment variables / GitHub Secrets, never in code.
- CORS locked to `https://varunsani.vercel.app` in production.
