import requests
import proton_db as proton

protonDB =  proton.protonDB()

USER_API_KEY = '' # ask steam for an API (it's free)
USER_STEAM_ID = '' # you can find your steam id on the Steam app by clicking "detail account" on the top right and it will be just under your username account
# Get the complete list of Steam apps
api = 'https://api.steampowered.com/ISteamApps/GetAppList/v2/'
res = requests.get(url=api)
dict_games = res.json()['applist']['apps']
data_clean = {game['appid']: game['name'] for game in dict_games}

def get_name(appid):
    # Check if the appid exists in the app list
    if appid in data_clean:
        return data_clean[appid]
    else:
        return f"Unknown AppID: {appid}"

# Get user's owned games
user_url = f'http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key={USER_API_KEY}&steamid={USER_STEAM_ID}&format=json'
user_game_data = requests.get(url=user_url).json()

games_owned_id = []
games_owned_names = []
UnknownAppId_list = []
for result in user_game_data['response']['games']:
    appid = result['appid']
    games_owned_id.append(appid)
    games_owned_names.append(get_name(appid))  # Check if appid exists before accessing

# Iterate through the names and IDs simultaneously using zip
for i, (game_name, appid) in enumerate(zip(games_owned_names, games_owned_id)):
    if 'Unknown AppID' in game_name:
        print("removing game id:", appid)
        UnknownAppId_list.append(game_name)
        # Remove both the game name and ID
        games_owned_names[i] = None  # Mark for removal
        games_owned_id[i] = None     # Mark for removal

# Remove marked items from both lists
games_owned_names = [game for game in games_owned_names if game is not None]
games_owned_id = [appid for appid in games_owned_id if appid is not None]

print('UnknownAppId_list:', UnknownAppId_list)
print('Cleaned Game List:', games_owned_names)
print('Cleaned Game ID List:', games_owned_id)
