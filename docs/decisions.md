# Project Decision Log

This document records significant project decisions, their rationale, alternatives considered and any outstanding questions.

## 25 October 2026 - Initial Project Direction

**Decision status:** Provisional - subject to API exploration.

**Proposed audience:** London local authority transport and environmental teams.

**Proposed focus:** Investigate nitrogen dioxide (NO₂) measurements at selected roadside and urban-background monitoring sites, focusing on rush-hour patterns and the completeness of monitoring data.

### Alternatives Considered

- Geographical comparisons of pollution levels across London.
- Air-quality patterns during school travel hours.
- Monitoring-site data completeness and reliability.
- Identification of unusual pollution events.

### Rationale

The proposed direction combines a clear question for a defined audience with opportunities to demonstrate historical data collection, data quality checks and useful visualisations.

A geographical monitoring-site map and an hourly heat map are being considered as possible outputs.

### Outstanding Questions

- Which monitoring sites currently provide suitable NO₂ measurements?
- Are both roadside and urban-background sites available?
- How complete and recent are their measurements?
- What fields and relationships does the API provide?
- How should the pipeline handle missing or delayed readings?
- What data model will best support incremental updates without duplicates?

The final scope and implementation approach will be determined after investigating the API and its data.

## 25 October 2026 - Exploring the LAQN API

### Findings

I explored the MonitoringSites and MonitoringSiteSpecies endpoints to understand how monitoring stations and pollutants are represented in the API.

The MonitoringSites response contains information about monitoring stations, including site codes, names, classifications, locations and opening/closing dates.

The MonitoringSiteSpecies response also includes information about the pollutants measured at each station.

I identified an inconsistency in how the Species field is represented:

- Stations with one pollutant can have Species represented as a JSON object (dictionary).
- Stations with multiple pollutants can have Species represented as a JSON array (list).

### Implications for the pipeline

If pollutant metadata from the MonitoringSiteSpecies endpoint is incorporated into the pipeline, the transformation will need to handle both structures consistently.

A possible approach is to convert a single Species dictionary into a one-element list before processing the pollutant records.

This approach has not yet been implemented or tested.

I also observed that some stations have historical closing dates, so the site metadata alone cannot establish which stations currently provide measurements. Recent readings will need to be checked separately.


## 27 October 2026 - Initial Historical Extraction and Storage

### Station selection

I tested recent NO₂ data availability for four monitoring stations:

- BQ7 (Urban Background): 24/24 readings available.
- BT6 (Roadside): 24/24 readings available.
- BT8 (Roadside): 0/24 readings available.
- BX2 (Suburban): 23/24 readings available.

I selected BQ7 and BT6 for the initial pipeline because both returned complete numerical readings for the test day. Additional stations may be included later.

### Historical data

I retrieved hourly NO₂ data for both selected stations covering 12-25 October 2026.

The original API responses were saved as JSON files in data/raw/, preserving the source data for reproducibility.

The extraction returned 336 hourly records per station, giving 672 records in total.

### Transformation and storage

I used pandas to organise the measurements and convert timestamps and numerical values into appropriate data types.

Missing measurements are excluded from the DuckDB table but remain in the saved JSON responses.

The DuckDB table uses a composite primary key consisting of site code, pollutant code and measurement timestamp.

After loading the historical files, the database contained 665 unique measurements.

### Testing

I ran the loading script multiple times using the same historical files.

The total remained at 665 measurements, confirming that reloading the same records did not create duplicates.

### Next steps

The extraction currently uses fixed dates. The next priority is to make it incremental so that future runs retrieve additional data without losing existing history.


## 28 October 2026 - Incremental Extraction

### Implementation

I updated the extraction script to identify the latest date already collected for each monitoring station using the saved JSON filenames.

The script requests measurements for new completed days and saves them as separate JSON files, preserving the previous historical responses.

If no new completed days are available, the script skips the API request.

### Testing

The updated script retrieved measurements for 26-27 October 2026:

- BQ7: 48 hourly records.
- BT6: 48 hourly records.

