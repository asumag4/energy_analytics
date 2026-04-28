{%
    set ml_drilling_cols = dbt_utils.get_column_values (
        table=ref('v_total_energy_series'),
        column='msn',
        where="(
            series_description LIKE '%Crude Oil Rotary Rigs in Operation%' 
            OR series_description LIKE '%Natural Gas Rotary Rigs in Operation%'
            OR series_description LIKE '%Crude Oil and Natural Gas Rotary Rigs in Operation%'
            OR series_description LIKE '%Crude Oil, Natural Gas, and Dry Wells Drilled%'
            OR series_description LIKE '%Wells Drilled%'
            OR series_description LIKE '%Natural Gas Imports%'
            OR series_description LIKE '%NGPL Production%'
            OR series_description LIKE '%Natural Gas in Underground Storage%'
            OR series_description LIKE '%Petroleum Imports%'
            OR series_description LIKE '%Petroleum Exports%'
            OR series_description LIKE '%Petroleum Products%'
            OR series_description LIKE '%Crude Oil Production%'
            OR series_description LIKE '%Crude Oil Stocks%'
            OR series_description LIKE '%Stock Change%'
            OR series_description LIKE '%Carbon Dioxide%'
            )
            AND series_description NOT LIKE '%Total%'"
    )
    %}

SELECT 
    period
    ,{% for col in ml_drilling_cols %}
        "{{ col | lower }}"
        {% if not loop.last %},{% endif %}
    {% endfor %}
FROM {{ ref('v_total_energy_pivot') }}