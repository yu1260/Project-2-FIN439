"""Run with: python -m streamlit run asof_app.py"""

from datetime import date
from io import StringIO
import re
from urllib.parse import urlencode
from urllib.request import urlopen

import pandas as pd
import streamlit as st


SERIES = {
    "BAA": "Moody's Baa corporate bond yield",
    "FEDFUNDS": "Federal funds rate",
    "DGS10": "10-year Treasury yield",
    "MORTGAGE30US": "30-year mortgage rate",
    "PAYEMS": "Payroll jobs (thousands, seasonally adjusted)",
}

DEFAULT_SERIES = ["BAA", "FEDFUNDS", "DGS10", "MORTGAGE30US"]


def style_page() -> None:
    st.html("""
    <style>
    :root { color-scheme: light; }
    .stApp { background: #faf9f6; color: #353530; }
    [data-testid="stHeader"] { background: rgba(250,249,246,.94); }
    [data-testid="stSidebar"] { background: #f0eee8; border-right: 1px solid #e5e2db; }
    [data-testid="stSidebar"] h2 { font-size: 1.15rem; }
    .stMainBlockContainer { max-width: 1120px; padding-top: 5rem; padding-bottom: 3rem; }
    h1, h2, h3 { color: #353530; letter-spacing: -.035em; }
    h1 { font-size: clamp(2rem, 4vw, 3.2rem) !important; font-weight: 600 !important; }
    h3 { font-size: 1.2rem !important; font-weight: 600 !important; }
    [data-testid="stCaptionContainer"] { color: #787870; }
    [data-testid="stCaptionContainer"] p { color: #787870 !important; }
    [data-testid="stVerticalBlockBorderWrapper"] > div,
    [data-testid="stLayoutWrapper"] [data-testid="stVerticalBlock"] > [data-testid="stVerticalBlockBorderWrapper"] {
      border-radius: 18px;
    }
    [data-testid="stVerticalBlockBorderWrapper"] { border-color: #e6e3dc !important; }
    [data-baseweb="tag"] { background: #e5e1f0 !important; color: #4e4568 !important; border-radius: 7px; }
    [data-baseweb="input"], [data-baseweb="select"] > div { border-radius: 10px !important; }
    .cat-brand { display: flex; align-items: center; gap: 9px; margin-bottom: 28px;
      color: #6e647d; font-size: 12px; font-weight: 650; letter-spacing: .16em; text-transform: uppercase; }
    .cat-intro { display: flex; align-items: center; justify-content: space-between; gap: 20px; }
    .cat-intro p { color: #858177; font-size: 12px; letter-spacing: .16em; text-transform: uppercase; margin: 0; }
    .cat-mark { width: 90px; height: 70px; flex-shrink: 0; position: relative; }
    .cat-face { position: absolute; top: 20px; left: 10px; width: 70px; height: 48px;
      border: 2px solid #7c718b; border-radius: 42% 42% 46% 46%; background: #e8e3f0; }
    .cat-ear { position: absolute; top: 10px; width: 24px; height: 30px; background: #e8e3f0;
      border: 2px solid #7c718b; border-radius: 3px; transform: rotate(-18deg); }
    .cat-ear.left { left: 11px; } .cat-ear.right { right: 11px; transform: rotate(18deg); }
    .cat-eye { position: absolute; top: 17px; width: 11px; height: 7px;
      border-bottom: 2px solid #7c718b; border-radius: 50%; }
    .cat-eye.left { left: 13px; } .cat-eye.right { right: 13px; }
    .cat-mouth { position: absolute; top: 24px; left: 27px; color: #7c718b; font-size: 15px; line-height: 1; }
    .cat-whiskers { position: absolute; top: 31px; left: -10px; width: 22px; border-top: 1px solid #7c718b; transform: rotate(8deg); }
    .cat-whiskers.right { left: auto; right: -10px; transform: rotate(-8deg); }
    .cat-whiskers::after { content: ''; position: absolute; top: 5px; width: 22px; border-top: 1px solid #7c718b; }
    .cat-strip { display: flex; flex-wrap: wrap; gap: 10px; margin: 14px 0 24px; }
    .cat-pill { padding: 7px 13px; border: 1px solid #e3e0d7; border-radius: 30px;
      font-size: 12px; color: #77766d; background: #f5f3ee; }
    .cat-footer { text-align: center; color: #979388; font-size: 12px; padding-top: 32px; }
    @media (prefers-reduced-motion: no-preference) {
      .cat-mark { animation: cat-arrive .6s ease-out; }
      @keyframes cat-arrive { from { opacity: 0; transform: translateY(5px); } to { opacity: 1; transform: translateY(0); } }
    }
    </style>
    <div class="cat-brand"><span aria-hidden="true">ฅ</span> little cat / economic observatory</div>
    <div class="cat-intro">
      <p>A quiet place to watch the numbers</p>
      <div class="cat-mark" role="img" aria-label="A little resting cat">
        <div class="cat-ear left"></div><div class="cat-ear right"></div>
        <div class="cat-face"><span class="cat-eye left"></span><span class="cat-eye right"></span>
          <span class="cat-mouth">ω</span><span class="cat-whiskers"></span><span class="cat-whiskers right"></span>
        </div>
      </div>
    </div>
    """)


