SELECT 
	msn
FROM pg.silver.v_total_energy_series
WHERE series_description LIKE '%Gas%'
	AND series_description LIKE '%Price%'
	AND unit LIKE '%Dollars per Gallon%'
	