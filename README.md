# London Air Quality Pipeline

## What I built and who for

I built an incremental data pipeline using the London Air Quality Network (LAQN) API to collect, store and analyse historical nitrogen dioxide (NO₂) measurements.

I designed the project as a prototype for London local authority environmental and transport teams who may need to monitor air quality patterns and assess the completeness of their monitoring data.

The pipeline provides a repeatable way to collect and update measurements, reducing the need for manual data collection. The dashboard allows users to explore hourly and daily NO₂ patterns, compare selected monitoring stations and identify gaps in the data that may require further investigation.

For the initial analysis, I selected two monitoring stations:

- **BT6 - Brent, John Keble Primary School:** Roadside.
- **BQ7 - Bexley, Belvedere West:** Urban Background.

The pipeline:

- Retrieves hourly NO₂ measurements from the LAQN API.
- Saves the original API responses as JSON files.
- Collects new dates incrementally, with a three-day lookback to check for delayed or updated measurements.
- Cleans and loads the data into two related DuckDB tables.
- Prevents duplicate measurements using a composite primary key.
- Uses SQL to analyse daily and hourly patterns, summary statistics and data completeness.
- Displays the results in a Streamlit dashboard, including charts and a monitoring-station map.

The current analysis compares two selected stations rather than making conclusions about pollution across London as a whole.


## About Me

I graduated with first-class honours in Mathematics with Computer Science with a strong interest in data, programming and problem solving. Python is the language I am most confident using, and I have been developing my experience with APIs, SQL and data pipelines through practical projects such as this one.

I am interested in The Information Lab's programme because it would allow me to develop my technical skills further while also gaining experience in consultancy. I like the idea of working with different clients, understanding their requirements and helping to turn data into useful solutions. The combination of structured training, practical project work and working collaboratively with others is particularly appealing to me.

## The data

The data comes from the London Air Quality Network (LAQN), using its public API.

- API reference: https://api.erg.ic.ac.uk/AirQuality/help
- API documentation: https://api.erg.ic.ac.uk/AirQuality/Information/Documentation/pdf

### Measurement units

Nitrogen dioxide (NO₂) concentrations are measured in micrograms per cubic metre (µg/m³). Measurement timestamps are in GMT.

### Data source and attribution

The air quality data was obtained from the Environmental Research Group at Imperial College London, using data from the London Air Quality Network (LAQN).

This information is licensed under the Open Government Licence, version 2.

- London Air Quality Network: https://www.londonair.org.uk/Londonair/API/
- API reference: https://api.erg.ic.ac.uk/AirQuality/help
- Open Government Licence v2: https://www.nationalarchives.gov.uk/doc/open-government-licence/version/2/

### Data collected

The initial dataset contains hourly nitrogen dioxide (NO₂) measurements from two monitoring stations:

- BT6 - Brent, John Keble Primary School (Roadside)
- BQ7 - Bexley, Belvedere West (Urban Background)

The current dataset covers 12 October to 1 November 2026, with measurement timestamps recorded in GMT.

Across the two stations, there are 1008 expected hourly records, of which 1000 contain numerical values.

Each station has 500 available measurements, with eight missing measurements across the dataset. The original API responses are preserved so these can be investigated.

### Data storage

The original measurements are saved as JSON files in `data/raw/`.

Monitoring-station metadata is saved in `data/raw/metadata/`.

The cleaned data is stored in two DuckDB tables:

- `hourly_measurements` - station code, pollutant code, measurement timestamp and numerical value.
- `monitoring_sites` - station code, name, classification and geographical coordinates.

The two tables are linked using `site_code`.

The DuckDB database is not uploaded to GitHub because it can be recreated from the saved JSON files using the loading script.

## How it works

The pipeline follows an Extract, Transform and Load (ETL) process.

### 1. Extract

`src/extract_air_quality.py` retrieves hourly NO₂ measurements from the LAQN API.

The script checks the dates already collected for each monitoring station and requests any new completed days.

It also uses a three-day lookback to recheck recent measurements for delayed or updated values.

Each API response is saved as a JSON file in `data/raw/`. Refreshed responses include a download timestamp in their filename so earlier files are preserved.

### 2. Transform and Load

