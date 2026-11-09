"""Reads orders from a text or CSV file and returns them as (line_number, fields) pairs"""

import csv


def read_lines(input_path):
    """Return (line_number, line) pairs for every non-blank line in the file."""
    lines = []
    with open(input_path) as infile:
        for line_number, line in enumerate(infile, start=1):
            # skip blank lines
            if line.strip():
                lines.append((line_number, line))
    return lines


def parse_record(line):
    """Split a raw line on '|' and strip spaces from each field."""
    return [field.strip() for field in line.split("|")]


class OrderReader:
    def __init__(self, path):
        self.path = path

    def read(self):
        raise NotImplementedError("subclasses must implement read()")


class TextOrderReader(OrderReader):
    # reads pipe-separated orders, like orders_raw.txt
    def read(self):
        rows = []
        for line_number, line in read_lines(self.path):
            rows.append((line_number, parse_record(line)))
        return rows


class CsvOrderReader(OrderReader):
    # reads orders from a CSV with a header row, like orders.csv
    def __init__(self, path, delimiter=","):
        super().__init__(path)
        self.delimiter = delimiter

    def read(self):
        rows = []
        with open(self.path, newline="") as f:
            reader = csv.reader(f, delimiter=self.delimiter)
            # skip the header, so data starts at line 2
            next(reader)
            for line_number, row in enumerate(reader, start=2):
                fields = [field.strip() for field in row]
                rows.append((line_number, fields))
        return rows