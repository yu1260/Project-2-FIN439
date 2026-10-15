"""Check candidate portfolios against Meridian's machine-checkable rules."""

# Editable inputs
HOLDINGS = {
    "Cash": {"issuer": None, "redeem_days": 0, "reserve_eligible": True},
    "Treasury bills": {
        "issuer": "U.S. Treasury",
        "redeem_days": 1,
        "reserve_eligible": True,
    },
    "Treasury 10-year note": {
        "issuer": "U.S. Treasury",
        "redeem_days": 1,
        "reserve_eligible": True,
    },
    "Global equity index fund": {
        "issuer": "diversified fund",
        "redeem_days": 2,
        "reserve_eligible": False,
    },
    "Investment-grade bond fund": {
        "issuer": "diversified fund",
        "redeem_days": 3,
        "reserve_eligible": False,
    },
    "Private real estate fund": {
        "issuer": "diversified fund",
        "redeem_days": 90,
        "reserve_eligible": False,
    },
    "Acme Corp bonds": {
        "issuer": "Acme Corp",
        "redeem_days": 4,
        "reserve_eligible": False,
    },
    "Acme Corp stock": {
        "issuer": "Acme Corp",
        "redeem_days": 1,
        "reserve_eligible": False,
    },
}

CANDIDATES = {
    "A": {
        "Cash": 2,
        "Treasury bills": 2,
        "Treasury 10-year note": 10,
        "Global equity index fund": 60,
        "Investment-grade bond fund": 26,
        "Private real estate fund": 0,
        "Acme Corp bonds": 0,
        "Acme Corp stock": 0,
    },
    "B": {
        "Cash": 1,
        "Treasury bills": 0,
        "Treasury 10-year note": 0,
        "Global equity index fund": 55,
        "Investment-grade bond fund": 20,
        "Private real estate fund": 15,
        "Acme Corp bonds": 5,
        "Acme Corp stock": 4,
    },
    "C": {
        "Cash": 1,
        "Treasury bills": 1,
        "Treasury 10-year note": 0,
        "Global equity index fund": 70,
        "Investment-grade bond fund": 20,
        "Private real estate fund": 0,
        "Acme Corp bonds": 0,
        "Acme Corp stock": 8,
    },
    # D passes the coded rules but may not be suitable under S2's return objective.
    "D": {
        "Cash": 0,
        "Treasury bills": 92,
        "Treasury 10-year note": 0,
        "Global equity index fund": 0,
        "Investment-grade bond fund": 0,
        "Private real estate fund": 0,
        "Acme Corp bonds": 0,
        "Acme Corp stock": 8,
    },
}

RESERVE_SIZE_MILLIONS = 100
QUARTERLY_DISTRIBUTION_MILLIONS = 0.75
QUARTERS_TO_COVER = 4
LIQUIDITY_WINDOW_DAYS = 5
MINIMUM_LIQUID_SHARE_PERCENT = 90
ISSUER_LIMIT_PERCENT = 8
ISSUER_LIMIT_EXEMPTIONS = {None, "U.S. Treasury", "diversified fund"}


def status(condition):
    """Return the required label for a Boolean test."""
    return "pass" if condition else "FAIL"


def check_candidate(name, weights, reserve_minimum_percent):
    """Calculate and print every checkable rule for one candidate."""
    total_weight = sum(weights.values())
    lowest_weight = min(weights.values())
    reserve_weight = sum(
        weight
        for holding, weight in weights.items()
        if HOLDINGS[holding]["reserve_eligible"]
    )
    liquid_weight = sum(
        weight
        for holding, weight in weights.items()
        if HOLDINGS[holding]["redeem_days"] <= LIQUIDITY_WINDOW_DAYS
    )

    company_weights = {}
    for holding, weight in weights.items():
        issuer = HOLDINGS[holding]["issuer"]
        if issuer not in ISSUER_LIMIT_EXEMPTIONS:
            company_weights[issuer] = company_weights.get(issuer, 0) + weight
    largest_company_weight = max(company_weights.values(), default=0)

    checks = [
        ("Weights sum to 100", total_weight, total_weight == 100),
        ("Long-only (lowest weight)", lowest_weight, lowest_weight >= 0),
        (
            f"Reserve >= {reserve_minimum_percent:.1f}%",
            reserve_weight,
            reserve_weight >= reserve_minimum_percent,
        ),
        (
            f"Redeemable in {LIQUIDITY_WINDOW_DAYS} days >= "
            f"{MINIMUM_LIQUID_SHARE_PERCENT:.1f}%",
            liquid_weight,
            liquid_weight >= MINIMUM_LIQUID_SHARE_PERCENT,
        ),
        (
            f"Largest single company <= {ISSUER_LIMIT_PERCENT:.1f}%",
            largest_company_weight,
            largest_company_weight <= ISSUER_LIMIT_PERCENT,
        ),
    ]

    print(f"\nCandidate {name}")
    failures = 0
    for label, measured_value, passed in checks:
        print(f"{label}: {measured_value:.1f} {status(passed)}")
        failures += not passed
    print("Calendar-year loss: requires CIO clarification")
    if failures:
        print(f"Verdict: fails {failures} rule(s)")
    else:
        print("Verdict: passes every checkable rule")


def main():
    reserve_minimum_percent = (
        QUARTERS_TO_COVER
        * QUARTERLY_DISTRIBUTION_MILLIONS
        / RESERVE_SIZE_MILLIONS
        * 100
    )
    print(f"Reserve minimum: {reserve_minimum_percent:.1f}% of the portfolio")
    for name, weights in CANDIDATES.items():
        check_candidate(name, weights, reserve_minimum_percent)


if __name__ == "__main__":
    main()
