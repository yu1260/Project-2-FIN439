"""Mandate checks, comparable portfolios and one-at-a-time stresses."""
from dataclasses import asdict, dataclass, replace
import csv
from pathlib import Path
import json

from portfolio import (
    build_covariance, equal_weight, estimate_from_csv, expected_return,
    inverse_volatility, portfolio_volatility, search_lowest_risk,
)

ROOT = Path(__file__).resolve().parent
AS_OF = "2026-10-22"
TICKERS = ("SGOV", "GOVT", "IGIB", "VT")
BENCHMARK = dict(zip(TICKERS, (0, 0, .4, .6)))
MAX_DRIFT = .15
GRID = .05


def signal_rows():
    with (ROOT / "data" / "dgs10-vintages.csv").open(newline="", encoding="utf-8") as source:
        return list(csv.DictReader(source))


@dataclass(frozen=True)
class Inputs:
    last_36: bool = False
    equity_shift: float = 0
    cost_bps: int = 10
    reserve: float = .10
    net_floor: float = .06


def evaluate(weights, sleeves, covariance, inputs):
    gross = expected_return(weights, sleeves)
    net = gross - inputs.cost_bps / 10_000
    failures = []
    if abs(sum(weights.values()) - 1) > 1e-10:
        failures.append("Fully invested")
    if min(weights.values()) < 0:
        failures.append("Long-only")
    if weights["SGOV"] + 1e-12 < inputs.reserve:
        failures.append("SGOV reserve minimum")
    if net + 1e-12 < inputs.net_floor:
        failures.append("Estimated net return floor")
    return {
        "weights": weights, "gross": gross, "net": net,
        "volatility": portfolio_volatility(weights, covariance),
        "reserve": weights["SGOV"], "failures": failures,
    }


def run(inputs):
    sleeves, correlations = estimate_from_csv(
        ROOT / "data" / "prices.csv", last_36=inputs.last_36
    )
    if tuple(sleeves) != TICKERS:
        raise ValueError("Expected the four mandate tickers in order.")
    sleeves["VT"]["return"] += inputs.equity_shift
    covariance = build_covariance(sleeves, correlations)
    candidate = search_lowest_risk(
        sleeves, correlations, inputs.net_floor + inputs.cost_bps / 10_000,
        {"SGOV"}, inputs.reserve, step=GRID,
    )
    portfolios = {
        "Equal weight": equal_weight(sleeves),
        "Inverse volatility": inverse_volatility(sleeves),
        "Policy benchmark": BENCHMARK,
        "Constrained": candidate["weights"] if candidate else None,
    }
    return {
        name: evaluate(weights, sleeves, covariance, inputs) if weights else None
        for name, weights in portfolios.items()
    }


def assess(inputs):
    portfolios = run(inputs)
    base = portfolios["Constrained"]
    stresses = []
    for label, changed in (
        ("VT return estimate −1 pp", replace(inputs, equity_shift=inputs.equity_shift - .01)),
        ("Alternate return window", replace(inputs, last_36=not inputs.last_36)),
        ("Annual cost +25 bp", replace(inputs, cost_bps=inputs.cost_bps + 25)),
        ("SGOV minimum +10 pp", replace(inputs, reserve=inputs.reserve + .10)),
    ):
        candidate = run(changed)["Constrained"] if changed.reserve <= 1 else None
        drift = (
            max(abs(base["weights"][ticker] - candidate["weights"][ticker]) for ticker in TICKERS)
            if base and candidate else None
        )
        stresses.append({
            "scenario": label, "inputs": asdict(changed), "candidate": candidate,
            "max_weight_change": drift,
            "stop": drift is None or drift + 1e-12 >= MAX_DRIFT,
        })
    return {
        "as_of": AS_OF, "inputs": asdict(inputs), "portfolios": portfolios,
        "stresses": stresses, "deployment": "STOP" if any(row["stop"] for row in stresses) else "REVIEW",
        "recommendation": "Pilot with no capital", "allocation_range_pct": [0, 0],
        "signal": next(row for row in reversed(signal_rows()) if row["vintage"] <= AS_OF),
    }


if __name__ == "__main__":
    print(json.dumps(assess(Inputs()), indent=2))
