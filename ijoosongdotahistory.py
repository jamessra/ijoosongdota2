import dota2api
import time
import pandas as pd

#ijoosong's Steam ID
steamID = 17854758
steamID3 = 35709316
steamID64 = 76561197995975044

#Valve API Key
api = dota2api.Initialise("Enter Valve Key")

#ijoosong's Match History
match_history = api.get_match_history(account_id=steamID64)

#List of Match ID, Match Details, Hero Picks, Deaths, Match Results
match_ids = []
teams = []
hero_picks = []
deaths = []
match_results = []
game_time = []

for match_number in match_history['matches']:
	match_ids.append(match_number['match_id'])
	
	match_details = api.get_match_details(match_id=match_number['match_id'])
	
	start_time = match_details['start_time']
	pre_game_duration = match_details['pre_game_duration']
	duration = match_details['duration']
	total_epoch_time = start_time + pre_game_duration + duration
	game_time.append(time.strftime('%m-%d %H:%M:%S', time.localtime(total_epoch_time)))
	
	for player in match_details['players']:
		if player['account_id'] == steamID3:
			if player['player_slot'] < 100:
				teams.append('Radiant')
			else:
				teams.append('Dire')
			hero_picks.append(player['hero_name'])
			deaths.append(player['deaths'])
	
	if match_details['radiant_win'] == 1:
		match_results.append('Radiant')
	else:
		match_results.append('Dire')

#Create DataFrame and CSV file		
df = pd.DataFrame(list(zip(game_time, match_ids, teams, hero_picks, deaths, match_results)), columns=['Game Time', 'Match ID', 'Team', 'Hero Picked', 'Deaths', 'Match Results'])
df.to_csv('ijoosong.csv', index=False)

print 'done'
