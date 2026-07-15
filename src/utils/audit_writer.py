from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from snowflake.connector import SnowflakeConnection

from src.utils.logger import get_logger

logger = get_logger()

_AUDIT_TABLE = "SHIPPING_DB.METADATA.PIPELINE_AUDIT"


def log_pipeline_start(
    connection: SnowflakeConnection,
    run_id: str,
    pipeline_name: str,
    batch_file: str = "",
) -> None:

    _execute(
        connection,
        f"""
        INSERT INTO {_AUDIT_TABLE}
            (RUN_ID, PIPELINE_NAME, BATCH_FILE, STATUS, START_TIME)
        VALUES
            (%(run_id)s, %(pipeline_name)s, %(batch_file)s, 'RUNNING', %(start_time)s)
        """,
        {
            "run_id":        run_id,
            "pipeline_name": pipeline_name,
            "batch_file":    batch_file,
            "start_time":    _now(),
        },
    )

    logger.info("Audit | run started | run_id={}", run_id)


def log_pipeline_end(
    connection: SnowflakeConnection,
    run_id: str,
    start_time: datetime,
    status: str,
    error_message: str | None = None,
    bronze_rows: int = 0,
    silver_rows: int = 0,
    gold_rows:   int = 0,
) -> None:

    end_time = _now()
    duration = round((end_time - start_time).total_seconds(), 2)

    _execute(
        connection,
        f"""
        UPDATE {_AUDIT_TABLE}
        SET
            STATUS           = %(status)s,
            END_TIME         = %(end_time)s,
            DURATION_SECONDS = %(duration)s,
            ERROR_MESSAGE    = %(error_message)s,
            BRONZE_ROWS      = %(bronze_rows)s,
            SILVER_ROWS      = %(silver_rows)s,
            GOLD_ROWS        = %(gold_rows)s
        WHERE RUN_ID = %(run_id)s
        """,
        {
            "run_id":        run_id,
            "status":        status,
            "end_time":      end_time,
            "duration":      duration,
            "error_message": str(error_message)[:4000] if error_message else None,
            "bronze_rows":   bronze_rows,
            "silver_rows":   silver_rows,
            "gold_rows":     gold_rows,
        },
    )

    logger.info("Audit | run {} | {}s | run_id={}", status, duration, run_id)


def _now() -> datetime:
    return datetime.now(timezone.utc).replace(tzinfo=None)


def _execute(
    connection: SnowflakeConnection,
    sql: str,
    params: dict[str, Any],
) -> None:

    cursor = connection.cursor()

    try:
        cursor.execute(sql, params)
    except Exception:
        logger.exception("Audit write failed — pipeline continues.")
    finally:
        cursor.close()
