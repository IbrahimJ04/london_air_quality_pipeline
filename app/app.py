import streamlit as st
import duckdb
from pathlib import Path

# Set up the dashboard
st.set_page_config(page_title="London Air Quality Dashboard", layout="wide")

st.title("London Air Quality Dashboard")
st.write("Exploring hourly nitrogen dioxide (NO₂) measurements across London monitoring stations.")
st.caption("NO₂ concentrations are measured in µg/m³ (micrograms per cubic metre).")
st.caption("Data source: London Air Quality Network (LAQN), Environmental Research Group, Imperial College London. Open Government Licence v2.")

# Connect to DuckDB and retrieve monitoring-site information
con = duckdb.connect("data/output/air_quality.duckdb", read_only=True)

# Read the SQL queries from the existing analysis file
sql_file = Path("sql/analysis_queries.sql")
queries = sql_file.read_text(encoding="utf-8").split(";")

sites = con.execute("""
    SELECT site_code, site_name, site_type, latitude, longitude
    FROM monitoring_sites
    ORDER BY site_code
""").df()

# Query 7: Average NO2 measurements by monitoring station
summary = con.execute(queries[6]).df()

# Query 5: Daily average NO2 measurements
daily = con.execute(queries[4]).df()

# Query 4: Average NO2 measurements by hour
hourly = con.execute(queries[3]).df()

# Query 6: Check data completeness
completeness = con.execute(queries[5]).df()

con.close()

# Display the monitoring stations
st.subheader("Monitoring Stations")
st.dataframe(sites)

# Display average NO2 measurements
st.subheader("NO₂ Summary")
st.dataframe(summary, hide_index=True)

# Display daily NO2 trends
st.subheader("Daily NO₂ Trends")
st.line_chart(daily, x="measurement_date", y="avg_no2", color="site_code")

# Display average NO2 measurements by hour
st.subheader("Hourly NO₂ Patterns")
st.line_chart(hourly, x="hour_gmt", y="avg_no2", color="site_code")

# Highlight days with missing measurements
st.subheader("Data Completeness")
missing_days = completeness[completeness["missing_readings"] > 0]
st.dataframe(missing_days, hide_index=True)


# Show the locations of the monitoring stations
st.subheader("Monitoring Station Locations")
st.map(sites, latitude="latitude", longitude="longitude")
