from __future__ import annotations

import uuid
from datetime import datetime, timezone
from pathlib import Path

from src.config.constants import PIPELINE_NAME, STATUS_FAILED, STATUS_SUCCESS
from src.config.sql_scripts import BOOTSTRAP_SCRIPTS, SQL_SCRIPTS
from src.database.execute_sql import execute_sql_file
from src.database.initialize_session import initialize_session
from src.database.snowflake_connection import get_connection
from src.ingestion.csv_reader import read_csv
from src.ingestion.upload_stage import upload_to_stage
from src.utils.audit_writer import log_pipeline_end, log_pipeline_start
from src.utils.logger import get_logger
from src.validation.data_quality import check_data_quality
from src.validation.schema_validation import validate_schema

logger = get_logger()


def _row_count(connection, full_table: str) -> int:
    cursor = connection.cursor()
    try:
        cursor.execute(f"SELECT COUNT(*) FROM {full_table}")
        row   = cursor.fetchone()
        count = int(row[0]) if row else 0
        logger.info("Row count | {} = {}", full_table, count)
        return count
    except Exception as exc:
        logger.warning("Row count failed for {}: {}", full_table, str(exc))
        return 0
    finally:
        cursor.close()


def _now() -> datetime:
    return datetime.now(timezone.utc).replace(tzinfo=None)


def run_pipeline(batch_file: Path) -> None:
    run_id     = str(uuid.uuid4())
    start_time = _now()

    logger.info("=" * 60)
    logger.info("Pipeline   : {}", PIPELINE_NAME)
    logger.info("Run ID     : {}", run_id)
    logger.info("Batch file : {}", batch_file.name)
    logger.info("=" * 60)

    dataframe      = read_csv(batch_file)
    validate_schema(dataframe)
    quality_report = check_data_quality(dataframe)

    logger.info(
        "Profiling done | rows={} | duplicates={}",
        quality_report["total_rows"],
        quality_report["duplicate_rows"],
    )

    with get_connection() as connection:

        initialize_session(connection)

        for sql_file in BOOTSTRAP_SCRIPTS:
            execute_sql_file(connection=connection, sql_file=sql_file)

        log_pipeline_start(
            connection    = connection,
            run_id        = run_id,
            pipeline_name = PIPELINE_NAME,
            batch_file    = batch_file.name,
        )

        try:
            upload_to_stage(connection, batch_file)

            for sql_file in SQL_SCRIPTS:
                logger.info("Executing : {}", sql_file.name)
                execute_sql_file(connection=connection, sql_file=sql_file)

            bronze_rows = _row_count(connection, "SHIPPING_DB.BRONZE.BRONZE_SUPERSTORE")
            silver_rows = _row_count(connection, "SHIPPING_DB.SILVER.SILVER_SUPERSTORE")
            gold_rows   = _row_count(connection, "SHIPPING_DB.GOLD.FACT_SHIPPING")

            log_pipeline_end(
                connection  = connection,
                run_id      = run_id,
                start_time  = start_time,
                status      = STATUS_SUCCESS,
                bronze_rows = bronze_rows,
                silver_rows = silver_rows,
                gold_rows   = gold_rows,
            )

            logger.info("=" * 60)
            logger.info("SUCCESS | bronze={} | silver={} | gold={}", bronze_rows, silver_rows, gold_rows)
            logger.info("=" * 60)

        except Exception as error:
            log_pipeline_end(
                connection    = connection,
                run_id        = run_id,
                start_time    = start_time,
                status        = STATUS_FAILED,
                error_message = str(error),
            )
            logger.exception("Pipeline FAILED | run_id={}", run_id)
            raise
