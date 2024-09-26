# SteamToLinux

This project is only for personal purpose and shouldn't be used in any illegal way.

## GameCompat_Platforms.py
This python file will use an Steam API and an ID steam account, that you'll need to provide (both of them). It will get all the games you own in your Steam library

## WebScrapingProtonDB.py
This program will:
- Check the id of all the games you own in your steam library
- Check if the id is in the .csv (random game sorted asc)
  - If we found an id of a game inside the .csv, we skip the game
- Loop over all the game ID that is not inside the .csv
  - Open a single window (Firefox) and goes to the link https://www.protondb.com/app/{app_id}  
  - Wait and scrap the specific div that holds the rating level in the page of the game id and the full name of the game
- Write inside the csv the following information [date_of_check, game_id, game_name, level_rating]
- And finally close the Firefow window manager.
