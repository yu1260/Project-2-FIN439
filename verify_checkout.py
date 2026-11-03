"""Verify the supplied COST benchmark and the live-data JPM gap probe."""
import json
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).parent / 'buffett-sec' / 'scripts'))
from sec_facts import audit, render

base = Path(__file__).parent
p = base / 'reports'
cost = json.loads((p / 'COST.facts.json').read_text())
expected = [
    ('2022-08-28', 226954, 5844, 7392, 3891, 20642, 28.3, 3501),
    ('2023-09-03', 242290, 6292, 11068, 4323, 25058, 25.1, 6745),
    ('2024-09-01', 254453, 7367, 11339, 4710, 23622, 31.2, 6629),
    ('2025-08-31', 275235, 8099, 13335, 5498, 29164, 27.8, 7837),
    ('2026-08-30', 303154, 9226, 15817, 6435, 35803, 25.8, 9382),
]
keys = ['revenue', 'net_income', 'operating_cash_flow', 'capital_spending', 'equity']
actual = [(r['fiscal_year_end'], *(r[k] / 1000000 for k in keys), round(r['roe'], 1), r['owner_earnings'] / 1000000) for r in cost['rows']]
assert actual == expected, (actual, expected)
assert all(v == 'pass' for v in cost['checks'].values())
jpm = json.loads((p / 'JPM.facts.json').read_text())
assert len(jpm['rows']) == 5
assert all(r['capital_spending'] is None and r['owner_earnings'] is None for r in jpm['rows'])
assert all(v == 'not known' for k, v in jpm['checks'].items() if k.startswith('Owner earnings'))
for ticker, report in [('COST', cost), ('JPM', jpm)]:
    printed = render(report)
    (p / f'{ticker}.printed.txt').write_text(printed, encoding='utf-8')
    assert not audit((p / f'{ticker}.memo.md').read_text(encoding='utf-8'), printed)
assert any(f['number'] == '40.0%' for f in audit('ROE was 40.0%.', render(cost)))
print('All COST benchmark cells and checks match; JPM gaps and both memo audits pass; 40.0% is flagged.')

if '--app' in sys.argv:
    from streamlit.testing.v1 import AppTest
    app = AppTest.from_file(str(base / 'app.py'), default_timeout=30).run()
    assert not app.exception
    app.text_area[0].set_value(app.text_area[0].value + '\nROE was 40.0%.').run()
    assert not app.exception and app.error
    assert any('40.0%' in str(table.value) for table in app.dataframe)
    app.text_input[0].set_value('JPM').run()
    assert not app.exception
    assert 'cannot judge' in app.text_area[0].value
    print('Streamlit flagged 40.0% and displayed JPM memo successfully. Saved COST memo unchanged.')
