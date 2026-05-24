SELECT 
	msn
FROM pg.silver.v_total_energy_series
WHERE series_description LIKE '%Emission%'
	AND (
	series_description LIKE '%Oil%'
	OR series_description LIKE '%Gas%'
	OR series_description LIKE '%Fuel%'
	)