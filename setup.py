import json
import sys
from pathlib import Path

import boto3
import snowflake.connector
from botocore.exceptions import BotoCoreError, ClientError
from dotenv import load_dotenv
import os

PROJECT_ROOT = Path(__file__).resolve().parent
load_dotenv(PROJECT_ROOT / ".env")

AWS_REGION            = os.getenv("AWS_REGION", "")
AWS_SECRET_NAME       = os.getenv("AWS_SECRET_NAME", "")
AWS_ACCESS_KEY_ID     = os.getenv("AWS_ACCESS_KEY_ID", "")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY", "")

SETUP_FILES = [
    PROJECT_ROOT / "sql" / "setup" / "create_warehouse.sql",
    PROJECT_ROOT / "sql" / "setup" / "create_database.sql",
    PROJECT_ROOT / "sql" / "setup" / "create_schemas.sql",
]


def get_snowflake_credentials() -> dict:
    print("[INFO] Fetching Snowflake credentials from AWS Secrets Manager...")
    try:
        client = boto3.client(
            service_name          = "secretsmanager",
            region_name           = AWS_REGION,
            aws_access_key_id     = AWS_ACCESS_KEY_ID,
            aws_secret_access_key = AWS_SECRET_ACCESS_KEY,
        )
        response    = client.get_secret_value(SecretId=AWS_SECRET_NAME)
        credentials = json.loads(response["SecretString"])
        print("[INFO] Credentials retrieved successfully.")
        return credentials
    except (ClientError, BotoCoreError) as error:
        print(f"[ERROR] Failed to retrieve AWS secret: {error}")
        sys.exit(1)


def run_sql_file(cursor, sql_file: Path) -> None:
    sql = sql_file.read_text(encoding="utf-8")
    for statement in sql.split(";"):
        statement = statement.strip()
        if statement:
            cursor.execute(statement)
    print(f"[OK]   {sql_file.name}")


def main() -> None:
    print("=" * 55)
    print("  Snowflake Setup — Shipping Logistics Pipeline")
    print("=" * 55)

    credentials = get_snowflake_credentials()

    print("[INFO] Connecting to Snowflake...")
    try:
        connection = snowflake.connector.connect(
            user     = credentials["user"],
            password = credentials["password"],
            account  = credentials["account"],
        )
    except Exception as error:
        print(f"[ERROR] Snowflake connection failed: {error}")
        sys.exit(1)

    print("[INFO] Connected. Running setup scripts...\n")
    cursor = connection.cursor()

    try:
        cursor.execute("USE ROLE ACCOUNTADMIN")
        for sql_file in SETUP_FILES:
            run_sql_file(cursor, sql_file)
    except Exception as error:
        print(f"\n[ERROR] Setup failed: {error}")
        sys.exit(1)
    finally:
        cursor.close()
        connection.close()
        print("\n[INFO] Snowflake connection closed.")

    print("\n" + "=" * 55)
    print("  Setup completed.")
    print("  1. python scripts/split_dataset.py")
    print("  2. python -m src.main   (repeat for each batch)")
    print("=" * 55)


if __name__ == "__main__":
    main()
