SELECT 
	msn
FROM pg.silver.v_total_energy_series
WHERE series_description LIKE '%Storage%'
	AND series_description LIKE '%Gas%'