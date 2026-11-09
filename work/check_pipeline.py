"""Checks the terminal run's output files: counts add up, no negative totals, rejects have reasons."""

import csv
import sys
from pathlib import Path

from orders_pipeline.readers import read_lines

data_dir = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("/workspace/data/module1")

non_blank = read_lines(data_dir / "orders_raw.txt")
with open(data_dir / "clean_orders_terminal.csv", newline="") as f:
    clean_rows = list(csv.DictReader(f))
rejects = (data_dir / "rejects_terminal.log").read_text().splitlines()

# 1. valid + rejected = all non-blank input lines
assert len(clean_rows) + len(rejects) == len(non_blank), "counts don't add up"

# 2. no negative totals in the clean file
for row in clean_rows:
    assert int(row["quantity"]) * float(row["unit_price"]) >= 0, f"negative total: {row}"

# 3. every reject has a reason after "line N:"
for reject in rejects:
    assert reject.split(":", 1)[1].strip() != "", f"reject has no reason: {reject}"

print(f"All 3 checks passed: {len(clean_rows)} valid + {len(rejects)} rejected = {len(non_blank)} lines")