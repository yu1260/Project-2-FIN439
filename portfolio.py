"""Meridian portfolio risk engine. Standard library only."""
import math

SLEEVES = {
    "Treasury bills": {"return": .035, "volatility": .005},
    "10-year Treasury note": {"return": .043, "volatility": .070},
    "Investment-grade bond fund": {"return": .050, "volatility": .060},
    "Global equity index fund": {"return": .080, "volatility": .160},
}
CORRELATIONS = {
    "Treasury bills": {
        "Treasury bills": 1.00, "10-year Treasury note": .10,
        "Investment-grade bond fund": .05, "Global equity index fund": .00,
    },
    "10-year Treasury note": {
        "Treasury bills": .10, "10-year Treasury note": 1.00,
        "Investment-grade bond fund": .80, "Global equity index fund": -.10,
    },
    "Investment-grade bond fund": {
        "Treasury bills": .05, "10-year Treasury note": .80,
        "Investment-grade bond fund": 1.00, "Global equity index fund": .25,
    },
    "Global equity index fund": {
        "Treasury bills": .00, "10-year Treasury note": -.10,
        "Investment-grade bond fund": .25, "Global equity index fund": 1.00,
    },
}
OBJECTIVE_RETURN = .065
RESERVE_ELIGIBLE = {"Treasury bills", "10-year Treasury note"}


def validate_correlations(sleeves, correlations):
    """Refuse values outside [-1, 1] and a table that is not symmetric."""
    names = set(sleeves)
    if set(correlations) != names:
        raise ValueError("Correlation rows must match the sleeve names.")
    for left in sleeves:
        if set(correlations[left]) != names:
            raise ValueError(f"Correlation row {left!r} must contain every sleeve.")
        for right in sleeves:
            value = correlations[left][right]
            if not -1 <= value <= 1:
                raise ValueError(
                    f"Correlation {left} / {right} must be between -1 and 1; got {value}."
                )
            if left == right and not math.isclose(value, 1.0):
                raise ValueError(f"Diagonal correlation {left} / {right} must be 1.")
            reverse = correlations[right][left]
            if not math.isclose(value, reverse, abs_tol=1e-12):
                raise ValueError(
                    f"Correlation table is not symmetric: {left} / {right} is "
                    f"{value}, but {right} / {left} is {reverse}."
                )


def build_covariance(sleeves, correlations):
    """Covariance = correlation x left volatility x right volatility."""
    validate_correlations(sleeves, correlations)
    return {
        left: {
            right: correlations[left][right]
            * sleeves[left]["volatility"]
            * sleeves[right]["volatility"]
            for right in sleeves
        }
        for left in sleeves
    }


def benchmark(sleeves):
    weights = {name: 0.0 for name in sleeves}
    weights["Investment-grade bond fund"] = .40
    weights["Global equity index fund"] = .60
    return weights


def equal_weight(sleeves):
    return {name: 1 / len(sleeves) for name in sleeves}


def inverse_volatility(sleeves):
    raw = {name: 1 / data["volatility"] for name, data in sleeves.items()}
    total = sum(raw.values())
    return {name: value / total for name, value in raw.items()}


def check_weights(weights, sleeves):
    if set(weights) != set(sleeves):
        raise ValueError("Weights must match the sleeve names.")
    if any(value < 0 for value in weights.values()):
        raise ValueError("Weights cannot be negative.")
    if not math.isclose(sum(weights.values()), 1.0, abs_tol=1e-12):
        raise ValueError("Weights must sum to 100%.")


def expected_return(weights, sleeves):
    check_weights(weights, sleeves)
    return sum(weights[name] * sleeves[name]["return"] for name in sleeves)


def portfolio_volatility(weights, covariance):
    """Square root of w'Cov w, including every correlation cross term."""
    variance = sum(
        weights[left] * weights[right] * covariance[left][right]
        for left in weights
        for right in weights
    )
    if variance < -1e-12:
        raise ValueError("Inputs imply a negative variance.")
    return math.sqrt(max(variance, 0.0))


def reserve_weight(weights):
    return sum(weights[name] for name in RESERVE_ELIGIBLE)


def calculate(weights, sleeves, covariance, objective):
    portfolio_return = expected_return(weights, sleeves)
    return {
        "weights": weights,
        "return": portfolio_return,
        "volatility": portfolio_volatility(weights, covariance),
        "reserve": reserve_weight(weights),
        "meets_objective": portfolio_return >= objective,
    }


def print_portfolio(name, result):
    print(name)
    for sleeve, weight in result["weights"].items():
        print(f"  {sleeve}: {weight:.1%}")
    print(f"  Expected return: {result['return']:.2%}")
    print(f"  Volatility: {result['volatility']:.2%}")
    print(f"  Reserve-eligible weight: {result['reserve']:.1%}")
    answer = "YES" if result["meets_objective"] else "NO"
    print(f"  Meets {OBJECTIVE_RETURN:.1%} objective: {answer}\n")


def main():
    covariance = build_covariance(SLEEVES, CORRELATIONS)
    portfolios = {
        "Benchmark": benchmark(SLEEVES),
        "Equal weight": equal_weight(SLEEVES),
        "Inverse volatility": inverse_volatility(SLEEVES),
    }
    for name, weights in portfolios.items():
        print_portfolio(
            name, calculate(weights, SLEEVES, covariance, OBJECTIVE_RETURN)
        )


