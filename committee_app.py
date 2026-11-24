"""Committee interface for the Reserve Portfolio Review."""
import json

import streamlit as st

from engine import AS_OF, MAX_DRIFT, ROOT, TICKERS, Inputs, assess, signal_rows

def render_portfolio():
    st.title("Reserve Portfolio Review")
    st.caption(f"Committee decision support · Frozen price snapshot {AS_OF} · Educational use")

    with st.sidebar:
        st.header("Scenario inputs")
        st.caption("Defaults use the confirmed Lab 15 mandate with a modeled cost. Edits are scenarios.")
        last_36 = st.radio("Return window", ["59 months", "36 months"]) == "36 months"
        shift = st.number_input("VT annual return adjustment (pp)", -20.0, 20.0, 0.0, .25)
        cost = st.number_input("Annual incremental cost (bp)", 0, 500, 10, 5)
        reserve = st.number_input("SGOV reserve minimum (%)", 0.0, 100.0, 10.0, 5.0)
        floor = st.number_input("Annual net return floor (%)", -20.0, 50.0, 6.0, .25)

    try:
        report = assess(Inputs(last_36, shift / 100, cost, reserve / 100, floor / 100))
    except (OSError, ValueError) as error:
        st.error(f"Model stopped. {error}")
        st.stop()

    st.subheader("Paper pilot · 0% capital")
    if report["deployment"] == "STOP":
        st.warning("Stop live allocation. At least one scenario is infeasible or moves a sleeve by 15 pp or more.")
    else:
        st.info("Scenario gate cleared. Committee review is required before any live allocation.")

    review, stress, signal = st.tabs(["Portfolio review", "Stress tests", "Signal"])
    with review:
        st.markdown(
            f"Minimize annualized volatility on a 5 pp grid. Long-only, fully invested, "
            f"with at least **{reserve:g}% SGOV** and **{floor:g}% estimated annual net return**. "
            "Policy comparator: 60% VT / 40% IGIB."
        )
        st.caption("SGOV · T-bills | GOVT · Treasuries | IGIB · Investment-grade corporates | VT · Global equities")
        rows = []
        for name, portfolio in report["portfolios"].items():
            row = {"Portfolio": name}
            if portfolio is None:
                row.update({"Verdict": "FAIL · No feasible grid mix"})
            else:
                failures = portfolio["failures"]
                row["Verdict"] = "FAIL · " + ", ".join(failures) if failures else "PASS · All coded rules"
                row.update({ticker: f"{portfolio['weights'][ticker]:.0%}" if name != "Inverse volatility"
                            else f"{portfolio['weights'][ticker]:.1%}" for ticker in TICKERS})
                row.update({"Gross return": f"{portfolio['gross']:.2%}",
                            "Net return": f"{portfolio['net']:.2%}", "Volatility": f"{portfolio['volatility']:.2%}"})
            rows.append(row)
        st.dataframe(rows, hide_index=True, width="stretch")
        st.caption("Estimated net returns are annualized sample means less the incremental cost assumption. "
                   "Volatility annualizes monthly sample covariance. Consult the memo for deployment gates.")

    with stress:
        st.write(f"Live allocation stops if any case is infeasible or a sleeve moves by at least {MAX_DRIFT:.0%} of portfolio weight.")
        rows = []
        for case in report["stresses"]:
            mix = case["candidate"]
            change = case["max_weight_change"]
            rows.append({
                "Scenario": case["scenario"],
                "Net return": f"{mix['net']:.2%}" if mix else "Infeasible",
                "Volatility": f"{mix['volatility']:.2%}" if mix else "—",
                "Weights (SGOV / GOVT / IGIB / VT)": " / ".join(f"{mix['weights'][t]:.0%}" for t in TICKERS) if mix else "—",
                "Largest move": f"{change * 100:.0f} pp" if change is not None else "—",
                "Gate": "STOP" if case["stop"] else "Clear",
            })
        st.dataframe(rows, hide_index=True, width="stretch")
        st.download_button("Download scenario evidence", json.dumps(report, indent=2),
                           "scenario-output.json", "application/json")

    with signal:
        st.subheader("10-year Treasury yield at each archived decision date")
        readings = signal_rows()
        selected = st.selectbox("ALFRED vintage", [row["vintage"] for row in readings])
        reading = next(row for row in readings if row["vintage"] == selected)
        st.metric("Latest yield in selected vintage", f"{float(reading['yield_pct']):.2f}%")
        st.caption(f"Observation date {reading['observed']} · Available by {selected}")
        st.markdown((ROOT / "docs" / "signal-data-card.md").read_text(encoding="utf-8"))


if __name__ == "__main__":
    st.set_page_config(page_title="Reserve Portfolio Review", layout="wide")
    render_portfolio()
