# import necessary libraries
from GameCompat_Platforms import games_owned_id
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv
import time

# set up the Firefox driver
service = Service()
options = webdriver.FirefoxOptions()
options.add_argument("--headless")
driver = webdriver.Firefox(service=service, options=options)

APP_ID = games_owned_id
print("APP_ID: ", APP_ID)

# specify the CSV headers
headers = ["Game Name", "Rating"]

# open the CSV file in append mode and keep track of whether headers were written
with open("rating.csv", "w", newline="", encoding="utf-8") as file:
    writer = csv.DictWriter(file, fieldnames=headers)
    writer.writeheader()  # Write headers once at the beginning

# loop through the game APP_IDs
for app_id in APP_ID:
    try:
        # navigate to the target webpage
        driver.get(f"https://www.protondb.com/app/{app_id}")

        # wait until the specific div is generated on the page (adjust selector if needed)
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, '.MedalSummary__ExpandingSpan-sc-1fjwtnh-1')
            )
        )

        # extract product details by finding elements that contain the necessary span
        ratings = []
        spans = driver.find_elements(By.CSS_SELECTOR, "span.MedalSummary__ExpandingSpan-sc-1fjwtnh-1")
        game_names = driver.find_elements(By.CSS_SELECTOR, "span.GameInfo__Title-sc-19o71ac-2.iCanPw")

        for game_name, span in zip(game_names, spans):  # iterate both lists at once
            game_name_text = game_name.text
            span_text = span.text

            # check if span_text is empty or None, assign "NOT ENOUGH REVIEW" if so
            if not span_text:  # this checks for both None and empty string
                span_text = "NOT ENOUGH REVIEW"

            print(f'{game_name_text}: {span_text}')

            # store the game name and rating as a dictionary (key-value pairs)
            ratings.append({"Game Name": game_name_text, "Rating": span_text})

        # open the CSV file in append mode and write the data
        with open("rating.csv", "a", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=headers)
            writer.writerows(ratings)

        # print the parsed data for each app_id
        print(f"Ratings for App ID {app_id}:")
        print(ratings)

    except Exception as e:
        # print the error message and continue to the next app_id
        print(f"Error occurred for App ID {app_id}: {str(e)}. Skipping this game.")
        continue  # continue with the next app_id

# close the browser
driver.quit()
