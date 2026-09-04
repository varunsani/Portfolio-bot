# Deployment guide

This guide walks through deploying your own copy of this project after
forking or cloning the repo. It assumes you're setting this up for a
portfolio site of your own — swap in your own URLs, usernames, and
repo name wherever an example value appears below.

## 1. Push the repo to your own GitHub account

```bash
git clone <this-repo-url>
cd race-engineer-bot
git remote set-url origin https://github.com/<your-username>/<your-repo-name>.git
git push -u origin main
```

If you're starting from a zip instead of a clone, `git init` first, then
`git add . && git commit -m "Initial commit"` before adding your remote.

## 2. Provision Railway services

1. Create a new Railway project.
2. Add a **PostgreSQL** plugin/service. Once it's up, open its query console
   and run `CREATE EXTENSION IF NOT EXISTS vector;` once (the app also does
   this automatically on startup, so this is just a sanity check).
3. Add a **Redis** plugin/service.
4. Add a new service from your GitHub repo, root directory `backend/`,
   using the provided `Dockerfile`.
5. Copy the connection strings Railway gives you for Postgres and Redis —
   you'll need both the internal (`.railway.internal`) and public
   ("Connect" tab → public network) versions; see step 3 below for which
   goes where.

## 3. Set environment variables

**On Railway** (backend service → Variables) — use the **internal**
connection strings here, since the app runs inside the same Railway
project as Postgres/Redis:
- `DATABASE_URL` — internal Postgres URL
- `REDIS_URL` — internal Redis URL
- `GROQ_API_KEY` — from console.groq.com
- `GROQ_MODEL` — `llama3-8b-8192`
- `FRONTEND_ORIGIN_PROD` — your deployed portfolio's URL, e.g. `https://yourname.vercel.app`
- everything else in `.env.example` has sensible defaults

**On GitHub** (your repo → Settings → Secrets and variables → Actions) —
use the **public** connection strings here instead, since GitHub Actions
runners are outside Railway's private network and can't reach the
`.railway.internal` hosts:
- `DATABASE_URL` — public Postgres URL (Postgres service → Connect tab)
- `GROQ_API_KEY`
- `REDIS_URL` — public Redis URL (Redis service → Connect tab)
- `RAILWAY_TOKEN` — Railway account → Tokens → create a token scoped to this project

## 4. Point the indexer at your own content

Before the first index, update `backend/scripts/index_knowledge.py`:
- `RESUME_DRIVE_VIEW_URL` — your resume's Google Drive share link, set to
  **"Anyone with the link can view."**
- `RESEARCH_PAPER_URL` — if you have one; delete the research-paper
  indexing step if not.
- `GITHUB_USERNAME` — your GitHub username (repos are auto-discovered from
  here, nothing to list manually).

Then update `backend/scripts/scrape_portfolio.py`'s `PORTFOLIO_URL` to your
deployed portfolio URL, and `backend/content/links.json` to the external
links your own portfolio references.

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

The widget's CSS and JS are already inlined into the portfolio HTML file.
Before deploying, set the placeholder near the bottom of your
HTML to your real backend URL:

```html
window.RACE_ENGINEER_API_URL = "https://<your-railway-app>.up.railway.app";
```

Deploy that HTML file to Vercel (or any static host) as you normally would.

## 7. Confirm the self-updating loop

1. Change something on your live portfolio and deploy it as usual.
2. In your repo's Actions tab, manually run **Scrape Portfolio & Trigger Reindex**.
3. It should commit an updated `portfolio.md` if content changed, which
   kicks off **Reindex Knowledge Base** automatically.
4. Ask the bot about the change in the widget — it should answer with the
   new content and a citation pointing at the right anchor.

The scheduled 1-hour cron on `scrape-and-reindex.yml` runs independently
after that, so you don't need to remember to trigger it manually going
forward. `reindex.yml` also runs its own 1-hour cron, since a resume update
on Google Drive never touches git and wouldn't otherwise trigger a rebuild.

## Troubleshooting

- **`vector` extension errors on Railway Postgres**: some Railway Postgres
  images need the extension allow-listed; check Railway's Postgres docs for
  "pgvector" if `CREATE EXTENSION` fails.
- **CORS errors in the browser console**: double check
  `FRONTEND_ORIGIN_PROD` matches your deployed domain exactly (no trailing slash).
- **Empty answers / "no data on that" for everything**: check `GET /health`
  and confirm `vectors_indexed > 0`; if it's 0, the indexing job likely
  failed — check the Action logs for a Groq/embedding error, or a
  `DATABASE_URL`/`REDIS_URL` pointed at an internal host from GitHub Actions
  (see step 3 above).
- **Resume missing from answers**: check the reindex Action log for a
  Drive fetch warning. Usually means the Drive file's sharing setting isn't
  "Anyone with the link," or `RESUME_DRIVE_VIEW_URL` needs updating after
  re-sharing the file.
- **Widget not appearing on the live site**: confirm the inlined
  `RACE_ENGINEER_API_URL` was actually updated before the last deploy, and
  that your host's build actually shipped the updated HTML file.