# Race Engineer — RAG assistant for varunsani.vercel.app

A self-updating RAG chatbot embedded in Varun Sani's portfolio. It answers
questions about Varun from his portfolio, resume, research paper, GitHub
projects, and the external links he references — nothing else, with
citations that scroll to the exact section.

## What's in this repo

```
backend/                                          FastAPI RAG service (retrieval, generation, memory)

portfolio-site/index.html   Your actual portfolio, widget already inlined
.github/workflows/                                CI/CD: auto-scrape, auto-reindex, auto-deploy
```

**`index.html` is your real portfolio file** with the
widget's CSS inlined in `<head>` and its JS inlined right before `</body>`,
deferred with `setTimeout(init, 1200)` after `window.onload` so it never
competes with the page's own load/Lighthouse timing. Before using it:
replace the placeholder in the inlined script —
`window.RACE_ENGINEER_API_URL = "https://your-app.railway.app"` — with your
real deployed backend URL, then upload it to Vercel in place of your
current `index.html`.

## How the self-updating part works

You said you'll change the portfolio later and want the bot to pick that up
automatically — here's the loop that does it, with no manual reindexing:

1. **`scrape-and-reindex.yml`** runs every 1 hours (and on manual trigger).
   It re-scrapes `https://varunsani.vercel.app` live, and only commits
   `backend/content/portfolio.md` / `links.json` back to the repo **if the
   text actually changed**.
2. That commit touches `backend/content/**`, which triggers **`reindex.yml`**:
   it re-embeds everything and does a zero-downtime swap into Postgres (old
   vectors stay live and queryable until the new batch is fully verified,
   then it flips atomically — see the comment block at the top of
   `backend/scripts/index_knowledge.py`).
3. Citations always point at `#anchor` links on the live site, so once the
   new content is live at those anchors, citation chips keep scrolling to
   the right place.

If you'd rather not wait up to 1 hours, click **Run workflow** on
`scrape-and-reindex.yml` in the Actions tab any time after a portfolio edit.

## Retrieval strategy (why it's not just cosine similarity)

- **Hybrid search with an "either" acceptance gate**: a chunk survives if
  its raw vector similarity clears one bar, OR its BM25 keyword score
  clears a separate bar — not one blended score with a single cutoff. This
  matters for queries with zero vocabulary overlap with the source text
  (e.g. "university" when the portfolio only ever says "Institute of
  Technology") — a blended score punishes those unfairly.
- **Thematic-name resilience**: F1 section names ("The Garage", "The Wind
  Tunnel") are resolved to plain labels (Projects, Research, ...) via
  `app/constants.py` before ever reaching the LLM's prompt, so the model
  never takes the theme literally. Those same plain labels are folded into
  each chunk's BM25 tokens (not its embedding) as keyword aliases, so a
  literal question like "what's his tech stack" still matches the Skills
  section by keyword even if "skills" never appears verbatim nearby.
- **MMR (Maximum Marginal Relevance)** re-ranking removes near-duplicate
  chunks (e.g. a project described in both the portfolio and the resume).
- **Contextual compression** trims each retrieved chunk down to its most
  query-relevant sentences before it ever reaches the LLM.

## Small talk vs. off-topic

Greetings, farewells, thanks, and date/time questions are matched by a
deterministic regex (`app/services/small_talk.py`) and answered directly —
with the real current date/time injected — without touching retrieval.
Anything else that retrieval turns up nothing for (unrelated general
knowledge, other people, current events) gets the fixed decline message
with no LLM call at all, so there's no path to a hallucinated answer.

## What gets scraped and indexed

- **Portfolio** — live-scraped on a schedule, anchor/section auto-detected
  from the page's own `id="..."` structure (see README "self-updating" section).
- **Resume** — prefers a `content/resume.pdf` committed directly in the
  repo (most reliable); falls back to fetching live from the Google Drive
  share link if no local file is present.
- **Research paper** — fetched directly from its public PDF URL.
- **GitHub** — every public, non-fork repo under the configured username is
  auto-discovered via the GitHub API (not a hardcoded list), and each
  repo's README is indexed. New repos are picked up on the next scheduled run.
- **Every external link found on the portfolio** — dispatched to a
  source-appropriate fetcher: chess.com ratings via their public stats API
  (the profile page itself is JS-rendered and returns no numbers to a plain
  scrape), YouTube via oEmbed for title/author, any other Google Drive link
  via the same PDF path as the resume, and a generic HTML text scrape for
  everything else (arXiv, Wikipedia, etc.). Heavily JS-rendered third-party
  sites (LinkedIn, IMDb, etc.) are still included but may yield thin text —
  there's no headless browser in this stack.

## Persona

95% of the voice is just a sharp, professional person giving a clear
briefing — plain sentences, no corporate filler. F1 language shows up as an
occasional word choice, never a full metaphor-per-sentence bit. See the
system prompt in `backend/app/services/generator.py` if you want to tune
the ratio further.

## Before you deploy — one thing left

1. **Groq API key**: sign up at console.groq.com (free tier) and grab a key.
2. **Railway project**: create one Postgres service (with the `vector`
   extension available — Railway's Postgres image supports it) and one Redis
   service.

`content/resume.pdf` is already bundled in this repo — no manual step needed there.

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
