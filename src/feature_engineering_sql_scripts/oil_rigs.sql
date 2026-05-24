SELECT 
	msn
FROM pg.silver.v_total_energy_series
WHERE (series_description LIKE '%Oil%'
	AND series_description LIKE '%Rig%')
	AND series_description NOT LIKE '%Gas%'