# As-of app: data card and checks

Downloaded and checked on **29 October 2026**. Built with AI help, a learning demonstration, not investment advice.

## Data card — DGS10

| Field | Details |
|---|---|
| Series | **DGS10**, 10-year Treasury constant maturity market yield |
| Source and link | Board of Governors of the Federal Reserve System, H.15 Selected Interest Rates, distributed by [FRED](https://fred.stlouisfed.org/series/DGS10); historical vintages from [ALFRED](https://alfred.stlouisfed.org/series?seid=DGS10) |
| What it measures | The market yield on U.S. Treasury securities at a constant 10-year maturity, quoted on an investment basis. It is a yield, not a bond price or investment return. |
| Units | Percent per annum; daily; not seasonally adjusted |
| Publication lag | About one business day in the checked vintages. On 30 September 2026 the newest observation was 29 September; on 29 October it was 28 October. Holidays and weekends do not supply observations. |
| Revisions | None observed on shared dates between the 30 September vintage and today's download: **0**. Daily market rates generally have little publication lag and few revisions; corrections remain possible. |
| Download date | **2026-10-29** |

The [H.15 publication description](https://www.federalreserve.gov/releases/h15/about.htm) says the release is published every business day except holidays. The lag above is measured from the downloaded vintages, rather than a guarantee about future releases.

### Three values read against the FRED page

I read these observations in the [DGS10 FRED page](https://fred.stlouisfed.org/series/DGS10) and compared them with the public CSV download. All three match.

| Date measured | FRED page | CSV | Match |
|---|---:|---:|---|
| 2026-10-26 | 5.00% | 5.00% | Yes |
| 2026-10-27 | 4.99% | 4.99% | Yes |
| 2026-10-28 | 5.05% | 5.05% | Yes |

### Last month-end versus today

Last day of last month: **30 September 2026**. Today: **29 October 2026**.

| As known on | Last measured date available | Value known then | New observations in today's data | Revised shared observations |
|---|---|---:|---:|---:|
| 2026-09-30 | 2026-09-29 | 5.26% | 20 | 0 |
| 2026-10-29 | 2026-10-28 | 5.05% | 0 | 0 |

The 20 newer observations disappear from the historical vintage because they had not yet been published by 30 September. For example, the 26–28 October observations above are absent then. A difference between the two latest values, 5.26% and 5.05%, reflects different measurement dates here, not a revision.

The app's line charts always show today's data, as requested. Changing the “As known on” date changes the historical caption and comparison table, not those charts.

## PAYEMS vintage probe

[PAYEMS](https://fred.stlouisfed.org/series/PAYEMS) measures total nonfarm payroll employment, in thousands, seasonally adjusted; the originating source is the U.S. Bureau of Labor Statistics.

Selected **15 January 2025** as the vintage and compared full histories:

| Check | Observed result |
|---|---:|
| Last measured month known then | December 2024 |
| December 2024 as known then | **159,536** |
| December 2024 in today's download | **158,316** |
| Downward revision for that same month | **1,220 thousand jobs** |
| Revised observations on shared dates | **381** |
| New observations after December 2024 | **21** |

**PASS.** The historical download differs from today's download. Monthly observation `2024-12-01` represents December 2024, not a daily employment reading. Today's latest month is September 2026 at 159,044; that is a different comparison from today's December 2024 value.

The app now includes a “Today's value for that same date” column so the December comparison is visible alongside the two latest observations. PAYEMS is available in the multiselect; the original four interest-rate series remain selected by default. ALFRED's returned column must identify the requested vintage, or the app reports an error rather than using it as historical data.

### Public downloads used

- [PAYEMS today](https://fred.stlouisfed.org/graph/fredgraph.csv?id=PAYEMS)
- [PAYEMS as known on 2025-01-15](https://alfred.stlouisfed.org/graph/alfredgraph.csv?id=PAYEMS&vintage_date=2025-01-15)
- [DGS10 today](https://fred.stlouisfed.org/graph/fredgraph.csv?id=DGS10)
- [DGS10 as known on 2026-09-30](https://alfred.stlouisfed.org/graph/alfredgraph.csv?id=DGS10&vintage_date=2026-09-30)
- [DGS10 as known on 2026-10-29](https://alfred.stlouisfed.org/graph/alfredgraph.csv?id=DGS10&vintage_date=2026-10-29)

Counts exclude missing observations (`.`) and compare full histories, independent of the chart start date. A revision is a changed numeric value on a measurement date present in both downloads.

## Run

```powershell
cd 'C:\Users\15453\Documents\Codex\2026-10-29\1-build-asof-app-py-a\outputs'
& 'C:\Users\15453\myproject\.venv\Scripts\python.exe' -m streamlit run 'C:\Users\15453\Documents\Codex\2026-10-29\1-build-asof-app-py-a\outputs\asof_app.py'
```

The `.streamlit/config.toml` file alongside the app supplies the cream and lavender light theme. Run from this folder to load that theme.
