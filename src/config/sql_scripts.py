from pathlib import Path

_SQL_ROOT = Path(__file__).resolve().parents[2] / "sql"

# Bootstrap — must run before audit logging and CSV upload
BOOTSTRAP_SCRIPTS: list[Path] = [
    _SQL_ROOT / "audit"  / "create_pipeline_audit.sql",
    _SQL_ROOT / "bronze" / "create_stage.sql",
    _SQL_ROOT / "bronze" / "create_file_format.sql",
    _SQL_ROOT / "bronze" / "create_bronze_table.sql",
    _SQL_ROOT / "bronze" / "create_stream.sql",
    _SQL_ROOT / "silver" / "create_silver_table.sql",
    _SQL_ROOT / "silver" / "create_stream.sql",
]

# Main pipeline — runs once per batch
SQL_SCRIPTS: list[Path] = [

    # Bronze
    _SQL_ROOT / "bronze" / "load_bronze.sql",

    # Silver
    _SQL_ROOT / "silver" / "transform_to_silver.sql",

    # Gold — dimensions
    _SQL_ROOT / "gold/dimensions" / "create_dim_date.sql",
    _SQL_ROOT / "gold/dimensions" / "create_dim_location.sql",
    _SQL_ROOT / "gold/dimensions" / "create_dim_ship_mode.sql",
    _SQL_ROOT / "gold/dimensions" / "create_dim_order_priority.sql",
    _SQL_ROOT / "gold/dimensions" / "load_dim_date.sql",
    _SQL_ROOT / "gold/dimensions" / "load_dim_location.sql",
    _SQL_ROOT / "gold/dimensions" / "load_dim_ship_mode.sql",
    _SQL_ROOT / "gold/dimensions" / "load_dim_order_priority.sql",

    # Gold — fact
    _SQL_ROOT / "gold/facts" / "create_fact_shipping.sql",
    _SQL_ROOT / "gold/facts" / "load_fact_shipping.sql",

    # Reports
    _SQL_ROOT / "gold/views" / "create_views.sql",
]
