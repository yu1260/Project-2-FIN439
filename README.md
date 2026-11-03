# Lab 18: Buffett business notebook

Completed COST and JPM snapshots and memos are in `reports/`. See `reports/checkout.md` for the benchmark, probes, fresh-chat comparison and trust decision. The project skill is also installed in `.agents/skills/buffett-sec/` within this folder.

From this folder in PowerShell:

```powershell
python -m pip install -r requirements.txt
python buffett-sec/scripts/sec_facts.py COST --user-agent "Your Name your-real-email@example.org" --out reports
python -m streamlit run app.py
```

Replace the example contact with your real name and email. No API key is needed.
The script saves the raw SEC response, computed JSON and the exact printed evidence.
Ask Codex to use `$buffett-sec` on COST and save its memo in `reports/COST.memo.md`.
The app reads that memo and audits numeric tokens whenever you edit it.

Install the `buffett-sec` folder in your Codex skills directory, or in the project's `.agents/skills/` directory for project discovery. Restart the Codex session if it does not yet see the new skill.

The fiscal end dates come from available annual observations, never a fabricated FY2026. The flow filter accepts annual durations of 330–380 days; short transition periods are excluded. The script uses annual USD facts and does not estimate absent/custom-tag facts. ROE uses year-end equity, not average equity. Repeated periods use the latest filing within the preferred tag. Provenance includes tag, period, filing date and accession in JSON.

The classroom owner-earnings formula subtracts all reported capital spending; maintenance spending is not known. Checks summarize historical observations and cannot prove a moat, management quality or future returns. The numeric audit is conservative about unprinted values but only verifies token membership, not correct association or prose written with number words.

No live model or paid services run in the app. Codex writes the memo from the saved evidence. A three-investor panel requires selecting the additional investor perspectives; the assignment's detailed build specifies Buffett only.
