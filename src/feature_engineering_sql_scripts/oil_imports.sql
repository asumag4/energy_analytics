SELECT 
	msn
FROM pg.silver.v_total_energy_series
WHERE series_description LIKE '%Import%'
	AND series_description LIKE '%Oil%'
	AND unit = 'Trillion Btu'