if __name__ == "__main__":
    try:
        main()
    except ValueError as error:
        raise SystemExit(f"Input error: {error}") from error


# Reusable Lab 15 additions.
def search_lowest_risk(
    sleeves, correlations, objective, reserve_eligible, minimum_reserve, step=0.05
):
    """Find the lowest-volatility feasible long-only portfolio on a weight grid."""
    if not 0 <= minimum_reserve <= 1:
        raise ValueError("Minimum reserve must be between 0 and 100%.")
    units = round(1 / step)
    if step <= 0 or not math.isclose(units * step, 1.0, abs_tol=1e-12):
        raise ValueError("Step must divide 100% exactly.")
    if not set(reserve_eligible) <= set(sleeves):
        raise ValueError("Reserve-eligible assets must be in the sleeve table.")

    covariance = build_covariance(sleeves, correlations)
    names = list(sleeves)
    best = None

    def mixes(remaining, places, prefix=()):
        if places == 1:
            yield prefix + (remaining,)
        else:
            for value in range(remaining + 1):
                yield from mixes(remaining - value, places - 1, prefix + (value,))

    for allocation in mixes(units, len(names)):
        weights = {name: allocation[i] / units for i, name in enumerate(names)}
        portfolio_return = expected_return(weights, sleeves)
        reserve = sum(weights[name] for name in reserve_eligible)
        if portfolio_return + 1e-12 < objective or reserve + 1e-12 < minimum_reserve:
            continue
        volatility = portfolio_volatility(weights, covariance)
        result = {
            "weights": weights,
            "return": portfolio_return,
            "volatility": volatility,
            "reserve": reserve,
            "meets_objective": True,
        }
        if best is None or volatility < best["volatility"] - 1e-15:
            best = result
    return best


def estimate_from_csv(source, last_36=False):
    """Estimate annual statistics from oldest-first monthly adjusted prices."""
    import csv
    import io
    import statistics
    from datetime import date
    from pathlib import Path

    if hasattr(source, "getvalue"):
        raw = source.getvalue()
        text = raw.decode("utf-8-sig") if isinstance(raw, bytes) else raw
    elif hasattr(source, "read"):
        raw = source.read()
        text = raw.decode("utf-8-sig") if isinstance(raw, bytes) else raw
    else:
        text = Path(source).read_text(encoding="utf-8-sig")

    rows = list(csv.reader(io.StringIO(text)))
    if len(rows) < 3 or len(rows[0]) < 2:
        raise ValueError("CSV needs a date column, asset columns, and two prices.")
    tickers = [heading.strip() for heading in rows[0][1:]]
    if not all(tickers) or len(set(tickers)) != len(tickers):
        raise ValueError("Each asset column needs a unique ticker.")

    dated_prices = []
    for row_number, row in enumerate(rows[1:], start=2):
        if not row or all(not cell.strip() for cell in row):
            continue
        if len(row) != len(tickers) + 1:
            raise ValueError(f"CSV row {row_number} has the wrong number of columns.")
        try:
            row_date = date.fromisoformat(row[0].strip())
            prices = [float(value) for value in row[1:]]
        except ValueError as error:
            raise ValueError(f"CSV row {row_number} has an invalid date or price.") from error
        if any(price <= 0 for price in prices):
            raise ValueError(f"CSV row {row_number} contains a nonpositive price.")
        dated_prices.append((row_date, prices))

    if any(a[0] >= b[0] for a, b in zip(dated_prices, dated_prices[1:])):
        raise ValueError("CSV dates must be unique and oldest first.")
    if last_36:
        dated_prices = dated_prices[-37:]
    if len(dated_prices) < 3:
        raise ValueError("At least three monthly prices are required.")

    monthly_returns = {ticker: [] for ticker in tickers}
    for (_, previous), (_, current) in zip(dated_prices, dated_prices[1:]):
        for i, ticker in enumerate(tickers):
            monthly_returns[ticker].append(current[i] / previous[i] - 1)

    sleeves = {
        ticker: {
            "return": statistics.mean(values) * 12,
            "volatility": statistics.stdev(values) * math.sqrt(12),
        }
        for ticker, values in monthly_returns.items()
    }
    correlations = {ticker: {} for ticker in tickers}
    means = {ticker: statistics.mean(values) for ticker, values in monthly_returns.items()}
    standard_deviations = {
        ticker: statistics.stdev(values) for ticker, values in monthly_returns.items()
    }
    for left in tickers:
        for right in tickers:
            if left == right:
                correlations[left][right] = 1.0
                continue
            if math.isclose(standard_deviations[left], 0.0) or math.isclose(
                standard_deviations[right], 0.0
            ):
                raise ValueError("Correlation is undefined for a zero-volatility asset.")
            covariance = sum(
                (a - means[left]) * (b - means[right])
                for a, b in zip(monthly_returns[left], monthly_returns[right])
            ) / (len(monthly_returns[left]) - 1)
            correlations[left][right] = covariance / (
                standard_deviations[left] * standard_deviations[right]
            )
    return sleeves, correlations
