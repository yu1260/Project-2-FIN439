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

### Prediction — written before the changed run

- Load-bearing input: VT annual expected-return estimate.
- Old value: 11.0502% per year. New value: 8.0000% per year, a decrease of 3.0502 percentage points.
- Expected movement: the optimizer will increase VT's portfolio weight and decrease SGOV's weight because each percentage point allocated to VT now contributes less expected return. The portfolio's volatility should increase and its reserve-eligible weight should decrease. The reported portfolio return should remain at or just above the 6.00% annual floor because the optimizer searches only feasible mixes on a 5-percentage-point weight grid.
- Expected decision effect: no change. I expect a feasible mix to continue meeting both the 6.00% annual return floor and the 10.00% reserve-eligible weight floor, so the recommendation remains to allocate to the lowest-volatility feasible mix.

Baseline output is preserved in [changed-input-before.txt](changed-input-before.txt). The changed case has not been run yet.

### Observed result

Pending the changed run after this prediction is committed and pushed.

## Committee decision

Pending student decision and reversal trigger.
