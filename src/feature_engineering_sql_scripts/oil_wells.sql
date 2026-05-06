SELECT 
	msn
	,series_description
	,unit
FROM silver.v_total_energy_series
WHERE (series_description LIKE '%Oil%'
	AND series_description LIKE '%Well%')
	AND series_description NOT LIKE '%Gas%'
	AND unit = 'Number'