When I ran the extraction script a second time, it recognised that the latest completed days had already been downloaded and therefore did not request the same data again.

After loading the new files, the DuckDB database increased from 665 to 760 measurements.

Running the loading script again left the total unchanged at 760, confirming that duplicate measurements were not added.

### Remaining limitation

The current extraction only requests dates that have not previously been collected. It does not revisit earlier dates to check whether missing or delayed measurements have become available.

This will need to be considered before the final pipeline is complete.


## 29 October 2026 - Database reproducibility

### Decision

Keep the original API responses and monitoring-station metadata as saved JSON files, rather than relying on a pre-built DuckDB database.

### Reason

The database is a generated output. Keeping the raw data means the database can be recreated by anyone running the project, without needing a copy of my local database file.

### Implementation
- Save hourly measurements in `data/raw/`.
- Save monitoring-station metadata in `data/raw/metadata/`.
- Exclude generated DuckDB files from Git using `.gitignore`.
- Rebuild the database using `src/load_air_quality.py`.

### Testing

I created backup copies of the original database, moved it out of the way and ran the loading script to create a new database from the saved JSON files.

The rebuilt database contained:
- 808 hourly measurements: 404 for BQ7 and 404 for BT6.
- Two monitoring-station records.
- The expected measurement period of 12-28 October 2026.

All seven SQL analysis queries ran successfully against the rebuilt database.

### Trade-off:

Rebuilding from all saved JSON files involves reprocessing historical data. This is manageable for the current dataset, but a larger pipeline would benefit from more selective processing.


## 29 October 2026 - Handling incremental updates and overlapping data

### Decision

Use a three-day lookback when new completed days become available, preserve each API response and update existing measurements without creating duplicates.

### Reason

Air quality measurements may be published late or revised after their initial collection. Downloading only completely new dates could miss changes to recent measurements.

### Implementation
- Check the end dates of previously saved JSON files for each monitoring station.
- Skip extraction when no new completed days are available.
- When new days are available, move the extraction start date back three days.
- Include a UTC download timestamp in refreshed JSON filenames so previous responses are not overwritten.
- Process older downloads before newer ones and retain the latest numerical value for overlapping measurements.
- Use a composite primary key of `site_code`, `species_code` and `measurement_datetime_gmt` in DuckDB.
- Use `INSERT OR REPLACE` to insert new measurements or update existing ones.

### Testing
- Repeated loading did not increase the number of unique measurements.
- A controlled database test confirmed that an existing measurement could be updated without creating a duplicate.
- Running the extraction script again on the same day correctly reported that there were no new completed days to download.

### Trade-off

The three-day lookback allows recent measurements to be rechecked for possible updates without repeatedly downloading the entire historical dataset. Corrections made further back in time would require a longer refresh period.


## 29 October 2026 - Data quality and completeness

### Decision

Preserve the original measurements, exclude missing numerical values from the analysis and identify gaps in the available hourly data.

### Reason

Air quality monitoring data may contain missing or unusual values. These need to be identified rather than silently treated as valid measurements or replaced with estimated values.

### Implementation
- Preserve the original API responses as JSON files.
- Exclude empty measurement values when loading numerical data into DuckDB.
- Do not replace missing values with zero or estimated readings.
- Use SQL to calculate the number of available and missing hourly measurements for each station and date.
- Retain unusual numerical readings for investigation rather than automatically removing them.

### Findings
- The dataset covers 12-28 October 2026.
- Across both stations, 816 hourly measurements were expected.
- There were 808 available numerical measurements and eight missing measurements.
- BQ7 had four missing measurements on 14 October.
- BT6 had three missing measurements on 22 October and one on 26 October.
- BQ7 also contained a negative NO₂ value of -0.9, which requires further investigation.

### Trade-off

Retaining unusual values avoids making unsupported assumptions about their validity. However, potentially erroneous measurements may affect summary statistics until they have been investigated.


The current completeness calculation assumes 24 hourly measurements per station per GMT date. A day with no numerical measurements would not appear in the current daily completeness results.
