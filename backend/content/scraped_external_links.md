# Scraped External Link Content

Extracted content for every external link referenced in content/links.json.


## [Skills] Skills

Source: https://varunsani.vercel.app/#skills

[Skills](#skills) Languages: Python, C++, C Backend & APIs: FastAPI, REST, JWT Auth, WebSockets Databases & ORMs: PostgreSQL, Redis, MongoDB, SQLModel, Alembic ML & Data: scikit-learn, PyTorch, NumPy, Pandas, Matplotlib Tools & Platforms: Docker, Git, GitHub, Postman, Ubuntu, Jupyter Certifications: Introduction to Machine Learning (NPTEL), Machine Learning A-Z: AI, Python (Udemy) Languages, frameworks, databases
[Skills](#skills) PTEL), Machine Learning A-Z: AI, Python (Udemy) Languages, frameworks, databases and the toolkit that makes the engineering possible.

## [About] About

Source: https://varunsani.vercel.app/#about

[About](#about) GAP BEHIND 0.3 · STRAT 6 · MODE: RACING Hey, I'm a Computer Science engineer who somehow ended up loving both queueing theory and qualifying laps. I've been building things since I first got my hands on a keyboard and these days that means API backends, async architectures and machine learning pipelines that actually survive contact with real, messy data
[About](#about) d machine learning pipelines that actually survive contact with real, messy data Off the clock, I'm probably reading a paper, chasing a proof, or watching a race, sometimes all three, badly, at once. Buckle up · see the work → Box box box · say hi → A live feed from the cockpit. Straight from the driver to the pit wall. Systems design, machine learning and a Computer Science degree that pointed me at both
[About](#about) s design, machine learning and a Computer Science degree that pointed me at both I'm a Computer Science engineer interested in building intelligent software systems, from backend infrastructure and distributed applications to machine learning and AI
[About](#about) m backend infrastructure and distributed applications to machine learning and AI I graduated with a B.Tech in Computer Science & Engineering from IIT Palakkad and somewhere in the middle of coursework I realised the parts I actually looked forward to were the ones that felt like puzzles: proving a bound, tracing a race condition, figuring out why a model was confidently wrong. That has become the throughline of everything since
[About](#about) model was confidently wrong. That has become the throughline of everything since I work across software development and machine learning , building async APIs, real-time pub/sub architectures and ML pipelines designed to hold up once they meet data that hasn't been cleaned up for them
[About](#about) nes designed to hold up once they meet data that hasn't been cleaned up for them My interests span machine learning, AI and software engineering , with a particular fascination for systems design and the architectural decisions that make software reliable, scalable and useful in the real world
[About](#about) ral decisions that make software reliable, scalable and useful in the real world Alongside coursework, I spent a year chasing an open question in combinatorics, which eventually turned into a research paper and taught me more about patience than anything in a classroom did. Off the clock, I race through problems the way I'd race through Eau Rouge, flat out, but never blind
[About](#about) e through problems the way I'd race through Eau Rouge, flat out, but never blind If something looks like it should have a clean, elegant answer, I will not let it go until I've found one. Hyderabad, India · reachable anywhere, working async
[About](#about) it go until I've found one. Hyderabad, India · reachable anywhere, working async Teamwork: I believe the best results happens when the "pit wall" (whole team) and the "driver" (team individual's) are in perfect sync, communicating openly, trusting each other's instincts and knowing that every great result comes from a united effort. Strategy: I plan like a race strategist
[About](#about) great result comes from a united effort. Strategy: I plan like a race strategist I map out the long game, anticipate disruptions and know exactly when to commit to the undercut or wait for the overcut. Determination: I approach every challenge like a wet qualifying session . Adaptable, relentless and always pushing for the gap, even when the conditions are unpredictable.

## [Experience] Experience

Source: https://varunsani.vercel.app/#experience

[Experience](#experience) One internship, two very different problems and a healthy respect for messy data. Two parallel briefs, same toolkit: work out who's about to leave, and price the risk of who might default. I ran both end to end, from a spreadsheet of raw numbers to a model I'd actually trust. The first brief was employee attrition
[Experience](#experience) aw numbers to a model I'd actually trust. The first brief was employee attrition HR loses real money every time someone leaves unexpectedly, in recruiting costs, lost productivity, and institutional knowledge walking out the door, so the question was whether the signals already sitting in HR data, tenure, satisfaction scores, overtime, promotions, could actually flag who's at risk before they hand in notice
[Experience](#experience) ertime, promotions, could actually flag who's at risk before they hand in notice The second was loan default risk in peer-to-peer lending, where individual lenders fund individual borrowers directly with no bank absorbing the risk in between, so the platform needed to price that risk accurately from a borrower's profile alone, not guess at it after the fact
[Experience](#experience) risk accurately from a borrower's profile alone, not guess at it after the fact Built classification pipelines across Logistic Regression, Decision Tree, Random Forest, XGBoost and a 3-layer Neural Network to predict employee attrition on a 15,000-row, 40-feature HR dataset
[Experience](#experience) ral Network to predict employee attrition on a 15,000-row, 40-feature HR dataset None of the five were the obvious winner going in, so I benchmarked all of them, then pushed the best performer from ~72% to ~85% accuracy and 0.68 to ~0.82 F1 through hyperparameter tuning and threshold optimization
[Experience](#experience) cy and 0.68 to ~0.82 F1 through hyperparameter tuning and threshold optimization Developed regression ensembles for loan default risk in the online P2P lending market on a 10,000-row, 60-feature dataset, cutting RMSE by ~18% via feature selection, stacking and weighted averaging, validated through 5-fold cross-validation across RMSE, MAE and R², so the number wasn't just a lucky split
[Experience](#experience) ross-validation across RMSE, MAE and R², so the number wasn't just a lucky split Ran end-to-end preprocessing: median/mode imputation for 12% missing values, SMOTE for a 15% minority class and StandardScaler normalization, then engineered 8 interaction features for the attrition model that alone contributed a 5% lift in F1 score, the kind of gain that only shows up once you stop trusting the raw columns. View certificate · purple sector →

## [Projects] Projects

Source: https://varunsani.vercel.app/#projects

[Projects](#projects) From a self-updating RAG pipeline to highly scalable async backends, every system is stress-tested against real edge cases. GitHub links are at the bottom of each write-up. A portfolio chatbot that never goes stale. It scrapes my live site, pulls my resume from Google Drive, and updates its own knowledge base automatically — so it always knows exactly what I'm working on
[Projects](#projects) wn knowledge base automatically — so it always knows exactly what I'm working on Most portfolio bots are hardcoded or require manual database updates. I built this one to be completely self-sufficient: a GitHub Actions workflow re-scrapes the live site and fetches the resume from Drive on a schedule, re-embeds the content, and swaps the knowledge base atomically in Postgres. The result is a production-grade RAG system that stays current without me touching a line of code
[Projects](#projects) roduction-grade RAG system that stays current without me touching a line of code Combined dense vector search (70%) with BM25 keyword scoring (30%) and Maximum Marginal Relevance (MMR) re-ranking to handle both semantic questions and exact-match details like numbers and names, with a 0.3 similarity cutoff to block hallucinated answers on out-of-scope questions
[Projects](#projects) a 0.3 similarity cutoff to block hallucinated answers on out-of-scope questions Designed a zero-downtime reindexing pipeline: GitHub Actions fetch fresh resume and portfolio content, generate embeddings via Groq, and atomically swap the active vectors in Postgres only after verification, so the chatbot never sees a partial or empty database
[Projects](#projects) s only after verification, so the chatbot never sees a partial or empty database Shipped anchor-linked citations so users can jump directly to the source on the site, backed by 10-turn Redis session memory (6h TTL) and 30 req/min/IP rate limiting to prevent quota abuse. Deployed as a fully Dockerized FastAPI service on Railway with automatic resume ingestion from Google Drive, handling the large-file "virus scan" interstitial that normally breaks automated Drive downloads
[Projects](#projects) ge-file "virus scan" interstitial that normally breaks automated Drive downloads View on GitHub · overtake → I built this to get rid of client-side polling entirely. The server should tell you when the weather turns, not the other way around. It's also where most of the async concepts I'd learned in isolation finally had to work together at once. Most weather apps make the client do all the work
[Projects](#projects) had to work together at once. Most weather apps make the client do all the work The phone keeps asking the server "anything new?" every few minutes, which is slow, wasteful and doesn't scale once thousands of clients are polling independently. The brief I set myself was to invert that so the server knows the moment conditions turn severe and pushes that update to every subscribed client instantly, with nobody having to ask
[Projects](#projects) shes that update to every subscribed client instantly, with nobody having to ask Replaced client-side polling with server-pushed alerts: a dedicated poller container queries the free Open-Meteo API for each subscribed location once per 5-minute cycle and publishes classified conditions over Redis Pub/Sub
[Projects](#projects) n once per 5-minute cycle and publishes classified conditions over Redis Pub/Sub Scaled live delivery horizontally by giving each API replica its own WebSocket forwarder that subscribes to the shared alert stream and pushes only to its locally connected clients, built to run behind a load balancer across N replicas
[Projects](#projects) locally connected clients, built to run behind a load balancer across N replicas Designed a configurable severity engine with hand-tunable thresholds across four condition categories at three escalating tiers and rounded coordinates to ~1.1 km so nearby subscriptions share a single polled point. Verified the system end to end in Postman before trusting it
[Projects](#projects) ingle polled point. Verified the system end to end in Postman before trusting it Exercised the REST subscription endpoints for correct status codes and validation errors and used Postman's WebSocket support to open a live connection, subscribe to a location and confirm pushed alert payloads arrived in the right shape within the expected 5-minute cycle
[Projects](#projects) hed alert payloads arrived in the right shape within the expected 5-minute cycle A deliberately over-engineered URL shortener, because the interesting part was never the redirect, it was everything protecting it. Rate limiting, caching and revocable auth all had to earn their place, not just exist for the resume line. On the surface, shortening a URL is a solved problem, just a lookup table from a short code to a long one
[Projects](#projects) g a URL is a solved problem, just a lookup table from a short code to a long one The brief I actually set for myself was what a URL shortener looks like once you take it seriously in production: who's allowed to create links, how you stop abuse, how you revoke access instantly and how you keep redirects fast under load, rather than a toy version that only ever does the insert and the redirect
[Projects](#projects) load, rather than a toy version that only ever does the insert and the redirect Structured a fully asynchronous URL shortener into router, middleware, service and repository layers, generating unique 6-character base62 short codes with bcrypt-hashed credentials in an ACID-compliant PostgreSQL schema
[Projects](#projects) hort codes with bcrypt-hashed credentials in an ACID-compliant PostgreSQL schema Authenticated requests with 15-minute JWT access tokens and 7-day refresh tokens, blacklisting revoked tokens in Redis with matched TTLs and capping abuse at 10 creations and 60 redirects per minute per IP. Lowered database load by caching redirect lookups in Redis for 1 hour and tracked click analytics across daily, weekly and monthly windows via non-blocking asynchronous counters
[Projects](#projects) across daily, weekly and monthly windows via non-blocking asynchronous counters Validated the whole flow manually in Postman before automating it, the full JWT lifecycle from login through access token, refresh and revocation, the rate limiter correctly returning a 429 on the 11th creation request within a minute and cache behavior staying consistent across repeated redirect calls to the same short code.

## [Research] Research

Source: https://varunsani.vercel.app/#research

[Research](#research) A paper accepted at ICTCS 2025, Pescara . First submission, first result. Undergraduate research into a six year old open question in combinatorics. I co-authored this alongside faculty at IIT Palakkad
[Research](#research) question in combinatorics. I co-authored this alongside faculty at IIT Palakkad The field had a conjecture that broadcast domination, the cheapest way to cover every node in a network from a few broadcasting stations, never costs more than twice a related lower-bound measure called the multipacking number
[Research](#research) sts more than twice a related lower-bound measure called the multipacking number Nobody had proven it in general and nobody had even found a single example of a growing network where that ratio actually got close to 2, the thing that would show the conjectured bound couldn't be improved. The brief we set ourselves was to find one
[Research](#research) njectured bound couldn't be improved. The brief we set ourselves was to find one Pinned down the multipacking number of the n -dimensional hypercube Q n to within a lower-order term, between ⌊ n /2⌋ and n /2 + O (√ n ), via a recursive construction that builds multipackings of larger hypercubes out of smaller ones
[Research](#research) construction that builds multipackings of larger hypercubes out of smaller ones Bounded the construction from above using Spencer's discrepancy theorem, a classic result usually applied to combinatorial set systems, repurposed here to cap how many points a hypercube multipacking can hold. Showed hypercubes are exactly the family the conjecture needed: γ b ( Q n ) / mp ( Q n ) → 2 as n grows, the first known infinite family of connected graphs to reach that ratio
[Research](#research) n grows, the first known infinite family of connected graphs to reach that ratio Getting there meant a year of constructions that looked promising, only to break when we tried to extend them to the next dimension. Proof, like a good qualifying lap, mostly happens in the small corrections you make after you've already committed to the line. Read the paper · DRS wide open → ORCID · fast lap ↗

## [Beyond] Beyond

Source: https://varunsani.vercel.app/#beyond

[Beyond](#beyond) The interests that keep the engineering honest and occasionally sneak into it. I read papers the way some people read the news, a running habit, not an assignment. Attention Is All You Need is the one I go back to most, mostly because it's rare to watch a single idea unseat an entire field's default architecture this cleanly
[Beyond](#beyond) o watch a single idea unseat an entire field's default architecture this cleanly More recently, LoRA: Low-Rank Adaptation of Large Language Models stuck with me for the opposite reason. Not a new architecture, just a sharp observation about how little actually needs to change during fine-tuning and a genuinely elegant way to exploit it
[Beyond](#beyond) lly needs to change during fine-tuning and a genuinely elegant way to exploit it Ramanujan, Newton and Euler are the three I keep coming back to, not for any one result, but for how differently each of them arrived at the same kind of certainty. Three problems in particular I can't leave alone
[Beyond](#beyond) at the same kind of certainty. Three problems in particular I can't leave alone The honeycomb conjecture : the proof that a hexagonal grid is the most efficient way to divide a flat surface into equal-area cells using the least total perimeter, which is exactly why bees build their combs that way and it took until 1999 for Thomas Hales to actually prove what bees seem to have known instinctively all along
[Beyond](#beyond) mas Hales to actually prove what bees seem to have known instinctively all along Then, on the more absurd end of the same instinct, there's the actual published mathematics behind tying shoelaces, working out through combinatorics and calculus exactly which lacing patterns are provably the strongest and which are the shortest, because apparently no everyday habit is too small to deserve a proof
[Beyond](#beyond) e shortest, because apparently no everyday habit is too small to deserve a proof And the one that still genuinely blows my mind, Fermat's Last Theorem , the claim that a^n + b^n = c^n has no whole-number solutions for n greater than 2, scribbled by Fermat in a margin in 1637 with a proof he said was too long to fit. It took over 350 years and the eventual proof pulled in elliptic curves, modular forms and ideas that echo through modern physics to finally settle it
[Beyond](#beyond) s, modular forms and ideas that echo through modern physics to finally settle it I'm nowhere near being able to follow the proof itself, but the fact that a seventeenth-century margin note ends up wired into some of the deepest structures in physics is the kind of interconnectedness I can't stop thinking about. Mine tends to be spontaneous, a line shows up uninvited, usually nothing to do with whatever I was actually doing and I write it down before it leaves
[Beyond](#beyond) ng to do with whatever I was actually doing and I write it down before it leaves Poems mostly, the occasional stretch toward something longer. That same instinct is exactly why I'm drawn to people who write on the spot, no drafts, no second attempt, just a person, a blank page and whatever a stranger just told them. Olivia Dodd , who sits with a typewriter in public and turns a total stranger's story into a finished poem in minutes, is the one I keep coming back to for that
[Beyond](#beyond) story into a finished poem in minutes, is the one I keep coming back to for that Robert Frost's Stopping by Woods on a Snowy Evening is the poem I return to most. That last quiet turn, "but I have promises to keep," is the entire tension between wanting to stay in the interesting problem and knowing there's a deadline attached to it. I've felt that exact pull more times than I can count
[Beyond](#beyond) a deadline attached to it. I've felt that exact pull more times than I can count Rooms I could get lost in for a full day, the Uffizi in Florence, the Louvre and Amsterdam's Rijksmuseum . I haven't stood in any of them yet. Visiting even one is the actual dream, not just a line on a list. I'll start with the book. Ian McEwan's Atonement , worth it alone for the final-act rewrite, where you have to decide how much of what you just read was ever true
[Beyond](#beyond) t rewrite, where you have to decide how much of what you just read was ever true (Its film adaptation goes out in France under the far more dramatic title Reviens-moi , "come back to me," which honestly might be the better title.) My favourite film, full stop, is Christopher Nolan's The Prestige : "Are you watching closely?" is doing all the work in that opening line and the rest of the film is just the trick
[Beyond](#beyond) ing all the work in that opening line and the rest of the film is just the trick Right behind it, Eternal Sunshine of the Spotless Mind : memory, love and the beautiful futility of trying to erase either. For evergreens I'll rewatch on any given evening, The Godfather and 12 Angry Men never miss. Michael Jackson on one end, La La Land's jazz score on the other and Carnatic classical filling the quiet in between
[Beyond](#beyond) nd's jazz score on the other and Carnatic classical filling the quiet in between Two gold medals at my college championships and a repertoire split cleanly down the middle: the Sicilian with Black, the Ruy Lopez with White. Three games I'll replay any time someone asks why I love this. Kasparov vs
[Beyond](#beyond) hite. Three games I'll replay any time someone asks why I love this. Kasparov vs Karpov , 1985 World Championship, Kasparov's octopus knight sits on d3 for eighteen moves before forcing a queen sacrifice out of pure positional pressure, as close to poetry as chess gets. Fischer vs
[Beyond](#beyond) ce out of pure positional pressure, as close to poetry as chess gets. Fischer vs Spassky , 1972 Game 6, the game Pawn Sacrifice builds its whole third act toward, Fischer playing the Queen's Gambit for the first time in a serious game and dismantling Spassky with an opening he'd never touched before. And for technique alone, Carlsen vs
[Beyond](#beyond) y with an opening he'd never touched before. And for technique alone, Carlsen vs Karjakin , 2016 World Championship tiebreak, a queen sacrifice on move 50 that forces mate, still one of the cleanest finishes any World Championship has ever produced. If you'd like to play a game, find me on Chess.com . Always up for a match, connect there as well. What draws me to F1 isn't the speed, it's the systems thinking
[Beyond](#beyond) ct there as well. What draws me to F1 isn't the speed, it's the systems thinking An undercut is a strategic bet made long before you have proof it'll pay off. The pit wall lives or dies by that call. Recognizing that rhythm, the interplay of pressure, timing and precision, is exactly what makes me a better engineer. Three drives I'll rewatch anytime
[Beyond](#beyond) n, is exactly what makes me a better engineer. Three drives I'll rewatch anytime Max Verstappen's P17-to-P1 at São Paulo 2024 , Ayrton Senna's 1988 Monaco qualifying lap , a lap so far ahead of the field it was never even fully captured on camera and Michael Schumacher's 1995 win at Spa from 16th on the grid in mixed wet-dry conditions, on the same circuit this whole page is modelled after.

## [Contact] Contact

Source: https://varunsani.vercel.app/#contact

[Contact](#contact) varunsani625@gmail.com · open channel ↗ +91 99890 44369 · copy that ↗ LinkedIn · full throttle ↗ GitHub · push to pass ↗ Resume · pit lane ↗ ICTCS 2025 Paper · chequered flag ↗ ORCID · parc fermé ↗ LeetCode · practice sessions ↗

## [Resume — VARUN SANI] Resume — VARUN SANI

Source: https://drive.google.com/file/d/1JjJZtAeLVnRYEXLAK_Xa-_nOhYypzAFn/view?usp=sharing

[Resume — VARUN SANI]() VARUN SANI: +919989044369 | varunsani625@gmail.com | Hyderabad, India | LinkedIn | GitHub | Portfolio | LeetCode

## [Resume — EDUCATION] Resume — Education

Source: https://drive.google.com/file/d/1JjJZtAeLVnRYEXLAK_Xa-_nOhYypzAFn/view?usp=sharing

[Resume — EDUCATION]() EDUCATION: Indian Institute of Technology PalakkadCGPA: 8.32 | 2021–2025
B.Tech, Computer Science & Engineering
Narayana Junior College, Hyderabad|Class XI & XII 96% | 2019–2021

## [Resume — TECHNICAL SKILLS] Resume — Skills

Source: https://drive.google.com/file/d/1JjJZtAeLVnRYEXLAK_Xa-_nOhYypzAFn/view?usp=sharing

[Resume — TECHNICAL SKILLS]() TECHNICAL SKILLS: Languages:Python, C++, C
Backend & APIs:FastAPI, REST APIs, JWT Authentication, WebSockets
Databases & ORMs:PostgreSQL, Redis, MongoDB, SQLModel, Alembic
ML & Data:Scikit-learn, PyTorch, NumPy, Pandas, Matplotlib
Tools & Platforms:Docker, Git, GitHub, Postman, Ubuntu, Jupyter Notebook

## [Resume — EXPERIENCE] Resume — Experience

Source: https://drive.google.com/file/d/1JjJZtAeLVnRYEXLAK_Xa-_nOhYypzAFn/view?usp=sharing

[Resume — EXPERIENCE]() EXPERIENCE: Machine Learning Engineer Intern·Technocolabs Softwares Inc.Jun 2024–Jul 2024
•Built classification pipelines across Logistic Regression, Decision Tree, Random Forest, XGBoost, and a 3-layer Neural
Network to predict employee attrition on a 15,000-row, 40-feature HR dataset, improving accuracy from ~72% to ~85%
and F1-score from 0.68 to ~0.82 through hyperparameter tuning and threshold optimization.
[Resume — EXPERIENCE]() EXPERIENCE: 82 through hyperparameter tuning and threshold optimization. •Developed regression ensembles for loan default risk in the online P2P lending market using the same model set on
a 10,000-row, 60-feature dataset, cutting RMSE by ~18% via feature selection, stacking, and weighted averaging,
validated through 5-fold cross-validation across RMSE, MAE, and R2.
•Performed end-to-end preprocessing including median/mode imputation for 12% missing values, SMOTE for a 15%
[Resume — EXPERIENCE]() EXPERIENCE: dian/mode imputation for 12% missing values, SMOTE for a 15% minority class, and StandardScaler normalization; engineered 8 interaction features contributing a 5% lift in model
performance.

## [Resume — PROJECTS] Resume — Projects

Source: https://drive.google.com/file/d/1JjJZtAeLVnRYEXLAK_Xa-_nOhYypzAFn/view?usp=sharing

[Resume — PROJECTS]() PROJECTS: Real-Time Severe Weather Alerting System|FastAPI·Redis Pub/Sub·WebSockets·PostgreSQL·Docker
•Replaced client-side polling with server-pushed alerts: a dedicated poller container queries the free Open-Meteo API
for each subscribed location once per 5-minute cycle and publishes classified conditions over Redis Pub/Sub.
•Scaled live delivery horizontally by giving each API replica its own WebSocket forwarder that subscribes to the shared
[Resume — PROJECTS]() PROJECTS: ca its own WebSocket forwarder that subscribes to the shared alert stream and pushes only to its locally connected clients, designed to run behind a load balancer across N replicas.
•Designed a configurable severity engine with hand-tunable thresholds across four condition categories at three escalating
tiers, and rounded coordinates to ~1.1km so nearby subscriptions share a single polled point.
URL Shortener|FastAPI·REST APIs·PostgreSQL·Redis·JWT·SQLModel·Alembic
[Resume — PROJECTS]() PROJECTS: ener|FastAPI·REST APIs·PostgreSQL·Redis·JWT·SQLModel·Alembic •Structured a fully asynchronous URL shortener into router, middleware, service, and repository layers, generating
unique 6-character base62 short codes with bcrypt-hashed credentials in an ACID-compliant PostgreSQL schema.
•Authenticated requests with 15-minute JWT access tokens and 7-day refresh tokens, blacklisting revoked tokens in
Redis with matched TTLs, and capping abuse at 10 creations and 60 redirects per minute per IP.
[Resume — PROJECTS]() PROJECTS: ng abuse at 10 creations and 60 redirects per minute per IP. •Lowered database load by caching redirect lookups in Redis for 1 hour, and tracked click analytics across daily, weekly,
and monthly windows via non-blocking asynchronous counters.

## [Resume — RESEARCH & PUBLICATIONS] Resume — Research

Source: https://drive.google.com/file/d/1JjJZtAeLVnRYEXLAK_Xa-_nOhYypzAFn/view?usp=sharing

[Resume — RESEARCH & PUBLICATIONS]() RESEARCH & PUBLICATIONS: Multipacking in Hypercubes|Co-author·ORCID Aug 2024–Jul 2025
•Established asymptotically tight bounds on the n-dimensional hypercube’s multipacking number, between ⌊n/2⌋and
n/2 +O(√n), via a recursive construction and Spencer’s discrepancy theorem.
•Showed the broadcast-domination-to-multipacking ratio approaches 2, the first infinite family attaining this bound,
open since Beaudou, Brewster, and Foucaud (2019); accepted at ICTCS 2025, Pescara, Italy.View paper→

## [Resume — CERTIFICATIONS] Resume — Certifications

Source: https://drive.google.com/file/d/1JjJZtAeLVnRYEXLAK_Xa-_nOhYypzAFn/view?usp=sharing

[Resume — CERTIFICATIONS]() CERTIFICATIONS: •Introduction to Machine Learning, NPTEL
•Machine Learning A-Z: AI, Python, Udemy

## [Resume] Resume

Source: https://drive.google.com/file/d/1JjJZtAeLVnRYEXLAK_Xa-_nOhYypzAFn/view?usp=sharing

[Resume]() Varun's resume is available here as a PDF, kept up to date on Google Drive.

## [The Wind Tunnel (Research) — Multipacking in Hypercubes] Multipacking in Hypercubes (ICTCS 2025)

Source: https://ceur-ws.org/Vol-4039/paper19.pdf

[The Wind Tunnel (Research) — Multipacking in Hypercubes](#research) Multipacking in Hypercubes
Deepak Rajendraprasad1,†, Varun Sani1,†, Birenjith Sasidharan1,†and Jishnu Sen1,*,†
1Indian Institute of Technology Palakkad, Kerala, India, 678623
Abstract
For an undirected graph 𝐺, adominating broadcast on𝐺is a function 𝑓:𝑉(𝐺)→Nsuch that for any vertex
𝑢∈𝑉(𝐺), there exists a vertex 𝑣∈𝑉(𝐺)with𝑓(𝑣)⩾1and𝑑(𝑢, 𝑣)⩽𝑓(𝑣). The costof𝑓is∑︀
𝑣∈𝑉𝑓(𝑣). The
[The Wind Tunnel (Research) — Multipacking in Hypercubes](#research) re exists a vertex 𝑣∈𝑉(𝐺)with𝑓(𝑣)⩾1and𝑑(𝑢, 𝑣)⩽𝑓(𝑣). The costof𝑓is∑︀
𝑣∈𝑉𝑓(𝑣). The minimum cost over all the dominating broadcasts on 𝐺is defined as the broadcast domination number 𝛾𝑏(𝐺)of
𝐺. Amultipacking in𝐺is a subset 𝑀⊆𝑉(𝐺)such that, for every vertex 𝑣∈𝑉(𝐺)and every positive integer
𝑟, the number of vertices in 𝑀within distance 𝑟of𝑣is at most 𝑟. The multipacking number of𝐺, denoted
[The Wind Tunnel (Research) — Multipacking in Hypercubes](#research) tices in 𝑀within distance 𝑟of𝑣is at most 𝑟. The multipacking number of𝐺, denoted mp(𝐺), is the maximum cardinality of a multipacking in 𝐺. These two optimisation problems are duals of each
other, and it easily follows that mp(𝐺)⩽𝛾𝑏(𝐺). It is known that 𝛾𝑏(𝐺)⩽2 mp( 𝐺) + 3 and conjectured that
𝛾𝑏(𝐺)⩽2 mp( 𝐺).
In this paper, we show that for the 𝑛-dimensional hypercube 𝑄𝑛
⌊︁𝑛
2⌋︁
⩽mp(𝑄𝑛)⩽𝑛
2+ 6√
2𝑛.
[The Wind Tunnel (Research) — Multipacking in Hypercubes](#research) per, we show that for the 𝑛-dimensional hypercube 𝑄𝑛
⌊︁𝑛
2⌋︁
⩽mp(𝑄𝑛)⩽𝑛
2+ 6√
2𝑛. Since 𝛾𝑏(𝑄𝑛) =𝑛−1for all 𝑛⩾3, this verifies the above conjecture on hypercubes and, more interestingly,
gives a sequence of connected graphs for which the ratio𝛾𝑏(𝐺)
mp(𝐺)approaches 2, a search for which was initiated
by Beaudou, Brewster and Foucaud in 2019. It follows that, for connected graphs 𝐺
lim sup
mp(𝐺)→∞{︂𝛾𝑏(𝐺)
mp(𝐺)}︂
= 2.
[The Wind Tunnel (Research) — Multipacking in Hypercubes](#research) 019. It follows that, for connected graphs 𝐺
lim sup
mp(𝐺)→∞{︂𝛾𝑏(𝐺)
mp(𝐺)}︂
= 2. The lower bound on mp(𝑄𝑛)is established by a recursive construction, and the upper bound is established
using a classic result from discrepancy theory.
Keywords
Broadcast domination, multipacking, hypercubes
1. Introduction
Adominating set in an undirected graph 𝐺is a set 𝑆⊆𝑉(𝐺)such that every node in 𝐺is either in
[The Wind Tunnel (Research) — Multipacking in Hypercubes](#research) set in an undirected graph 𝐺is a set 𝑆⊆𝑉(𝐺)such that every node in 𝐺is either in 𝑆or adjacent to a node in 𝑆. One of the many motivations to study dominating sets and its variants
comes from optimising the placement of facilities on the nodes of a network so that services can be
easily distributed to every node in the network. In particular, if placing a facility at a node serves that
[The Wind Tunnel (Research) — Multipacking in Hypercubes](#research) node in the network. In particular, if placing a facility at a node serves that node and all its neighbours, and the cost of establishing a facility is the same across all the nodes, then
the best strategy is to identify a smallest dominating set of the graph and place one facility on each
node of this set. Suppose we can set up facilities that can serve a larger range, even at a larger cost,
[The Wind Tunnel (Research) — Multipacking in Hypercubes](#research) e we can set up facilities that can serve a larger range, even at a larger cost, then we might be able to do a better distribution than the above strategy. In particular, if the cost of
setting up a facility is proportional to the distance up to which it can serve, then the task becomes that
of finding a dominating broadcast of minimum cost as defined next.
Definition 1.1. Abroadcast on a graph 𝐺= (𝑉, 𝐸)is a function 𝑓:𝑉→N. The cost of a broadcast
𝑓is∑︀
[The Wind Tunnel (Research) — Multipacking in Hypercubes](#research) broadcast on a graph 𝐺= (𝑉, 𝐸)is a function 𝑓:𝑉→N. The cost of a broadcast
𝑓is∑︀ 𝑣∈𝑉𝑓(𝑣). A broadcast is said to be dominating if every vertex of 𝐺lies within a distance 𝑓(𝑣)of
some vertex 𝑣∈𝑉with𝑓(𝑣)⩾1. The broadcast domination number , denoted 𝛾𝑏(𝐺), is the minimum
cost over all dominating broadcasts on 𝐺.
ICTCS 2025: Italian Conference on Theoretical Computer Science, September 10 – 12, 2025, Pescara, Italy
*Corresponding author.
†These authors contributed equally.
[The Wind Tunnel (Research) — Multipacking in Hypercubes](#research) 2025, Pescara, Italy
*Corresponding author.
†These authors contributed equally. /envel⌢pe-⌢pendeepak@iitpkd.ac.in (D. Rajendraprasad); varunsani625@gmail.com (V. Sani); biren@iitpkd.ac.in (B. Sasidharan);
senjishnu5@gmail.com (J. Sen)
/orcid0000-0001-9101-8967 (D. Rajendraprasad); 0000-0001-7444-7161 (B. Sasidharan); 0000-0002-8724-9583 (J. Sen)
[The Wind Tunnel (Research) — Multipacking in Hypercubes](#research) jendraprasad); 0000-0001-7444-7161 (B. Sasidharan); 0000-0002-8724-9583 (J. Sen) ©2025 Copyright for this paper by its authors. Use permitted under Creative Commons License Attribution 4.0 International (CC BY 4.0).
CEURWorkshopProceedingsceur-ws.orgISSN 1613-0073
Trees of radius 2give an example of a family of graphs where 𝛾(𝐺)(the size of a smallest dominating
set in 𝐺) is unbounded but 𝛾𝑏(𝐺)is at most 2. The notion of broadcast domination was introduced by
[The Wind Tunnel (Research) — Multipacking in Hypercubes](#research) nded but 𝛾𝑏(𝐺)is at most 2. The notion of broadcast domination was introduced by Erwin [1]in 2001 under the name of cost domination . It is easy to see that the broadcast domination
number 𝛾𝑏(𝐺)is bounded above by both the radius of 𝐺and𝛾(𝐺). Erwin showed that 𝛾𝑏(𝐺)is bounded
below by (diam( 𝐺) + 1) /3. Heggernes and Lokshtanov [2]in 2006 showed, quite contrary to the usual
case for domination problems, that the broadcast domination number of a graph can be determined
[The Wind Tunnel (Research) — Multipacking in Hypercubes](#research) tion problems, that the broadcast domination number of a graph can be determined in polynomial time. In 2013, Brewster et al. [3]modelled broadcast domination as an Integer Linear
Program (ILP), relaxed it to a Linear Program (LP), and used the ILP strengthening of the dual LP to
find lower bounds on broadcast domination number for some graphs. This ILP strengthening gave the
cute combinatorial problem of multipacking that we define next. Here 𝑁𝑘[𝑣]denotes the set of vertices
[The Wind Tunnel (Research) — Multipacking in Hypercubes](#research) oblem of multipacking that we define next. Here 𝑁𝑘[𝑣]denotes the set of vertices which are at a distance at most 𝑘from 𝑣.
Definition 1.2. For a graph 𝐺= (𝑉, 𝐸), a set 𝑀⊆𝑉is amultipacking in𝐺if for every vertex 𝑣∈𝑉,
|𝑁𝑘[𝑣]∩𝑀|⩽𝑘for all 𝑘⩾1. The multipacking number mp(𝐺)is the maximum cardinality of a
multipacking in 𝐺.
From the LP duality, we get that mp(𝐺)⩽𝛾𝑏(𝐺)for every graph 𝐺. On the other hand, Hartnell and
[The Wind Tunnel (Research) — Multipacking in Hypercubes](#research) ality, we get that mp(𝐺)⩽𝛾𝑏(𝐺)for every graph 𝐺. On the other hand, Hartnell and Mynhardt [4]in 2014 proved that 𝛾𝑏(𝐺)⩽3 mp( 𝐺)−2for any graph 𝐺with mp(𝐺)⩾2. Beaudou
et al. [5]in 2019 improved this to 𝛾𝑏(𝐺)⩽2 mp( 𝐺) + 3 and conjectured that the additive factor of 3
can be removed from this bound.
Conjecture 1.3. [5]For any graph 𝐺,𝛾𝑏(𝐺)⩽2 mp( 𝐺).
The reason for the multiplier of 2in the above conjecture is that there are a few small graphs
[The Wind Tunnel (Research) — Multipacking in Hypercubes](#research) the multiplier of 2in the above conjecture is that there are a few small graphs (including 𝐶4and𝐶5, cycles on 4and5vertices) where mp(𝐺) = 1 and𝛾𝑏(𝐺) = 2 and a few others
where mp(𝐺) = 2 and𝛾𝑏(𝐺) = 4 . By taking disjoint copies of these examples, one can construct, for
any𝑘⩾1, a graph with mp(𝐺) =𝑘and𝛾𝑏(𝐺) = 2 𝑘. Hence, the above conjecture, if true, is tight.
While noting this, Beaudou et al. [5]lamented that we do not have an infinite family of connected
[The Wind Tunnel (Research) — Multipacking in Hypercubes](#research) , Beaudou et al. [5]lamented that we do not have an infinite family of connected graphs where the ratio𝛾𝑏(𝐺)
mp(𝐺)approaches 2. The best construction known so far is by Hartnell and
Mynhardt [4] who constructed an infinite family of connected graphs where𝛾𝑏(𝐺)
mp(𝐺)=4
3.
1.1. Results
The main contribution of this note is to show that hypercubes form an infinite family of connected
graphs where𝛾𝑏(𝐺)
mp(𝐺)approaches 2. An 𝑛-dimensional hypercube 𝑄𝑛is the Cartesian product of 𝑛
[The Wind Tunnel (Research) — Multipacking in Hypercubes](#research) 𝐺)
mp(𝐺)approaches 2. An 𝑛-dimensional hypercube 𝑄𝑛is the Cartesian product of 𝑛 copies of the complete graph 𝐾2. Alternatively, it can be visualized as a graph whose vertex set is
{0,1}𝑛and two vertices are adjacent if exactly one coordinate is different. Our main result is
Theorem 1.4. For any positive integer 𝑛,
⌊︁𝑛
2⌋︁
⩽mp(𝑄𝑛)⩽𝑛
2+ 6√
2𝑛.
Brešar and Špacapan [6]showed in 2019 that 𝛾𝑏(𝑄𝑛) =𝑛−1for𝑛⩾3and𝛾𝑏(𝑄𝑛) =𝑛for𝑛∈{1,2}.
Since 𝑛−1⩽2⌊︀𝑛
2⌋︀
[The Wind Tunnel (Research) — Multipacking in Hypercubes](#research) ]showed in 2019 that 𝛾𝑏(𝑄𝑛) =𝑛−1for𝑛⩾3and𝛾𝑏(𝑄𝑛) =𝑛for𝑛∈{1,2}.
Since 𝑛−1⩽2⌊︀𝑛
2⌋︀ , the lower bound in Theorem 1.4 proves Conjecture 1.3 on hypercubes. More
interestingly, we see that lim
𝑛→∞𝛾𝑏(𝑄𝑛)
mp(𝑄𝑛)= 2. This, together with the upper bound 𝛾𝑏(𝐺)⩽2 mp( 𝐺) + 3
[5] lets us conclude
Corollary 1.5. For all connected graphs 𝐺,
lim sup
mp(𝐺)→∞{︂𝛾𝑏(𝐺)
mp(𝐺)}︂
= 2.
1.2. Proof Techniques
[The Wind Tunnel (Research) — Multipacking in Hypercubes](#research) ll connected graphs 𝐺,
lim sup
mp(𝐺)→∞{︂𝛾𝑏(𝐺)
mp(𝐺)}︂
= 2.
1.2. Proof Techniques The lower bound in Theorem 1.4 is proved by introducing a recursive technique that systematically
generates multipacking of higher-dimensional hypercubes by combining multipackings from lower
dimensions. For the proof of the upper bound, we bank on a classic result by Spencer [7]from
combinatorial discrepancy theory.
1.3. Related Results
[The Wind Tunnel (Research) — Multipacking in Hypercubes](#research) result by Spencer [7]from
combinatorial discrepancy theory.
1.3. Related Results The first inequality in mp(𝐺)⩽𝛾𝑏(𝐺)⩽2 mp( 𝐺) + 3 was shown to be tight in some graph families
like trees [ 8], grid graphs 𝑃𝑚□𝑃𝑛(except (𝑚, 𝑛)̸= (4,6)) [9] and strongly chordal graphs [ 10]. A
graph is strongly chordal if it is chordal and every even cycle of length at least 6has a chord that
connects two vertices which are at an odd distance apart on the cycle.
[The Wind Tunnel (Research) — Multipacking in Hypercubes](#research) hord that
connects two vertices which are at an odd distance apart on the cycle. Hartnell and Mynhardt [4]shown that the difference between mp(𝐺)and𝛾𝑏(𝐺)can be arbitrarily
large by constructing an infinite family of connected graphs 𝐺such that𝛾𝑏(𝐺)
mp(𝐺)=4
3. This construction
and the upper bound 𝛾𝑏(𝐺)⩽2𝑚𝑝(𝐺) + 3 meant that for connected graphs 𝐺
4
3⩽lim sup
mp(𝐺)→∞{︂𝛾𝑏(𝐺)
mp(𝐺)}︂
⩽2.
[The Wind Tunnel (Research) — Multipacking in Hypercubes](#research) (𝐺) + 3 meant that for connected graphs 𝐺
4
3⩽lim sup
mp(𝐺)→∞{︂𝛾𝑏(𝐺)
mp(𝐺)}︂
⩽2. While our Corollary 1.5 improves the above, optimal bounds for this ratio were studied for special graph
classes. For connected chordal graphs 𝐺, Das et al. [11] showed that
10
9⩽lim sup
mp(𝐺)→∞{︂𝛾𝑏(𝐺)
mp(𝐺)}︂
⩽3
2.
Acactus is a connected graph in which any two cycles share at most one vertex. A graph 𝐺is
[The Wind Tunnel (Research) — Multipacking in Hypercubes](#research) a connected graph in which any two cycles share at most one vertex. A graph 𝐺is a𝛿-hyperbolic graph , if for any four vertices 𝑢, 𝑣, 𝑤, 𝑥 of𝐺, among the three sumations 𝑑(𝑢, 𝑣) +
𝑑(𝑤, 𝑥), 𝑑(𝑢, 𝑤) +𝑑(𝑣, 𝑥)and𝑑(𝑢, 𝑥) +𝑑(𝑣, 𝑤), the difference between the two of the largest sums is
at most 2𝛿. A graph class is said to be hyperbolic if there exists a constant 𝛿such that every graph in
that class is 𝛿-hyperbolic. Das and Islam [12] proved that for cactus graphs and1
[The Wind Tunnel (Research) — Multipacking in Hypercubes](#research) hat class is 𝛿-hyperbolic. Das and Islam [12] proved that for cactus graphs and1 2-hyperbolic graphs 𝐺,
4
3⩽lim sup
mp(𝐺)→∞{︂𝛾𝑏(𝐺)
mp(𝐺)}︂
⩽3
2.
1.4. Terminology
Every graph discussed in this note is finite, simple, and undirected. Ndenotes the set of natural numbers
(including 0). For any positive integer 𝑛, we denote the set {1,2, . . . , 𝑛}as[𝑛]. Any undefined terms
and notations are in accordance with Chartrand et al. [13].
2. Proof of Theorem 1.4
[The Wind Tunnel (Research) — Multipacking in Hypercubes](#research) notations are in accordance with Chartrand et al. [13].
2. Proof of Theorem 1.4 We use exponential notation to indicate repeated sequences in the vertex so that a vertex 110001 in𝑄6
will be written as 12031. The hamming weight wt(𝑢)of a vertex 𝑢is the distance of 𝑢from 0𝑛in𝑄𝑛. As
a warm-up, first we determine mp(𝑄𝑛)for𝑛⩽6. It is easy to observe that mp(𝑄1) = 1 ,mp(𝑄2) =
1,mp(𝑄3) = 2 ,mp(𝑄4) = 2 andmp(𝑄5) = 2 .
Proposition 2.1. mp(𝑄6) = 4 .
[The Wind Tunnel (Research) — Multipacking in Hypercubes](#research) ,mp(𝑄2) =
1,mp(𝑄3) = 2 ,mp(𝑄4) = 2 andmp(𝑄5) = 2 .
Proposition 2.1. mp(𝑄6) = 4 . Proof. One can observe that, since the set {06,0313,1303,16}is a multipacking in 𝑄6,mp(𝑄6)⩾4.
Now, we show that no set of order 5can be a multipacking in 𝑄6. On the contrary, let 𝑃be a
multipacking in 𝑄𝑛of5vertices. As 𝑄𝑛is vertex-transitive, without loss of generality, suppose 06∈𝑃.
Then 𝑃cannot contain any vertex of hamming weight 1or2. Then 𝑃∖{06}⊆ 𝑁3[16]. Hence,
[The Wind Tunnel (Research) — Multipacking in Hypercubes](#research) n 𝑃cannot contain any vertex of hamming weight 1or2. Then 𝑃∖{06}⊆ 𝑁3[16]. Hence, |𝑁3[16]∩𝑃|= 4>3, a contradiction to the fact that 𝑃is a multipacking. Therefore, mp(𝑄6) = 4 .
Since 𝑄𝑛+1contains a copy of 𝑄𝑛as a distance preserving subgraph, it is easy to observe that the
multipacking number of 𝑄𝑛is monotonic in 𝑛.
Observation 2.2. For any positive integer 𝑛,mp(𝑄𝑛)⩽mp(𝑄𝑛+1).
2.1. Lower bound
[The Wind Tunnel (Research) — Multipacking in Hypercubes](#research) 𝑛.
Observation 2.2. For any positive integer 𝑛,mp(𝑄𝑛)⩽mp(𝑄𝑛+1).
2.1. Lower bound We begin with a couple of lemmas needed for the recursive construction. Given a vertex 𝑥∈𝑄𝑛, and
an integer 𝑚⩾1, we define 𝑖𝑚·𝑥as the binary string obtained by concatenating 𝑖𝑚to𝑥, where
𝑖∈{0,1}. For any set of vertices 𝑆,
𝑖𝑚·𝑆={𝑖𝑚·𝑥:𝑥∈𝑆}.
Lemma 2.3. Let𝑛0⩾𝑛1be two positive integers, and 𝑄𝑛0and𝑄𝑛1be two hypercubes equipped with
multipackings 𝑃0and𝑃1, respectively. Further, let
[The Wind Tunnel (Research) — Multipacking in Hypercubes](#research) e two hypercubes equipped with
multipackings 𝑃0and𝑃1, respectively. Further, let 𝑛=𝑛0+ max(|𝑃0|,2) + max(|𝑃1|,2)−1,
and𝑃be the set
(0𝑛−𝑛0·𝑃0)∪(1𝑛−𝑛1·𝑃1).
Then 𝑃is a multipacking in 𝑄𝑛.
Proof. Let𝑝=|𝑃|=|𝑃0|+|𝑃1|. Pick any 𝑥∈𝑉(𝑄𝑛)and any 𝑘∈[𝑝−1]. We will show that the
number of vertices of 𝑃in𝑁𝑘[𝑥]is at most 𝑘by counting separately the number of vertices of 0𝑛−𝑛0·𝑃0
and1𝑛−𝑛1·𝑃1in𝑁𝑘[𝑥].
[The Wind Tunnel (Research) — Multipacking in Hypercubes](#research) t 𝑘by counting separately the number of vertices of 0𝑛−𝑛0·𝑃0
and1𝑛−𝑛1·𝑃1in𝑁𝑘[𝑥]. Let𝑥0denote the 𝑛0-length suffix of 𝑥(the last 𝑛0bits) and 𝑥1denote the 𝑛1-length suffix of 𝑥. Let
𝑞0and𝑞1respectively denote the number of zeros and ones in the first (𝑛−𝑛0)bits of 𝑥. For any
vertex 𝑦∈𝑃0,𝑑𝑄𝑛(𝑥,0𝑛−𝑛0·𝑦) =𝑞1+𝑑𝑄𝑛0(𝑥0, 𝑦). For any vertex 𝑦∈𝑃1,𝑑𝑄𝑛(𝑥,1𝑛−𝑛1·𝑦)⩾
𝑞0+𝑑𝑄𝑛1(𝑥1, 𝑦). Hence we have
|𝑁𝑘[𝑥]∩𝑃|=|𝑁𝑘[𝑥]∩0𝑛−𝑛0·𝑃0|+|𝑁𝑘[𝑥]∩1𝑛−𝑛1·𝑃1|
⩽|𝑁𝑘−𝑞1[𝑥0]∩𝑃0|+|𝑁𝑘−𝑞0[𝑥1]∩𝑃1|. (1)
[The Wind Tunnel (Research) — Multipacking in Hypercubes](#research) |𝑁𝑘[𝑥]∩𝑃|=|𝑁𝑘[𝑥]∩0𝑛−𝑛0·𝑃0|+|𝑁𝑘[𝑥]∩1𝑛−𝑛1·𝑃1|
⩽|𝑁𝑘−𝑞1[𝑥0]∩𝑃0|+|𝑁𝑘−𝑞0[𝑥1]∩𝑃1|. (1) If both (𝑘−𝑞1)and(𝑘−𝑞0)are positive, then the right hand side of (1) is bounded above by
(𝑘−𝑞1) + (𝑘−𝑞0), since 𝑃𝑖is a multipacking in 𝑄𝑛𝑖for each 𝑖∈{0,1}. Since (𝑞0+𝑞1) = (𝑛−𝑛0)⩾
(𝑝−1)⩾𝑘, this bound is at most 𝑘and we are done. If (𝑘−𝑞1)<0, then the right hand side of (1) is
bounded above by 0 + (𝑘−𝑞0)⩽𝑘. The case when (𝑘−𝑞0)<0is similar. If (𝑘−𝑞1) = 0 but𝑞0>0,
[The Wind Tunnel (Research) — Multipacking in Hypercubes](#research) above by 0 + (𝑘−𝑞0)⩽𝑘. The case when (𝑘−𝑞0)<0is similar. If (𝑘−𝑞1) = 0 but𝑞0>0, then the right hand side of (1) is bounded above by 1 + (𝑘−𝑞0)⩽𝑘. The case when (𝑘−𝑞0) = 0 but
𝑞1>0is also similar.
We are only left with two boundary cases, viz., 𝑘−𝑞1= 0 = 𝑞0and𝑘−𝑞0= 0 = 𝑞1. Here we use
the fact that 𝑛−𝑛0= max(|𝑃0|,2) + max(|𝑃1|,2)−1⩾max{|𝑃0|,|𝑃1|}+ 1. In the first boundary
case, since 𝑞0= 0, we have 𝑞1= (𝑛−𝑛0)⩾|𝑃1|+ 1. Further since 𝑘−𝑞1= 0in this case, we have
[The Wind Tunnel (Research) — Multipacking in Hypercubes](#research) ce 𝑞0= 0, we have 𝑞1= (𝑛−𝑛0)⩾|𝑃1|+ 1. Further since 𝑘−𝑞1= 0in this case, we have 𝑘=𝑞1⩾|𝑃1|+ 1. Hence, the right-hand side of (1), which is at most 1 +|𝑃1|, is bounded above by 𝑘.
The second boundary case ( 𝑘−𝑞0= 0 = 𝑞1) is similar.
It should be noted that if 𝑛=𝑛0+|𝑃0|+|𝑃1|−1(rather than 𝑛0+max(|𝑃0|,2)+max(|𝑃1|,2)−1),
then for small values of 𝑛0(particularly 𝑛0= 1 or2), the resulting set 𝑃does not form a valid
multipacking.
[The Wind Tunnel (Research) — Multipacking in Hypercubes](#research) (particularly 𝑛0= 1 or2), the resulting set 𝑃does not form a valid
multipacking. Corollary 2.4. Let𝑛0⩾𝑛1be two positive integers. Let mp(𝑄𝑛0)⩾𝑝0andmp(𝑄𝑛1)⩾𝑝1. Then
mp(𝑄𝑛)⩾𝑝0+𝑝1, where
𝑛=𝑛0+ max( 𝑝0,2) + max( 𝑝1,2)−1.
This recursive approach leads to a general lower bound of the multipacking number on hypercubes,
which we formalize in the subsequent results.
Lemma 2.5. For any positive integer 𝑘,mp(𝑄2𝑘)⩾𝑘.
[The Wind Tunnel (Research) — Multipacking in Hypercubes](#research) lize in the subsequent results.
Lemma 2.5. For any positive integer 𝑘,mp(𝑄2𝑘)⩾𝑘. Proof. We use induction on 𝑘. The statement is easy to verify for 𝑘⩽2and holds for 𝑘= 3 by
Proposition 2.1. Suppose 𝑘⩾4and that the statement holds for all natural numbers less than 𝑘. Due to
the induction hypothesis, we have
mp(︁
𝑄2⌈𝑘
2⌉)︁
⩾⌈︂𝑘
2⌉︂
,andmp(︁
𝑄2⌊𝑘
2⌋)︁
⩾⌊︂𝑘
2⌋︂
.
Since⌊︀𝑘
2⌋︀
⩾2, by Corollary 2.4, we have
mp(𝑄𝑛)⩾⌈︂𝑘
2⌉︂
+⌊︂𝑘
2⌋︂
=𝑘,
where
𝑛= 2⌈︂𝑘
2⌉︂
+⌈︂𝑘
2⌉︂
+⌊︂𝑘
2⌋︂
−1⩽2𝑘.
[The Wind Tunnel (Research) — Multipacking in Hypercubes](#research) , we have
mp(𝑄𝑛)⩾⌈︂𝑘
2⌉︂
+⌊︂𝑘
2⌋︂
=𝑘,
where
𝑛= 2⌈︂𝑘
2⌉︂
+⌈︂𝑘
2⌉︂
+⌊︂𝑘
2⌋︂
−1⩽2𝑘. Hence by Observation 2.2, we have mp(𝑄2𝑘)⩾𝑘.
Proof of the lower bound of Theorem 1.4. If𝑛= 1, then mp(𝑄1)>0. When 𝑛is an even positive integer,
the proof follows from Lemma 2.5. When 𝑛= 2𝑘+ 1is odd for some positive integer 𝑘, by Lemma 2.5
and Observation 2.2 we have,
mp(𝑄𝑛) = mp( 𝑄2𝑘+1)⩾mp(𝑄2𝑘)⩾𝑘=⌊︁𝑛
2⌋︁
.
Though we cannot improve the lower bound of⌊︀𝑛
2⌋︀
in general, we show that mp(𝑄𝑛)−⌊︀𝑛
2⌋︀
[The Wind Tunnel (Research) — Multipacking in Hypercubes](#research) cannot improve the lower bound of⌊︀𝑛
2⌋︀
in general, we show that mp(𝑄𝑛)−⌊︀𝑛
2⌋︀ can be
arbitrarily large.
Proposition 2.6. For every positive integer 𝑖,mp(𝑄𝑛𝑖)⩾𝑛𝑖
2+log2𝑛𝑖−1
2, where 𝑛𝑖= 2𝑖+1−𝑖.
Proof. We construct a specific sequence of hypercubes {𝑄𝑛𝑖}by repeatedly applying Corollary 2.4
starting from 𝑄3, for which the multipacking number is 2. Hence, we consider 𝑛1= 3and𝑝1= 2. At
[The Wind Tunnel (Research) — Multipacking in Hypercubes](#research) 𝑄3, for which the multipacking number is 2. Hence, we consider 𝑛1= 3and𝑝1= 2. At each step, we consider two identical copies multipacking of the hypercube 𝑄𝑛𝑖−1, and using Lemma
2.3, we obtain a multipacking of 𝑄𝑛𝑖. Therefore, using mp(𝑄𝑛𝑖−1)⩾𝑝𝑖−1as an inductive hypothesis
for𝑖⩾2, we have mp(𝑄𝑛𝑖)⩾𝑝𝑖, due to Corollary 2.4., where
𝑛𝑖=𝑛𝑖−1+ 2𝑝𝑖−1−1, 𝑝 𝑖= 2𝑝𝑖−1.
On solving these recurrence relations with initial conditions 𝑛1= 3and𝑝1= 2, we obtain
𝑛𝑖= 2𝑖+1−𝑖, 𝑝 𝑖= 2𝑖for all 𝑖⩾1.
[The Wind Tunnel (Research) — Multipacking in Hypercubes](#research) with initial conditions 𝑛1= 3and𝑝1= 2, we obtain
𝑛𝑖= 2𝑖+1−𝑖, 𝑝 𝑖= 2𝑖for all 𝑖⩾1. From 𝑛𝑖= 2𝑖+1−𝑖, we get 𝑝𝑖=𝑛𝑖
2+𝑖
2, and using 𝑛𝑖⩽2𝑖+1, it follows that 𝑖⩾log2𝑛𝑖−1. As
mp(𝑄𝑛𝑖)⩾𝑝𝑖, we have
mp(𝑄𝑛𝑖)⩾𝑛𝑖
2+log2𝑛𝑖−1
2.
2.2. Upper bound
Suppose we have a finite family of sets with finite elements, and we intend to color the underlying set
with two colors such that each subset has roughly half of each color. The discrepancy quantifies how
[The Wind Tunnel (Research) — Multipacking in Hypercubes](#research) that each subset has roughly half of each color. The discrepancy quantifies how unbalanced any set in the family can be under the best possible two-coloring of the underlying set.
Formally, let𝒜be a family of subsets of Ω, and consider the coloring as a mapping
𝜒: Ω→{− 1,+1}.
Suppose for every 𝐴⊆Ω,𝜒(𝐴) =∑︀
𝑎∈𝐴𝜒(𝑎). Then, the discrepancy of 𝒜with respect to 𝜒is defined
as
disc(𝒜, 𝜒) = max
𝐴∈𝒜|𝜒(𝐴)|.
The discrepancy of 𝒜is defined as
disc(𝒜) = min
𝜒:Ω→{− 1,+1}disc(𝒜, 𝜒).
[The Wind Tunnel (Research) — Multipacking in Hypercubes](#research) 𝒜|𝜒(𝐴)|.
The discrepancy of 𝒜is defined as
disc(𝒜) = min
𝜒:Ω→{− 1,+1}disc(𝒜, 𝜒). Let’s recall a classic result due to Spencer [7] from the discrepancy theory.
Theorem 2.7. [7]Let𝒜be a family of 𝑛subsets of an 𝑛-element set Ω. Then
disc(𝒜)⩽6√𝑛.
The next lemma establishes an upper bound on mp(𝑄𝑛)using this bound.
Lemma 2.8. For any positive integer 𝑛, we have
mp(𝑄𝑛)⩽𝑛
2+ 6√︀
2 mp( 𝑄𝑛)
Proof. Let𝑃={𝑥1, 𝑥2, . . . , 𝑥 𝑝}be a maximum multipacking in 𝑄𝑛of size 𝑝(⩾𝑛
2). For each 𝑥𝑖∈𝑃,
[The Wind Tunnel (Research) — Multipacking in Hypercubes](#research) , 𝑥2, . . . , 𝑥 𝑝}be a maximum multipacking in 𝑄𝑛of size 𝑝(⩾𝑛
2). For each 𝑥𝑖∈𝑃, we construct a set 𝐴𝑖⊆[𝑛]comprising of the coordinates at which 𝑥𝑖has1, and 𝐴𝑖= [𝑛]∖𝐴𝑖. In
particular, 𝐴𝑖contains the coordinate values at which 𝑥𝑖has0. Now, consider the family of 2𝑝sets
𝒜={𝐴1,𝐴1, 𝐴2,𝐴2, . . . , 𝐴 𝑝,𝐴𝑝},
with the underlying set Ω = [2 𝑝]⊇[𝑛]. Let𝜒be a mapping such that disc(𝒜, 𝜒) = disc(𝒜). For each
[The Wind Tunnel (Research) — Multipacking in Hypercubes](#research) ing set Ω = [2 𝑝]⊇[𝑛]. Let𝜒be a mapping such that disc(𝒜, 𝜒) = disc(𝒜). For each 𝑖∈[𝑛], if𝜒(𝑖) =−1, then we flip the bit at the 𝑖-th coordinate for all the vertices of 𝑄𝑛. All such
flippings induce an automorphism 𝜙on the vertex set of 𝑄𝑛. Hence, the set 𝑃contains new vertices of
𝑄𝑛. Further, a bit-flipping preserves the hamming distance, and therefore 𝑃is still a multipacking in
𝑄𝑛.
Since, for each 𝑖∈[𝑛],|𝜒(𝐴𝑖)|,|𝜒(𝐴𝑖)|⩽disc(𝒜), the number of ones in 𝜙(𝑥𝑖)is at most(︁
|𝐴𝑖|
[The Wind Tunnel (Research) — Multipacking in Hypercubes](#research) each 𝑖∈[𝑛],|𝜒(𝐴𝑖)|,|𝜒(𝐴𝑖)|⩽disc(𝒜), the number of ones in 𝜙(𝑥𝑖)is at most(︁
|𝐴𝑖| 2+disc(𝒜)
2)︁
+(︁
|𝐴𝑖|
2+disc(𝒜)
2)︁
=𝑛
2+ disc(𝒜). Hence wt(𝑥𝑖)⩽𝑛
2+ disc(𝒜)for every 𝑥𝑖∈𝑃
after flipping. This means that, after flipping, 𝑃⊆𝑁𝑛
2+disc(𝒜)[0𝑛]. As𝑃is still a multipacking, we
have
|𝑃|⩽𝑛
2+ disc(𝒜)⩽𝑛
2+ 6√︀
2𝑝,
where the last inequality is due to Theorem 2.7. As 𝑃is a maximum multipacking in 𝑄𝑛, we have the
desired upper bound.
[The Wind Tunnel (Research) — Multipacking in Hypercubes](#research) eorem 2.7. As 𝑃is a maximum multipacking in 𝑄𝑛, we have the
desired upper bound. Proof of the upper bound of Theorem 1.4. The upper bound mp(𝑄𝑛)⩽𝑛
2+ 6√
2𝑛in Theorem 1.4 now
follows from Lemma 2.8 since mp(𝑄𝑛)⩽𝑛.
Declaration on Generative AI
The author(s) have not employed any Generative AI tools.
References
[1]D. J. Erwin, Cost domination in graphs, Ph.D. Thesis, Department of Mathematics and Statistics,
Western Michigan University (2001).
[The Wind Tunnel (Research) — Multipacking in Hypercubes](#research) s, Department of Mathematics and Statistics,
Western Michigan University (2001). [2]P. Heggernes, D. Lokshtanov, Optimal broadcast domination in polynomial time, Discrete Math.
306 (2006) 3267–3280.
[3]R. C. Brewster, C. M. Mynhardt, L. E. Teshima, New bounds for the broadcast domination number
of a graph, Cent. Eur. J. Math. 11 (2013) 1334–1343.
[4]B. L. Hartnell, C. M. Mynhardt, On the difference between broadcast and multipacking numbers
[The Wind Tunnel (Research) — Multipacking in Hypercubes](#research) ll, C. M. Mynhardt, On the difference between broadcast and multipacking numbers of graphs, Util. Math. 94 (2014) 19–29.
[5]L. Beaudou, R. C. Brewster, F. Foucaud, Broadcast domination and multipacking: bounds and the
integrality gap, Australas. J. Comb. 74 (2019) 86–97.
[6]B. Brešar, S. Špacapan, Broadcast domination of products of graphs, Ars Comb. 92 (2009) 303–320.
[7] J. Spencer, Six standard deviations suffice, Trans. Am. Math. Soc. 289 (1985) 679–706.
[The Wind Tunnel (Research) — Multipacking in Hypercubes](#research) ncer, Six standard deviations suffice, Trans. Am. Math. Soc. 289 (1985) 679–706. [8]L. E. Teshima, Broadcasts and multipackings in graphs, 2012. Master’s Thesis, Department of
Mathematics and Statistics, University of Victoria.
[9]L. Beaudou, R. C. Brewster, On the multipacking number of grid graphs, Discret. Math. Theor.
Comput. Sci. 21 (2019).
[10] R. C. Brewster, G. MacGillivray, F. Yang, Broadcast domination and multipacking in strongly
[The Wind Tunnel (Research) — Multipacking in Hypercubes](#research) ter, G. MacGillivray, F. Yang, Broadcast domination and multipacking in strongly chordal graphs, Discret. Appl. Math. 261 (2019) 108–118.
[11] S. Das, F. Foucaud, S. S. Islam, J. Mukherjee, Relation between broadcast domination and multipack-
ing numbers on chordal graphs, in: Conference on Algorithms and Discrete Applied Mathematics,
Springer, 2023, pp. 297–308.
[12] S. Das, S. S. Islam, Multipacking and broadcast domination on cactus graphs and its impact on
[The Wind Tunnel (Research) — Multipacking in Hypercubes](#research) Islam, Multipacking and broadcast domination on cactus graphs and its impact on hyperbolic graphs, in: S.-I. Nakano, M. Xiao (Eds.), WALCOM: Algorithms and Computation,
volume 15411, Springer, 2025, pp. 111–126.
[13] G. Chartrand, L. Lesniak, P. Zhang, Graphs & digraphs, volume 39, CRC press, 2010.

## [The Wind Tunnel (Research) — Multipacking in Hypercubes] Multipacking in Hypercubes (ICTCS 2025) — Authors

Source: https://ceur-ws.org/Vol-4039/paper19.pdf

[The Wind Tunnel (Research) — Multipacking in Hypercubes](#research) Co-authors of Varun's ICTCS 2025 paper 'Multipacking in Hypercubes': Deepak Rajendraprasad, Varun Sani, Birenjith Sasidharan, and Jishnu Sen, all affiliated with the Indian Institute of Technology Palakkad.

## [The Garage (Projects) — Portfolio-bot] Portfolio-bot

Source: https://github.com/varunsani/Portfolio-bot

[The Garage (Projects) — Portfolio-bot](#projects) Portfolio-bot (written in HTML)
[The Garage (Projects) — Portfolio-bot](#projects) Portfolio-bot — Race Engineer — RAG assistant for varunsani.vercel.app: A self-updating RAG chatbot embedded in Varun Sani's portfolio. It answers
questions about Varun from his portfolio, resume, research paper, GitHub
projects, and the external links he references — nothing else, with
citations that scroll to the exact section.
[The Garage (Projects) — Portfolio-bot](#projects) Portfolio-bot — What's in this repo: ```
backend/                                          FastAPI RAG service (retrieval, generation, memory)

portfolio-site/index.html   Your actual portfolio, widget already inlined
.github/workflows/                                CI/CD: auto-scrape, auto-reindex, auto-deploy
```
[The Garage (Projects) — Portfolio-bot](#projects) Portfolio-bot — What's in this repo:                                CI/CD: auto-scrape, auto-reindex, auto-deploy
``` **`index.html` is your real portfolio file** with the
widget's CSS inlined in `<head>` and its JS inlined right before `</body>`,
deferred with `setTimeout(init, 1200)` after `window.onload` so it never
competes with the page's own load/Lighthouse timing. Before using it:
replace the placeholder in the inlined script —
`window.RACE_ENGINEER_API_URL = "https://your-app.railway.app"` — with your
real deployed backend URL, then upload it to Vercel in place of your
current `index.html`.
[The Garage (Projects) — Portfolio-bot](#projects) Portfolio-bot — How the self-updating part works: You said you'll change the portfolio later and want the bot to pick that up
automatically — here's the loop that does it, with no manual reindexing:
[The Garage (Projects) — Portfolio-bot](#projects) Portfolio-bot — How the self-updating part works: that up
automatically — here's the loop that does it, with no manual reindexing: 1. **`scrape-and-reindex.yml`** runs every 1 hours (and on manual trigger).
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
[The Garage (Projects) — Portfolio-bot](#projects) Portfolio-bot — How the self-updating part works: t is live at those anchors, citation chips keep scrolling to
   the right place. If you'd rather not wait up to 1 hours, click **Run workflow** on
`scrape-and-reindex.yml` in the Actions tab any time after a portfolio edit.
[The Garage (Projects) — Portfolio-bot](#projects) Portfolio-bot — Retrieval strategy (why it's not just cosine similarity): - **Hybrid search with an "either" acceptance gate**: a chunk survives if
  its raw vector similarity clears one bar, OR its BM25 keyword score
  clears a separate bar — not one blended score with a single cutoff. This
  matters for queries with zero vocabulary overlap with the source text
  (e.g. "university" when the portfolio only ever says "Institute of
[The Garage (Projects) — Portfolio-bot](#projects) Portfolio-bot — Retrieval strategy (why it's not just cosine similarity): source text
  (e.g. "university" when the portfolio only ever says "Institute of Technology") — a blended score punishes those unfairly.
- **Thematic-name resilience**: F1 section names ("The Garage", "The Wind
  Tunnel") are resolved to plain labels (Projects, Research, ...) via
  `app/constants.py` before ever reaching the LLM's prompt, so the model
  never takes the theme literally. Those same plain labels are folded into
[The Garage (Projects) — Portfolio-bot](#projects) Portfolio-bot — Retrieval strategy (why it's not just cosine similarity): model
  never takes the theme literally. Those same plain labels are folded into each chunk's BM25 tokens (not its embedding) as keyword aliases, so a
  literal question like "what's his tech stack" still matches the Skills
  section by keyword even if "skills" never appears verbatim nearby.
- **MMR (Maximum Marginal Relevance)** re-ranking removes near-duplicate
  chunks (e.g. a project described in both the portfolio and the resume).
[The Garage (Projects) — Portfolio-bot](#projects) Portfolio-bot — Retrieval strategy (why it's not just cosine similarity): licate
  chunks (e.g. a project described in both the portfolio and the resume). - **Contextual compression** trims each retrieved chunk down to its most
  query-relevant sentences before it ever reaches the LLM.
[The Garage (Projects) — Portfolio-bot](#projects) Portfolio-bot — Small talk vs. off-topic: Greetings, farewells, thanks, and date/time questions are matched by a
deterministic regex (`app/services/small_talk.py`) and answered directly —
with the real current date/time injected — without touching retrieval.
Anything else that retrieval turns up nothing for (unrelated general
knowledge, other people, current events) gets the fixed decline message
[The Garage (Projects) — Portfolio-bot](#projects) Portfolio-bot — Small talk vs. off-topic:  general
knowledge, other people, current events) gets the fixed decline message with no LLM call at all, so there's no path to a hallucinated answer.
[The Garage (Projects) — Portfolio-bot](#projects) Portfolio-bot — What gets scraped and indexed: - **Portfolio** — live-scraped on a schedule, anchor/section auto-detected
  from the page's own `id="..."` structure (see README "self-updating" section).
- **Resume** — prefers a `content/resume.pdf` committed directly in the
  repo (most reliable); falls back to fetching live from the Google Drive
  share link if no local file is present.
[The Garage (Projects) — Portfolio-bot](#projects) Portfolio-bot — What gets scraped and indexed: to fetching live from the Google Drive
  share link if no local file is present. - **Research paper** — fetched directly from its public PDF URL.
- **GitHub** — every public, non-fork repo under the configured username is
  auto-discovered via the GitHub API (not a hardcoded list), and each
  repo's README is indexed. New repos are picked up on the next scheduled run.
- **Every external link found on the portfolio** — dispatched to a
[The Garage (Projects) — Portfolio-bot](#projects) Portfolio-bot — What gets scraped and indexed: cheduled run.
- **Every external link found on the portfolio** — dispatched to a source-appropriate fetcher: chess.com ratings via their public stats API
  (the profile page itself is JS-rendered and returns no numbers to a plain
  scrape), YouTube via oEmbed for title/author, any other Google Drive link
  via the same PDF path as the resume, and a generic HTML text scrape for
  everything else (arXiv, Wikipedia, etc.). Heavily JS-rendered third-party
[The Garage (Projects) — Portfolio-bot](#projects) Portfolio-bot — What gets scraped and indexed:  for
  everything else (arXiv, Wikipedia, etc.). Heavily JS-rendered third-party sites (LinkedIn, IMDb, etc.) are still included but may yield thin text —
  there's no headless browser in this stack.
[The Garage (Projects) — Portfolio-bot](#projects) Portfolio-bot — Persona: 95% of the voice is just a sharp, professional person giving a clear
briefing — plain sentences, no corporate filler. F1 language shows up as an
occasional word choice, never a full metaphor-per-sentence bit. See the
system prompt in `backend/app/services/generator.py` if you want to tune
the ratio further.
[The Garage (Projects) — Portfolio-bot](#projects) Portfolio-bot — Before you deploy — one thing left: 1. **Groq API key**: sign up at console.groq.com (free tier) and grab a key.
2. **Railway project**: create one Postgres service (with the `vector`
   extension available — Railway's Postgres image supports it) and one Redis
   service.

`content/resume.pdf` is already bundled in this repo — no manual step needed there.

Full step-by-step in [DEPLOYMENT.md](./DEPLOYMENT.md).
[The Garage (Projects) — Portfolio-bot](#projects) Portfolio-bot — Local development: ```bash
cd backend
cp .env.example .env   # fill in DATABASE_URL, REDIS_URL, GROQ_API_KEY
pip install -r requirements.txt
python scripts/scrape_portfolio.py     # refresh content/portfolio.md
python scripts/index_knowledge.py      # build the vector index
uvicorn app.main:app --reload
```
[The Garage (Projects) — Portfolio-bot](#projects) Portfolio-bot — Evaluation: ```bash
python backend/scripts/evaluate.py --url https://your-app.railway.app
```

Prints each test question, the answer, citations, and latency, so you can
eyeball faithfulness/relevance before wiring up full RAGAS metrics (optional
— see the docstring in `evaluate.py`).
[The Garage (Projects) — Portfolio-bot](#projects) Portfolio-bot — Non-negotiables this build respects: - Never answers from the LLM's general knowledge about Varun — only retrieved context.
- Every substantive answer carries at least one citation chip.
- Citation clicks scroll to the exact `#anchor`, not just the top of the page.
- Widget loads lazily after the page is interactive — doesn't touch Lighthouse's TTI.
- Conversation history persists per session (last 10 turns, Redis, 6h TTL).
[The Garage (Projects) — Portfolio-bot](#projects) Portfolio-bot — Non-negotiables this build respects: TTI.
- Conversation history persists per session (last 10 turns, Redis, 6h TTL). - Reindexing is zero-downtime (pending → verify → atomic swap → delete old).
- Rate limited: 30 requests/minute/IP, F1-flavoured 429 message.
- All secrets live in environment variables / GitHub Secrets, never in code.
- CORS locked to `https://varunsani.vercel.app` in production.

## [The Garage (Projects) — UrlShortener] UrlShortener

Source: https://github.com/varunsani/UrlShortener

[The Garage (Projects) — UrlShortener](#projects) UrlShortener (written in Python)
[The Garage (Projects) — UrlShortener](#projects) UrlShortener — 🔗 URL Shortener: A fully asynchronous, production-ready URL shortener service built with **FastAPI**, **PostgreSQL**, and **Redis**. Converts long URLs into compact 6-character links, complete with JWT authentication, role-based access control, click analytics, Redis caching, and per-IP rate limiting.

---
[The Garage (Projects) — UrlShortener](#projects) UrlShortener — 📋 Table of Contents: - [Overview](#overview)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Running the Application](#running-the-application)
- [Database Migrations](#database-migrations)
- [How It Works](#how-it-works)
  - [Authentication Flow](#authentication-flow)
  - [URL Shortening Flow](#url-shortening-flow)
  - [Redirect & Caching Flow](#redirect--caching-flow)
  - [Analytics Tracking](#analytics-tracking)
  - [Security Architecture](#security-architecture)
- [API Reference](#api-reference)
  - [Auth Endpoints](#auth-endpoints)
  - [URL Endpoints](#url-endpoints)
  - [Analytics Endpoints](#analytics-endpoints)
  - [Admin Endpoints](#admin-endpoints)
- [Rate Limiting](#rate-limiting)
- [Environment Variables](#environment-variables)
- [Error Handling](#error-handling)
- [Limitations](#limitations)
- [Future Improvements](#future-improvements)
- [License](#license)
[The Garage (Projects) — UrlShortener](#projects) UrlShortener — 📋 Table of Contents: limitations)
- [Future Improvements](#future-improvements)
- [License](#license) ---
[The Garage (Projects) — UrlShortener](#projects) UrlShortener — 🔍 Overview: This service transforms long, cumbersome URLs into concise, shareable short links while providing enterprise-grade features. Built on a fully asynchronous stack, it handles hundreds of concurrent requests efficiently — ideal for high-traffic use cases where speed and reliability matter.

---
[The Garage (Projects) — UrlShortener](#projects) UrlShortener — ✨ Features: - **URL Shortening** — generates unique 6-character base62 codes (A–Z, a–z, 0–9)
- **JWT Authentication** — short-lived access tokens (15 min) + long-lived refresh tokens (7 days)
- **Role-Based Access Control** — standard users vs. admin users with elevated privileges
- **Click Analytics** — tracks total, daily, weekly, and monthly click counts
- **Redis Caching** — popular redirects served from cache with a 1-hour TTL, slashing DB load
- **Token Blacklisting** — logout immediately invalidates tokens in Redis with precise TTL
- **Rate Limiting** — per-IP protection: 10 URL creations/min, 60 redirects/min
- **Fully Async Architecture** — built on FastAPI + asyncpg for maximum throughput
- **Database Migrations** — managed with Alembic for safe schema evolution
- **CORS Support** — configurable allowed origins
[The Garage (Projects) — UrlShortener](#projects) UrlShortener — ✨ Features: mbic for safe schema evolution
- **CORS Support** — configurable allowed origins ---
[The Garage (Projects) — UrlShortener](#projects) UrlShortener — 🛠 Tech Stack: | Layer | Technology | Version |
|---|---|---|
| Framework | FastAPI | 0.104.1 |
| ASGI Server | Uvicorn | 0.24.0 |
| ORM | SQLAlchemy | 2.0.23 |
| Async DB Driver | asyncpg | 0.29.0 |
| Database | PostgreSQL | 15+ |
| Cache | Redis | 7+ |
| Migrations | Alembic | 1.12.1 |
| Auth (JWT) | python-jose | 3.3.0 |
| Password Hashing | bcrypt | 4.1.2 |
| Settings | pydantic-settings | 2.1.0 |
| Validation | pydantic | 2.5.0 |
[The Garage (Projects) — UrlShortener](#projects) UrlShortener — 🛠 Tech Stack: 1.2 |
| Settings | pydantic-settings | 2.1.0 |
| Validation | pydantic | 2.5.0 | ---
[The Garage (Projects) — UrlShortener](#projects) UrlShortener — 📁 Project Structure: ```
UrlShortener/
│
├── app/                        # Main application package
│   ├── __pycache__/
│   ├── dependencies/           # Dependency injection (auth, db, redis)
│   ├── middleware/             # Custom middleware (rate limiting, CORS)
│   ├── models/                 # SQLAlchemy ORM models
│   ├── routers/                # FastAPI route definitions
│   ├── schemas/                # Pydantic request/response schemas
│   ├── services/               # Business logic layer
│   ├── utils/                  # Utility/helper functions
│   ├── __init__.py
│   ├── config.py               # App settings via pydantic-settings
│   ├── database.py             # Async DB engine and session setup
│   ├── main.py                 # App entry point, middleware registration
│   └── redis_client.py         # Redis connection and helper functions
│
├── migrations/                 # Alembic migration scripts
│   └── versions/
│
├── .env.example                # Sample environment variables
├── .gitignore
├── alembic.ini                 # Alembic configuration
├── requirements.txt            # Python dependencies
└── README.md
```
[The Garage (Projects) — UrlShortener](#projects) UrlShortener — 📁 Project Structure: guration
├── requirements.txt            # Python dependencies
└── README.md
``` ---
[The Garage (Projects) — UrlShortener](#projects) UrlShortener — ✅ Prerequisites: - **Python 3.10+** — https://www.python.org/downloads/
- **PostgreSQL 15+** — https://www.postgresql.org/download/
- **Redis 7+** — https://redis.io/download
- **Git** — https://git-scm.com/downloads

---
[The Garage (Projects) — UrlShortener](#projects) UrlShortener — 📦 Installation: **1. Clone the repository**

```bash
git clone https://github.com/varunsani/UrlShortener.git
cd UrlShortener
```

**2. Create and activate a virtual environment**

```bash
python -m venv venv
[The Garage (Projects) — UrlShortener](#projects) UrlShortener — On Linux/macOS:: source venv/bin/activate
[The Garage (Projects) — UrlShortener](#projects) UrlShortener — On Windows:: venv\Scripts\activate
```

**3. Install dependencies**

```bash
pip install -r requirements.txt
```

---
[The Garage (Projects) — UrlShortener](#projects) UrlShortener — ⚙️ Configuration: **1. Copy the example environment file**

```bash
cp .env.example .env
```

**2. Edit `.env` with your actual values**

```env
APP_NAME=URL Shortener
DEBUG=True
BASE_URL=http://localhost:8000
[The Garage (Projects) — UrlShortener](#projects) UrlShortener — Security: SECRET_KEY=your-super-secret-key-change-this-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=15
REFRESH_TOKEN_EXPIRE_DAYS=7
[The Garage (Projects) — UrlShortener](#projects) UrlShortener — Database: DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/urlshortener
[The Garage (Projects) — UrlShortener](#projects) UrlShortener — Redis: REDIS_URL=redis://localhost:6379/0
[The Garage (Projects) — UrlShortener](#projects) UrlShortener — Rate Limiting: RATE_LIMIT_CREATE_URL=10
RATE_LIMIT_CLICK_URL=60
RATE_LIMIT_WINDOW_SECONDS=60
[The Garage (Projects) — UrlShortener](#projects) UrlShortener — URL Settings: SHORT_CODE_LENGTH=6
[The Garage (Projects) — UrlShortener](#projects) UrlShortener — CORS: ALLOWED_ORIGINS=http://localhost:3000,http://localhost:8000
[The Garage (Projects) — UrlShortener](#projects) UrlShortener — Default Admin Account: ADMIN_EMAIL=admin@example.com
ADMIN_PASSWORD=Admin123!
ADMIN_USERNAME=admin
```

> ⚠️ **Security Note:** Always change `SECRET_KEY` and the default admin credentials before deploying to production.

---
[The Garage (Projects) — UrlShortener](#projects) UrlShortener — 🚀 Running the Application: **1. Make sure PostgreSQL and Redis are running**

```bash
[The Garage (Projects) — UrlShortener](#projects) UrlShortener — PostgreSQL (Linux/macOS): sudo service postgresql start
[The Garage (Projects) — UrlShortener](#projects) UrlShortener — Redis (Linux/macOS): sudo service redis start
```

**2. Run database migrations**

```bash
alembic upgrade head
```

**3. Start the development server**

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`.

**Interactive API Docs (Swagger UI):** `http://localhost:8000/docs`

**Alternative Docs (ReDoc):** `http://localhost:8000/redoc`

---
[The Garage (Projects) — UrlShortener](#projects) UrlShortener — 🗄️ Database Migrations: This project uses **Alembic** to manage database schema changes.

```bash
[The Garage (Projects) — UrlShortener](#projects) UrlShortener — Apply all pending migrations: alembic upgrade head
[The Garage (Projects) — UrlShortener](#projects) UrlShortener — Roll back the last migration: alembic downgrade -1
[The Garage (Projects) — UrlShortener](#projects) UrlShortener — Create a new migration after model changes: alembic revision --autogenerate -m "describe your change"
[The Garage (Projects) — UrlShortener](#projects) UrlShortener — View migration history: alembic history
```

---
[The Garage (Projects) — UrlShortener](#projects) UrlShortener — Authentication Flow: **Registration**

1. User submits email, username, and password.
2. The password is hashed with **bcrypt** and stored in PostgreSQL.
3. A default admin account is seeded on first startup using the values in `.env`.

**Login**
[The Garage (Projects) — UrlShortener](#projects) UrlShortener — Authentication Flow:  admin account is seeded on first startup using the values in `.env`.

**Login** 1. User provides credentials; the system validates them against the database.
2. Two JWT tokens are issued:
   - **Access Token** — expires in 15 minutes; used for all authenticated API calls.
   - **Refresh Token** — expires in 7 days; used only to obtain a new access token.
3. The refresh token is persisted in PostgreSQL to support rotation and revocation.

**Token Refresh**
[The Garage (Projects) — UrlShortener](#projects) UrlShortener — Authentication Flow: s persisted in PostgreSQL to support rotation and revocation.

**Token Refresh** 1. Client sends the refresh token to `/auth/refresh`.
2. The system validates it, issues a new access token, and optionally rotates the refresh token.

**Logout**

1. The access token is blacklisted in Redis with a TTL matching the token's remaining validity.
2. The refresh token is deleted from the database.
3. The user is effectively logged out across all sessions.

---
[The Garage (Projects) — UrlShortener](#projects) UrlShortener — URL Shortening Flow: 1. Authenticated user submits a long URL via `POST /urls/`.
2. The system generates a unique **6-character base62 code** (characters: `A–Z`, `a–z`, `0–9`).
3. The short code, original URL, and creator's user ID are saved in PostgreSQL.
4. The shortened URL (e.g., `http://localhost:8000/abc123`) is returned.
[The Garage (Projects) — UrlShortener](#projects) UrlShortener — URL Shortening Flow: greSQL.
4. The shortened URL (e.g., `http://localhost:8000/abc123`) is returned. **Collision Handling:** If the generated code already exists, the system regenerates until a unique code is found.

---
[The Garage (Projects) — UrlShortener](#projects) UrlShortener — Redirect & Caching Flow: When a user visits a short URL (e.g., `GET /abc123`):
[The Garage (Projects) — UrlShortener](#projects) UrlShortener — Redirect & Caching Flow: When a user visits a short URL (e.g., `GET /abc123`): ```
Request
   │
   ▼
Check Redis Cache
   │
   ├── Cache HIT  ──► Return original URL instantly
   │
   └── Cache MISS ──► Query PostgreSQL
                           │
                           ▼
                     Store in Redis (TTL: 1 hour)
                           │
                           ▼
                     Return original URL
                     + Increment click count (async)
```
[The Garage (Projects) — UrlShortener](#projects) UrlShortener — Redirect & Caching Flow:     Return original URL
                     + Increment click count (async)
``` This caching strategy dramatically reduces database load for popular short links, delivering sub-millisecond redirects on cache hits.

---
[The Garage (Projects) — UrlShortener](#projects) UrlShortener — Analytics Tracking: Every redirect triggers asynchronous analytics updates — no blocking the redirect itself.

Tracked metrics per short URL:

| Metric | Description |
|---|---|
| Total Clicks | Lifetime click count |
| Daily Clicks | Clicks in the current calendar day |
| Weekly Clicks | Clicks in the current week |
| Monthly Clicks | Clicks in the current month |
| Creator Stats | Per-user aggregated analytics |
[The Garage (Projects) — UrlShortener](#projects) UrlShortener — Analytics Tracking:  Clicks in the current month |
| Creator Stats | Per-user aggregated analytics | Analytics are stored in PostgreSQL with proper indexing for fast aggregation queries.

---
[The Garage (Projects) — UrlShortener](#projects) UrlShortener — Security Architecture: | Layer | Mechanism |
|---|---|
| Password Storage | bcrypt hashing with appropriate work factor |
| API Authentication | JWT (HS256) — validated on every protected request |
| Token Revocation | Redis-based blacklist; TTL matches token expiry |
| Access Control | Role-based (user / admin) enforced per endpoint |
| Abuse Prevention | Per-IP rate limiting via Redis counters |
| CORS | Configurable allowed origins via `ALLOWED_ORIGINS` |
[The Garage (Projects) — UrlShortener](#projects) UrlShortener — Security Architecture: a Redis counters |
| CORS | Configurable allowed origins via `ALLOWED_ORIGINS` | ---
[The Garage (Projects) — UrlShortener](#projects) UrlShortener — Auth Endpoints: | Method | Endpoint | Description | Auth Required |
|---|---|---|---|
| `POST` | `/auth/register` | Create a new user account | No |
| `POST` | `/auth/login` | Login and receive tokens | No |
| `POST` | `/auth/refresh` | Refresh access token | No (refresh token) |
| `POST` | `/auth/logout` | Blacklist tokens and log out | Yes |
| `GET` | `/auth/me` | Get current user's profile | Yes |
[The Garage (Projects) — UrlShortener](#projects) UrlShortener — Auth Endpoints: ns and log out | Yes |
| `GET` | `/auth/me` | Get current user's profile | Yes | **Register — Request Body:**
```json
{
  "username": "johndoe",
  "email": "john@example.com",
  "password": "SecurePass123!"
}
```

**Login — Request Body:**
```json
{
  "username": "johndoe",
  "password": "SecurePass123!"
}
```

**Login — Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5...",
  "token_type": "bearer"
}
```

---
[The Garage (Projects) — UrlShortener](#projects) UrlShortener — URL Endpoints: | Method | Endpoint | Description | Auth Required |
|---|---|---|---|
| `POST` | `/urls/` | Create a short URL | Yes |
| `GET` | `/{short_code}` | Redirect to original URL | No |
| `GET` | `/urls/` | List all URLs created by the current user | Yes |
| `GET` | `/urls/{short_code}` | Get details of a specific short URL | Yes |
| `DELETE` | `/urls/{short_code}` | Delete a short URL | Yes (owner only) |
[The Garage (Projects) — UrlShortener](#projects) UrlShortener — URL Endpoints: es |
| `DELETE` | `/urls/{short_code}` | Delete a short URL | Yes (owner only) | **Create Short URL — Request Body:**
```json
{
  "original_url": "https://www.example.com/some/very/long/path?query=value"
}
```

**Create Short URL — Response:**
```json
{
  "short_code": "abc123",
  "short_url": "http://localhost:8000/abc123",
  "original_url": "https://www.example.com/some/very/long/path?query=value",
  "created_at": "2024-01-15T10:30:00Z"
}
```

---
[The Garage (Projects) — UrlShortener](#projects) UrlShortener — Analytics Endpoints: | Method | Endpoint | Description | Auth Required |
|---|---|---|---|
| `GET` | `/urls/{short_code}/analytics` | Get click analytics for a specific URL | Yes (owner) |
| `GET` | `/users/me/analytics` | Get aggregated analytics for the current user | Yes |
[The Garage (Projects) — UrlShortener](#projects) UrlShortener — Analytics Endpoints:  | `/users/me/analytics` | Get aggregated analytics for the current user | Yes | **Analytics Response:**
```json
{
  "short_code": "abc123",
  "total_clicks": 1523,
  "daily_clicks": 42,
  "weekly_clicks": 310,
  "monthly_clicks": 1250
}
```

---
[The Garage (Projects) — UrlShortener](#projects) UrlShortener — Admin Endpoints: > Requires admin role. Set via `ADMIN_EMAIL`, `ADMIN_USERNAME`, and `ADMIN_PASSWORD` in `.env`.

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/admin/urls` | View all short URLs across all users |
| `GET` | `/admin/analytics` | View system-wide aggregated usage metrics |
| `GET` | `/admin/users` | List all registered users |

---
[The Garage (Projects) — UrlShortener](#projects) UrlShortener — 🚦 Rate Limiting: Rate limiting is enforced per IP address using Redis counters with a sliding window.

| Endpoint Type | Default Limit | Window |
|---|---|---|
| URL Creation (`POST /urls/`) | 10 requests | 60 seconds |
| URL Redirects (`GET /{code}`) | 60 requests | 60 seconds |

When the limit is exceeded, the API returns:

```json
{
  "detail": "Rate limit exceeded. Try again later."
}
```
[The Garage (Projects) — UrlShortener](#projects) UrlShortener — 🚦 Rate Limiting: PI returns:

```json
{
  "detail": "Rate limit exceeded. Try again later."
}
``` HTTP Status: `429 Too Many Requests`

Limits are configurable via environment variables:
```env
RATE_LIMIT_CREATE_URL=10
RATE_LIMIT_CLICK_URL=60
RATE_LIMIT_WINDOW_SECONDS=60
```

---
[The Garage (Projects) — UrlShortener](#projects) UrlShortener — 🔑 Environment Variables: | Variable | Default | Description |
|---|---|---|
| `APP_NAME` | `URL Shortener` | Application name |
| `DEBUG` | `True` | Enable debug mode (set `False` in production) |
| `BASE_URL` | `http://localhost:8000` | Base URL used to construct short links |
| `SECRET_KEY` | — | JWT signing secret (must be changed) |
| `ALGORITHM` | `HS256` | JWT signing algorithm |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | `15` | Access token lifetime in minutes |
| `REFRESH_TOKEN_EXPIRE_DAYS` | `7` | Refresh token lifetime in days |
| `DATABASE_URL` | — | PostgreSQL connection string (asyncpg) |
| `REDIS_URL` | `redis://localhost:6379/0` | Redis connection string |
| `RATE_LIMIT_CREATE_URL` | `10` | Max URL creations per window per IP |
| `RATE_LIMIT_CLICK_URL` | `60` | Max redirects per window per IP |
| `RATE_LIMIT_WINDOW_SECONDS` | `60` | Rate limit time window in seconds |
| `SHORT_CODE_LENGTH` | `6` | Length of the generated short code |
| `ALLOWED_ORIGINS` | — | Comma-separated list of allowed CORS origins |
| `ADMIN_EMAIL` | — | Default admin email (seeded on startup) |
| `ADMIN_PASSWORD` | — | Default admin password |
| `ADMIN_USERNAME` | — | Default admin username |
[The Garage (Projects) — UrlShortener](#projects) UrlShortener — 🔑 Environment Variables: | — | Default admin password |
| `ADMIN_USERNAME` | — | Default admin username | ---
[The Garage (Projects) — UrlShortener](#projects) UrlShortener — 🛡️ Error Handling: | HTTP Status | Scenario |
|---|---|
| `400 Bad Request` | Invalid URL format or missing required fields |
| `401 Unauthorized` | Missing, expired, or blacklisted JWT token |
| `403 Forbidden` | Authenticated but insufficient permissions (e.g., non-admin accessing `/admin/*`) |
| `404 Not Found` | Short code does not exist in the database |
| `409 Conflict` | Username or email already registered |
| `422 Unprocessable Entity` | Request body fails Pydantic validation |
| `429 Too Many Requests` | Per-IP rate limit exceeded |
| `500 Internal Server Error` | Unexpected server-side error |
[The Garage (Projects) — UrlShortener](#projects) UrlShortener — 🛡️ Error Handling:  limit exceeded |
| `500 Internal Server Error` | Unexpected server-side error | ---
[The Garage (Projects) — UrlShortener](#projects) UrlShortener — ⚠️ Limitations: - **No custom aliases** — short codes are auto-generated; users cannot choose their own.
- **No link expiration** — short URLs do not expire unless manually deleted.
- **Single-region** — no built-in support for multi-region deployment or geo-routing.
- **No web UI** — the application is API-only; a frontend is not included.
- **No SSL out of the box** — HTTPS must be configured via a reverse proxy (e.g., Nginx, Caddy).
- **No email verification** — user registration does not require email confirmation.
[The Garage (Projects) — UrlShortener](#projects) UrlShortener — ⚠️ Limitations: No email verification** — user registration does not require email confirmation. ---
[The Garage (Projects) — UrlShortener](#projects) UrlShortener — 🚧 Future Improvements: - [ ] Custom short code aliases (vanity URLs)
- [ ] Link expiration with configurable TTL per URL
- [ ] QR code generation for each short URL
- [ ] Web frontend (React / Next.js)
- [ ] Docker + Docker Compose setup for one-command deployment
- [ ] Email verification on registration
- [ ] Password reset via email
- [ ] Geo-analytics (click location by country/region)
- [ ] Webhook support — notify external services on each redirect
- [ ] Bulk URL import via CSV
- [ ] OpenAPI schema export for third-party client generation
[The Garage (Projects) — UrlShortener](#projects) UrlShortener — 🚧 Future Improvements: URL import via CSV
- [ ] OpenAPI schema export for third-party client generation ---
[The Garage (Projects) — UrlShortener](#projects) UrlShortener — 📄 License: This project is open source and available under the [MIT License](LICENSE).

---

## [The Garage (Projects) — weather-alert-platform] weather-alert-platform

Source: https://github.com/varunsani/weather-alert-platform

[The Garage (Projects) — weather-alert-platform](#projects) weather-alert-platform (written in Python)
[The Garage (Projects) — weather-alert-platform](#projects) weather-alert-platform — Weather Alert Platform: A real-time weather alerting platform: WebSocket-based live push delivery,
Redis Pub/Sub fan-out across independently polled location feeds, a
configurable severity-classification engine, JWT-authenticated location
subscriptions (access + refresh tokens, with Redis-backed blacklisting),
on-demand cached location queries, and PostgreSQL-backed time-series
persistence. Fully async throughout (FastAPI, SQLModel + asyncpg,
redis.asyncio).
[The Garage (Projects) — weather-alert-platform](#projects) weather-alert-platform — Weather Alert Platform: ersistence. Fully async throughout (FastAPI, SQLModel + asyncpg,
redis.asyncio). ---
[The Garage (Projects) — weather-alert-platform](#projects) weather-alert-platform — 1. Architecture: ```
                                   ┌─────────────────────┐
                                   │   Open-Meteo API     │  (free, no key)
                                   └───────────▲──────────┘
                                               │ HTTP (polled)
                                   ┌───────────┴──────────┐
                                   │       poller          │  <- single process
                                   │ (app/services/poller) │     polls each UNIQUE
                                   └──────┬───────┬────────┘     subscribed location
                                          │       │               once per cycle
                          persists        │       │ publishes alert
                       WeatherReading,    │       │ (Redis Pub/Sub)
                          Alert rows      │       │
                                   ┌──────▼──┐ ┌──▼─────────────────┐
                                   │ Postgres│ │       Redis         │
                                   └────▲────┘ │ (blacklist / cache  │
                                        │      │  / pub-sub channel) │
                                        │      └──┬───────────┬──────┘
                              CRUD via  │         │ psubscribe│
                              SQLModel  │   ┌─────▼───┐  ┌────▼────┐
                                        │   │ api #1   │  │ api #2  │   <- horizontally
                                        └───┤ FastAPI  │  │ FastAPI │      scalable
                                            │ +WS      │  │ +WS     │
                                            └────┬─────┘  └────┬────┘
                                                 │ ws push       │ ws push
                                            ┌────▼────┐    ┌────▼────┐
                                            │ Client A │    │ Client B│
                                            └──────────┘    └─────────┘
```
[The Garage (Projects) — weather-alert-platform](#projects) weather-alert-platform — 1. Architecture: t B│
                                            └──────────┘    └─────────┘
``` **Why a separate poller service?** If polling lived inside every API
replica, N replicas would mean N redundant calls to Open-Meteo for the
same location, and duplicate DB rows. Instead, exactly one poller
process asks Postgres for the distinct set of locations that currently
have an active subscriber, polls each one exactly once, classifies
severity, persists the reading + any alerts, and **publishes** the
alert to a Redis Pub/Sub channel named `alerts.location.{id}`. Every API
replica subscribes to the wildcard pattern `alerts.location.*` once at
startup and forwards incoming messages only to the WebSocket clients
that are connected *to that replica* and *subscribed to that location*.
That's the fan-out.
[The Garage (Projects) — weather-alert-platform](#projects) weather-alert-platform — 2. Repository layout: ```
weather-alert-platform/
├── app/
│   ├── main.py                  # FastAPI app, lifespan, router registration
│   ├── config.py                # pydantic-settings, reads .env
│   ├── database.py              # async SQLAlchemy engine + session dependency
│   ├── redis_client.py          # shared async Redis connection pool
│   ├── models/                  # SQLModel table definitions
[The Garage (Projects) — weather-alert-platform](#projects) weather-alert-platform — 2. Repository layout: is connection pool
│   ├── models/                  # SQLModel table definitions │   │   ├── user.py, refresh_token.py, location.py,
│   │   └── subscription.py, weather_reading.py, alert.py
│   ├── schemas/                 # Pydantic request/response contracts
│   ├── auth/
│   │   ├── password.py          # bcrypt hashing
│   │   ├── jwt_handler.py        # access + refresh token create/decode
│   │   ├── blacklist.py          # Redis-backed token revocation
[The Garage (Projects) — weather-alert-platform](#projects) weather-alert-platform — 2. Repository layout:  create/decode
│   │   ├── blacklist.py          # Redis-backed token revocation │   │   └── dependencies.py       # get_current_user (HTTP) / get_current_user_ws
│   ├── routers/
│   │   ├── auth.py               # register / login / refresh / logout
│   │   ├── locations.py          # create/list polled locations
│   │   ├── subscriptions.py      # subscribe / unsubscribe / list
│   │   ├── weather.py            # cached current query + history
[The Garage (Projects) — weather-alert-platform](#projects) weather-alert-platform — 2. Repository layout: scribe / list
│   │   ├── weather.py            # cached current query + history │   │   └── ws.py                 # /ws/alerts live push endpoint
│   ├── services/
│   │   ├── weather_client.py     # Open-Meteo async HTTP client
│   │   ├── severity_engine.py    # ALL tunable thresholds live here
│   │   ├── poller.py              # the standalone polling loop
│   │   ├── pubsub.py              # publish (poller) + forward (api) via Redis
[The Garage (Projects) — weather-alert-platform](#projects) weather-alert-platform — 2. Repository layout: 
│   │   ├── pubsub.py              # publish (poller) + forward (api) via Redis │   │   └── connection_manager.py  # per-instance in-memory WS registry
│   ├── core/exceptions.py        # global exception handlers
│   └── static/test_client.html   # zero-dependency browser test client
├── alembic/                      # migrations (hand-written initial schema)
├── scripts/run_poller.py         # poller process entrypoint
[The Garage (Projects) — weather-alert-platform](#projects) weather-alert-platform — 2. Repository layout: en initial schema)
├── scripts/run_poller.py         # poller process entrypoint ├── docker/                       # entrypoint shell scripts for containers
├── Dockerfile
├── docker-compose.yml            # postgres + redis + api + poller
├── requirements.txt
├── .env.example
└── README.md
```
[The Garage (Projects) — weather-alert-platform](#projects) weather-alert-platform — 3. Prerequisites: - Docker + Docker Compose (recommended path — everything below assumes this)
- OR: Python 3.12+, a local PostgreSQL 16 and Redis 7, if you'd rather run
  it without Docker
- Git
- A free GitHub account (to push the repo, since we're using your own new repo)
[The Garage (Projects) — weather-alert-platform](#projects) weather-alert-platform — Step 1 — Get the code onto your machine: You already have the generated project folder. Open a terminal inside it:
```bash
cd weather-alert-platform
```
[The Garage (Projects) — weather-alert-platform](#projects) weather-alert-platform — Step 2 — Create your local environment file: ```bash
cp .env.example .env
```
Open `.env` and replace `JWT_SECRET_KEY` with a real random secret:
```bash
python3 -c "import secrets; print(secrets.token_urlsafe(64))"
```
Paste the output as the value of `JWT_SECRET_KEY` in `.env`.
Everything else in `.env.example` already matches the Docker Compose
service names (`postgres`, `redis`) and works out of the box.
[The Garage (Projects) — weather-alert-platform](#projects) weather-alert-platform — Step 3 — Build and start everything: ```bash
docker compose up --build
```
This starts, in order:
1. `postgres` (with a healthcheck so nothing else starts before it's ready)
2. `redis` (same)
3. `api` — waits for both, runs `alembic upgrade head` to create every
   table, then starts `uvicorn` on port 8000
4. `poller` — waits for Postgres, Redis, *and* for the `alerts` table to
   exist (i.e. api's migration has run), then starts its polling loop
[The Garage (Projects) — weather-alert-platform](#projects) weather-alert-platform — Step 3 — Build and start everything: ` table to
   exist (i.e. api's migration has run), then starts its polling loop You should see logs like:
```
weather_api      | INFO:     Uvicorn running on http://0.0.0.0:8000
weather_poller   | INFO:poller:Poller starting. Interval=300s
```
[The Garage (Projects) — weather-alert-platform](#projects) weather-alert-platform — Step 4 — Open the test client: Go to **http://localhost:8000/static/test_client.html** in a browser.
Also available: interactive API docs at **http://localhost:8000/docs**.
[The Garage (Projects) — weather-alert-platform](#projects) weather-alert-platform — Step 5 — Walk through the flow: In the test client (or via `curl`/Postman using `/docs`):
1. **Register** a user, then **Login** — this stores an access + refresh
   token in the page.
2. **Create/Get Location** — e.g. name "Hyderabad", lat `17.385`, lon
   `78.4867`. Coordinates are rounded to 2 decimals (~1.1km) so nearby
   requests reuse the same polled location instead of creating duplicates.
[The Garage (Projects) — weather-alert-platform](#projects) weather-alert-platform — Step 5 — Walk through the flow: earby
   requests reuse the same polled location instead of creating duplicates. 3. **Subscribe** to that location.
4. **Connect WebSocket** — opens `/ws/alerts?token=<access_token>`. You'll
   get a `"connected"` confirmation listing which location_ids you're
   registered for.
5. Wait for the poller's next cycle (default every 300s, configurable via
   `POLL_INTERVAL_SECONDS` in `.env` — set it to something like `30` while
[The Garage (Projects) — weather-alert-platform](#projects) weather-alert-platform — Step 5 — Walk through the flow: e via
   `POLL_INTERVAL_SECONDS` in `.env` — set it to something like `30` while testing so you don't have to wait 5 minutes). If the classified
   severity for that location crosses any threshold, you'll see an
   `ALERT PUSH` message appear live in the log, with no page refresh.
6. Try **Query Current Weather** any time — this hits the cached
   on-demand endpoint (`/weather/{id}/current`), which only calls
   Open-Meteo directly if the 5-minute Redis cache has expired.
[The Garage (Projects) — weather-alert-platform](#projects) weather-alert-platform — Step 6 — See real fan-out across multiple instances (optional): ```bash
docker compose up --build --scale api=1   # already the default
```
To actually witness cross-instance fan-out: run a second api container by
hand on a different port (`docker run` with the same image/env pointing
at the same Postgres/Redis, mapped to e.g. `8001:8000`), connect one
browser tab's WebSocket to `:8000` and another to `:8001` with the same
[The Garage (Projects) — weather-alert-platform](#projects) weather-alert-platform — Step 6 — See real fan-out across multiple instances (optional): nect one
browser tab's WebSocket to `:8000` and another to `:8001` with the same subscribed location — both will receive the same poller-published alert,
proving delivery goes through Redis, not direct process memory.
[The Garage (Projects) — weather-alert-platform](#projects) weather-alert-platform — 5. Running without Docker (local Python): ```bash
python3 -m venv venv
source venv/bin/activate           # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env                # then edit DATABASE_URL(_SYNC) and REDIS_URL
[The Garage (Projects) — weather-alert-platform](#projects) weather-alert-platform — and set a real JWT_SECRET_KEY: alembic upgrade head                 # create all tables
[The Garage (Projects) — weather-alert-platform](#projects) weather-alert-platform — terminal 1: python -m uvicorn app.main:app --reload
[The Garage (Projects) — weather-alert-platform](#projects) weather-alert-platform — terminal 2: python -m scripts.run_poller
```
[The Garage (Projects) — weather-alert-platform](#projects) weather-alert-platform — 6. Database migrations (Alembic): The initial migration (`alembic/versions/0001_initial.py`) is
hand-written to precisely match every SQLModel table. If you add or
change a model afterwards:
```bash
alembic revision --autogenerate -m "describe your change"
alembic upgrade head
```
Always review autogenerated migrations before applying them — autogenerate
is a helpful diff, not a guarantee.
[The Garage (Projects) — weather-alert-platform](#projects) weather-alert-platform — 7. API reference (summary): All endpoints except `/auth/*` and `/health` require
`Authorization: Bearer <access_token>`.
[The Garage (Projects) — weather-alert-platform](#projects) weather-alert-platform — 7. API reference (summary): s except `/auth/*` and `/health` require
`Authorization: Bearer <access_token>`. | Method | Path                          | Purpose                                   |
|--------|-------------------------------|--------------------------------------------|
| POST   | `/auth/register`              | Create a user                              |
| POST   | `/auth/login`                 | Get access + refresh token pair            |
| POST   | `/auth/refresh`                | Exchange a valid refresh token for a new access token |
| POST   | `/auth/logout`                 | Blacklist current access + refresh tokens  |
| POST   | `/locations`                   | Create or fetch an existing polled location|
| GET    | `/locations`                   | List all known locations                   |
| GET    | `/locations/{id}`              | Get one location                           |
| POST   | `/subscriptions`               | Subscribe to a location                    |
| GET    | `/subscriptions`                | List your active subscriptions            |
| DELETE | `/subscriptions/{location_id}` | Unsubscribe                                |
| GET    | `/weather/{id}/current`         | Cached on-demand current weather           |
| GET    | `/weather/{id}/history?limit=` | Persisted time-series readings             |
| WS     | `/ws/alerts?token=`             | Live alert push for your subscriptions     |
[The Garage (Projects) — weather-alert-platform](#projects) weather-alert-platform — 7. API reference (summary): | `/ws/alerts?token=`             | Live alert push for your subscriptions     | Full interactive schema: `/docs` (Swagger UI) or `/redoc`.
[The Garage (Projects) — weather-alert-platform](#projects) weather-alert-platform — 8. Severity engine — how it decides what's "severe": Every threshold lives in **`app/services/severity_engine.py`** in two
plain dicts (`SEVERITY_RULES`, `WEATHER_CODE_SEVERITY`) — nothing else in
the codebase needs to change to retune sensitivity:
[The Garage (Projects) — weather-alert-platform](#projects) weather-alert-platform — 8. Severity engine — how it decides what's "severe": SEVERITY`) — nothing else in
the codebase needs to change to retune sensitivity: - **Extreme heat / cold** — three tiers each (`WATCH` → `WARNING` →
  `SEVERE`) based on °C thresholds.
- **High wind** — three tiers based on km/h.
- **Heavy precipitation** — three tiers based on mm/hour.
- **Severe weather codes** — Open-Meteo returns a WMO weather code (fog,
  drizzle, rain, snow, thunderstorm, hail, etc.); each code is mapped
  directly to a severity tier (e.g. plain fog is a `WATCH`, hail-bearing
  thunderstorms are `SEVERE`).
[The Garage (Projects) — weather-alert-platform](#projects) weather-alert-platform — 8. Severity engine — how it decides what's "severe": y tier (e.g. plain fog is a `WATCH`, hail-bearing
  thunderstorms are `SEVERE`). For one weather reading, each of the four categories independently
produces **at most one** alert, at the highest tier it crosses — so a
single violent thunderstorm reading won't spam five overlapping alerts
for the same underlying event.
[The Garage (Projects) — weather-alert-platform](#projects) weather-alert-platform — 9. JWT auth design: - **Access token**: 15 minutes, used for all HTTP + WebSocket auth.
- **Refresh token**: 7 days, tracked in Postgres (`refresh_tokens` table)
  so a specific session can be identified/revoked, not just blacklisted.
- **Blacklisting**: both token types carry a unique `jti`. On logout,
  the presented tokens' `jti`s are written to Redis with a TTL equal to
[The Garage (Projects) — weather-alert-platform](#projects) weather-alert-platform — 9. JWT auth design:  logout,
  the presented tokens' `jti`s are written to Redis with a TTL equal to their remaining lifetime — so the blacklist entry expires exactly when
  the token would have anyway, with no manual cleanup needed.
- **WebSocket auth**: the access token is passed as `?token=` on the
  connect URL (browsers can't set custom headers during the WS
  handshake). Same validation + blacklist check as HTTP.
[The Garage (Projects) — weather-alert-platform](#projects) weather-alert-platform — 10. Git & GitHub — from zero: Inside the project folder:
```bash
git init
git add .
git commit -m "Initial commit: real-time weather alert platform"
```

Create a **new, empty** repository on GitHub (no README/license/gitignore —
those already exist locally), then:
```bash
git branch -M main
git remote add origin https://github.com/<your-username>/<your-repo-name>.git
git push -u origin main
```
[The Garage (Projects) — weather-alert-platform](#projects) weather-alert-platform — 10. Git & GitHub — from zero: ps://github.com/<your-username>/<your-repo-name>.git
git push -u origin main
``` If you use SSH instead of HTTPS:
```bash
git remote add origin git@github.com:<your-username>/<your-repo-name>.git
git push -u origin main
```

`.env` is already gitignored — never commit real secrets. Anyone cloning
the repo starts from `.env.example` as documented in Step 2 above.
[The Garage (Projects) — weather-alert-platform](#projects) weather-alert-platform — 11. A note on the free weather API: Open-Meteo's free tier requires no API key and has a generous rate limit
for non-commercial use, which is exactly why the poller design polls each
unique location once per cycle rather than once per subscriber — it's
respectful of the upstream free tier by construction, not just by luck.

## [The Garage (Projects) — WebSockets-Demo] WebSockets-Demo

Source: https://github.com/varunsani/WebSockets-Demo

[The Garage (Projects) — WebSockets-Demo](#projects) WebSockets-Demo (written in Python)
[The Garage (Projects) — WebSockets-Demo](#projects) WebSockets-Demo — 💬 WebSocket Chat Application: A real-time, multi-client chat application built with Python and WebSockets. This project consists of a **WebSocket server** that broadcasts messages to all connected clients and a **WebSocket client** that allows users to send and receive messages in real time.

---
[The Garage (Projects) — WebSockets-Demo](#projects) WebSockets-Demo — 📋 Table of Contents: - [Overview](#overview)
- [Features](#features)
- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
  - [Starting the Server](#starting-the-server)
  - [Starting the Client](#starting-the-client)
- [How It Works](#how-it-works)
  - [Server](#server)
  - [Client](#client)
- [Code Breakdown](#code-breakdown)
  - [Server Code](#server-code)
  - [Client Code](#client-code)
- [Configuration](#configuration)
- [Example Session](#example-session)
- [Error Handling](#error-handling)
- [Limitations](#limitations)
- [Future Improvements](#future-improvements)
- [License](#license)
[The Garage (Projects) — WebSockets-Demo](#projects) WebSockets-Demo — 📋 Table of Contents: limitations)
- [Future Improvements](#future-improvements)
- [License](#license) ---
[The Garage (Projects) — WebSockets-Demo](#projects) WebSockets-Demo — 🔍 Overview: This project demonstrates a lightweight, real-time chat system using Python's `asyncio` library and the `websockets` package. The server listens for incoming WebSocket connections and relays messages from one client to all other connected clients. The client connects to the server, reads input from the terminal, and displays messages from other users.

---
[The Garage (Projects) — WebSockets-Demo](#projects) WebSockets-Demo — ✨ Features: - Real-time message broadcasting to all connected clients
- Supports multiple simultaneous clients
- Asynchronous, non-blocking I/O using `asyncio`
- Graceful handling of client disconnections
- Minimal dependencies — only the `websockets` package required
- Simple terminal-based interface

---
[The Garage (Projects) — WebSockets-Demo](#projects) WebSockets-Demo — 📁 Project Structure: ```
websocket-chat/
│
├── server.py       # WebSocket server — handles connections and broadcasts messages
├── client.py       # WebSocket client — sends and receives messages via terminal
└── README.md       # Project documentation
```

---
[The Garage (Projects) — WebSockets-Demo](#projects) WebSockets-Demo — ✅ Prerequisites: - Python **3.7** or higher
- pip (Python package manager)

---
[The Garage (Projects) — WebSockets-Demo](#projects) WebSockets-Demo — 📦 Installation: **1. Clone the repository**

```bash
git clone https://github.com/varunsani/WebSockets-Demo.git
cd WebSockets-Demo
```

**2. (Optional) Create and activate a virtual environment**

```bash
python -m venv venv
[The Garage (Projects) — WebSockets-Demo](#projects) WebSockets-Demo — On Linux/macOS:: source venv/bin/activate
[The Garage (Projects) — WebSockets-Demo](#projects) WebSockets-Demo — On Windows:: venv\Scripts\activate
```

**3. Install the required dependency**

```bash
pip install websockets
```

---
[The Garage (Projects) — WebSockets-Demo](#projects) WebSockets-Demo — Starting the Server: Run the server first. It will listen for incoming WebSocket connections on `localhost` at port `12345`.

```bash
python server.py
```

The server will start silently. It is now ready to accept client connections.
[The Garage (Projects) — WebSockets-Demo](#projects) WebSockets-Demo — Starting the Client: Open one or more new terminal windows and run the client in each:

```bash
python client.py
```

Each terminal represents a separate chat user. Type a message and press **Enter** to send it. Messages from other connected clients will appear automatically.

---
[The Garage (Projects) — WebSockets-Demo](#projects) WebSockets-Demo — Server: 1. The server starts a WebSocket listener on `ws://localhost:12345`.
2. When a new client connects, it is added to a global `connected_clients` set.
3. For every message received from a client, the server loops through all other connected clients and sends them the message.
4. If a client disconnects (cleanly or due to an error), it is safely removed from the set.
[The Garage (Projects) — WebSockets-Demo](#projects) WebSockets-Demo — Client: 1. The client establishes a WebSocket connection to `ws://localhost:12345`.
2. Two asynchronous tasks run concurrently using `asyncio.gather`:
   - **`send_messages`**: Reads input from the terminal (using `asyncio.to_thread` to avoid blocking the event loop) and sends it to the server.
   - **`receive_messages`**: Listens for incoming messages from the server and prints them to the terminal.

---
[The Garage (Projects) — WebSockets-Demo](#projects) WebSockets-Demo — Server Code: ```python
import asyncio
import websockets
[The Garage (Projects) — WebSockets-Demo](#projects) WebSockets-Demo — Set of connected clients: connected_clients = set()
[The Garage (Projects) — WebSockets-Demo](#projects) WebSockets-Demo — Function to handle each client connection: async def handle_client(websocket):
[The Garage (Projects) — WebSockets-Demo](#projects) WebSockets-Demo — Add the new client to the set of connected clients: connected_clients.add(websocket)
    try:
[The Garage (Projects) — WebSockets-Demo](#projects) WebSockets-Demo — Listen for messages from the client: async for message in websocket:
[The Garage (Projects) — WebSockets-Demo](#projects) WebSockets-Demo — Broadcast the message to all other connected clients: for client in connected_clients.copy():
                if client != websocket:
                    try:
                        await client.send(message)
                    except websockets.exceptions.ConnectionClosed:
                        pass
    except websockets.exceptions.ConnectionClosed:
        pass
    finally:
[The Garage (Projects) — WebSockets-Demo](#projects) WebSockets-Demo — Remove the client from the set of connected clients: connected_clients.remove(websocket)
[The Garage (Projects) — WebSockets-Demo](#projects) WebSockets-Demo — Main function to start the WebSocket server: async def main():
    server = await websockets.serve(handle_client, 'localhost', 12345)
    await server.wait_closed()
[The Garage (Projects) — WebSockets-Demo](#projects) WebSockets-Demo — Run the server: if __name__ == "__main__":
    asyncio.run(main())
```

**Key Points:**
[The Garage (Projects) — WebSockets-Demo](#projects) WebSockets-Demo — Run the server: if __name__ == "__main__":
    asyncio.run(main())
```

**Key Points:** | Component | Description |
|---|---|
| `connected_clients` | A `set` that tracks all currently active WebSocket connections |
| `handle_client()` | Coroutine invoked for each new connection; handles receiving and broadcasting |
| `connected_clients.copy()` | Used to avoid modifying the set while iterating over it |
| `ConnectionClosed` | Caught to gracefully handle clients that disconnect mid-broadcast |
| `finally` block | Ensures a client is always removed from the set on disconnect |
[The Garage (Projects) — WebSockets-Demo](#projects) WebSockets-Demo — Run the server: finally` block | Ensures a client is always removed from the set on disconnect | ---
[The Garage (Projects) — WebSockets-Demo](#projects) WebSockets-Demo — Client Code: ```python
import asyncio
import websockets
[The Garage (Projects) — WebSockets-Demo](#projects) WebSockets-Demo — Function to send messages to the server: async def send_messages(websocket):
    while True:
        message = await asyncio.to_thread(input, "Enter message: ")
        await websocket.send(message)
[The Garage (Projects) — WebSockets-Demo](#projects) WebSockets-Demo — Function to receive messages from the server: async def receive_messages(websocket):
    async for message in websocket:
        print(f"Received: {message}")
[The Garage (Projects) — WebSockets-Demo](#projects) WebSockets-Demo — Function to handle the chat client: async def chat():
    async with websockets.connect('ws://localhost:12345') as websocket:
        await asyncio.gather(
            send_messages(websocket),
            receive_messages(websocket)
        )
[The Garage (Projects) — WebSockets-Demo](#projects) WebSockets-Demo — Run the client: if __name__ == "__main__":
    asyncio.run(chat())
```

**Key Points:**
[The Garage (Projects) — WebSockets-Demo](#projects) WebSockets-Demo — Run the client: if __name__ == "__main__":
    asyncio.run(chat())
```

**Key Points:** | Component | Description |
|---|---|
| `asyncio.to_thread(input, ...)` | Runs the blocking `input()` call in a separate thread so it doesn't block the event loop |
| `asyncio.gather()` | Runs both send and receive coroutines concurrently |
| `async for message in websocket` | Listens for incoming messages as an async generator |
| `async with websockets.connect(...)` | Ensures the connection is properly opened and closed |
[The Garage (Projects) — WebSockets-Demo](#projects) WebSockets-Demo — Run the client: ebsockets.connect(...)` | Ensures the connection is properly opened and closed | ---
[The Garage (Projects) — WebSockets-Demo](#projects) WebSockets-Demo — 🔧 Configuration: The server host and port are currently hardcoded. To change them, update these values in both files:

**In `server.py`:**
```python
server = await websockets.serve(handle_client, 'localhost', 12345)
[The Garage (Projects) — WebSockets-Demo](#projects) WebSockets-Demo — host        port: ```

**In `client.py`:**
```python
async with websockets.connect('ws://localhost:12345') as websocket:
[The Garage (Projects) — WebSockets-Demo](#projects) WebSockets-Demo — host        port: ```

---
[The Garage (Projects) — WebSockets-Demo](#projects) WebSockets-Demo — 💡 Example Session: **Terminal 1 — Server:**
```
$ python server.py
(server is running silently, waiting for connections)
```

**Terminal 2 — Client A:**
```
$ python client.py
Enter message: Hello, everyone!
Enter message: 
Received: Hey there! — from Client B
```

**Terminal 3 — Client B:**
```
$ python client.py
Received: Hello, everyone!
Enter message: Hey there! — from Client B
Enter message: 
```

---
[The Garage (Projects) — WebSockets-Demo](#projects) WebSockets-Demo — 🛡️ Error Handling: | Scenario | Handling |
|---|---|
| Client disconnects abruptly | `ConnectionClosed` exception is caught; client is removed from `connected_clients` |
| Server sends to a disconnected client | `ConnectionClosed` caught inside broadcast loop; other clients continue to receive |
| `input()` blocking the event loop | Resolved by using `asyncio.to_thread()` |
| Iterating over `connected_clients` while removing | Solved by iterating over `connected_clients.copy()` |
[The Garage (Projects) — WebSockets-Demo](#projects) WebSockets-Demo — 🛡️ Error Handling: _clients` while removing | Solved by iterating over `connected_clients.copy()` | ---
[The Garage (Projects) — WebSockets-Demo](#projects) WebSockets-Demo — ⚠️ Limitations: - **No usernames**: Messages are broadcast without any sender identification.
- **No message history**: New clients joining mid-session will not see past messages.
- **No authentication**: Any client can connect to the server.
- **Local only (by default)**: The server binds to `localhost` and is not accessible from other machines without reconfiguration.
- **No SSL/TLS**: Communication is unencrypted (`ws://` not `wss://`).
[The Garage (Projects) — WebSockets-Demo](#projects) WebSockets-Demo — ⚠️ Limitations: guration.
- **No SSL/TLS**: Communication is unencrypted (`ws://` not `wss://`). ---
[The Garage (Projects) — WebSockets-Demo](#projects) WebSockets-Demo — 🚧 Future Improvements: - [ ] Add username support (prompt on connection)
- [ ] Add message timestamps
- [ ] Store and replay recent message history for new clients
- [ ] Add SSL/TLS support for secure connections (`wss://`)
- [ ] Allow server host/port to be configured via command-line arguments or a config file
- [ ] Add a simple web-based UI using HTML/JavaScript WebSocket API
- [ ] Implement private/direct messaging between users
- [ ] Add reconnection logic to the client
[The Garage (Projects) — WebSockets-Demo](#projects) WebSockets-Demo — 🚧 Future Improvements: rivate/direct messaging between users
- [ ] Add reconnection logic to the client ---
[The Garage (Projects) — WebSockets-Demo](#projects) WebSockets-Demo — 📄 License: This project is open source and available under the [MIT License](LICENSE).

---

## [The Garage (Projects) — Todo-List] Todo-List

Source: https://github.com/varunsani/Todo-List

[The Garage (Projects) — Todo-List](#projects) Todo-List (written in Python)
[The Garage (Projects) — Todo-List](#projects) Todo-List — Authentication & Security: - JWT authentication with access & refresh tokens
- Email verification (mandatory)
- Password reset functionality
- bcrypt password hashing
- Token refresh mechanism
[The Garage (Projects) — Todo-List](#projects) Todo-List — Todo Management: - Multiple todo lists support
- CRUD operations for tasks
- Priority levels (Low, Medium, High, Urgent)
- Status tracking (Pending, In Progress, Completed, Archived, Deleted)
- Due dates and reminders
- Soft delete with restore capability
- File attachments support
- Subtasks support
[The Garage (Projects) — Todo-List](#projects) Todo-List — Ideas Module: - Quick idea capture
- Convert ideas to todo lists
- Categorization
- Status tracking (New, Considered, Converted, Discarded)
[The Garage (Projects) — Todo-List](#projects) Todo-List — Notifications: - In-app notifications
- Email reminders for due tasks
[The Garage (Projects) — Todo-List](#projects) Todo-List — Prerequisites: - Python 3.11+
- PostgreSQL
[The Garage (Projects) — Todo-List](#projects) Todo-List — Environment Setup: 1. Clone and setup:
```bash
cp .env.example .env

## [The Garage (Projects) — FlaskDemo] FlaskDemo

Source: https://github.com/varunsani/FlaskDemo

[The Garage (Projects) — FlaskDemo](#projects) FlaskDemo (written in Python)

## [Experience] View certificate · purple sector →

Source: https://drive.google.com/file/d/189W7YA8ieMVIF-pLQ5YEOP7R1dHGe52Q/view?usp=sharing

[Experience](#experience) (Referenced by Varun in 'Experience') View certificate · purple sector →: INTERNSHIP
COMPLETION CERTIFICATE
PRACHI PATEL
Program Manager
YASIN SHAH
Founder & CEO
PRESENTED TO:
SANI VARUN
Has successfully completed his internship as a Machine
Learning Engineer from 03rd June 2024 to 19th July 2024.
He has shown superior dedication and outstanding
performance toward Machine Learning projects.Technocolabs
Softwares Inc. T
[Experience](#experience) (Referenced by Varun in 'Experience') View certificate · purple sector →: nding
performance toward Machine Learning projects.Technocolabs
Softwares Inc. T Certificate ID: 0108202490242Date: 01-08-2024I n t e r n s h i p
T r a i n e e
TECHNOCOLOABS SOFTWARES PVT.LTD    CIN: U72900MP2020PTC052601

## [Projects] View on GitHub · overtake →

Source: https://github.com/varunsani/Portfolio-bot

[Projects](#projects) (Referenced by Varun in 'Projects') View on GitHub · overtake →: Contribute to varunsani/Portfolio-bot development by creating an account on GitHub.

## [Projects] View on GitHub · overtake →

Source: https://github.com/varunsani/weather-alert-platform

[Projects](#projects) (Referenced by Varun in 'Projects') View on GitHub · overtake →: Contribute to varunsani/weather-alert-platform development by creating an account on GitHub.

## [Projects] View on GitHub · overtake →

Source: https://github.com/varunsani/UrlShortener

[Projects](#projects) (Referenced by Varun in 'Projects') View on GitHub · overtake →: Contribute to varunsani/UrlShortener development by creating an account on GitHub.

## [Contact] ICTCS 2025 Paper · chequered flag ↗

Source: https://ceur-ws.org/Vol-4039/paper19.pdf

[Contact](#contact) (Referenced by Varun in 'Contact') ICTCS 2025 Paper · chequered flag ↗: %PDF-1.7
%����
1 0 obj 
<<
/Kids [2 0 R 3 0 R 4 0 R 5 0 R 6 0 R 7 0 R 8 0 R]
/Type /Pages
/Count 7
>>
endobj 
2 0 obj 
<<
/Annots [9 0 R 10 0 R 11 0 R 12 0 R 13 0 R 14 0 R 15 0 R 16 0 R]
/Resources 
<<
/Font 
<<
/F161 17 0 R
/F29 18 0 R
/F37 19 0 R
/F32 20 0 R
/F68 21 0 R
/F118 22 0 R
/F67 23 0 R
/F117 24 0 R
/F213 25 0 R
/F65 26 0 R
/F223 27 0 R
/F99 28 0 R
/F98 29 0 R
/F101 30 0 R
/F97 31 0 R
[Contact](#contact) (Referenced by Varun in 'Contact') ICTCS 2025 Paper · chequered flag ↗: 25 0 R
/F65 26 0 R
/F223 27 0 R
/F99 28 0 R
/F98 29 0 R
/F101 30 0 R
/F97 31 0 R /F100 32 0 R
/F96 33 0 R
/F71 34 0 R
/F70 35 0 R
/F133 36 0 R
/F132 37 0 R
/F131 38 0 R
/F167 39 0 R
/F164 40 0 R
>>
/ProcSet [/PDF /Text /ImageB /ImageC /ImageI]
/XObject 
<<
/Im1 41 0 R
/Xi1 42 0 R
/Xi0 43 0 R
>>
>>
/Type /Page
/Parent 1 0 R
/Contents [44 0 R 45 0 R 46 0 R 47 0 R 48 0 R]
/MediaBox [0 0 595.276 841.89]
/Group 49 0 R
>>
endobj 
9 0 obj 
<<
/Subtype /Link
/Border [0 0 0]
[Contact](#contact) (Referenced by Varun in 'Contact') ICTCS 2025 Paper · chequered flag ↗: .276 841.89]
/Group 49 0 R
>>
endobj 
9 0 obj 
<<
/Subtype /Link
/Border [0 0 0] /Type /Annot
/H /I
/F 4
/C [0 1 1]
/Rect [82.71 105.348 159.329 117.302]
/A 
<<
/URI (mailto:deepak@iitpkd.ac.in)
/Type /Action
/S /URI
>>
>>
endobj 
10 0 obj 
<<
/Subtype /Link
/Border [0 0 0]
/Type /Annot
/H /I
/F 4
/C [0 1 1]
/Rect [237.123 105.348 333.917 117.302]
/A 
<<
/URI (mailto:varunsani625@gmail.com)
/Type /Action
/S /URI
>>
>>
endobj 
11 0 obj 
<<
/Subtype /Link
/Border [0 0 0]
[Contact](#contact) (Referenced by Varun in 'Contact') ICTCS 2025 Paper · chequered flag ↗: 
/Type /Action
/S /URI
>>
>>
endobj 
11 0 obj 
<<
/Subtype /Link
/Border [0 0 0] /Type /Annot
/H /I
/F 4
/C [0 1 1]
/Rect [369.623 105.348 439.266 117.302]
/A 
<<
/URI (mailto:biren@iitpkd.ac.in)
/Type /Action
/S /URI
>>
>>
endobj 
12 0 obj 
<<
/Subtype /Link
/Border [0 0 0]
/Type /Annot
/H /I
/F 4
/C [0 1 1]
/Rect [71.502 93.217 158.738 104.788]
/A 
<<
/URI (mailto:senjishnu5@gmail.com)
/Type /Action
/S /URI
>>
>>
endobj 
13 0 obj 
<<
/Subtype /Link
/Border [0 0 0]
[Contact](#contact) (Referenced by Varun in 'Contact') ICTCS 2025 Paper · chequered flag ↗: 
/Type /Action
/S /URI
>>
>>
endobj 
13 0 obj 
<<
/Subtype /Link
/Border [0 0 0] /Type /Annot
/H /I
/F 4
/C [0 1 1]
/Rect [82.71 82.259 160.504 95.21]
/A 
<<
/URI (https://orcid.org/0000-0001-9101-8967)
/Type /Action
/S /URI
>>
>>
endobj 
14 0 obj 
<<
/Subtype /Link
/Border [0 0 0]
/Type /Annot
/H /I
/F 4
/C [0 1 1]
/Rect [238.298 82.259 316.092 95.21]
/A 
<<
/URI (https://orcid.org/0000-0001-7444-7161)
/Type /Action
/S /URI
>>
>>
endobj 
15 0 obj 
<<
/Subtype /Link
[Contact](#contact) (Referenced by Varun in 'Contact') ICTCS 2025 Paper · chequered flag ↗: -0001-7444-7161)
/Type /Action
/S /URI
>>
>>
endobj 
15 0 obj 
<<
/Subtype /Link /Border [0 0 0]
/Type /Annot
/H /I
/F 4
/C [0 1 1]
/Rect [376.401 82.259 454.196 95.21]
/A 
<<
/URI (https://orcid.org/0000-0002-8724-9583)
/Type /Action
/S /URI
>>
>>
endobj 
16 0 obj 
<<
/Subtype /Link
/Border [0 0 0]
/Type /Annot
/H /I
/F 4
/C [0 1 1]
/Rect [71.502 68.895 111.676 84.251]
/A 
<<
/URI (https://creativecommons.org/licenses/by/4.0/deed.en)
/Type /Action
/S /URI
>>
>>
endobj
[Contact](#contact) (Referenced by Varun in 'Contact') ICTCS 2025 Paper · chequered flag ↗: /creativecommons.org/licenses/by/4.0/deed.en)
/Type /Action
/S /URI
>>
>>
endobj 17 0 obj 
<<
/Encoding 50 0 R
/ToUnicode 51 0 R
/Widths 52 0 R
/Subtype /Type1
/Type /Font
/FirstChar 46
/LastChar 121
/FontDescriptor 53 0 R
/BaseFont /ILXCAD+LibertinusSans-Bold
>>
endobj 
50 0 obj 
<<
/Type /Encoding
[Contact](#contact) (Referenced by Varun in 'Contact') ICTCS 2025 Paper · chequered flag ↗:  R
/BaseFont /ILXCAD+LibertinusSans-Bold
>>
endobj 
50 0 obj 
<<
/Type /Encoding /Differences [46 /period 49 /one /two /three /four 65 /A 68 /D 71 /G /H /I 75 /K /L /M 80 /P 82 /R 84 /T /U 97 /a /b /c /d /e /f /g /h /i 107 /k /l /m /n /o /p /q /r /s /t /u /v /w 121 /y]
>>
endobj 
51 0 obj 
<<
/Filter /FlateDecode
/Length 867
>>
stream
[Contact](#contact) (Referenced by Varun in 'Contact') ICTCS 2025 Paper · chequered flag ↗: /v /w 121 /y]
>>
endobj 
51 0 obj 
<<
/Filter /FlateDecode
/Length 867
>>
stream x��Uˊ�@��+&���A�zc�H,�E��܂-�7[2�|ؿ�Tw{!��`SjWwW���ݛ/���ƃ�wZ}u�x�ZV��������'�:��~�߫/���ܢ���q藷��8��k�n����{���Q�O�{��?�i���sh�S.�c��0<�g����|�w�S�1�_N~�t+ߢ

## [Contact] ORCID · parc fermé ↗

Source: https://orcid.org/0009-0001-4816-2119

[Contact](#contact) (Referenced by Varun in 'Contact') ORCID · parc fermé ↗: ORCID Please enable JavaScript to continue using this application.

## [Beyond] Attention Is All You Need

Source: https://arxiv.org/abs/1706.03762

[Beyond](#beyond) (Referenced by Varun in 'Beyond') Attention Is All You Need: The dominant sequence transduction models are based on complex recurrent or convolutional neural networks in an encoder-decoder configuration. The best performing models also connect the encoder and decoder through an attention mechanism. We propose a new simple network architecture, the Transformer, based solely on attention mechanisms, dispensing with recurrence and convolutions entirely
[Beyond](#beyond) (Referenced by Varun in 'Beyond') Attention Is All You Need: ly on attention mechanisms, dispensing with recurrence and convolutions entirely Experiments on two machine translation tasks show these models to be superior in quality while being more parallelizable and requiring significantly less time to train. Our model achieves 28.4 BLEU on the WMT 2014 English-to-German translation task, improving over the existing best results, including ensembles by over 2 BLEU
[Beyond](#beyond) (Referenced by Varun in 'Beyond') Attention Is All You Need: sk, improving over the existing best results, including ensembles by over 2 BLEU On the WMT 2014 English-to-French translation task, our model establishes a new single-model state-of-the-art BLEU score of 41.8 after training for 3.5 days on eight GPUs, a small fraction of the training costs of the best models from the literature
[Beyond](#beyond) (Referenced by Varun in 'Beyond') Attention Is All You Need: s, a small fraction of the training costs of the best models from the literature We show that the Transformer generalizes well to other tasks by applying it successfully to English constituency parsing both with large and limited training data.

## [Beyond] LoRA: Low-Rank Adaptation of Large Language Models

Source: https://arxiv.org/abs/2106.09685

[Beyond](#beyond) (Referenced by Varun in 'Beyond') LoRA: Low-Rank Adaptation of Large Language Models: An important paradigm of natural language processing consists of large-scale pre-training on general domain data and adaptation to particular tasks or domains. As we pre-train larger models, full fine-tuning, which retrains all model parameters, becomes less feasible
[Beyond](#beyond) (Referenced by Varun in 'Beyond') LoRA: Low-Rank Adaptation of Large Language Models: ls, full fine-tuning, which retrains all model parameters, becomes less feasible Using GPT-3 175B as an example -- deploying independent instances of fine-tuned models, each with 175B parameters, is prohibitively expensive. We propose Low-Rank Adaptation, or LoRA, which freezes the pre-trained model weights and injects trainable rank decomposition matrices into each layer of the Transformer architecture, greatly reducing the number of trainable parameters for downstream tasks
[Beyond](#beyond) (Referenced by Varun in 'Beyond') LoRA: Low-Rank Adaptation of Large Language Models: ecture, greatly reducing the number of trainable parameters for downstream tasks Compared to GPT-3 175B fine-tuned with Adam, LoRA can reduce the number of trainable parameters by 10,000 times and the GPU memory requirement by 3 times. LoRA performs on-par or better than fine-tuning in model quality on RoBERTa, DeBERTa, GPT-2, and GPT-3, despite having fewer trainable parameters, a higher training throughput, and, unlike adapters, no additional inference latency
[Beyond](#beyond) (Referenced by Varun in 'Beyond') LoRA: Low-Rank Adaptation of Large Language Models: igher training throughput, and, unlike adapters, no additional inference latency We also provide an empirical investigation into rank-deficiency in language model adaptation, which sheds light on the efficacy of LoRA. We release a package that facilitates the integration of LoRA with PyTorch models and provide our implementations and model checkpoints for RoBERTa, DeBERTa, and GPT-2 at https://github.com/microsoft/LoRA.

## [Beyond] honeycomb conjecture

Source: https://en.wikipedia.org/wiki/Honeycomb_conjecture

[Beyond](#beyond) (Referenced by Varun in 'Beyond') honeycomb conjecture: Honeycomb theorem:

## [Beyond] actual published mathematics

Source: https://plus.maths.org/shoelace-book

[Beyond](#beyond) (Referenced by Varun in 'Beyond') actual published mathematics: How do you do it? Horizontally from side to side, or perhaps criss-cross, producing a series of Xs running up your feet? Towards the end of The shoelace book, its author Burkard Polster raises a troubling question
[Beyond](#beyond) (Referenced by Varun in 'Beyond') actual published mathematics: end of The shoelace book, its author Burkard Polster raises a troubling question Despite all the here-today, gone-tomorrow vagaries of fashion, and in spite of the huge variety of shoe styles available to us in this golden age of footwear, why does almost everyone lace their shoes in one of these two ways?

## [Beyond] Fermat's Last Theorem

Source: https://en.wikipedia.org/wiki/Fermat%27s_Last_Theorem

[Beyond](#beyond) (Referenced by Varun in 'Beyond') Fermat's Last Theorem: Fermat's Last Theorem:

## [Beyond] Stopping by Woods on a Snowy Evening

Source: https://www.poetryfoundation.org/poems/42891/stopping-by-woods-on-a-snowy-evening

[Beyond](#beyond) (Referenced by Varun in 'Beyond') Stopping by Woods on a Snowy Evening: My little horse must think it queer To stop without a farmhouse near Between the woods and frozen lake The darkest evening of the year.

## [Beyond] Uffizi

Source: https://www.uffizi.it/en

[Beyond](#beyond) (Referenced by Varun in 'Beyond') Uffizi: Welcome to the official website of the Uffizi Galleries in Florence. Here you can find information about the collections of the Uffizi, Palazzo Pitti, and Boboli Gardens.

## [Beyond] Louvre

Source: https://www.louvre.fr/en

[Beyond](#beyond) (Referenced by Varun in 'Beyond') Louvre: Welcome to the Louvre – prepare your visit, explore the palace and museum collections and check out the latest news

## [Beyond] Rijksmuseum

Source: https://www.rijksmuseum.nl/en

[Beyond](#beyond) (Referenced by Varun in 'Beyond') Rijksmuseum: The museum of the Netherlands, in Amsterdam. 800 years of Dutch history, with the great Dutch masters as Rembrandt, Vermeer and Van Gogh.

## [Beyond] Atonement

Source: https://www.goodreads.com/book/show/6867.Atonement

[Beyond](#beyond) (Referenced by Varun in 'Beyond') Atonement: Atonement:

## [Beyond] Michael Jackson

Source: https://www.michaeljackson.com/

[Beyond](#beyond) (Referenced by Varun in 'Beyond') Michael Jackson: The official Michael Jackson website. Explore the albums and videos, read the latest news from the Estate, and shop official MJ merchandise and vinyl.

## [Beyond] La La Land's

Source: https://en.wikipedia.org/wiki/La_La_Land_(soundtrack)

[Beyond](#beyond) (Referenced by Varun in 'Beyond') La La Land's: La La Land (soundtrack):

## [Beyond] Sicilian

Source: https://en.wikipedia.org/wiki/Sicilian_Defence

[Beyond](#beyond) (Referenced by Varun in 'Beyond') Sicilian: Sicilian Defence:

## [Beyond] Ruy Lopez

Source: https://en.wikipedia.org/wiki/Ruy_Lopez

[Beyond](#beyond) (Referenced by Varun in 'Beyond') Ruy Lopez: Ruy Lopez:

## [Beyond] Chess.com ratings

Source: https://www.chess.com/member/varunsani

[Beyond](#beyond) Varun's Chess.com ratings — Rapid rating: 1882; Blitz rating: 1222 (best: 1257).

## [Beyond] Extended Highlights | 2024 Sao Paulo Grand Prix

Source: https://www.youtube.com/watch?v=QGTErgNcpDM

[Beyond](#beyond) (Referenced by Varun in 'Beyond') YouTube video: "Extended Highlights | 2024 Sao Paulo Grand Prix" by FORMULA 1

## [Beyond] 1988 Monaco qualifying lap

Source: https://www.mclaren.com/racing/heritage/formula-1/drivers/ayrton-senna/f1s-greatest-ever-qualifying-lap-ayrton-senna-in-monaco-1988/

[Beyond](#beyond) (Referenced by Varun in 'Beyond') 1988 Monaco qualifying lap: McLaren Racing:  How Senna pulled off the finest Qualifying lap in F1 history, and why you’ve never seen it

## [Beyond] Extended Highlights | 1995 Belgian Grand Prix

Source: https://www.youtube.com/watch?v=X8x4RTdo5_8

[Beyond](#beyond) (Referenced by Varun in 'Beyond') YouTube video: "Extended Highlights | 1995 Belgian Grand Prix" by FORMULA 1