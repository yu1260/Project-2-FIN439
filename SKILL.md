---
name: buffett-sec
description: Analyze a public company's business in a Buffett-inspired style using keyless SEC 10-K facts, deterministic owner earnings and ROE checks, and a numerically audited memo. Use for the Lab 18 business-quality review, without price or valuation data.
---

Run `scripts/sec_facts.py TICKER --user-agent "USER NAME REAL_EMAIL" --out REPORT_DIRECTORY` with Python. Obtain the user's real name and email if not supplied; never invent a contact. Alternatively use an existing saved raw SEC snapshot explicitly labelled with its retrieval limitations. Do not install FAskills or use paid data sources.

Read the printed output before writing the memo. The script uses USD, 10-K only, the latest five available annual fiscal ends, annual flow periods including retail calendars, preferred tags then fallbacks, and the latest filing for each period/tag. Missing facts stay `not found`; calculations or checks with missing inputs stay `not known`. Nonpositive equity makes ROE `not known`. Owner earnings here means operating cash flow less total capital spending, a classroom proxy, not a maintenance-capex estimate.

Write a short Buffett-inspired educational memo (not an authentic statement by Buffett). Choose **own the business**, **watch it**, or **pass** as a business-quality judgment. Discuss earning consistency, returns on equity, and cash generation from the printed checks. Distinguish evidence from judgment: moat durability, management integrity, maintenance capital spending, and competitive threats are not established by these facts. State `not known` where evidence is absent. No price, target, intrinsic value estimate, buy signal, invented moat score, or unsupported company narrative.

Use only numeric tokens actually present in the script's printed output, in their printed units and correct metric/year context. Do not calculate additional numbers in prose. Save `TICKER.memo.md` alongside `TICKER.printed.txt`, `TICKER.facts.json`, and `TICKER.raw.json`. Run `audit(memo, printed)` from the bundled script and correct every flagged occurrence before delivery. Also review context manually; token membership alone cannot establish factual correctness.

The three checks are computed by code: ROE at least fifteen percent in every year, owner earnings positive in every year, and owner earnings higher at the final fiscal end than the first. Missing any required input or fewer than five fiscal years yields `not known`.

Source inspiration: https://github.com/CinderZhang/FAskills/blob/main/financial-researcher/experts/warren_buffett.md . Only the business-quality ideas are adapted; numbers come solely from https://www.sec.gov/search-filings/edgar-application-programming-interfaces .
