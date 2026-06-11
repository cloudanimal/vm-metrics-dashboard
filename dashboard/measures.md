# DAX Measures

Paste these into Power BI after loading `findings_fact.csv` as table `Findings`.

## Core KPIs

```dax
Open Findings = CALCULATE(COUNTROWS(Findings), Findings[state] <> "fixed")

Total Assets = DISTINCTCOUNT(Findings[asset_id])

Vulns Per Node = DIVIDE([Open Findings], [Total Assets], 0)

SLA Compliance % =
DIVIDE(
    CALCULATE(COUNTROWS(Findings),
        Findings[state] <> "fixed", Findings[within_sla] = TRUE()),
    [Open Findings], 0
)

Critical Open = CALCULATE([Open Findings], Findings[severity] = "critical")
```

## Velocity

```dax
Fixed This Week =
CALCULATE(COUNTROWS(Findings),
    Findings[state] = "fixed",
    Findings[fixed_week] = FORMAT(TODAY(), "YYYY-\WWW"))

Remediation Rate % =
DIVIDE(
    CALCULATE(COUNTROWS(Findings), Findings[state] = "fixed"),
    COUNTROWS(Findings), 0)
```

## Aging

```dax
Backlog 90d+ =
CALCULATE([Open Findings], Findings[aging_bucket] = "90d+")

Avg Age (Open) =
CALCULATE(AVERAGE(Findings[age_days]), Findings[state] <> "fixed")
```

## Tips

- Put `Vulns Per Node` and `SLA Compliance %` as cards at top-left — those are the two numbers leadership reads.
- Slice everything by `owner_team`: SLA compliance per team turns an abstract metric into accountability.
- Trend `Fixed This Week` as a line over `fixed_week` to show velocity — a flat line with a growing backlog is your early warning.
