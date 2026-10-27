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

If monitoring-site and pollutant metadata are incorporated into the pipeline, the transformation will need to handle both structures consistently.

A possible approach is to convert a single Species dictionary into a one-element list before processing the pollutant records.

This approach has not yet been implemented or tested.

I also observed that some stations have historical closing dates, so the site metadata alone cannot establish which stations currently provide measurements. Recent readings will need to be checked separately.


## 27 October 2026 - Initial Historical Extraction and Storage

### Station selection

I tested recent NO2 data availability for four monitoring stations:

- BQ7 (Urban Background): 24/24 readings available.
- BT6 (Roadside): 24/24 readings available.
- BT8 (Roadside): 0/24 readings available.
- BX2 (Suburban): 23/24 readings available.

I selected BQ7 and BT6 for the initial pipeline because both returned complete numerical readings for the test day. Additional stations may be included later.

### Historical data

I retrieved hourly NO2 data for both selected stations covering 12–25 October 2026.

The original API responses were saved as JSON files in data/raw, preserving the source data for reproducibility.

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
