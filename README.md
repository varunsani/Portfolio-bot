# Race Engineer — RAG assistant for varunsani.vercel.app

A self-updating RAG chatbot embedded in Varun Sani's portfolio. It answers
questions about Varun from his portfolio, resume, research paper, GitHub
projects, and the external links he references — nothing else, with
citations that scroll to the exact section. In conversation it introduces
itself as **Winter**, Varun's AI assist.

## What's in this repo

```
backend/                     FastAPI RAG service (retrieval, generation, memory)
portfolio-site/index.html    Varun's actual portfolio, widget already inlined
.github/workflows/           CI/CD: auto-scrape, auto-reindex, auto-deploy
```

**`index.html` is the real portfolio file**, with the widget's CSS inlined
in `<head>` and its JS inlined right before `</body>`, deferred with
`setTimeout(init, 1200)` after `window.onload` so it never competes with the
page's own load/Lighthouse timing. The backend URL is set near the bottom
of the inlined script:

```js
window.RACE_ENGINEER_API_URL = "https://portfolio-bot-production-0413.up.railway.app";
```

If you fork this for your own portfolio, replace that with your own
deployed backend URL before uploading the file to your host. Scroll-reveal
(`.reveal` sections) fires on `threshold: 0` plus a bottom `rootMargin`,
not a fixed intersection-ratio threshold — a section taller than the
viewport (common on phones for Projects/Beyond) would otherwise never
cross a percentage-based threshold and would stay invisible.

## How the self-updating part works

There's no manual reindexing step. Four GitHub Actions workflows chain
together to keep the bot's knowledge current:

1. **`deploy-portfolio.yml`** fires the moment `portfolio-site/**` is
   pushed to `main`. Vercel's own Git integration deploys the HTML (no
   tokens needed for that part); this workflow just waits 45s for that
   deploy to land, then triggers `scrape-and-reindex.yml` immediately
   instead of waiting for its next scheduled tick.
2. **`scrape-and-reindex.yml`** also runs on its own hourly cron (and on
   manual trigger). It re-scrapes `https://varunsani.vercel.app` live, and
   only commits `backend/content/portfolio.md` / `links.json` back to the
   repo **if the text actually changed**.
3. That commit touches `backend/content/**`, which triggers
   **`reindex.yml`**: it re-embeds everything and does a zero-downtime
   swap into Postgres (old vectors stay live and queryable until the new
   batch is fully verified, then it flips atomically — see the comment
   block at the top of `backend/scripts/index_knowledge.py`). It also runs
   its own hourly cron independent of any git push, since a resume update
   on Google Drive never touches git and wouldn't otherwise trigger a
   rebuild.
4. **`deploy.yml`** redeploys the backend to Railway whenever
   `backend/app/**`, `backend/Dockerfile`, or `backend/requirements.txt`
   change — code changes and content changes are deployed independently of
   each other.

Citations always point at `#anchor` links on the live site, so once new
content is live at those anchors, citation chips keep scrolling to the
right place. If you'd rather not wait for a scheduled run, click **Run
workflow** on `scrape-and-reindex.yml` in the Actions tab any time after a
portfolio edit.

The moment a reindex actually ships *different* content (compared by
content hash against the previous run), every in-flight session's Redis
conversation history is wiped (`memory.flush_all_sessions`). This isn't
about the knowledge base itself — Postgres already reindexes with zero
downtime either way. It's about the fact that a session's history holds
the assistant's own *previous replies*, which get replayed verbatim into
the next LLM call. If those replies were generated against now-stale
facts, the model can end up half-anchored to an old answer even though the
fresh retrieval context for the new question is correct. Sessions living
entirely between two reindexes are untouched.

## Retrieval strategy (why it's not just cosine similarity)

