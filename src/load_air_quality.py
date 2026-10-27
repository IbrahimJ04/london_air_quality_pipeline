import json
import glob
import pandas as pd
import duckdb

# Read the saved JSON files and extract the measurements
rows = []

for filename in glob.glob("data/raw/*.json"):

    with open(filename, "r", encoding="utf-8") as file:
        data = json.load(file)

    site_code = data["RawAQData"]["@SiteCode"]
    species_code = data["RawAQData"]["@SpeciesCode"]

    for reading in data["RawAQData"]["Data"]:

        # Skip missing measurements
        if reading["@Value"] == "":
            continue

        rows.append({
            "site_code": site_code,
            "species_code": species_code,
            "measurement_datetime_gmt": reading["@MeasurementDateGMT"],
            "value": float(reading["@Value"])
        })

# Convert the measurements into a DataFrame
df = pd.DataFrame(rows)
df["measurement_datetime_gmt"] = pd.to_datetime(df["measurement_datetime_gmt"])

# Remove any repeated measurements
df = df.drop_duplicates(
    subset=["site_code", "species_code", "measurement_datetime_gmt"]
)

# Connect to DuckDB and create the table if needed
con = duckdb.connect("data/output/air_quality.duckdb")

con.execute("""
    CREATE TABLE IF NOT EXISTS hourly_measurements (
        site_code VARCHAR,
        species_code VARCHAR,
        measurement_datetime_gmt TIMESTAMP,
        value DOUBLE,
        PRIMARY KEY (site_code, species_code, measurement_datetime_gmt)
    )
""")

# Insert measurements without creating duplicate records
con.execute("""
    INSERT OR REPLACE INTO hourly_measurements
    SELECT site_code, species_code, measurement_datetime_gmt, value
    FROM df
""")

total = con.execute("SELECT COUNT(*) FROM hourly_measurements").fetchone()[0]
print(f"Total measurements in DuckDB: {total}")

con.close()