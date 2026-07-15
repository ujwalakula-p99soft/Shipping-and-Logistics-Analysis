CREATE TABLE IF NOT EXISTS SHIPPING_DB.GOLD.FACT_SHIPPING
(
    FACT_KEY                          NUMBER IDENTITY(1,1),
    ORDER_ID                          VARCHAR(50)     NOT NULL,
    ORDER_DATE_KEY                    NUMBER          NOT NULL,
    SHIP_DATE_KEY                     NUMBER          NOT NULL,
    LOCATION_KEY                      NUMBER          NOT NULL,
    SHIP_MODE_KEY                     NUMBER          NOT NULL,
    ORDER_PRIORITY_KEY                NUMBER          NOT NULL,
    SHIPPING_DURATION                 NUMBER,
    SHIPPING_DURATION_MEDIAN_BY_MODE  NUMBER(10, 4),
    IS_DELAYED                        BOOLEAN,
    SHIPPING_COST                     NUMBER(18, 4),
    LOAD_TIMESTAMP                    TIMESTAMP_NTZ   DEFAULT CURRENT_TIMESTAMP(),
    CONSTRAINT PK_FACT_SHIPPING PRIMARY KEY (FACT_KEY)
);
