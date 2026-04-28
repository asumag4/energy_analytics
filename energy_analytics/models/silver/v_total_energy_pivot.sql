-- Get distinct MSN values dynamically at compile time --
{% set msn_values = dbt_utils.get_column_values(
    table=source('bronze','t_total_energy'),
    column='msn'
)
%}

-- pivot --
SELECT
    period
    ,{{ dbt_utils.pivot(
        column='msn'
        ,values=msn_values
        ,agg='MAX'
        ,then_value='value'
        ,else_value='NULL'
        ,quote_identifiers=false
    )
    }}
FROM {{ source('bronze','t_total_energy') }}
GROUP BY period
ORDER BY period