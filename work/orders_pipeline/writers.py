"""Writes clean orders to a CSV file and rejected orders to a log file."""

import csv

FIELD_NAMES = ("order_id", "product", "quantity", "unit_price")


def write_outputs(valid_rows, rejects, clean_path, rejects_path, header=FIELD_NAMES):
    """Write valid rows to a CSV (with a header) and reject messages to a log file."""
    with open(clean_path, "w", newline="") as clean_file, open(rejects_path, "w") as rejects_file:
        writer = csv.writer(clean_file)
        writer.writerow(header)
        writer.writerows(valid_rows)
        for reject in rejects:
            rejects_file.write(reject + "\n")


class CsvOrderWriter:
    def __init__(self, clean_path, rejects_path):
        self.clean_path = clean_path
        self.rejects_path = rejects_path

    def write(self, records, rejects):
        # turn OrderRecord objects back into rows, price with 2 decimals like the input
        rows = []
        for r in records:
            rows.append([r.order_id, r.product, r.quantity, f"{r.unit_price:.2f}"])
        write_outputs(rows, rejects, self.clean_path, self.rejects_path)