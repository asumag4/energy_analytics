SELECT 
	msn
	,series_description
	,unit
FROM silver.v_total_energy_series
WHERE (series_description LIKE '%Oil%'
	AND series_description LIKE '%Price%')
	AND unit LIKE '%Dollars per Gallon%'
	OR unit LIKE '%Dollars per Barrel%'