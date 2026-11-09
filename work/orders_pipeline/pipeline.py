"""Connects a reader and a writer: loads orders, splits valid from rejected, and writes both."""

from orders_pipeline.models import OrderRecord
from orders_pipeline.validators import validate_record

def load_orders(reader):
    """Read with any reader and return (records, rejects)."""
    records = []
    rejects = []
    for line_number, fields in reader.read():
        reason = validate_record(fields)
        if reason:
            rejects.append(f"line {line_number}: {reason}")
        else:
            records.append(OrderRecord(*fields))
    return records, rejects


class OrderPipeline:
    def __init__(self, reader, writer):
        self.reader = reader
        self.writer = writer

    def run(self):
        records, rejects = load_orders(self.reader)
        self.writer.write(records, rejects)
        return len(records), len(rejects)