def read_csv_url(url: str) -> pd.Series:
    """One HTTP request; accept FRED and vintage-suffixed ALFRED headers."""
    with urlopen(url, timeout=30) as response:
        frame = pd.read_csv(StringIO(response.read().decode("utf-8-sig")), na_values=["."])
    if frame.shape[1] != 2:
        raise ValueError("The server did not return a two-column series CSV.")
    dates = pd.to_datetime(frame.iloc[:, 0], errors="coerce")
    values = pd.to_numeric(frame.iloc[:, 1], errors="coerce")
    result = pd.Series(values.to_numpy(), index=dates, name="Value")
    result = result[result.index.notna()].dropna().sort_index()
    result = result[~result.index.duplicated(keep="last")]
    if result.empty:
        raise ValueError("No numeric observations were returned.")
    result.index.name = "Date measured"
    result.attrs["csv_column"] = str(frame.columns[1])
    return result


@st.cache_data(ttl=3600, show_spinner=False)
def download_today(series_id: str, downloaded_on: date) -> pd.Series:
    """The date in the cache key prevents reuse across calendar days."""
    return read_csv_url("https://fred.stlouisfed.org/graph/fredgraph.csv?" + urlencode({"id": series_id}))


@st.cache_data(ttl=3600, show_spinner=False)
def download_asof(series_id: str, vintage_date: date, downloaded_on: date) -> pd.Series:
    result = read_csv_url(
        "https://alfred.stlouisfed.org/graph/alfredgraph.csv?"
        + urlencode({"id": series_id, "vintage_date": vintage_date.isoformat()})
    )
    expected_column = f"{series_id}_{vintage_date:%Y%m%d}"
    if result.attrs.get("csv_column") != expected_column:
        raise ValueError("ALFRED did not return the requested vintage column; refusing to compare it as historical data.")
    return result


def summarize(series_id: str, current: pd.Series, vintage: pd.Series) -> dict:
    """Compare full histories; missing days are never counted as observations."""
    last_then = vintage.index[-1]
    common = current.index.intersection(vintage.index)
    return {
        "Series": f"https://fred.stlouisfed.org/series/{series_id}",
        "Last measured date known then": last_then.date().isoformat(),
        "Value known then": float(vintage.iloc[-1]),
        "Today's value for that same date": float(current.loc[last_then]) if last_then in current.index else None,
        "Last measured date today": current.index[-1].date().isoformat(),
        "Value today": float(current.iloc[-1]),
        "New observations since then": int((current.index > last_then).sum()),
        "Revised shared observations": int((current.loc[common] != vintage.loc[common]).sum()),
    }


