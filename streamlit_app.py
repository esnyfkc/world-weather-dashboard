import sqlite3
import pandas as pd
import plotly.express as px
import streamlit as st

# Page title
st.title("World Weather Dashboard")
st.write("Explore current weather data from cities around the world.")

# Connect to the database
connection = sqlite3.connect("data/weather.db")

# Load weather data
df = pd.read_sql_query("SELECT * FROM weather", connection)

connection.close()

# Temperature filter
min_temp = int(df["Temperature_F"].min())
max_temp = int(df["Temperature_F"].max())

temperature_range = st.slider(
    "Select temperature range (°F)",
    min_temp,
    max_temp,
    (min_temp, max_temp)
)

# Filter the data
filtered_df = df[
    (df["Temperature_F"] >= temperature_range[0]) &
    (df["Temperature_F"] <= temperature_range[1])
]

# Stop if there is no data in the selected range
if filtered_df.empty:
    st.warning("No weather data found for this temperature range.")
    st.stop()

# Weather summary
st.subheader("Weather Summary")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Cities", len(filtered_df))

with col2:
    st.metric(
        "Average Temperature",
        f"{filtered_df['Temperature_F'].mean():.1f} °F"
    )

with col3:
    st.metric(
        "Highest Temperature",
        f"{filtered_df['Temperature_F'].max()} °F"
    )

# Chart 1: Top 10 hottest cities
st.subheader("Top 10 Hottest Cities")

hottest_cities = filtered_df.nlargest(10, "Temperature_F")

fig1 = px.bar(
    hottest_cities,
    x="City",
    y="Temperature_F",
    title="Top 10 Hottest Cities",
    labels={"Temperature_F": "Temperature (°F)"}
)

st.plotly_chart(fig1, use_container_width=True)

# Chart 2: Temperature distribution
st.subheader("Temperature Distribution")

fig2 = px.histogram(
    filtered_df,
    x="Temperature_F",
    title="Temperature Distribution",
    labels={"Temperature_F": "Temperature (°F)"}
)

# Use 5-degree temperature ranges
fig2.update_traces(
    xbins=dict(
        start=filtered_df["Temperature_F"].min(),
        end=filtered_df["Temperature_F"].max() + 5,
        size=5
    )
)

fig2.update_layout(
    xaxis_title="Temperature (°F)",
    yaxis_title="Number of Cities",
    bargap=0.1
)

st.plotly_chart(fig2, use_container_width=True)

# Chart 3: Most common weather conditions
st.subheader("Most Common Weather Conditions")

condition_counts = (
    filtered_df["Condition"]
    .value_counts()
    .head(10)
    .reset_index()
)

condition_counts.columns = ["Condition", "Count"]

fig3 = px.bar(
    condition_counts,
    x="Count",
    y="Condition",
    orientation="h",
    title="Top 10 Weather Conditions"
)

fig3.update_layout(
    yaxis={"categoryorder": "total ascending"}
)

st.plotly_chart(fig3, use_container_width=True)

# Show the filtered weather data
st.subheader("Weather Data")

display_df = filtered_df[
    ["City", "Local Time", "Condition", "Temperature"]
]

st.dataframe(display_df, use_container_width=True)