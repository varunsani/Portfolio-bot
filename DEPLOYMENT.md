# Deployment guide

This guide walks through deploying your own copy of this project after
forking or cloning the repo. It assumes you're setting this up for a
portfolio site of your own — swap in your own URLs, usernames, and repo
name wherever an example value appears below.

## 1. Push the repo to your own GitHub account

```bash
git clone <this-repo-url>
cd Portfolio-bot
git remote set-url origin https://github.com/<your-username>/<your-repo-name>.git
git push -u origin main
```

If you're starting from a zip instead of a clone, `git init` first, then
`git add . && git commit -m "Initial commit"` before adding your remote.

**Don't commit `venv/` or `.mypy_cache/`** if your zip/clone includes them —
they're local tooling artifacts, not part of the app. Add them to
`.gitignore` and `git rm -r --cached venv .mypy_cache` if they're already
tracked.

## 2. Provision Railway services

1. Create a new Railway project.
2. Add a **PostgreSQL** plugin/service. Once it's up, open its query console
   and run `CREATE EXTENSION IF NOT EXISTS vector;` once (the app also does
   this automatically on startup — see `app/db/connection.py` — so this is
   just a sanity check if something later fails).
3. Add a **Redis** plugin/service.
4. Add a new service from your GitHub repo, root directory `backend/`,
   using the provided `Dockerfile`.
5. Copy the connection strings Railway gives you for Postgres and Redis —
   you'll need both the internal (`.railway.internal`) and public
   ("Connect" tab → public network) versions; see step 3 for which goes
   where.

## 3. Set environment variables

