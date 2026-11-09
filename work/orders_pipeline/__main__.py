"""Entry point -> runs the pipeline on orders_raw.txt when called with python -m orders_pipeline"""

import sys
from pathlib import Path

from orders_pipeline.readers import TextOrderReader
from orders_pipeline.writers import CsvOrderWriter
from orders_pipeline.pipeline import OrderPipeline


def main(data_dir):
    reader = TextOrderReader(data_dir / "orders_raw.txt")
    writer = CsvOrderWriter(data_dir / "clean_orders_terminal.csv", data_dir / "rejects_terminal.log")
    valid, rejected = OrderPipeline(reader, writer).run()
    print(f"Valid: {valid}, Rejected: {rejected}")


if __name__ == "__main__":
    data_dir = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("/workspace/data/module1")
    main(data_dir)