# Varun Sani Portfolio
Source: https://varunsani.vercel.app

## [Hero / Introduction](#about)
[Hero / Introduction](#about) Varun Sani is a Computer Science engineer who loves both queueing theory and qualifying laps. He builds API backends, async architectures and machine learning pipelines designed to survive contact with real, messy data. Off the clock he reads papers, chases proofs, and watches races.

## [Team Radio](#about)
[Team Radio](#about) A live feed from the cockpit, styled as radio chatter between "Race Engineer" and "VS1" (Varun). The tone: precise, confident, F1-inflected communication between pit wall and driver.

## [Formation Lap (About)](#about)
[Formation Lap (About)](#about) Varun is a Computer Science engineer interested in building intelligent software systems, from backend infrastructure and distributed applications to machine learning and AI. He graduated with a B.Tech in Computer Science & Engineering from IIT Palakkad. He works across software development and machine learning, building async APIs, real-time pub/sub architectures and ML pipelines. His interests span machine learning, AI and software engineering, with a particular fascination for systems design. Alongside coursework, he spent a year chasing an open question in combinatorics that turned into a research paper. He is based in Hyderabad, India, and works async, reachable anywhere.

## [The Pit Crew (Skills)](#skills)
[The Pit Crew (Skills)](#skills) Languages: Python, C++, C. Backend & APIs: FastAPI, REST, JWT Auth, WebSockets. Databases & ORMs: PostgreSQL, Redis, MongoDB, SQLModel, Alembic. ML & Data: scikit-learn, PyTorch, NumPy, Pandas, Matplotlib. Tools & Platforms: Docker, Git, GitHub, Postman, Ubuntu, Jupyter. Certifications: Introduction to Machine Learning (NPTEL), Machine Learning A-Z: AI, Python (Udemy).

## [Race Stints (Experience)](#experience)
[Race Stints (Experience)](#experience) Machine Learning Engineer Intern at Technocolabs Softwares Inc., June to July 2024, remote. Worked on two problems: employee attrition prediction and loan default risk in peer-to-peer lending. Built classification pipelines (Logistic Regression, Decision Tree, Random Forest, XGBoost, a 3-layer Neural Network) on a 15,000-row, 40-feature HR dataset, pushing the best performer from about 72% to about 85% accuracy and F1 from 0.68 to about 0.82 through hyperparameter tuning and threshold optimization. Developed regression ensembles for loan default risk on a 10,000-row, 60-feature dataset, cutting RMSE by about 18% via feature selection, stacking and weighted averaging, validated with 5-fold cross-validation. Ran end-to-end preprocessing: median/mode imputation for 12% missing values, SMOTE for a 15% minority class, StandardScaler normalization, and engineered 8 interaction features that contributed a 5% lift in F1 score for the attrition model.

## [The Garage (Projects)](#projects)
[The Garage (Projects)](#projects) Real-Time Severe Weather Alerting System — built with FastAPI, Redis Pub/Sub, WebSockets, PostgreSQL, Docker. Replaces client-side polling with server-pushed alerts: a poller container queries the Open-Meteo API every 5 minutes per subscribed location and publishes classified conditions over Redis Pub/Sub. Each API replica has its own WebSocket forwarder for horizontal scaling. Configurable severity engine across four condition categories at three tiers, coordinates rounded to about 1.1 km. Verified end to end in Postman including live WebSocket connections. GitHub: https://github.com/varunsani/weather-alert-platform

[The Garage (Projects)](#projects) URL Shortener — built with FastAPI, REST APIs, PostgreSQL, Redis, JWT, SQLModel, Alembic. A deliberately over-engineered URL shortener focused on production concerns: rate limiting, caching, revocable auth. Fully asynchronous, router/middleware/service/repository layered architecture, unique 6-character base62 short codes, bcrypt-hashed credentials, ACID-compliant PostgreSQL schema. 15-minute JWT access tokens and 7-day refresh tokens, revoked tokens blacklisted in Redis with matched TTLs. Rate limiting: 10 creations and 60 redirects per minute per IP. Redirect lookups cached in Redis for 1 hour. Click analytics tracked across daily/weekly/monthly windows via async counters. GitHub: https://github.com/varunsani/UrlShortener

## [The Wind Tunnel (Research)](#research)
[The Wind Tunnel (Research)](#research) Paper: "Multipacking in Hypercubes," accepted at ICTCS 2025, Pescara, Italy, co-authored with faculty at IIT Palakkad, worked on from August 2024 to July 2025. The research addressed a six-year-old open question in combinatorics about broadcast domination and multipacking numbers. Key results: pinned down the multipacking number of the n-dimensional hypercube Qn to within a lower-order term, between floor(n/2) and n/2 + O(sqrt(n)), via a recursive construction; bounded the construction using Spencer's discrepancy theorem; showed that hypercubes are the first known infinite family of connected graphs where the ratio of broadcast domination number to multipacking number approaches 2 as n grows. Paper: https://ceur-ws.org/Vol-4039/paper19.pdf. ORCID: https://orcid.org/0009-0001-4816-2119

## [Off Track (Interests)](#beyond)
[Off Track (Interests)](#beyond) Engineering: reads papers regularly; favorites include "Attention Is All You Need" (https://arxiv.org/abs/1706.03762) and "LoRA: Low-Rank Adaptation of Large Language Models" (https://arxiv.org/abs/2106.09685).

[Off Track (Interests)](#beyond) Mathematics: drawn to Ramanujan, Newton and Euler. Follows the honeycomb conjecture, the mathematics of shoelace tying, and Fermat's Last Theorem.

[Off Track (Interests)](#beyond) Writing: writes spontaneous poems. Admires typewriter poet Olivia Dodd and Robert Frost's "Stopping by Woods on a Snowy Evening."

[Off Track (Interests)](#beyond) Art: dream destinations are the Uffizi in Florence, the Louvre, and Amsterdam's Rijksmuseum — not yet visited.

[Off Track (Interests)](#beyond) Books & Films: favorite book is Ian McEwan's "Atonement"; favorite film is Christopher Nolan's "The Prestige," followed by "Eternal Sunshine of the Spotless Mind," with "The Godfather" and "12 Angry Men" as evergreen rewatches.

[Off Track (Interests)](#beyond) Music: Michael Jackson, La La Land's jazz score, and Carnatic classical.

[Off Track (Interests)](#beyond) Chess: two gold medals at college championships. Plays the Sicilian Defence with Black and the Ruy Lopez with White. Favorite games to replay: Kasparov vs. Karpov (1985 World Championship), Fischer vs. Spassky (1972 Game 6), Carlsen vs. Karjakin (2016 World Championship tiebreak). Chess.com profile: https://www.chess.com/member/varunsani

[Off Track (Interests)](#beyond) Racing: drawn to F1's systems thinking and strategy. Favorite drives to rewatch: Max Verstappen's P17-to-P1 at São Paulo 2024, Ayrton Senna's 1988 Monaco qualifying lap, and Michael Schumacher's 1995 win at Spa from 16th on the grid.

## [Post-Race Debrief (Contact)](#contact)
[Post-Race Debrief (Contact)](#contact) Email: varunsani625@gmail.com. Phone: +91 99890 44369. LinkedIn: https://www.linkedin.com/in/varun-sani-b2056a371/. GitHub: https://github.com/varunsani. Resume: https://drive.google.com/file/d/1JjJZtAeLVnRYEXLAK_Xa-_nOhYypzAFn/view. ICTCS 2025 Paper: https://ceur-ws.org/Vol-4039/paper19.pdf. ORCID: https://orcid.org/0009-0001-4816-2119. LeetCode: https://leetcode.com/u/varun_sani/
