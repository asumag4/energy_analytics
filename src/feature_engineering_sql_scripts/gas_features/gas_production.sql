SELECT 
	msn
FROM pg.silver.v_total_energy_series
WHERE series_description LIKE '%Production%'
	AND series_description LIKE '%Gas%'
	AND unit = 'Trillion Btu'