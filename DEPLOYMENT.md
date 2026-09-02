# Deployment guide

## 1. Push this repo to GitHub

```bash
cd race-engineer-bot
git init
git add .
git commit -m "Initial commit: Race Engineer RAG chatbot"
git branch -M main
git remote add origin https://github.com/varunsani/<new-repo-name>.git
git push -u origin main
```

## 2. Provision Railway services

1. Create a new Railway project.
2. Add a **PostgreSQL** plugin/service. Once it's up, open its query console
   and run `CREATE EXTENSION IF NOT EXISTS vector;` once (the app also does
   this automatically on startup, so this is just a sanity check).
3. Add a **Redis** plugin/service.
4. Add a new service from your GitHub repo, root directory `backend/`,
   using the provided `Dockerfile`.
5. Copy the connection strings Railway gives you for Postgres and Redis.

## 3. Set environment variables

**On Railway** (backend service → Variables):
- `DATABASE_URL` — from the Postgres service
- `REDIS_URL` — from the Redis service
- `GROQ_API_KEY` — from console.groq.com
- `GROQ_MODEL` — `llama3-8b-8192`
- `FRONTEND_ORIGIN_PROD` — `https://varunsani.vercel.app`
- everything else in `.env.example` has sensible defaults

**On GitHub** (repo → Settings → Secrets and variables → Actions):
- `DATABASE_URL`
- `GROQ_API_KEY`
- `REDIS_URL`
- `RAILWAY_TOKEN` — Railway account → Tokens → create a token scoped to this project

## 4. First index

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

## 5. Deploy the portfolio (Vercel) — connected to Git, no tokens needed

Your existing Vercel project (`varunsani.vercel.app`) was deployed via
drag-and-drop, not connected to a GitHub repo — connect it once and Vercel
handles every future deploy on its own:

1. **Push this repo to GitHub** first if it isn't already there (this
   `race-engineer-bot` folder as the repo root, containing both `backend/`
   and `portfolio-site/`).
2. In the Vercel dashboard, open your existing project, click **Connect
   Git** (top right), authorize the Vercel GitHub App if prompted, and pick
   this repo.
3. In **Settings → General → Root Directory**, set it to `portfolio-site`
   and save. This tells Vercel that folder — not the repo root — is what
   gets deployed.
4. In the same **Settings → General**, confirm **Framework Preset** is
   **Other** (plain static HTML, no build step, no output directory needed).
5. Before your first Git-connected deploy, open `portfolio-site/index.html`
   and set the inlined placeholder near the bottom to your real backend URL:
   ```html
   window.RACE_ENGINEER_API_URL = "https://<your-railway-app>.up.railway.app";
   ```
   then commit and push that change.

That's it — no `VERCEL_TOKEN`, no API keys, nothing to add as a GitHub
secret for the deploy itself. From here, `deploy-portfolio.yml` only waits
for Vercel's own deploy to land, then triggers `scrape-and-reindex.yml` —
so editing your portfolio and pushing is the entire workflow.

## 6. Confirm the self-updating loop

1. Edit something in `portfolio-site/index.html` and push to `main`.
2. Check Vercel's dashboard — it should show a new deployment starting on
   its own within a few seconds of the push.
3. Watch **Sync Chatbot After Portfolio Push** run in the Actions tab of
   your GitHub repo — it waits ~45s then kicks off **Scrape Portfolio &
   Trigger Reindex** automatically.
4. That should commit an updated `portfolio.md` if content changed, which
   kicks off **Reindex Knowledge Base**.
5. Ask the bot about the change in the widget — it should answer with the
   new content and a citation pointing at the right anchor.

The scheduled cron on `scrape-and-reindex.yml` (every 6 hours) still runs
independently, as a safety net for live-site changes that didn't go through
a push to this repo.

## Troubleshooting

- **`vector` extension errors on Railway Postgres**: some Railway Postgres
  images need the extension allow-listed; check Railway's Postgres docs for
  "pgvector" if `CREATE EXTENSION` fails.
- **CORS errors in the browser console**: double check
  `FRONTEND_ORIGIN_PROD` matches your Vercel domain exactly (no trailing slash).
- **Empty answers / "no data on that" for everything**: `GET /health` and
  confirm `vectors_indexed > 0`; if it's 0, the indexing job likely failed —
  check the Action logs for a Groq/embedding error.
- **Resume missing from answers**: check the reindex Action log for
  `WARNING: could not fetch resume from Google Drive`. Usually means the
  Drive file's sharing setting isn't "Anyone with the link," or the link in
  `RESUME_URL` (`backend/scripts/index_knowledge.py`) needs updating after
  re-sharing the file.
- **Vercel isn't auto-deploying on push**: in the Vercel project, check
  **Settings → Git** that a repo is actually connected (not just visited via
  "Connect Git" without finishing the flow), and that **Settings → General
  → Root Directory** is exactly `portfolio-site`.
