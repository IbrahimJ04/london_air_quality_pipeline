import duckdb
from pathlib import Path

# Read the SQL queries from the file
sql_file = Path("sql/analysis_queries.sql")
queries = sql_file.read_text(encoding="utf-8").split(";")

# Connect to the existing DuckDB database
con = duckdb.connect("data/output/air_quality.duckdb")

# Run each SQL query and display its results
for number, query in enumerate(queries, start=1):

    if query.strip():
        result = con.execute(query).df()

        print(f"\nQuery {number}")
        print(result.to_string(index=False))

con.close()


