#!/usr/bin/env python3
"""Generate a synthetic vulnerability findings dataset.

Lets you exercise the ETL and dashboard without scanner access or risking
real data. Distributions are loosely realistic: mostly medium/low findings,
a long tail of aged criticals, ~70% remediation rate.
"""

from __future__ import annotations

import argparse
import csv
import random
from datetime import datetime, timedelta, timezone

SEVERITY_WEIGHTS = {"critical": 5, "high": 15, "medium": 45, "low": 35}
PLATFORMS = ["windows"] * 3 + ["linux"] * 1  # typical enterprise mix


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--assets", type=int, default=500)
    parser.add_argument("--days", type=int, default=90)
    parser.add_argument("--findings-per-asset", type=float, default=8.0)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--output", default="findings_raw.csv")
    args = parser.parse_args()

    rng = random.Random(args.seed)
    now = datetime.now(timezone.utc)
    severities = list(SEVERITY_WEIGHTS)
    weights = list(SEVERITY_WEIGHTS.values())

    rows = []
    for asset_num in range(args.assets):
        platform = rng.choice(PLATFORMS)
        asset_id = f"asset-{asset_num:05d}"
        n_findings = max(0, int(rng.gauss(args.findings_per_asset, 4)))
        for _ in range(n_findings):
            severity = rng.choices(severities, weights=weights)[0]
            age = int(rng.expovariate(1 / 25)) + 1  # most findings young, long tail
            first_found = now - timedelta(days=min(age, args.days))
            fixed = rng.random() < 0.70
            last_found = (
                first_found + timedelta(days=rng.randint(0, max(1, age - 1)))
                if fixed else now
            )
            rows.append({
                "asset_id": asset_id,
                "platform": platform,
                "owner_team": rng.choice(
                    ["server-ops", "desktop-eng", "db-admin", "network", "app-team-a"]
                ),
                "severity": severity,
                "first_found": first_found.date().isoformat(),
                "last_found": last_found.date().isoformat(),
                "state": "fixed" if fixed else "open",
            })

    with open(args.output, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)
    print(f"{len(rows)} findings across {args.assets} assets -> {args.output}")


if __name__ == "__main__":
    main()
