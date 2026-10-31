import duckdb

# Create a temporary database for testing
con = duckdb.connect(":memory:")

# Create a table with the same primary key as our main database
con.execute("""
    CREATE TABLE hourly_measurements (
        site_code VARCHAR,
        species_code VARCHAR,
        measurement_datetime_gmt TIMESTAMP,
        value DOUBLE,
        PRIMARY KEY (site_code, species_code, measurement_datetime_gmt)
    )
""")

# Insert an original measurement
con.execute("""
    INSERT INTO hourly_measurements
    VALUES ('TEST', 'NO2', '2026-10-28 09:00:00', 10.0)
""")

# Simulate a corrected measurement for the same hour
con.execute("""
    INSERT OR REPLACE INTO hourly_measurements
    VALUES ('TEST', 'NO2', '2026-10-28 09:00:00', 12.0)
""")

# Simulate a previously missing measurement becoming available
con.execute("""
    INSERT OR REPLACE INTO hourly_measurements
    VALUES ('TEST', 'NO2', '2026-10-28 10:00:00', 8.0)
""")

# Check the final values
print(con.execute("""
    SELECT measurement_datetime_gmt, value
    FROM hourly_measurements
    ORDER BY measurement_datetime_gmt
""").df())

con.close()