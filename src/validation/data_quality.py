from __future__ import annotations

from typing import Any

import pandas as pd

from src.config.constants import DATE_COLUMNS
from src.utils.logger import (
    get_logger,
    get_quality_logger,
)

logger = get_logger()
quality_logger = get_quality_logger()


def check_data_quality(df: pd.DataFrame) -> dict[str, Any]:
    logger.info("Starting data quality checks.")

    report = {
        "total_rows": len(df),
        "duplicate_rows": df.duplicated().sum(),
        "missing_values": df.isna().sum().to_dict(),
        "missing_percentage": (df.isna().mean() * 100).round(2).to_dict(),
        "invalid_dates": {
            column: (
                pd.to_datetime(df[column], errors="coerce").isna().sum()
                - df[column].isna().sum()
            )
            for column in DATE_COLUMNS
        },
    }

    log_quality_report(report)

    logger.info("Data quality checks completed.")

    return report


def log_quality_report(report: dict[str, Any]) -> None:
    quality_logger.info("========== DATA QUALITY REPORT ==========")
    quality_logger.info("Total Rows: {}", report["total_rows"])
    quality_logger.info("Duplicate Rows: {}", report["duplicate_rows"])

    for title in ("missing_values", "missing_percentage", "invalid_dates"):
        quality_logger.info("")
        quality_logger.info(title.replace("_", " ").title())

        for key, value in report[title].items():
            suffix = " %" if title == "missing_percentage" else ""
            quality_logger.info("{}: {}{}", key, value, suffix)
