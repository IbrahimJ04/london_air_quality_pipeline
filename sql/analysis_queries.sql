-- Check the number of measurements and date range for each station
SELECT
    site_code,
    COUNT(*) AS reading_count,
    MIN(measurement_datetime_gmt) AS first_reading,
    MAX(measurement_datetime_gmt) AS last_reading
FROM hourly_measurements
GROUP BY site_code
ORDER BY site_code;


-- Compare average NO2 measurements between stations
SELECT
    site_code,
    COUNT(*) AS reading_count,
    ROUND(AVG(value), 2) AS avg_no2,
    ROUND(MIN(value), 2) AS min_no2,
    ROUND(MAX(value), 2) AS max_no2
FROM hourly_measurements
GROUP BY site_code
ORDER BY site_code;


-- Check which pollutants are stored
SELECT DISTINCT species_code
FROM hourly_measurements;


-- Calculate average NO2 levels for each hour of the day
SELECT
    site_code,
    EXTRACT(HOUR FROM measurement_datetime_gmt) AS hour_gmt,
    ROUND(AVG(value), 2) AS avg_no2
FROM hourly_measurements
WHERE species_code = 'NO2'
GROUP BY site_code, hour_gmt
ORDER BY site_code, hour_gmt;


-- Calculate average NO2 measurements for each day
SELECT
    site_code,
    CAST(measurement_datetime_gmt AS DATE) AS measurement_date,
    ROUND(AVG(value), 2) AS avg_no2
FROM hourly_measurements
WHERE species_code = 'NO2'
GROUP BY site_code, measurement_date
ORDER BY measurement_date, site_code;


-- Check missing hourly measurements for each station and day
SELECT
    site_code,
    CAST(measurement_datetime_gmt AS DATE) AS measurement_date,
    COUNT(*) AS available_readings,
    24 - COUNT(*) AS missing_readings
FROM hourly_measurements
GROUP BY site_code, measurement_date
ORDER BY measurement_date, site_code;


-- Compare average NO2 levels by monitoring-site type
SELECT
    s.site_name,
    s.site_type,
    COUNT(*) AS reading_count,
    ROUND(AVG(m.value), 2) AS avg_no2
FROM hourly_measurements m
JOIN monitoring_sites s
    ON m.site_code = s.site_code
WHERE m.species_code = 'NO2'
GROUP BY s.site_name, s.site_type
ORDER BY avg_no2 DESC;
