INSERT INTO SHIPPING_DB.SILVER.SILVER_SUPERSTORE
(
    ROW_ID,
    ORDER_ID,
    ORDER_DATE,
    SHIP_DATE,
    SHIP_MODE,
    ORDER_PRIORITY,
    CUSTOMER_ID,
    CUSTOMER_NAME,
    SEGMENT,
    COUNTRY,
    STATE,
    CITY,
    REGION,
    MARKET,
    MARKET2,
    PRODUCT_ID,
    PRODUCT_NAME,
    CATEGORY,
    SUB_CATEGORY,
    SALES,
    QUANTITY,
    DISCOUNT,
    PROFIT,
    SHIPPING_COST,
    SOURCE_FILE,
    LOAD_TIMESTAMP
)

WITH STREAM_DATA AS
(
    SELECT *
    FROM   SHIPPING_DB.BRONZE.BRONZE_STREAM
    WHERE  METADATA$ACTION = 'INSERT'
),

CLEANED AS
(
    SELECT
        ROW_ID,
        TRIM(ORDER_ID)                                          AS ORDER_ID,
        TRY_TO_DATE(ORDER_DATE, 'YYYY-MM-DD HH24:MI:SS.FF3')   AS ORDER_DATE,
        TRY_TO_DATE(SHIP_DATE,  'YYYY-MM-DD HH24:MI:SS.FF3')   AS SHIP_DATE,
        TRIM(UPPER(SHIP_MODE))                                  AS SHIP_MODE,
        TRIM(UPPER(ORDER_PRIORITY))                             AS ORDER_PRIORITY,
        TRIM(CUSTOMER_ID)                                       AS CUSTOMER_ID,
        TRIM(CUSTOMER_NAME)                                     AS CUSTOMER_NAME,
        TRIM(UPPER(SEGMENT))                                    AS SEGMENT,
        TRIM(UPPER(COUNTRY))                                    AS COUNTRY,
        TRIM(STATE)                                             AS STATE,
        TRIM(CITY)                                              AS CITY,
        TRIM(UPPER(REGION))                                     AS REGION,
        TRIM(UPPER(MARKET))                                     AS MARKET,
        TRIM(UPPER(MARKET2))                                    AS MARKET2,
        TRIM(PRODUCT_ID)                                        AS PRODUCT_ID,
        TRIM(PRODUCT_NAME)                                      AS PRODUCT_NAME,
        TRIM(UPPER(CATEGORY))                                   AS CATEGORY,
        TRIM(UPPER(SUB_CATEGORY))                               AS SUB_CATEGORY,
        SALES,
        QUANTITY,
        DISCOUNT,
        PROFIT,
        SHIPPING_COST,
        LOAD_TIMESTAMP                                          AS LOAD_TIMESTAMP,
        NULL::VARCHAR                                           AS SOURCE_FILE
    FROM STREAM_DATA
    WHERE TRIM(ORDER_ID)       IS NOT NULL
      AND TRIM(ORDER_ID)       != ''
      AND TRIM(SHIP_MODE)      IS NOT NULL
      AND TRIM(ORDER_PRIORITY) IS NOT NULL
      AND TRIM(COUNTRY)        IS NOT NULL
      AND TRIM(REGION)         IS NOT NULL
      AND TRY_TO_DATE(ORDER_DATE, 'YYYY-MM-DD HH24:MI:SS.FF3') IS NOT NULL
      AND TRY_TO_DATE(SHIP_DATE,  'YYYY-MM-DD HH24:MI:SS.FF3') IS NOT NULL
      AND SHIPPING_COST >= 0
),

DEDUPLICATED AS
(
    SELECT
        *,
        ROW_NUMBER() OVER (
            PARTITION BY ROW_ID
            ORDER BY     LOAD_TIMESTAMP DESC
        ) AS RN
    FROM CLEANED
)

SELECT
    ROW_ID, ORDER_ID, ORDER_DATE, SHIP_DATE, SHIP_MODE, ORDER_PRIORITY,
    CUSTOMER_ID, CUSTOMER_NAME, SEGMENT, COUNTRY, STATE, CITY, REGION,
    MARKET, MARKET2, PRODUCT_ID, PRODUCT_NAME, CATEGORY, SUB_CATEGORY,
    SALES, QUANTITY, DISCOUNT, PROFIT, SHIPPING_COST,
    SOURCE_FILE, LOAD_TIMESTAMP
FROM DEDUPLICATED
WHERE RN = 1;
