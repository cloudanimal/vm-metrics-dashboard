# Recommended Report Layout

## Page 1 — Executive Summary
- **Cards (top row):** Vulns Per Node, SLA Compliance %, Critical Open, Total Assets
- **Line chart:** Open Findings over time (snapshot table or incremental refresh)
- **Bar chart:** Open Findings by severity
- One page, no scrolling. This is the page leadership sees.

## Page 2 — Remediation Operations
- **Line chart:** Fixed This Week by fixed_week (velocity trend)
- **Stacked bar:** Aging buckets by owner_team
- **Matrix:** SLA Compliance % by owner_team x severity
- This is the page that drives the weekly cross-functional meeting.

## Page 3 — Asset Drill-down
- **Table:** asset_id, platform, open findings, oldest finding age, owner_team
- Drill-through from any visual on pages 1-2.

## Refresh strategy
- Daily scheduled refresh from the ETL output is enough for program metrics.
- Don't chase real-time: VM metrics move on a weekly cadence, and intraday
  refreshes just create noise and dashboard-watching.
