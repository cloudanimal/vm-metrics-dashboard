# Vulnerability Management Metrics Dashboard

ETL pipeline + Power BI starter kit for vulnerability management KPIs. Turns raw scanner exports into the metrics that actually run a VM program:

- **Vulnerabilities per node** — the single best headline metric for program health
- **SLA compliance by severity** — % remediated within policy windows
- **Remediation velocity** — findings closed per week, trending
- **Aging backlog** — where the old findings live (and which teams own them)
- **Coverage** — % of assets with a recent authenticated scan (the metric everyone forgets)

## Why these metrics

Counting "total vulnerabilities" rewards nobody and panics everybody — it grows with asset count and scanner signature updates. Normalizing per node, tracking SLA aging, and watching velocity tells you whether the *program* is improving, independent of environment growth. I've written more on this in my series on [KPIs/KRIs for vulnerability management](https://www.linkedin.com/in/josephwcook/).

## Contents

| File | Purpose |
|---|---|
| `etl/generate_sample_data.py` | Synthetic findings dataset so you can try the pipeline without scanner access |
| `etl/transform.py` | Cleans/derives the metric columns from raw findings (any scanner's CSV export) |
| `dashboard/measures.md` | DAX measures for every KPI, ready to paste into Power BI |
| `dashboard/layout.md` | Recommended report pages and visuals |

## Quick start

```bash
pip install -r requirements.txt

# Generate 90 days of synthetic findings for 500 assets
python etl/generate_sample_data.py --assets 500 --days 90 --output findings_raw.csv

# Transform into the dashboard-ready fact table
python etl/transform.py --input findings_raw.csv --output findings_fact.csv
```

Then load `findings_fact.csv` into Power BI and paste in the measures from `dashboard/measures.md`.

## Adapting to your scanner

`transform.py` expects these columns (rename mappings at the top of the file):
`asset_id, severity, first_found, last_found, state`. Tenable, Qualys, and Rapid7 exports all map cleanly.

## License

MIT
