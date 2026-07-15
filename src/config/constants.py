PROJECT_NAME  = "Shipping Logistics Analysis"
PIPELINE_NAME = "Shipping Logistics Pipeline"

REQUIRED_COLUMNS = [
    "order_id",
    "order_date",
    "ship_date",
    "ship_mode",
    "order_priority",
    "country",
    "state",
    "city",
    "region",
    "shipping_cost",
]

DATE_COLUMNS = [
    "order_date",
    "ship_date",
]

SNOWFLAKE_ROLE      = "ACCOUNTADMIN"
SNOWFLAKE_WAREHOUSE = "COMPUTE_WH"
SNOWFLAKE_DATABASE  = "SHIPPING_DB"

STATUS_RUNNING = "RUNNING"
STATUS_SUCCESS = "SUCCESS"
STATUS_FAILED  = "FAILED"
