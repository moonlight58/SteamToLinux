from GameCompat_Platforms import games_owned_id
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv
import os
from datetime import datetime

# Set up the Firefox driver
service = Service()
options = webdriver.FirefoxOptions()
options.add_argument("--headless")  # Ensure the browser runs in headless mode
options.add_argument("--no-sandbox")  # Needed for some environments
options.add_argument("--disable-dev-shm-usage")  # Overcomes limited resource problems

driver = webdriver.Firefox(service=service, options=options)

# Get the APP_ID(s) from GameCompat_Platforms.py
app_ids = games_owned_id

# Define the file name for the CSV
csv_file = "rating.csv"
headers = ["Date of Check", "Game ID", "Game Name", "Rating"]

# Load existing data from the CSV if it exists
existing_data = {}
if os.path.exists(csv_file):
    with open(csv_file, "r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            existing_data[row["Game ID"]] = row  # Store existing data by Game ID

# Open the CSV file in append mode (add new data only if not already present)
with open(csv_file, "a", newline="", encoding="utf-8") as file:
    writer = csv.DictWriter(file, fieldnames=headers)

    # Write headers if the file is empty
    if os.stat(csv_file).st_size == 0:
        writer.writeheader()

    # Iterate over each game ID
    for app_id in app_ids:
        # Check if the game is already in the CSV by Game ID
        if str(app_id) in existing_data:
            print(f"Game ID {app_id} already exists in CSV. Skipping...")
            continue

        try:
            driver.get(f"https://www.protondb.com/app/{app_id}")

            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '.MedalSummary__ExpandingSpan-sc-1fjwtnh-1'))
            )

            ratings = []
            spans = driver.find_elements(By.CSS_SELECTOR, "span.MedalSummary__ExpandingSpan-sc-1fjwtnh-1")
            game_names = driver.find_elements(By.CSS_SELECTOR, "span.GameInfo__Title-sc-19o71ac-2.iCanPw")

            if not app_id or not game_names:
                raise Exception(f"Unable to locate elements for App ID {app_id}")

            for game_name, span in zip(game_names, spans):
                game_name_text = game_name.text
                span_text = span.text if span.text else "NOT ENOUGH REVIEW"

                # Record the date of check, app ID, game name, and rating
                ratings.append({
                    "Date of Check": datetime.now().strftime("%Y-%m-%d"),
                    "Game ID": app_id,
                    "Game Name": game_name_text,
                    "Rating": span_text
                })

                print(f"{game_name_text} ({app_id}): {span_text}")

            # Append the new data to the CSV
            writer.writerows(ratings)

        except Exception as e:
            print(f"Error occurred for App ID {app_id}: {str(e)}")
            continue

# Quit the driver after scraping
driver.quit()