`src/load_air_quality.py` reads the saved JSON files and prepares the measurements for DuckDB.

The script:

- Converts measurement timestamps and numerical values into appropriate data types.
- Excludes missing numerical measurements from the database while preserving them in the raw JSON.
- Handles overlapping measurements by retaining the latest downloaded numerical value.
- Creates or updates the `hourly_measurements` table without introducing duplicate records.
- Loads monitoring-station information into a separate `monitoring_sites` table.

Each hourly measurement is uniquely identified by its station code, pollutant code and measurement timestamp.

### 3. Analyse

The SQL queries in `sql/analysis_queries.sql` examine:

- Measurement counts and date coverage.
- Average, minimum and maximum NO₂ measurements.
- Daily and hourly pollution patterns.
- Missing measurements.
- Differences between the selected roadside and urban-background stations.

`src/run_analysis.py` runs the queries against DuckDB.

### 4. Visualise

The Streamlit application in `app/app.py` reads the existing SQL queries and displays:

- Monitoring-station information.
- NO₂ summary statistics.
- Daily and hourly trends.
- Data completeness.
- Monitoring-station locations on a map.

### Incremental loading

The extraction script downloads new completed days and rechecks the previous three days when new data is available.

The loading script processes the saved JSON files and uses a composite primary key with `INSERT OR REPLACE` to add new measurements or update existing ones without creating duplicates.

The three-day lookback helps capture recent corrections, although older corrections may require a longer historical refresh.

## How to run it

### 1. Clone the repository

```powershell
git clone https://github.com/IbrahimJ04/london_air_quality_pipeline.git
cd london_air_quality_pipeline
```

### 2. Create and activate a virtual environment

The project was developed using Python.

On Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 3. Install the required packages

```powershell
python -m pip install -r requirements.txt
```

### 4. Extract the latest measurements

```powershell
python src/extract_air_quality.py
```

This checks the existing raw files and retrieves new completed days from the LAQN API. When new days are available, it also rechecks the previous three days for updated measurements.

The API responses are saved in `data/raw/`.

An internet connection is required when downloading new data.

### 5. Load the data into DuckDB

```powershell
python src/load_air_quality.py
```

This creates or updates the DuckDB database using the saved JSON files.

The database contains two tables: `hourly_measurements` and `monitoring_sites`.

The database is stored at `data/output/air_quality.duckdb` and can be recreated from the saved raw data.

### 6. Run the SQL analysis

```powershell
python src/run_analysis.py
```

This executes the queries in `sql/analysis_queries.sql` and displays the results in the terminal.

### 7. Launch the Streamlit dashboard

```powershell
streamlit run app/app.py
```

The dashboard opens in a web browser, usually at `http://localhost:8501`.

Run all commands from the main project folder.

## What I would do next

With more time, I would consider the following improvements:

1. **Expand the monitoring stations:** Include more roadside and urban-background stations across London to make comparisons more meaningful.

2. **Extend the historical dataset:** Collect measurements over a longer period to investigate seasonal trends and provide a more reliable basis for comparison.

3. **Improve data quality checks:** Investigate negative readings and monitor missing measurements.

4. **Improve pipeline reliability:** Add more detailed error handling and logging to make the pipeline more robust if API requests fail or return unexpected data.

## Where AI helped

I used ChatGPT as a learning and development tool throughout this project, particularly when working with the London Air Quality Network API and implementing incremental data extraction.

Some specific examples include:

- **Preserving raw data:** While implementing the three-day lookback mechanism, I identified a potential risk of repeated downloads overwriting earlier JSON files. ChatGPT suggested including a UTC download timestamp in filenames, which I adopted to preserve previous API responses.

- **Reusing SQL queries:** I used ChatGPT to explore how the Streamlit dashboard could read queries directly from the SQL file rather than maintaining duplicate queries in Python.

- **Understanding and testing incremental loading:** ChatGPT helped explain the use of composite primary keys and `INSERT OR REPLACE`, and assisted with reviewing the Python and SQL implementation. I tested repeat loading, measurement updates and rebuilding the database from the saved JSON files.

I also used ChatGPT to review the project structure and documentation. I checked the outputs myself, investigated issues as they arose and made the final decisions about which suggestions to implement.