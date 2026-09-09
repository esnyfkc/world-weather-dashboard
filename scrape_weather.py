from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

import pandas as pd


options = webdriver.ChromeOptions()
options.page_load_strategy = "eager"

driver = webdriver.Chrome(
    service=ChromeService(ChromeDriverManager().install()),
    options=options
)

try:
    driver.get("https://www.timeanddate.com/weather/")

    rows = driver.find_elements(By.CSS_SELECTOR, "table tbody tr")

    print("Number of rows:", len(rows))

    results = []

    for row in rows:
        cells = row.find_elements(By.CSS_SELECTOR, "td")

        for i in range(0, len(cells), 4):
            city = cells[i].text

            if not city.strip():
                continue

            local_time = cells[i + 1].text

            try:
                weather_image = cells[i + 2].find_element(
                    By.CSS_SELECTOR,
                    "img"
                )
                condition = weather_image.get_attribute("alt")
            except Exception:
                condition = "Unknown"

            temperature = cells[i + 3].text

            weather_data = {
                "City": city,
                "Local Time": local_time,
                "Condition": condition,
                "Temperature": temperature
            }

            results.append(weather_data)

    print("Number of cities:", len(results))

    # Before cleaning
    df = pd.DataFrame(results)

    print("\nBefore cleaning:")
    print(df.head())

    print("\nMissing values:")
    print(df.isnull().sum())

    print("\nDuplicate rows:")
    print(df.duplicated().sum())


    # Clean the data

    # Remove * from city names
    df["City"] = (
        df["City"]
        .str.replace("*", "", regex=False)
        .str.strip()
    )

    # Create a numeric temperature column
    df["Temperature_F"] = (
        df["Temperature"]
        .str.replace("°F", "", regex=False)
        .str.strip()
    )

    df["Temperature_F"] = pd.to_numeric(
        df["Temperature_F"],
        errors="coerce"
    )

    # Remove rows with invalid temperatures
    df = df.dropna(subset=["Temperature_F"])

    # Remove duplicate rows
    df = df.drop_duplicates()


    # After cleaning

    print("\nAfter cleaning:")
    print(df.head())

    print("\nMissing values after cleaning:")
    print(df.isnull().sum())

    print("\nShape after cleaning:")
    print(df.shape)


    # Save to CSV

    df.to_csv(
        "data/weather_data.csv",
        index=False
    )

    print("\nweather_data.csv created successfully.")


except Exception as e:
    print("An error occurred:", type(e).__name__, e)

finally:
    driver.quit()