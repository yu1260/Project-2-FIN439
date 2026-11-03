from pathlib import Path
import sys
import json
import pandas as pd
import streamlit as st

BASE = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE / 'buffett-sec' / 'scripts'))
from sec_facts import fetch, render, audit

st.set_page_config(page_title='Buffett business notebook', layout='wide')
st.title('Buffett business notebook')
st.caption('Data from SEC EDGAR; built with AI help, a learning demonstration, not investment advice.')
ticker = st.text_input('Ticker', 'COST').strip().upper()
contact = st.text_input('SEC User-Agent: your name and email', placeholder='Your Name your@email.com')
reports = BASE / 'reports'
if st.button('Download SEC facts'):
    try:
        with st.spinner('Downloading from SEC EDGAR…'):
            raw, report = fetch(ticker, contact)
        reports.mkdir(exist_ok=True)
        # Validate the ticker before using it as a filename.
        import re
        if not re.fullmatch(r'[A-Z0-9.-]+', ticker):
            raise ValueError('Invalid ticker.')
        for suffix, content in [('raw.json', json.dumps(raw)), ('facts.json', json.dumps(report, indent=2)), ('printed.txt', render(report))]:
            (reports / f'{ticker}.{suffix}').write_text(content, encoding='utf-8')
        st.success('Downloaded. Use the skill to write a memo from these printed facts.')
    except Exception as exc:
        st.error(f'Download failed: {exc}. No values estimated.')

import re
if not re.fullmatch(r'[A-Z0-9.-]+', ticker):
    st.stop()
path = reports / f'{ticker}.facts.json'
if not path.exists():
    st.info('Enter your SEC contact and download facts to begin.')
    st.stop()
report = json.loads(path.read_text(encoding='utf-8'))
printed = render(report)
st.subheader(report['company'])
st.caption('Saved snapshot. Click Download SEC facts to refresh. ' + report['source'])
frame = pd.DataFrame([{k: v for k, v in row.items() if k != 'facts'} for row in report['rows']])
if not frame.empty:
    st.line_chart(frame.set_index('fiscal_year_end')[['owner_earnings', 'net_income']], y_label='USD')
    displayed = frame.astype(object)
    for column in displayed.columns:
        displayed[column] = displayed[column].where(frame[column].notna(), 'not known' if column == 'roe' else 'not found')
    st.dataframe(displayed, hide_index=True)
else:
    st.warning('No qualifying annual facts found.')
st.table(pd.DataFrame(report['checks'].items(), columns=['Check', 'Result']))
with st.expander('Printed evidence: tags, dates and derived formulas'):
    st.code(printed)
    st.json(report)
st.download_button('Download printed facts', printed, f'{ticker}.printed.txt')
memo_path = reports / f'{ticker}.memo.md'
memo = st.text_area('Memo — paste the skill’s memo here to audit edits', value=memo_path.read_text(encoding='utf-8') if memo_path.exists() else '', height=250)
if memo:
    st.markdown(memo)
    flags = audit(memo, printed)
    if flags:
        st.error('Unsupported numeric tokens found. Each occurrence is listed below.')
        st.dataframe(flags, hide_index=True)
    else:
        st.success('Every numeric token matches a printed token.')
    st.caption('The audit checks numeric tokens and percent units. It does not prove that a number belongs to the claimed metric/year, or validate written-out numbers or qualitative claims.')
    st.download_button('Download memo', memo, f'{ticker}.memo.md')
else:
    st.info('Memo not found. Ask Codex to use $buffett-sec on this ticker, using the saved printed facts. The app does not invent an AI memo.')
