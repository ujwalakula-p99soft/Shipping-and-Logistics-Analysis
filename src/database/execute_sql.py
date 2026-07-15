from pathlib import Path

from snowflake.connector import SnowflakeConnection

from src.utils.logger import get_logger

logger = get_logger()


def execute_sql_file(
    connection: SnowflakeConnection,
    sql_file: Path,
) -> None:

    sql = sql_file.read_text(encoding="utf-8")

    cursor = connection.cursor()

    try:

        logger.info("Executing {}", sql_file.name)

        for statement in sql.split(";"):

            statement = statement.strip()

            if statement:

                cursor.execute(statement)

        logger.info("{} executed successfully.", sql_file.name)

    finally:

        cursor.close()
