import pandas as pd
import sqlite3

# Load CSV file
csv_file = "childcare_data.csv"  # Change if needed
df = pd.read_csv(csv_file)

# Connect to SQLite (or create it)
conn = sqlite3.connect("childcare.db")
cursor = conn.cursor()

# Define table schema (adjust as needed)
table_name = "childcare_facilities"
df.to_sql(table_name, conn, if_exists="replace", index=False)

# Verify import
print("Imported rows:", len(df))

# Close connection
conn.close()