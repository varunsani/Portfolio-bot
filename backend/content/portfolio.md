# Varun Sani Portfolio
Source: https://varunsani.vercel.app


## [Formation lap — Building race pace] Varun Sani

[Formation lap — Building race pace](#about) GAP BEHIND 0.3 · STRAT 6 · MODE: RACING
[Formation lap — Building race pace](#about) Hey, I'm a Computer Science engineer who somehow ended up loving both queueing theory and qualifying laps. I've been building things since I first got my hands on a keyboard and these days that means API backends, async architectures and machine learning pipelines that actually survive contact with real, messy data. Off the clock, I'm probably reading a paper, chasing a proof, or watching a race, sometimes all three, badly, at once.

## [Formation lap — Building race pace] Radio check. Loud and clear.

[Formation lap — Building race pace](#about) A live feed from the cockpit. Straight from the driver to the pit wall.

## [Formation lap — Building race pace] Building race pace

[Formation lap — Building race pace](#about) Systems design, machine learning and a Computer Science degree that pointed me at both.
[Formation lap — Building race pace](#about) I'm a Computer Science engineer interested in building intelligent software systems, from backend infrastructure and distributed applications to machine learning and AI.
[Formation lap — Building race pace](#about) I graduated with a B.Tech in Computer Science & Engineering from IIT Palakkad and somewhere in the middle of coursework I realised the parts I actually looked forward to were the ones that felt like puzzles: proving a bound, tracing a race condition, figuring out why a model was confidently wrong. That has become the throughline of everything since. I work across software development and machine learning , building async APIs, real-time pub/sub architectures and ML pipelines designed to hold up once they meet data that hasn't been cleaned up for them.
[Formation lap — Building race pace](#about) My interests span machine learning, AI and software engineering , with a particular fascination for systems design and the architectural decisions that make software reliable, scalable and useful in the real world. Alongside coursework, I spent a year chasing an open question in combinatorics, which eventually turned into a research paper and taught me more about patience than anything in a classroom did.
[Formation lap — Building race pace](#about) Off the clock, I race through problems the way I'd race through Eau Rouge, flat out, but never blind. If something looks like it should have a clean, elegant answer, I will not let it go until I've found one.
[Formation lap — Building race pace](#about) Hyderabad, India · reachable anywhere, working async.
[Formation lap — Building race pace](#about) Teamwork: I believe the best results happens when the "pit wall" (whole team) and the "driver" (team individual's) are in perfect sync, communicating openly, trusting each other's instincts and knowing that every great result comes from a united effort.
[Formation lap — Building race pace](#about) Strategy: I plan like a race strategist . I map out the long game, anticipate disruptions and know exactly when to commit to the undercut or wait for the overcut.
[Formation lap — Building race pace](#about) Determination: I approach every challenge like a wet qualifying session . Adaptable, relentless and always pushing for the gap, even when the conditions are unpredictable.

## [The Pit Crew — Everything under the hood] Everything under the hood

[The Pit Crew — Everything under the hood](#skills) Languages, frameworks, databases and the toolkit that makes the engineering possible.

## [Race Stints — Time on track so far] Time on track so far

[Race Stints — Time on track so far](#experience) One internship, two very different problems and a healthy respect for messy data.

## [Race Stints — Time on track so far] Machine Learning Engineer Intern

[Race Stints — Time on track so far](#experience) Two parallel briefs, same toolkit: work out who's about to leave, and price the risk of who might default. I ran both end to end, from a spreadsheet of raw numbers to a model I'd actually trust.
[Race Stints — Time on track so far](#experience) The first brief was employee attrition. HR loses real money every time someone leaves unexpectedly, in recruiting costs, lost productivity, and institutional knowledge walking out the door, so the question was whether the signals already sitting in HR data, tenure, satisfaction scores, overtime, promotions, could actually flag who's at risk before they hand in notice. The second was loan default risk in peer-to-peer lending, where individual lenders fund individual borrowers directly with no bank absorbing the risk in between, so the platform needed to price that risk accurately from a borrower's profile alone, not guess at it after the fact.
[Race Stints — Time on track so far](#experience) Built classification pipelines across Logistic Regression, Decision Tree, Random Forest, XGBoost and a 3-layer Neural Network to predict employee attrition on a 15,000-row, 40-feature HR dataset. None of the five were the obvious winner going in, so I benchmarked all of them, then pushed the best performer from ~72% to ~85% accuracy and 0.68 to ~0.82 F1 through hyperparameter tuning and threshold optimization.
[Race Stints — Time on track so far](#experience) Developed regression ensembles for loan default risk in the online P2P lending market on a 10,000-row, 60-feature dataset, cutting RMSE by ~18% via feature selection, stacking and weighted averaging, validated through 5-fold cross-validation across RMSE, MAE and R², so the number wasn't just a lucky split.
[Race Stints — Time on track so far](#experience) Ran end-to-end preprocessing: median/mode imputation for 12% missing values, SMOTE for a 15% minority class and StandardScaler normalization, then engineered 8 interaction features for the attrition model that alone contributed a 5% lift in F1 score, the kind of gain that only shows up once you stop trusting the raw columns.

## [The Garage — Fresh off the lift] Fresh off the lift

[The Garage — Fresh off the lift](#projects) From a self-updating RAG pipeline to highly scalable async backends, every system is stress-tested against real edge cases. GitHub links are at the bottom of each write-up.

## [The Garage — Fresh off the lift] Self-Updating RAG Portfolio Assistant

[The Garage — Fresh off the lift](#projects) A portfolio chatbot that never goes stale. It scrapes my live site, pulls my resume from Google Drive, and updates its own knowledge base automatically — so it always knows exactly what I'm working on.
[The Garage — Fresh off the lift](#projects) Most portfolio bots are hardcoded or require manual database updates. I built this one to be completely self-sufficient: a GitHub Actions workflow re-scrapes the live site and fetches the resume from Drive on a schedule, re-embeds the content, and swaps the knowledge base atomically in Postgres. The result is a production-grade RAG system that stays current without me touching a line of code.
[The Garage — Fresh off the lift](#projects) Combined dense vector search (70%) with BM25 keyword scoring (30%) and Maximum Marginal Relevance (MMR) re-ranking to handle both semantic questions and exact-match details like numbers and names, with a 0.3 similarity cutoff to block hallucinated answers on out-of-scope questions.
[The Garage — Fresh off the lift](#projects) Designed a zero-downtime reindexing pipeline: GitHub Actions fetch fresh resume and portfolio content, generate embeddings via Groq, and atomically swap the active vectors in Postgres only after verification, so the chatbot never sees a partial or empty database.
[The Garage — Fresh off the lift](#projects) Shipped anchor-linked citations so users can jump directly to the source on the site, backed by 10-turn Redis session memory (6h TTL) and 30 req/min/IP rate limiting to prevent quota abuse.
[The Garage — Fresh off the lift](#projects) Deployed as a fully Dockerized FastAPI service on Railway with automatic resume ingestion from Google Drive, handling the large-file "virus scan" interstitial that normally breaks automated Drive downloads.

## [The Garage — Fresh off the lift] Real-Time Severe Weather Alerting System

[The Garage — Fresh off the lift](#projects) I built this to get rid of client-side polling entirely. The server should tell you when the weather turns, not the other way around. It's also where most of the async concepts I'd learned in isolation finally had to work together at once.
[The Garage — Fresh off the lift](#projects) Most weather apps make the client do all the work. The phone keeps asking the server "anything new?" every few minutes, which is slow, wasteful and doesn't scale once thousands of clients are polling independently. The brief I set myself was to invert that so the server knows the moment conditions turn severe and pushes that update to every subscribed client instantly, with nobody having to ask.
[The Garage — Fresh off the lift](#projects) Replaced client-side polling with server-pushed alerts: a dedicated poller container queries the free Open-Meteo API for each subscribed location once per 5-minute cycle and publishes classified conditions over Redis Pub/Sub.
[The Garage — Fresh off the lift](#projects) Scaled live delivery horizontally by giving each API replica its own WebSocket forwarder that subscribes to the shared alert stream and pushes only to its locally connected clients, built to run behind a load balancer across N replicas.
[The Garage — Fresh off the lift](#projects) Designed a configurable severity engine with hand-tunable thresholds across four condition categories at three escalating tiers and rounded coordinates to ~1.1 km so nearby subscriptions share a single polled point.
[The Garage — Fresh off the lift](#projects) Verified the system end to end in Postman before trusting it. Exercised the REST subscription endpoints for correct status codes and validation errors and used Postman's WebSocket support to open a live connection, subscribe to a location and confirm pushed alert payloads arrived in the right shape within the expected 5-minute cycle.

## [The Garage — Fresh off the lift] URL Shortener

[The Garage — Fresh off the lift](#projects) A deliberately over-engineered URL shortener, because the interesting part was never the redirect, it was everything protecting it. Rate limiting, caching and revocable auth all had to earn their place, not just exist for the resume line.
[The Garage — Fresh off the lift](#projects) On the surface, shortening a URL is a solved problem, just a lookup table from a short code to a long one. The brief I actually set for myself was what a URL shortener looks like once you take it seriously in production: who's allowed to create links, how you stop abuse, how you revoke access instantly and how you keep redirects fast under load, rather than a toy version that only ever does the insert and the redirect.
[The Garage — Fresh off the lift](#projects) Structured a fully asynchronous URL shortener into router, middleware, service and repository layers, generating unique 6-character base62 short codes with bcrypt-hashed credentials in an ACID-compliant PostgreSQL schema.
[The Garage — Fresh off the lift](#projects) Authenticated requests with 15-minute JWT access tokens and 7-day refresh tokens, blacklisting revoked tokens in Redis with matched TTLs and capping abuse at 10 creations and 60 redirects per minute per IP.
[The Garage — Fresh off the lift](#projects) Lowered database load by caching redirect lookups in Redis for 1 hour and tracked click analytics across daily, weekly and monthly windows via non-blocking asynchronous counters.
[The Garage — Fresh off the lift](#projects) Validated the whole flow manually in Postman before automating it, the full JWT lifecycle from login through access token, refresh and revocation, the rate limiter correctly returning a 429 on the 11th creation request within a minute and cache behavior staying consistent across repeated redirect calls to the same short code.

## [The Wind Tunnel — First podium] First podium

[The Wind Tunnel — First podium](#research) A paper accepted at ICTCS 2025, Pescara . First submission, first result.

## [The Wind Tunnel — First podium] Multipacking in Hypercubes

[The Wind Tunnel — First podium](#research) Undergraduate research into a six year old open question in combinatorics. I co-authored this alongside faculty at IIT Palakkad.
[The Wind Tunnel — First podium](#research) The field had a conjecture that broadcast domination, the cheapest way to cover every node in a network from a few broadcasting stations, never costs more than twice a related lower-bound measure called the multipacking number. Nobody had proven it in general and nobody had even found a single example of a growing network where that ratio actually got close to 2, the thing that would show the conjectured bound couldn't be improved. The brief we set ourselves was to find one.
[The Wind Tunnel — First podium](#research) Pinned down the multipacking number of the n -dimensional hypercube Q n to within a lower-order term, between ⌊ n /2⌋ and n /2 + O (√ n ), via a recursive construction that builds multipackings of larger hypercubes out of smaller ones.
[The Wind Tunnel — First podium](#research) Bounded the construction from above using Spencer's discrepancy theorem, a classic result usually applied to combinatorial set systems, repurposed here to cap how many points a hypercube multipacking can hold.
[The Wind Tunnel — First podium](#research) Showed hypercubes are exactly the family the conjecture needed: γ b ( Q n ) / mp ( Q n ) → 2 as n grows, the first known infinite family of connected graphs to reach that ratio.
[The Wind Tunnel — First podium](#research) Getting there meant a year of constructions that looked promising, only to break when we tried to extend them to the next dimension. Proof, like a good qualifying lap, mostly happens in the small corrections you make after you've already committed to the line.

## [Off Track — Cool-down lap thoughts] Cool-down lap thoughts

[Off Track — Cool-down lap thoughts](#beyond) The interests that keep the engineering honest and occasionally sneak into it.

## [Off Track — Cool-down lap thoughts] Engineering

[Off Track — Cool-down lap thoughts](#beyond) I read papers the way some people read the news, a running habit, not an assignment. Attention Is All You Need is the one I go back to most, mostly because it's rare to watch a single idea unseat an entire field's default architecture this cleanly. More recently, LoRA: Low-Rank Adaptation of Large Language Models stuck with me for the opposite reason. Not a new architecture, just a sharp observation about how little actually needs to change during fine-tuning and a genuinely elegant way to exploit it.

## [Off Track — Cool-down lap thoughts] Mathematics

[Off Track — Cool-down lap thoughts](#beyond) Ramanujan, Newton and Euler are the three I keep coming back to, not for any one result, but for how differently each of them arrived at the same kind of certainty. Three problems in particular I can't leave alone. The honeycomb conjecture : the proof that a hexagonal grid is the most efficient way to divide a flat surface into equal-area cells using the least total perimeter, which is exactly why bees build their combs that way and it took until 1999 for Thomas Hales to actually prove what bees seem to have known instinctively all along. Then, on the more absurd end of the same instinct, there's the actual published mathematics behind tying shoelaces, working out through combinatorics and calculus exactly which lacing patterns are provably the strongest and which are the shortest, because apparently no everyday habit is too small to deserve a proof. And the one that still genuinely blows my mind, Fermat's Last Theorem , the claim that a^n + b^n = c^n has no whole-number solutions for n greater than 2, scribbled by Fermat in a margin in 1637 with a proof he said was too long to fit. It took over 350 years and the eventual proof pulled in elliptic curves, modular forms and ideas that echo through modern physics to finally settle it. I'm nowhere near being able to follow the proof itself, but the fact that a seventeenth-century margin note ends up wired into some of the deepest structures in physics is the kind of interconnectedness I can't stop thinking about.

## [Off Track — Cool-down lap thoughts] Writing

[Off Track — Cool-down lap thoughts](#beyond) Mine tends to be spontaneous, a line shows up uninvited, usually nothing to do with whatever I was actually doing and I write it down before it leaves. Poems mostly, the occasional stretch toward something longer. That same instinct is exactly why I'm drawn to people who write on the spot, no drafts, no second attempt, just a person, a blank page and whatever a stranger just told them. Olivia Dodd , who sits with a typewriter in public and turns a total stranger's story into a finished poem in minutes, is the one I keep coming back to for that. Robert Frost's Stopping by Woods on a Snowy Evening is the poem I return to most. That last quiet turn, "but I have promises to keep," is the entire tension between wanting to stay in the interesting problem and knowing there's a deadline attached to it. I've felt that exact pull more times than I can count.

## [Off Track — Cool-down lap thoughts] Art

[Off Track — Cool-down lap thoughts](#beyond) Rooms I could get lost in for a full day, the Uffizi in Florence, the Louvre and Amsterdam's Rijksmuseum . I haven't stood in any of them yet. Visiting even one is the actual dream, not just a line on a list.

## [Off Track — Cool-down lap thoughts] Books & Films

[Off Track — Cool-down lap thoughts](#beyond) I'll start with the book. Ian McEwan's Atonement , worth it alone for the final-act rewrite, where you have to decide how much of what you just read was ever true. (Its film adaptation goes out in France under the far more dramatic title Reviens-moi , "come back to me," which honestly might be the better title.) My favourite film, full stop, is Christopher Nolan's The Prestige : "Are you watching closely?" is doing all the work in that opening line and the rest of the film is just the trick. Right behind it, Eternal Sunshine of the Spotless Mind : memory, love and the beautiful futility of trying to erase either. For evergreens I'll rewatch on any given evening, The Godfather and 12 Angry Men never miss.

## [Off Track — Cool-down lap thoughts] Music

[Off Track — Cool-down lap thoughts](#beyond) Michael Jackson on one end, La La Land's jazz score on the other and Carnatic classical filling the quiet in between.

## [Off Track — Cool-down lap thoughts] Chess

[Off Track — Cool-down lap thoughts](#beyond) Two gold medals at my college championships and a repertoire split cleanly down the middle: the Sicilian with Black, the Ruy Lopez with White. Three games I'll replay any time someone asks why I love this. Kasparov vs. Karpov , 1985 World Championship, Kasparov's octopus knight sits on d3 for eighteen moves before forcing a queen sacrifice out of pure positional pressure, as close to poetry as chess gets. Fischer vs. Spassky , 1972 Game 6, the game Pawn Sacrifice builds its whole third act toward, Fischer playing the Queen's Gambit for the first time in a serious game and dismantling Spassky with an opening he'd never touched before. And for technique alone, Carlsen vs. Karjakin , 2016 World Championship tiebreak, a queen sacrifice on move 50 that forces mate, still one of the cleanest finishes any World Championship has ever produced.
[Off Track — Cool-down lap thoughts](#beyond) If you'd like to play a game, find me on Chess.com . Always up for a match, connect there as well.

## [Off Track — Cool-down lap thoughts] Racing

[Off Track — Cool-down lap thoughts](#beyond) What draws me to F1 isn't the speed, it's the systems thinking. An undercut is a strategic bet made long before you have proof it'll pay off. The pit wall lives or dies by that call. Recognizing that rhythm, the interplay of pressure, timing and precision, is exactly what makes me a better engineer. Three drives I'll rewatch anytime. Max Verstappen's P17-to-P1 at São Paulo 2024 , Ayrton Senna's 1988 Monaco qualifying lap , a lap so far ahead of the field it was never even fully captured on camera and Michael Schumacher's 1995 win at Spa from 16th on the grid in mixed wet-dry conditions, on the same circuit this whole page is modelled after.

## [Post-Race Debrief — Got something worth racing toward? Box box box — let's talk.] Got something worth racing toward? Box box box — let's talk.
