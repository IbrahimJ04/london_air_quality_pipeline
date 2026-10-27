import requests

# Monitoring stations to check
site_codes = ["BQ7", "BT6", "BT8", "BX2"]

# Date range for checking recent measurements
start_date = "2026-10-24"
end_date = "2026-10-25"

for site_code in site_codes:

    # Build the API URL for each station
    url = (
        "https://api.erg.ic.ac.uk/AirQuality/Data/SiteSpecies/"
        f"SiteCode={site_code}/SpeciesCode=NO2/"
        f"StartDate={start_date}/EndDate={end_date}/Json"
    )

    # Request data from the LAQN API
    response = requests.get(url, timeout=30)
    response.raise_for_status()

    # Extract the hourly measurements from the JSON response
    data = response.json()
    readings = data["RawAQData"]["Data"]

    # Count how many measurements have values
    available = 0
    for reading in readings:
        if reading.get("@Value") != "" and reading.get("@Value") is not None:
            available += 1

    # Display the results for this station
    print(f"{site_code}: {available} of {len(readings)} readings available")