- **Hybrid candidate generation**: candidates come from two sources merged
  into one pool — pgvector cosine search (HNSW index, `m=16,
  ef_construction=64`) over a pool sized `top_k * candidate_pool_multiplier`,
  and a Postgres full-text-search pass (`to_tsvector`/`plainto_tsquery`
  against a GIN index) run in parallel. Vector-only candidate generation
  has a blind spot: a short, specific chunk can sit outside the top
  vector-similarity results whenever the pool also contains a lot of
  longer, topically-adjacent content (e.g. a referenced arXiv page that
  also uses the same vocabulary). The full-text pass guarantees an exact
  keyword hit isn't lost just because the embedding model didn't rank it
  as "similar" — see `retriever._fetch_keyword_candidates`.
- **"Either" acceptance gate**: a candidate survives if its raw vector
  cosine clears one bar, OR its normalized BM25 score clears a separate
  bar — not one blended score with a single cutoff. Primary-source content
  (portfolio, resume, research paper, GitHub) uses looser floors than
  chunks from referenced external links, which use stricter floors —
  external-link noise was the actual source of irrelevant citations, so
  only that gate got tightened rather than starving primary-source recall.
  A weighted score (vector/BM25 weighted) still ranks whatever clears the
  gate.
- **Project-diversity guarantee**: every chunk is tagged at indexing time
  with a best-guess `project_id`, based on real GitHub repo names/
  descriptions (not on matching inconsistent titles across
  portfolio/resume/README, which don't share a naming convention). Before
  final selection, at least one chunk per distinct `project_id` present in
  the accepted pool is guaranteed a slot, so a heavily-documented project
  (mentioned in portfolio + resume + README) can't silently crowd out one
  that's only mentioned once. This only ever acts on chunks that already
  passed the relevance gate, so an unrelated query (e.g. about skills)
  never gets polluted with an irrelevant project chunk.
- **Source-priority nudge**: a small score boost (`SOURCE_SCORE_BOOST`)
  applies to primary-content chunks over external-link chunks, so a page
  Varun merely links to from "Beyond" can't out-rank content that's
  actually about him on a close call.
- **Thematic-name resilience**: F1 section names ("The Garage", "The Wind
  Tunnel") are resolved to plain labels (Projects, Research, ...) via
  `app/constants.py` before ever reaching the LLM's prompt, derived
  directly from each section's real HTML `id`, so the model never takes
  the theme literally. Those same plain labels back the citation chips the
  user sees, so what the model reasons about and what's shown in the UI
  always agree. GitHub chunks get a repo-specific label (`Projects —
  reponame`) instead of a generic `Projects`, so multiple repos in one
  answer don't collapse into identical-looking citation chips.
- **MMR (Maximum Marginal Relevance)** re-ranking fills any remaining slots
  after the project-diversity guarantee, removing near-duplicate chunks
  (e.g. a project described in both the portfolio and the resume).
- **Contextual compression** trims each retrieved chunk down to its most
  query-relevant sentences before it ever reaches the LLM.
- Citation chips are deduped two ways — by normalized URL (scheme, `www.`,
  trailing slash, query string, and `#fragment` all stripped) and by
  visible label — so the same page, or two different anchors that render
  the same label, never show up twice (see `rag_pipeline._dedupe_citations`).

Current tuning lives entirely in `backend/app/config.py` — `top_k`,
`candidate_pool_multiplier`, the four `*_min_threshold*` floors,
`vector_weight`/`bm25_weight`, `mmr_lambda`, and `keyword_candidate_limit`
are all one-line changes there, with the reasoning for the current values
in the comments above each field.

## Small talk vs. off-topic

Greetings, farewells, thanks, and date/time questions are matched by a
deterministic regex (`app/services/small_talk.py`, capped at ~8 words so a
longer sentence starting with "hi" isn't misclassified) and answered
directly — with the real current date/time (IST) injected — without
touching retrieval. Anything else that retrieval turns up nothing for
(unrelated general knowledge, other people, current events) gets a fixed
decline reply with no LLM call at all, so there's no path to a
hallucinated answer.

## What gets scraped and indexed

- **Portfolio** — live-scraped on a schedule, anchor/section auto-detected
  from the page's own `id="..."` structure (see "self-updating" above).
- **Resume** — fetched live from a Google Drive share link on every
  indexing run. It is **not** committed to the repo; the only maintenance
  step is keeping the Drive file up to date and shared as "Anyone with the
  link can view."
- **Research paper** — fetched directly from its public PDF URL, extracted
  per-page so a single image/formula-heavy page failing to extract cleanly
  doesn't take the rest of the document down with it.
- **GitHub** — every public, non-fork repo under the configured username is
  auto-discovered via the GitHub API (not a hardcoded list); each repo
  gets at least one chunk (name + language + description) even with no
  README, so nothing goes entirely unrepresented. New repos are picked up
  on the next scheduled run.
- **Every external link found on the portfolio** (`content/links.json`) —
  dispatched to a source-appropriate fetcher: chess.com ratings via their
  public stats API (the profile page itself is JS-rendered and returns no
  numbers to a plain scrape), YouTube via the transcript API, any other
  Google Drive link via the same PDF path as the resume, and a generic
  HTML text scrape for everything else (arXiv, Wikipedia, etc.). Heavily
  JS-rendered third-party sites (LinkedIn, IMDb, etc.) are still included
  but may yield thin text — there's no headless browser in this stack.

## Persona

The assistant introduces itself as **Winter**, Varun's AI assist — a
sharp, professional colleague giving a clear briefing, not a themed
chatbot. Roughly 95% of the voice is plain, human sentences with no
corporate filler; F1 language shows up as an occasional word choice
("quick", "another lap", "an off"), never a full metaphor-per-sentence bit,
and never more than one per answer.

Built into the system prompt is a hard authorship boundary: only chunks
tagged `Source: research_paper` are Varun's own publication. Content under
`Beyond`/`external_link` — theorems, proofs, other people's papers Varun
merely reads about — must never be presented as his. Varun's actual paper
("Multipacking in Hypercubes", ICTCS 2025) and its four co-authors are
pinned as fixed facts the model anchors to, rather than something it's
expected to reconstruct correctly from retrieval alone every time.

See the full system prompt in `backend/app/services/generator.py` if you
want to tune the ratio or the ground rules further.

## Before you deploy — two things

1. **Groq API key**: sign up at console.groq.com (free tier) and grab a
   key. Check which model names are currently live on your account —
   Groq's free-tier model lineup changes over time, and `.env.example`'s
   suggested value may not match `config.py`'s current default
   (`groq_model`) by the time you read this.
2. **Railway project**: create one Postgres service (with the `vector`
   extension available — Railway's Postgres image supports it) and one
   Redis service.

Full step-by-step in [DEPLOYMENT.md](./DEPLOYMENT.md).

## Local development

```bash
cd backend
cp .env.example .env   # fill in DATABASE_URL, REDIS_URL, GROQ_API_KEY
pip install -r requirements.txt
python scripts/scrape_portfolio.py     # refresh content/portfolio.md
python scripts/index_knowledge.py      # build the vector index (also fetches the resume live)
uvicorn app.main:app --reload
```

## Evaluation

```bash
python backend/scripts/evaluate.py --url https://your-app.railway.app
```

Prints each test question, the answer, citations, and latency, so you can
eyeball faithfulness/relevance before wiring up full RAGAS metrics
(optional — see the docstring in `evaluate.py`).

## Non-negotiables this build respects

- Never answers from the LLM's general knowledge about Varun — only
  retrieved context.
- Every substantive answer carries at least one citation chip.
- Citation clicks scroll to the exact `#anchor`, not just the top of the page.
- Widget loads lazily after the page is interactive — doesn't touch
  Lighthouse's TTI.
- Conversation history persists per session (last `conversation_turns`
  turns, Redis, 6h TTL) — and is wiped for every session the moment a
  reindex actually changes underlying content, so no reply can be
  half-anchored to stale facts.
- Reindexing is zero-downtime: pending batch → verify → atomic swap →
  delete old.
- Rate limited: 30 requests/minute/IP, F1-flavoured 429 message
  ("Box box box. Too many requests. Slow down.").
- All secrets live in environment variables / GitHub Secrets, never in code.
- CORS locked to `FRONTEND_ORIGIN_PROD` in production (plus `localhost:3000`
  / `localhost:5500` for local dev).
