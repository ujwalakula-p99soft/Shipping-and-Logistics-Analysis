SELECT
    sm.SHIP_MODE,
    COUNT(f.ORDER_ID)                                       AS TOTAL_ORDERS,
    ROUND(
        COUNT(f.ORDER_ID) * 100.0
        / SUM(COUNT(f.ORDER_ID)) OVER ()
    , 2)                                                    AS ORDER_SHARE_PCT,
    ROUND(AVG(f.SHIPPING_COST), 2)                          AS AVG_SHIPPING_COST,
    ROUND(SUM(f.SHIPPING_COST), 2)                          AS TOTAL_SHIPPING_COST,
    ROUND(AVG(f.SHIPPING_DURATION), 2)                      AS AVG_SHIPPING_DAYS,
    SUM(CASE WHEN f.IS_DELAYED THEN 1 ELSE 0 END)           AS DELAYED_ORDERS,
    ROUND(
        SUM(CASE WHEN f.IS_DELAYED THEN 1 ELSE 0 END)
        * 100.0
        / NULLIF(COUNT(f.ORDER_ID), 0)
    , 2)                                                    AS DELAY_RATE_PCT
FROM GOLD.FACT_SHIPPING        f
INNER JOIN GOLD.DIM_SHIP_MODE  sm ON f.SHIP_MODE_KEY = sm.SHIP_MODE_KEY
GROUP BY
    sm.SHIP_MODE
ORDER BY
    TOTAL_ORDERS DESC;
