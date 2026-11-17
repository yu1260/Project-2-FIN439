"""Streamlit interface for the reusable Meridian risk engine."""
from pathlib import Path

import streamlit as st

from portfolio import (
    estimate_from_csv,
    search_lowest_risk,
)


st.set_page_config(page_title="Lowest-risk mandate mix", page_icon="chart", layout="wide")
st.title("Lowest-risk mandate mix")
st.write("Built with AI help, a learning demonstration, not investment advice.")

objective = st.sidebar.number_input(
    "Objective return (%)",
    min_value=-20.0,
    max_value=50.0,
    value=6.0,
    step=0.5,
) / 100
minimum_reserve = st.sidebar.number_input(
    "Minimum reserve-eligible weight (%)",
    min_value=0.0,
    max_value=100.0,
    value=10.0,
    step=1.0,
) / 100
uploaded = st.sidebar.file_uploader("Upload prices.csv", type="csv")
last_36 = st.sidebar.checkbox("Use only the last 36 monthly returns", value=False)

try:
    prices = uploaded if uploaded is not None else Path(__file__).with_name("prices.csv")
    universe_name = prices.name
    loaded_sleeves, loaded_correlations = estimate_from_csv(prices, last_36=False)
    current_sleeves, current_correlations = estimate_from_csv(prices, last_36=last_36)
    loaded_reserve = {
        ticker for ticker in loaded_sleeves
        if ticker.upper() in {"SGOV", "BIL", "SHV", "TBIL"}
    }
    estimate_label = (
        "Historical estimate from the last 36 monthly returns"
        if last_36
        else "Historical estimate from all available monthly returns"
    )

    st.subheader(universe_name)
    st.caption(f"{estimate_label}; history, not a forecast.")
    st.markdown("#### Inputs")
    edited_reserve = set()
    input_columns = st.columns(2)
    for index, (asset, values) in enumerate(current_sleeves.items()):
        with input_columns[index % 2]:
            edited_return = st.number_input(
                f"{asset} expected return (%)",
                value=float(values["return"] * 100),
                step=0.25,
                key=f"return-{universe_name}-{last_36}-{asset}",
            )
            current_sleeves[asset]["return"] = edited_return / 100
            if st.checkbox(
                f"{asset} is reserve-eligible",
                value=asset in loaded_reserve,
                key=f"reserve-{universe_name}-{asset}",
            ):
                edited_reserve.add(asset)

    loaded_answer = search_lowest_risk(
        loaded_sleeves,
        loaded_correlations,
        objective,
        loaded_reserve,
        minimum_reserve,
    )
    current_answer = search_lowest_risk(
        current_sleeves,
        current_correlations,
        objective,
        edited_reserve,
        minimum_reserve,
    )

    def show_answer(title, answer):
        st.markdown(f"#### {title}")
        if answer is None:
            st.warning("No mix meets the objective")
            return
        for asset, weight in answer["weights"].items():
            st.write(f"{asset}: **{weight:.1%}**")
        st.metric("Expected return", f"{answer['return']:.2%}")
        st.metric("Volatility", f"{answer['volatility']:.2%}")
        st.metric("Reserve-eligible weight", f"{answer['reserve']:.2%}")

    left, right = st.columns(2)
    with left:
        show_answer("Current controls", current_answer)
    with right:
        show_answer("Inputs as loaded", loaded_answer)

    if current_answer is not None and loaded_answer is not None:
        changes = {
            asset: abs(
                current_answer["weights"][asset] - loaded_answer["weights"][asset]
            ) * 100
            for asset in current_answer["weights"]
        }
        changed_asset = max(changes, key=changes.get)
        st.info(
            f"Largest weight change: {changed_asset}, "
            f"{changes[changed_asset]:.1f} percentage points."
        )
    else:
        st.info("Largest weight change is unavailable because one answer is infeasible.")
except (ValueError, KeyError) as error:
    st.error(str(error))