**On Railway** (backend service → Variables) — use the **internal**
connection strings here, since the app runs inside the same Railway
project as Postgres/Redis:
- `DATABASE_URL` — internal Postgres URL
- `REDIS_URL` — internal Redis URL
- `GROQ_API_KEY` — from console.groq.com
- `GROQ_MODEL` — a currently-available Groq model name (check
  console.groq.com/docs/models — free-tier model names get deprecated and
  replaced periodically, so don't assume `.env.example`'s example value or
  `config.py`'s hardcoded default are still live by the time you deploy)
- `FRONTEND_ORIGIN_PROD` — your deployed portfolio's URL, e.g.
  `https://yourname.vercel.app` (must match exactly, no trailing slash —
  this is what the backend's CORS check compares against)
- everything else in `.env.example` has sensible defaults

**On GitHub** (your repo → Settings → Secrets and variables → Actions) —
use the **public** connection strings here instead, since GitHub Actions
runners are outside Railway's private network and can't reach the
`.railway.internal` hosts:
- `DATABASE_URL` — public Postgres URL (Postgres service → Connect tab)
- `GROQ_API_KEY`
- `REDIS_URL` — public Redis URL (Redis service → Connect tab)
- `RAILWAY_TOKEN` — Railway account → Tokens → create a token scoped to
  this project (used by `deploy.yml` to redeploy the backend on push)

`GITHUB_TOKEN` is provided automatically by GitHub Actions for
`deploy-portfolio.yml` — you don't need to create it yourself.

## 4. Point the indexer and scraper at your own content

Before the first index, update `backend/scripts/index_knowledge.py`'s
constants near the top of the file:
- `RESUME_DRIVE_VIEW_URL` — your resume's Google Drive share link, set to
  **"Anyone with the link can view."** The resume is fetched live from
  this URL on every indexing run — it's never committed to the repo, so
  updating the file on Drive is the only step needed to keep it current.
- `RESEARCH_PAPER_URL` — if you have one; remove the research-paper
  indexing step if not.
- `GITHUB_USERNAME` — your GitHub username (repos are auto-discovered from
  here, nothing to list manually).

Then update `backend/scripts/scrape_portfolio.py`'s portfolio URL constant
to your deployed portfolio URL, and `backend/content/links.json` to the
external links your own portfolio references. `content/*.md` files are
generated output, not hand-maintained — don't edit them directly, they get
overwritten on the next scrape/reindex.

## 5. First index

Either let `reindex.yml` run (it triggers on any push touching
`backend/content/**`, which your first commit already does), or run it
locally once:

```bash
cd backend
python scripts/index_knowledge.py
python scripts/verify_index.py
```

Check `GET /health` on your Railway URL afterwards — `vectors_indexed`
should be well above zero.

## 6. Wire up the chat widget on your portfolio

The widget's CSS and JS are already inlined into `portfolio-site/index.html`.
Before deploying, set the backend URL near the bottom of the file to your
real Railway app:

```html
window.RACE_ENGINEER_API_URL = "https://<your-railway-app>.up.railway.app";
```

Deploy that HTML file to Vercel (or any static host) as you normally
would. If you're on Vercel with its Git integration connected, a push to
`main` on the `portfolio-site/**` path deploys automatically — that's what
`deploy-portfolio.yml` waits on before triggering a scrape (see next
section).

## 7. Confirm the self-updating loop

1. Change something on your live portfolio, commit under
   `portfolio-site/**`, and push to `main`.
2. **`deploy-portfolio.yml`** fires, waits 45s for Vercel's own deploy to
   land, then triggers **`scrape-and-reindex.yml`** for you — no manual
   step needed here if you're on Vercel with Git integration.
3. `scrape-and-reindex.yml` re-scrapes your now-live portfolio and commits
   an updated `portfolio.md`/`links.json` if the content actually changed,
   which kicks off **`reindex.yml`** automatically (path filter on
   `backend/content/**`).
4. Ask the bot about the change in the widget — it should answer with the
   new content and a citation pointing at the right anchor.

If you're not using Vercel's Git integration (a different host, or a
manual deploy step), skip step 2 and instead manually run
**Scrape Portfolio & Trigger Reindex** from the Actions tab once your
new content is actually live.

Beyond that first push, `scrape-and-reindex.yml`'s own hourly cron and
`reindex.yml`'s own hourly cron both run independently as safety nets —
the former catches drift you forgot to push, the latter catches a
resume update on Google Drive, which never touches git and wouldn't
otherwise trigger a rebuild.

## 8. Redeploying backend code changes

`deploy.yml` redeploys the backend to Railway automatically whenever a
push touches `backend/app/**`, `backend/Dockerfile`, or
`backend/requirements.txt`. You can also trigger it manually from the
Actions tab (`workflow_dispatch`) if you need to force a redeploy without
a code change — e.g. after rotating `RAILWAY_TOKEN`.

## Troubleshooting

- **`vector` extension errors on Railway Postgres**: some Railway Postgres
  images need the extension allow-listed; check Railway's Postgres docs
  for "pgvector" if `CREATE EXTENSION` fails.
- **CORS errors in the browser console**: double check
  `FRONTEND_ORIGIN_PROD` matches your deployed domain exactly (no trailing
  slash) — see `ALLOWED_ORIGINS` in `app/main.py`.
- **Empty answers / "no data on that" for everything**: check `GET /health`
  and confirm `vectors_indexed > 0`; if it's 0, the indexing job likely
  failed — check the Action logs for a Groq/embedding error (a stale
  `GROQ_MODEL` name is a common cause — see step 3), or a
  `DATABASE_URL`/`REDIS_URL` pointed at an internal host from GitHub
  Actions instead of the public one.
- **Resume missing from answers**: check the reindex Action log for a
  Drive fetch warning. Usually means the Drive file's sharing setting
  isn't "Anyone with the link," or `RESUME_DRIVE_VIEW_URL` needs updating
  after re-sharing the file.
- **Widget not appearing on the live site**: confirm the inlined
  `RACE_ENGINEER_API_URL` was actually updated before the last deploy, and
  that your host's build actually shipped the updated HTML file.
- **429 rate-limit errors during normal use**: the limit is 30
  requests/minute/IP (`chat.py`); if that's too aggressive for your use
  case, adjust the `@limiter.limit(...)` decorator on the `/chat` route.
- **A reindex seems to have "forgotten" an ongoing conversation**: this is
  expected, not a bug — see the README's "self-updating" section on why
  session memory is deliberately wiped the moment a reindex ships
  genuinely new content.
