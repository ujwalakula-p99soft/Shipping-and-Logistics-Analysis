SELECT
    l.REGION,
    l.COUNTRY,
    COUNT(f.ORDER_ID)                                           AS TOTAL_ORDERS,
    ROUND(AVG(f.SHIPPING_DURATION), 2)                          AS AVG_SHIPPING_DURATION,
    ROUND(
        PERCENTILE_CONT(0.5)
            WITHIN GROUP (ORDER BY f.SHIPPING_DURATION)
    , 2)                                                        AS MEDIAN_SHIPPING_DURATION,
    SUM(CASE WHEN f.IS_DELAYED THEN 1 ELSE 0 END)               AS DELAYED_ORDERS,
    ROUND(
        SUM(CASE WHEN f.IS_DELAYED THEN 1 ELSE 0 END)
        * 100.0
        / NULLIF(COUNT(f.ORDER_ID), 0)
    , 2)                                                        AS DELAY_RATE_PCT,
    ROUND(AVG(f.SHIPPING_COST), 2)                              AS AVG_SHIPPING_COST,
    ROUND(SUM(f.SHIPPING_COST), 2)                              AS TOTAL_SHIPPING_COST,
    RANK() OVER (
        ORDER BY
            SUM(CASE WHEN f.IS_DELAYED THEN 1 ELSE 0 END)
            * 100.0
            / NULLIF(COUNT(f.ORDER_ID), 0) DESC
    )                                                           AS DELAY_RANK
FROM GOLD.FACT_SHIPPING    f
INNER JOIN GOLD.DIM_LOCATION l ON f.LOCATION_KEY = l.LOCATION_KEY
GROUP BY
    l.REGION,
    l.COUNTRY
ORDER BY
    DELAY_RANK ASC;
