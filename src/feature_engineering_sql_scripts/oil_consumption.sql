SELECT 
	msn
FROM pg.silver.v_total_energy_series
WHERE series_description LIKE '%Consumption%'
	AND series_description LIKE '%Oil%'
	AND unit = 'Thousand Barrels'