SELECT
    DATE_TRUNC('month', period::DATE)   AS period,
    series								AS msn,
    SUM(value)                          AS value,
    MAX(series_description)             AS series_description,
    MAX(units)                          AS unit
FROM bronze.t_crude_inventory
GROUP BY
    DATE_TRUNC('month', period::DATE),
    series
ORDER BY
    period,
    series