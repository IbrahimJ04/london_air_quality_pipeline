import requests
import json
import os
from datetime import datetime, timezone

site_codes = ["BQ7", "BT6"]

# Use today's UTC date as the end of the collection period
end_date = datetime.now(timezone.utc).date().isoformat()

os.makedirs("data/raw", exist_ok=True)

for site_code in site_codes:

    # Find where the previous extraction finished
    start_date = "2026-10-12"

    for filename in os.listdir("data/raw"):
        if filename.startswith(f"{site_code}_NO2_") and filename.endswith(".json"):
            saved_end_date = filename.replace(".json", "").split("_")[-1]

            if saved_end_date > start_date:
                start_date = saved_end_date

    # Skip stations that already have the latest completed day
    if start_date >= end_date:
        print(f"{site_code}: No new completed days to download")
        continue

    # Request the new hourly measurements
    url = (
        "https://api.erg.ic.ac.uk/AirQuality/Data/SiteSpecies/"
        f"SiteCode={site_code}/SpeciesCode=NO2/"
        f"StartDate={start_date}/EndDate={end_date}/Json"
    )

    response = requests.get(url, timeout=30)
    response.raise_for_status()
    data = response.json()

    # Save the new data without replacing previous historical files
    filename = f"data/raw/{site_code}_NO2_{start_date}_{end_date}.json"

    with open(filename, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=2)

    readings = data["RawAQData"]["Data"]
    print(f"{site_code}: saved {len(readings)} hourly records")