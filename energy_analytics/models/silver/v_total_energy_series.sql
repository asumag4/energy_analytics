with source AS (
    select * from {{ source('bronze', 't_total_energy') }}
)

SELECT
    DISTINCT
        msn
        ,series_description
FROM source