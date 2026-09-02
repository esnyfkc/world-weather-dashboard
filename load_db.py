import sqlite3
import pandas as pd

# Load cleaned CSV into a DataFrame
df = pd.read_csv("data/weather_data.csv")

print("First 5 rows:")
print(df.head())

print("\nNumber of rows:", len(df))

# Connect to SQLite database
conn = sqlite3.connect("data/weather.db")

# Save DataFrame into a table called weather
df.to_sql(
    "weather",
    conn,
    if_exists="replace",
    index=False
)

# Verify data was saved
cursor = conn.cursor()

cursor.execute("SELECT COUNT(*) FROM weather")
row_count = cursor.fetchone()[0]

print("Rows in weather table:", row_count)

conn.close()

print("\nWeather data saved to SQLite successfully.")