def main() -> None:
    st.set_page_config(page_title="Little Cat · As known then", page_icon="🐈", layout="wide")
    today = date.today()
    style_page()
    st.title("Interest rates, as known then.")
    st.caption(
        f"Data from FRED and ALFRED, Federal Reserve Bank of St. Louis, downloaded today ({today.isoformat()}); "
        "built with AI help, a learning demonstration, not investment advice."
    )
    with st.sidebar:
        st.html('<div class="cat-brand"><span aria-hidden="true">/ᐠ｡ꞈ｡ᐟ\\</span> make yourself at home</div>')
        st.header("Your watchlist")
        st.caption("Pick a few series. Take a look back.")
        selected = st.multiselect(
            "Series", list(SERIES), default=DEFAULT_SERIES,
            format_func=lambda sid: f"{sid} — {SERIES[sid]}",
        )
        extra = st.text_input("Add any other FRED series ID", placeholder="For example, DGS2").strip().upper()
        st.divider()
        st.header("A moment in time")
        start = st.date_input("Start date", value=date(2020, 1, 1), min_value=date(1776, 1, 1), max_value=today)
        vintage_date = st.date_input("As known on", value=today, min_value=date(1776, 1, 1), max_value=today)
        st.caption("Charts show today's history. The table remembers what was available then.")
    if extra:
        if re.fullmatch(r"[A-Z0-9_]+", extra):
            selected = list(dict.fromkeys([*selected, extra]))
        else:
            st.error("Invalid series ID. Use letters, numbers, or underscores.")
    if not selected:
        st.info("Select a series or enter a FRED series ID.")
        return
    st.html(f'<div class="cat-strip"><span class="cat-pill">{len(selected)} series on watch</span>'
            f'<span class="cat-pill">Chart from {start:%d %b %Y}</span>'
            f'<span class="cat-pill">As known on {vintage_date:%d %b %Y}</span></div>')
    rows = []
    for sid in selected:
        with st.container(border=True):
            heading, latest = st.columns([3, 1])
            with heading:
                st.subheader(sid)
                if sid in SERIES:
                    st.caption(SERIES[sid])
            current = vintage = None
            try:
                with st.spinner(f"Downloading today's {sid} data…"):
                    current = download_today(sid, today)
                units = "Thousands of jobs" if sid == "PAYEMS" else "Percent" if sid in DEFAULT_SERIES else "Value (series units)"
                with latest:
                    value = f"{current.iloc[-1]:,.0f}" if sid == "PAYEMS" else f"{current.iloc[-1]:,.2f}" + ("%" if units == "Percent" else "")
                    st.metric("Latest today", value)
                    st.caption(f"Measured {current.index[-1]:%d %b %Y}")
                visible = current.loc[current.index >= pd.Timestamp(start)]
                if visible.empty:
                    st.info("No observations on or after the start date.")
                else:
                    st.line_chart(visible, y_label=units, color="#9583b0", height=240)
            except Exception as exc:
                st.error(f"{sid}: could not load today's data. Check the ID or try again. {exc}")
            try:
                with st.spinner(f"Downloading {sid} as known on {vintage_date}…"):
                    vintage = download_asof(sid, vintage_date, today)
                st.caption(f"As known on {vintage_date:%d %b %Y} · last measured date {vintage.index[-1]:%d %b %Y}")
            except Exception as exc:
                st.error(f"{sid}: could not load data as known on {vintage_date}. {exc}")
        if current is not None and vintage is not None:
            rows.append(summarize(sid, current, vintage))
        else:
            rows.append({"Series": f"https://fred.stlouisfed.org/series/{sid}"})
    st.subheader("Then and today")
    st.caption("The two latest values can refer to different measurement dates; a difference between them is not necessarily a revision.")
    st.caption("Counts compare full histories, independent of the chart start date. Only numeric observations count; revisions compare dates present in both downloads. Unavailable data appears blank.")
    st.dataframe(
        pd.DataFrame(rows), hide_index=True, width="stretch",
        column_config={"Series": st.column_config.LinkColumn("Series", display_text=r"https://fred\.stlouisfed\.org/series/(.*)")},
    )
    st.html('<div class="cat-footer">/ᐠ – ˕ –マ &nbsp; A little perspective, one observation at a time.</div>')


if __name__ == "__main__":
    main()
