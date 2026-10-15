# Meridian Foundation Reserve: Mandate Classification

| Statement | Classification | One-line reason |
|---|---|---|
| **S1.** Horizon seven years; annual rebalancing. | Hard constraint | It fixes the planning period and limits the portfolio process to one scheduled rebalance each year. |
| **S2.** Objective: CPI + 4% a year, net of costs, over rolling five-year periods. | Objective | It states the reserve's desired real, net performance and the period over which success is measured. |
| **S3.** Pays out $0.75 million every quarter; twelve months of payouts held in cash or daily-liquid government securities. | Hard constraint | It requires at least $3.0 million to remain in the specified liquid assets to fund four quarterly payouts. |
| **S4.** Benchmark: 60% global equities, 40% U.S. investment-grade bonds. | Hard constraint | It mandates the reference portfolio used to evaluate performance, although it does not require the actual portfolio to hold those weights. |
| **S5.** Long-only: no borrowing, short sales or derivatives. | Hard constraint | It explicitly prohibits leverage, negative positions, and derivative holdings. |
| **S6.** No single issuer above 8%. | Hard constraint | It imposes a measurable maximum concentration after all holdings from the same issuer are aggregated. |
| **S7.** Annual turnover at most 25% without committee approval. | Hard constraint | Turnover may not exceed 25% unless a documented committee exception exists. |
| **S8.** At least 90% redeemable within five business days. | Hard constraint | It sets a measurable minimum for portfolio liquidity. |
| **S9.** “The reserve cannot have a calendar-year loss greater than 10%.” No measure, no breach rule. | Unverifiable promise | The 10% ceiling cannot be tested or enforced until “loss,” its measurement method, and the response to a breach are defined. |
| **S10.** No sector, ESG, tax or home-bias preference; nobody has said what the pilot should optimize. | Missing | The stated preferences are neutral, but the optimization objective needed to rank permitted portfolios has not been supplied. |

## Investment policy statement

An investment policy statement (IPS) is the written rulebook connecting a client's purpose to portfolio decisions. It works by stating objectives—the outcomes sought—and constraints—the boundaries a portfolio must obey—so that proposed portfolios can be evaluated consistently before optimization begins.

In this case, S2 is the return objective. S1 and S3–S8 constrain the time horizon, rebalancing, cash reserve, benchmark, permitted instruments, concentration, turnover, and liquidity. S9 sounds like a constraint but is not testable until the CIO defines the loss measure and breach response. S10 records neutral preferences but, crucially, exposes the missing optimization objective.

## Attack portfolio D

Candidate D holds 92% Treasury bills and 8% Acme Corp stock. It passes every rule checked by `mandate.py`, but the CIO could reasonably reject it because its Treasury-heavy design may not achieve the CPI + 4% return objective in S2.

The objection holds: passing constraints establishes permissibility, not expected suitability. S2 decides the objection because the portfolio still must be designed to pursue the stated real-return objective.

### Sceptical colleague check

Playing the colleague's role, I would challenge candidate D under S2: although its 92% Treasury-bill weight satisfies the coded limits, the proposal gives no evidence that it can earn CPI + 4% net over rolling five-year periods. That is a suitability objection rather than another coded failure, so D should remain a passing attack portfolio in the checker.

## Checker evidence

The baseline run matched the supplied known answers: A passed every checkable rule, B failed three rules, C failed one rule, and D passed every checkable rule. For the required probe, I temporarily changed A's cash weight from 2% to -2% and its global equity fund weight from 60% to 64%; A kept a 100.0% total, reported a -2.0% lowest weight and failed long-only, retained a 10.0% reserve that passed, and failed no other rule. I then restored A's original weights and reran the checker successfully.

## One question for the CIO

**Question:** What should the pilot optimize among portfolios that meet the hard constraints?

If the CIO answers “minimize the probability of falling short of CPI + 4% net over rolling five-year periods,” I would replace the Treasury-heavy candidate D with a diversified allocation selected for that shortfall objective while retaining every hard constraint.

## Reflection

1. A portfolio can pass every checkable rule and still be wrong because the checker tests minimum boundaries, not whether the portfolio is likely to achieve the client's objective; candidate D demonstrates that difference.
2. S4 was the type I was least sure of because the benchmark is mandatory for evaluation but is not a required 60/40 portfolio allocation; I classified it as a hard constraint on measurement.
