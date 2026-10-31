import requests
import json
from pathlib import Path
import pandas as pd
import duckdb

# Find the saved JSON files
RAW_DIR = Path("data/raw")

# Sort files by download time so newer responses take priority
def download_order(filename):
    parts = filename.stem.split("_")

    if len(parts) == 5:
        return parts[3]

    return ""

# Read the saved JSON files and extract the measurements
rows = []

for filename in sorted(RAW_DIR.glob("*.json"), key=download_order):

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

# Keep the latest value for each station, pollutant and timestamp
df = df.drop_duplicates(
    subset=["site_code", "species_code", "measurement_datetime_gmt"],
    keep="last"
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


# Load monitoring-site information
metadata_file = Path("data/raw/metadata/monitoring_sites.json")

# Download and save the metadata if it has not been saved before
if not metadata_file.exists():
    metadata_file.parent.mkdir(parents=True, exist_ok=True)

    url = "https://api.erg.ic.ac.uk/AirQuality/Information/MonitoringSites/GroupName=London/Json"
    response = requests.get(url, timeout=30)
    response.raise_for_status()

    with open(metadata_file, "w", encoding="utf-8") as file:
        json.dump(response.json(), file, indent=2)

# Read the saved station information
with open(metadata_file, "r", encoding="utf-8") as file:
    metadata = json.load(file)

site_codes = ["BQ7", "BT6"]
sites = []

for site in metadata["Sites"]["Site"]:
    if site["@SiteCode"] in site_codes:
        sites.append({
            "site_code": site["@SiteCode"],
            "site_name": site["@SiteName"],
            "site_type": site["@SiteType"],
            "latitude": float(site["@Latitude"]),
            "longitude": float(site["@Longitude"])
        })

sites_df = pd.DataFrame(sites)

# Create the monitoring-sites table
con.execute("""
    CREATE TABLE IF NOT EXISTS monitoring_sites (
        site_code VARCHAR PRIMARY KEY,
        site_name VARCHAR,
        site_type VARCHAR,
        latitude DOUBLE,
        longitude DOUBLE
    )
""")

# Add or update monitoring-site information
con.execute("""
    INSERT OR REPLACE INTO monitoring_sites
    SELECT site_code, site_name, site_type, latitude, longitude
    FROM sites_df
""")

print(con.execute("SELECT * FROM monitoring_sites").df())



con.close()