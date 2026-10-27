import requests
import json
import os

# Stations and historical date range
site_codes = ["BQ7", "BT6"]
start_date = "2026-10-12"
end_date = "2026-10-26"

# Create the folder for the original API responses
os.makedirs("data/raw", exist_ok=True)

for site_code in site_codes:

    # Request hourly NO2 measurements
    url = (
        "https://api.erg.ic.ac.uk/AirQuality/Data/SiteSpecies/"
        f"SiteCode={site_code}/SpeciesCode=NO2/"
        f"StartDate={start_date}/EndDate={end_date}/Json"
    )

    response = requests.get(url, timeout=30)
    response.raise_for_status()
    data = response.json()

    # Save the response as a JSON file
    filename = f"data/raw/{site_code}_NO2_{start_date}_{end_date}.json"

    with open(filename, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=2)

    readings = data["RawAQData"]["Data"]
    print(f"{site_code}: saved {len(readings)} hourly records")