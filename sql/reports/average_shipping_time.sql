SELECT
    sm.SHIP_MODE,
    COUNT(f.ORDER_ID)                                   AS TOTAL_ORDERS,
    ROUND(AVG(f.SHIPPING_DURATION), 2)                  AS AVG_SHIPPING_DAYS,
    ROUND(
        PERCENTILE_CONT(0.5)
            WITHIN GROUP (ORDER BY f.SHIPPING_DURATION)
    , 2)                                                AS MEDIAN_SHIPPING_DAYS,
    MIN(f.SHIPPING_DURATION)                            AS MIN_SHIPPING_DAYS,
    MAX(f.SHIPPING_DURATION)                            AS MAX_SHIPPING_DAYS
FROM GOLD.FACT_SHIPPING        f
INNER JOIN GOLD.DIM_SHIP_MODE  sm ON f.SHIP_MODE_KEY = sm.SHIP_MODE_KEY
GROUP BY
    sm.SHIP_MODE
ORDER BY
    AVG_SHIPPING_DAYS ASC;
