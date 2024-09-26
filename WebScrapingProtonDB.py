from GameCompat_Platforms import games_owned_id
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv

# Set up the Chrome driver
service = Service()
options = webdriver.FirefoxOptions()
options.add_argument("--headless")  # Ensure the browser runs in headless mode
options.add_argument("--no-sandbox")  # Needed for some environments
options.add_argument("--disable-dev-shm-usage")  # Overcomes limited resource problems

driver = webdriver.Firefox(service=service, options=options)

# Get the APP_ID(s) from command-line arguments
app_ids = games_owned_id

headers = ["Game Name", "Rating"]

# Open the CSV file in write mode
with open("rating.csv", "w", newline="", encoding="utf-8") as file:
    writer = csv.DictWriter(file, fieldnames=headers)
    writer.writeheader()  # Write headers once at the beginning

for app_id in app_ids:
    try:
        driver.get(f"https://www.protondb.com/app/{app_id}")
        # time.sleep(1)

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

            ratings.append({"Game Name": game_name_text, "Rating": span_text})
            print(game_name_text, ": ", span_text)

        with open("rating.csv", "a", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=headers)
            writer.writerows(ratings)

    except Exception as e:
        print(f"Error occurred for App ID {app_id}: {str(e)}")
        continue

driver.quit()
