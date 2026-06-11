#!/usr/bin/env python3
"""Transform raw scanner findings into a dashboard-ready fact table.

Adds the derived columns the Power BI measures expect: age, SLA window,
SLA status, and aging bucket. Rename COLUMN_MAP entries to fit your
scanner's export format.
"""

from __future__ import annotations

import argparse

import pandas as pd

# Map your scanner's column names to the canonical ones (left = canonical)
COLUMN_MAP = {
    "asset_id": "asset_id",
    "severity": "severity",
    "first_found": "first_found",
    "last_found": "last_found",
    "state": "state",
}

SLA_DAYS = {"critical": 15, "high": 30, "medium": 60, "low": 90}
AGING_BUCKET_EDGES = [0, 15, 30, 60, 90, float("inf")]
AGING_BUCKET_LABELS = ["0-15d", "16-30d", "31-60d", "61-90d", "90d+"]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True)
    parser.add_argument("--output", default="findings_fact.csv")
    args = parser.parse_args()

    df = pd.read_csv(args.input).rename(
        columns={v: k for k, v in COLUMN_MAP.items()}
    )
    df["first_found"] = pd.to_datetime(df["first_found"])
    df["last_found"] = pd.to_datetime(df["last_found"])
    df["severity"] = df["severity"].str.lower()
    df["state"] = df["state"].str.lower()

    today = pd.Timestamp.today().normalize()
    is_open = df["state"] != "fixed"
    # Age: open findings age against today; fixed findings against close date
    df["age_days"] = (
        (df["last_found"].where(~is_open, today) - df["first_found"]).dt.days
    )
    df["sla_days"] = df["severity"].map(SLA_DAYS).fillna(90).astype(int)
    df["within_sla"] = df["age_days"] <= df["sla_days"]
    df["aging_bucket"] = pd.cut(
        df["age_days"], bins=AGING_BUCKET_EDGES,
        labels=AGING_BUCKET_LABELS, include_lowest=True,
    )
    # ISO week of remediation, for velocity trending
    df["fixed_week"] = (
        df["last_found"].dt.strftime("%G-W%V").where(df["state"] == "fixed")
    )

    df.to_csv(args.output, index=False)
    open_count = int(is_open.sum())
    nodes = df["asset_id"].nunique()
    print(f"{len(df)} findings -> {args.output}")
    print(f"Open: {open_count}  |  Assets: {nodes}  |  "
          f"Open vulns/node: {open_count / nodes:.2f}")
    print(f"SLA compliance (open): "
          f"{df.loc[is_open, 'within_sla'].mean() * 100:.1f}%")


if __name__ == "__main__":
    main()
