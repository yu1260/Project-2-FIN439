# Project 2 universe and mandate

## Working mandate

Find the long-only, fully invested portfolio with the lowest estimated volatility that has an estimated annual return of at least **6.0%** and at least **10.0%** in the reserve-eligible sleeve. These numeric assumptions are editable in the app because no separate Project 2 mandate file with a return objective was available.

## Funds

| Ticker | Fund | Role |
|---|---|---|
| SGOV | iShares 0-3 Month Treasury Bond ETF | Cash and reserve; Treasury bills stand in for cash. |
| GOVT | iShares U.S. Treasury Bond ETF | Government bonds across Treasury maturities. |
| IGIB | iShares 5-10 Year Investment Grade Corporate Bond ETF | Investment-grade fixed income. |
| VT | Vanguard Total World Stock ETF | Broad global equity. |

SGOV is reserve-eligible. Money market funds are excluded because their nearly constant $1 price does not provide a useful total-return price history.

## Price sources

`prices.csv` contains 60 completed months of adjusted-close prices, with the oldest month first. The current partial month is excluded. Adjusted close incorporates distributions and splits.

| Ticker | Source | Download date |
|---|---|---|
| SGOV | [Yahoo Finance Historical Data](https://finance.yahoo.com/quote/SGOV/history/) | 2026-10-22 |
| GOVT | [Yahoo Finance Historical Data](https://finance.yahoo.com/quote/GOVT/history/) | 2026-10-22 |
| IGIB | [Yahoo Finance Historical Data](https://finance.yahoo.com/quote/IGIB/history/) | 2026-10-22 |
| VT | [Yahoo Finance Historical Data](https://finance.yahoo.com/quote/VT/history/) | 2026-10-22 |

The return displayed by the app is an annualized arithmetic average estimated from five years of monthly historical adjusted-close returns. It is history, not a forecast or recommendation.


## App results

The Project 2 app uses the mandate without relaxing it: an estimated return objective of **6.0%**, a minimum reserve-eligible allocation of **10.0%**, and **SGOV** as the reserve-eligible fund. Portfolio weights are searched in five-percentage-point steps.

| Price window | SGOV | GOVT | IGIB | VT | Estimated return | Estimated volatility | Reserve eligible |
|---|---:|---:|---:|---:|---:|---:|---:|
| All available monthly returns | 65.0% | 0.0% | 0.0% | 35.0% | 6.32% | 5.31% | 65.0% |
| Last 36 monthly returns | 90.0% | 0.0% | 0.0% | 10.0% | 6.02% | 1.21% | 90.0% |

Both historical windows produce a feasible mix. The largest allocation change is **SGOV: 25.0 percentage points**. This sensitivity reinforces that historical estimates are not forecasts.
