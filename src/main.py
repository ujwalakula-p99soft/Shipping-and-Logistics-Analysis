from __future__ import annotations

import argparse
import sys
from pathlib import Path

from src.config.settings import settings
from src.pipeline.run_pipeline import run_pipeline
from src.utils.logger import configure_logger, get_logger

logger = get_logger()


def _resolve_batch(batch_arg: str | None) -> Path:
    raw_dir = settings.RAW_DATA_DIR

    if batch_arg:
        batch = Path(batch_arg)
        if not batch.is_absolute():
            batch = settings.PROJECT_ROOT / batch
        if not batch.exists():
            raise FileNotFoundError(f"Batch file not found: {batch}")
        return batch

    all_batches = sorted(raw_dir.glob("batch_*.csv"))
    if not all_batches:
        raise FileNotFoundError("No batch files found in data/raw/. Run scripts/split_dataset.py first.")

    state_file = raw_dir / ".processed_batches"
    processed  = set(state_file.read_text().splitlines()) if state_file.exists() else set()

    for batch in all_batches:
        if batch.name not in processed:
            return batch

    logger.info("All batches have already been processed.")
    sys.exit(0)


def _mark_processed(batch: Path) -> None:
    state_file = settings.RAW_DATA_DIR / ".processed_batches"
    with state_file.open("a") as f:
        f.write(batch.name + "\n")


def main():
    configure_logger()

    parser = argparse.ArgumentParser(description="Shipping Logistics Pipeline")
    parser.add_argument("--batch", help="Path to batch CSV file", default=None)
    args = parser.parse_args()

    batch = _resolve_batch(args.batch)
    logger.info("Processing {}", batch.name)

    run_pipeline(batch)
    _mark_processed(batch)

    logger.info("{} processed successfully.", batch.name)


if __name__ == "__main__":
    main()
