import requests
import json
import time

# heros metadata
heroes_metadata_url = "https://api.opendota.com/api/heroes"

# Get the list of heroes
heroes_metadata_response = requests.get(heroes_metadata_url)
# if heroes_metadata_response.status_code != 200:
    # print('----------FAILED heroes_metadata')
heroes_metadata_list = heroes_metadata_response.json()

# Loop through the list of heroes
counter = 1
for hero in heroes_metadata_list:
    id = hero['id']
    # print(hero['localized_name'])
    hero.pop('legs', None)
    hero_matchups_url = "https://api.opendota.com/api/heroes/"+str(id)+"/matchups"
    hero_matchups_response = requests.get(hero_matchups_url)
    counter = counter + 1
    if hero_matchups_response.status_code != 200:
        # print('----------FAILED hero_matchups id='+str(id)+' counter='+str(counter))
        break
    heroes_matchups_list = hero_matchups_response.json()
    games_played = 0
    games_won = 0
    # Loop through the matchups of hero
    for matchup_hero in heroes_matchups_list:
        games_played = games_played + matchup_hero['games_played']
        games_won = games_won + matchup_hero['wins']
        winrate = matchup_hero['wins']/matchup_hero['games_played']
        matchup_hero[matchup_hero['hero_id']] = round(winrate, 2)
        matchup_hero.pop('hero_id', None)
        matchup_hero.pop('games_played', None)
        matchup_hero.pop('wins', None)
    hero['games_played'] = games_played
    overall_winrate = 0
    if games_played != 0:
        overall_winrate = games_won/games_played
    hero['overall_winrate'] = round(overall_winrate, 2)
    hero['matchups'] = heroes_matchups_list
    if counter % 55 == 0:
        # print('----------Going to sleep')
        time.sleep(90)

# Write the processed data to a JSON file
with open("hero_data.json", "w") as outfile:
    json.dump(heroes_metadata_list, outfile)
