import copy
from pathlib import Path
import sys
import unittest
sys.path.insert(0, str(Path(__file__).parent / 'buffett-sec' / 'scripts'))
from sec_facts import TAGS, extract, render, audit

def fixture():
    facts = {}
    for metric, tags in TAGS.items():
        entries = []
        for year in range(2021, 2026):
            f = dict(end=f'{year}-08-31', filed=f'{year}-10-01', form='10-K', val=100,
                     accn=str(year), start=f'{year-1}-09-01')
            if metric == 'equity':
                f.pop('start')
                f['val'] = 500
            if metric == 'capital_spending':
                f['val'] = 30
            entries.append(f)
        facts[tags[0]] = {'units': {'USD': entries}}
    return {'entityName': 'Fixture only', 'facts': {'us-gaap': facts}}

class FactsTests(unittest.TestCase):
    def test_latest_filing_and_quarter_exclusion(self):
        raw = fixture()
        entries = raw['facts']['us-gaap']['NetIncomeLoss']['units']['USD']
        revised = dict(entries[-1], filed='2026-10-01', val=110)
        entries += [revised, dict(revised, start='2025-06-01', filed='2026-11-01', val=999)]
        report = extract(raw)
        self.assertEqual(report['rows'][-1]['net_income'], 110)
        self.assertEqual(report['rows'][-1]['roe'], 22)
        self.assertEqual(report['rows'][-1]['owner_earnings'], 70)
        self.assertEqual(list(report['checks'].values()), ['pass', 'pass', 'fail'])

    def test_missing_and_nonpositive_equity(self):
        raw = fixture()
        gaap = raw['facts']['us-gaap']
        gaap['StockholdersEquity']['units']['USD'][-1]['val'] = 0
        del gaap['PaymentsToAcquirePropertyPlantAndEquipment']
        report = extract(raw)
        self.assertIsNone(report['rows'][-1]['roe'])
        self.assertIsNone(report['rows'][-1]['owner_earnings'])
        self.assertTrue(all(v == 'not known' for v in report['checks'].values()))
        self.assertIn('not found', render(report))

    def test_tag_fallback_and_incomplete_window(self):
        raw = fixture()
        gaap = raw['facts']['us-gaap']
        gaap['Revenues'] = gaap.pop('RevenueFromContractWithCustomerExcludingAssessedTax')
        for item in gaap.values():
            item['units']['USD'] = item['units']['USD'][-4:]
        report = extract(raw)
        self.assertEqual(report['rows'][-1]['facts']['revenue']['tag'], 'us-gaap:Revenues')
        self.assertTrue(all(v == 'not known' for v in report['checks'].values()))

    def test_numeric_probe(self):
        self.assertEqual(audit('Cash 1,000; ROE 20.00%.', 'Cash 1000 ROE 20.00%'), [])
        flags = audit('Cash 999999; return 1000%; cash 999999.', 'Cash 1000 ROE 20.00%')
        self.assertEqual([f['number'] for f in flags], ['999999', '1000%', '999999'])

if __name__ == '__main__':
    unittest.main()
