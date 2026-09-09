import sqlite3
import pandas as pd

# Load the cleaned CSV
df = pd.read_csv("data/weather_data.csv")

print("First 5 rows:")
print(df.head())

print("\nNumber of rows:", len(df))

conn = None

try:
    # Connect to the database
    conn = sqlite3.connect("data/weather.db")

    # Save the cleaned data into the weather table
    df.to_sql(
        "weather",
        conn,
        if_exists="replace",
        index=False
    )

    # Check that the data was saved
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM weather")
    row_count = cursor.fetchone()[0]

    print("\nRows in weather table:", row_count)

    # Show a few rows from the database
    cursor.execute("SELECT * FROM weather LIMIT 5")
    rows = cursor.fetchall()

    print("\nFirst 5 rows from the database:")

    for row in rows:
        print(row)

    print("\nWeather data saved to SQLite successfully.")

except sqlite3.Error as e:
    print("Database error:", e)

finally:
    if conn:
        conn.close()