# Lab 20 — Project 2 Readiness

## Cold run

Codex cold-run reviewer, starting from commit b6fc5ff0d17508d6239d60a388658603d62036be.

- Command attempted from a fresh clone: python -m pip install -r requirements.txt
- First failure: [Errno 2] No such file or directory: 'requirements.txt'.
- Elapsed time: 9.35 seconds for the attempted setup command.
- Result: app launch was blocked. The README described the Lab 18 notebook. Project 2 historical results were visible in the [Lab 15 write-up](../lab-15-streamlit-portfolio-app.md#project-2-results).

## Fix

Restored the existing portfolio app, its engine, and dependency list. Updated the README to launch the portfolio app with the bundled prices and the 6% return and 10% reserve floors documented in Lab 15. A Streamlit app test using the existing project environment loaded the default case and reproduced 6.32% estimated return, 5.31% volatility, and 65.00% reserve weight.

## Locked Changed-Input Record

Pending student prediction written with AI closed and committed and pushed before the changed run.

## Committee decision

Pending student decision and reversal trigger.
