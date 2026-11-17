# Project 2 — Meridian portfolio app

The portfolio app was developed with Codex for implementation and verification. The analysis and decision are mine. Education, not investment advice.

## Run from this folder

```powershell
python -m pip install -r requirements.txt
python -m streamlit run portfolio_app.py
```

The app loads the checked-in prices.csv by default. Under **Current controls**, read the portfolio weights, estimated return, volatility, and reserve weight. The default checks are a 6% estimated return floor and a 10% reserve-eligible allocation floor. The weights shown satisfy both controls. If no mix meets both rules, the app displays a warning.

- [Visible output](lab-15-streamlit-portfolio-app.md#project-2-results)
- [Inputs and data source](project2-universe.md)
- [Baseline lab](lab-14-portfolio-baselines.md)
- [Point-in-time data card](asof_data_card.md)
- [Lab 20 cold-run record](docs/lab-20-checkout.md)
- [Lab 18 notes](lab-18-readme.md)
