SELECT 
	msn
FROM pg.silver.v_total_energy_series
WHERE series_description LIKE '%Oil%'
	AND series_description LIKE '%Suppl%'
	AND unit = 'Trillion Btu'

/*
Note: we'll be using an energy-based comparison instead of a 
volume-based comparison to ensure comparability between fuel 
products and their quality
*/