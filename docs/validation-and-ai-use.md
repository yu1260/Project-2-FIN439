# Validation and AI use

## What was evaluated

The student confirmed the Lab 15 working rules as the final Project 2 mandate. The review applies the return floor after modeled incremental cost and separately tests a proposed 15 pp deployment stop.

Frozen Lab 15 Yahoo Finance adjusted closes for SGOV, GOVT, IGIB and VT, downloaded October 22, 2026. The CSV contains 60 completed price months, October 2021 through September 2026, which yield 59 adjacent-month returns. Monthly labels use the first day of the month. The adjusted-close snapshot may embody later adjustments relative to earlier months, so the model uses this panel only as an October 22 estimation exercise. [Price provenance and working mandate](https://github.com/yu1260/Project-2-FIN439/blob/e1c3ed89daf6c7a5e051b1bf942f9e2f88ddbf95/project2-universe.md)

The code multiplies the monthly arithmetic mean by 12. Annualized risk equals the square root of 12 times the weighted monthly covariance. The inverse-volatility baseline normalizes each asset's reciprocal standalone volatility. The 5 pp search exhausts 1,771 fully invested long-only mixes. It filters on reserve and net return, then keeps the lowest-volatility feasible mix. Subtracting the same 10 bp from every portfolio models incremental cost. Fund-level expenses are reflected in price performance. There is no turnover model or live liquidity verification.

## Results and checks

The default constrained mix is 65% SGOV and 35% VT, with 6.22% estimated net return and 5.31% annualized volatility. The complete baselines and stress outputs are in [frozen output](visible-output.json). The estimate, cost and reserve scenarios stay under the 15 pp threshold. The 36-month scenario moves VT by 25 pp, stopping deployment. Default DGS10 is 5.26% as known September 30. The later October 29 row is excluded from the October 22 frozen output. [Signal data card](signal-data-card.md)

Run `python -m unittest -v test_engine` to check the four default verdicts, weighted cross terms against the Lab 14 known answer, stress behavior, the infeasibility path, and the vintage boundary. The Lab 20 cold run found that `requirements.txt` was missing from the earlier checkout. That was fixed before the historical rerun. The [Lab 20 checkout](https://github.com/yu1260/Project-2-FIN439/blob/e1c3ed89daf6c7a5e051b1bf942f9e2f88ddbf95/docs/lab-20-checkout.md) has the timing and fix. On November 23, the five model tests passed. Streamlit AppTest verified the default verdicts, a 50% net floor with no feasible mix, and the October 29 vintage switch to 5.05%. The local server health endpoint returned OK. An independent cold run on this review branch remains pending.

## Locked Changed-Input Record

The Lab 20 record predates this review-branch cost and deployment overlay. It uses the same universe, price panel, 5 pp grid and 6% return and 10% reserve floors under the original no-incremental-cost configuration. The original prediction is preserved verbatim in the immutable pre-run commit. [Prediction commit](https://github.com/yu1260/Project-2-FIN439/commit/462071965b76c9dc972c75ed9792be8564a15ad0) · [Result commit](https://github.com/yu1260/Project-2-FIN439/commit/e1c3ed89daf6c7a5e051b1bf942f9e2f88ddbf95)

| Field | Historical evidence |
|---|---|
| Only changed input | VT annual return estimate decreased from 11.0502% to 8.0000%, down 3.0502 pp |
| Expected direction | VT weight and volatility rise, SGOV weight and reserve fall, estimated return remains near the 6% floor |
| Observed direction | VT 35% → 55%, SGOV 65% → 45%, volatility 5.31% → 8.26%, return 6.32% → 6.10% |
| Decision effect then | Both portfolios passed the two floors, so the recorded allocation recommendation persisted |
| Explanation | Less estimated return per unit of VT required 20 pp more VT on the discrete grid |
| Decision effect now | The proposed review policy considers weight stability as well. A 20 pp drift would breach its 15 pp stop threshold |

[Before output](https://github.com/yu1260/Project-2-FIN439/blob/462071965b76c9dc972c75ed9792be8564a15ad0/docs/changed-input-before.txt) · [After output](https://github.com/yu1260/Project-2-FIN439/blob/e1c3ed89daf6c7a5e051b1bf942f9e2f88ddbf95/docs/changed-input-after.txt)

## Material AI uses

| Interaction | Exposed tool / model | Use and disposition |
|---|---|---|
| November 23, 2026 | OpenAI Codex, GPT-6 family, application exposes no exact revision | Reused the lab engine and drafted comparison, stress, signal and disclosure materials. Kept the prior locked record and validated the new default with model and interface checks. |
| Earlier labs | AI use disclosed in the existing lab material | This draft preserves the earlier source and results. Student to supply tool names, versions when exposed, dates and accepted or rejected material suggestions from those interactions. |

Student to confirm the AI-off provenance of the original prediction and record one personally checked AI output before submitting.
