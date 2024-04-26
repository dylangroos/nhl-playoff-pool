from gsheet import get_players, range_mappings, get_nightly_baseline, get_sheet_state, set_update
from api import  get_scores

from pprint import pprint

import json

from datetime import datetime
import os
import pickle
import time
from unidecode import unidecode

def correct_misspellings():
    pass

def run(baseline):
    current_state = get_nightly_baseline()
    boxscores = get_scores()
    range_mapping = range_mappings()
    baseline=baseline


    for game in boxscores['box']:
        # is the game started?
        if game['gameState'] == 'LIVE' or game['gameState'] == 'CRIT':
            print(f"{game['homeTeam']['abbrev']} v {game['awayTeam']['abbrev']} is {game['gameState']}")
            print(f"{game['gameState']}")
            # get live data
            updates = {}
            players_live_stats = {
                    "forwards": {},
                    "defense": {},
                    "goalies": {}
                }
            by_team_player_stats = game['playerByGameStats']
            # home v away
            for team in by_team_player_stats:
                # forwards v defense v goalies
                for position_type in by_team_player_stats[team]:
                    for player in by_team_player_stats[team][position_type]:

                        name = unidecode(player['name']['default'].split(' ')[-1])
                        if position_type == 'goalies':
                            # need to set the postgame stats
                            players_live_stats[position_type][name] = {
                                'goals_against': player['goalsAgainst'],
                                'saves': int(player['saveShotsAgainst'].split('/')[0]),
                            }
                        else:
                            players_live_stats[position_type][name] = {
                                'goals': player['goals'],
                                'assists': player['assists'],
                                'plus_minus': player['plusMinus'],
                            }
            
            # do the updates
            for player_type in baseline:
                positional_baseline = baseline[player_type]
                for player in players_live_stats[player_type]:
                    if player in positional_baseline:
                        if player_type == 'goalies':
                            sub_baseline = {
                                    "goals_against": int(current_state[player_type][player]['goals_against']) - int(positional_baseline[player]['goals_against']),
                                    "saves": int(current_state[player_type][player]['saves']) - int(positional_baseline[player]['saves']),
                                }
                        else:
                            sub_baseline = {
                                "goals": int(current_state[player_type][player]['goals']) - int(positional_baseline[player]['goals']),
                                "assists": int(current_state[player_type][player]['assists']) - int(positional_baseline[player]['assists']),
                                "plus_minus": int(current_state[player_type][player]['plus_minus']) - int(positional_baseline[player]['plus_minus']),
                            }
                        
                        # do we need to update
                        if (players_live_stats[player_type][player] == sub_baseline) or all(int(value) == 0 for value in players_live_stats[player_type][player].values()):
                            pass
                        else:
                            print('updating....')
                            print(player)
                            print(players_live_stats[player_type][player])
                            print(sub_baseline)
                            print('---------------------------------------------')
                            if player_type == 'goalies':
                                update = [
                                    int(positional_baseline[player]['wins']),
                                    int(positional_baseline[player]['losses']),
                                    int(positional_baseline[player]['shutouts']), 
                                    int(positional_baseline[player]['saves']) + int(players_live_stats[player_type][player]['saves']),
                                    int(positional_baseline[player]['goals_against']) + int(players_live_stats[player_type][player]['goals_against']),
                                ]
                                updates[range_mapping[player_type][player]] = update
                            else:
                                update = [
                                    int(positional_baseline[player]['goals']) + int(players_live_stats[player_type][player]['goals']),
                                    int(positional_baseline[player]['assists']) + int(players_live_stats[player_type][player]['assists']),
                                    int(positional_baseline[player]['plus_minus']) + int(players_live_stats[player_type][player]['plus_minus']),
                                    int(positional_baseline[player]['ot_goal']),
                                ]
                                updates[range_mapping[player_type][player]] = update
            set_update(updates)
        
        elif game['gameState'] == 'FINAL' or game['gameState'] == 'OFF':
            # get live data
            print(f"{game['homeTeam']['abbrev']} v {game['awayTeam']['abbrev']} is {game['gameState']}")
            updates = {}
            players_live_stats = {
                "forwards": {},
                "defense": {},
                "goalies": {}
            }
            by_team_player_stats = game['playerByGameStats']
            # home v away
            for team in by_team_player_stats:
                # forwards v defense v goalies
                for position_type in by_team_player_stats[team]:
                    for player in by_team_player_stats[team][position_type]:
                        name = player['name']['default'].split(' ')[-1]
                        if position_type == 'goalies':
                            # need to set the postgame stats
                            if 'decision' in player:
                                players_live_stats[position_type][name] = {
                                    'goals_against': player['goalsAgainst'],
                                    'saves': int(player['saveShotsAgainst'].split('/')[0]),
                                    'wins': 1 if player['decision'] == 'W' else 0,
                                    'losses': 0 if player['decision'] == 'W' else 1,
                                    'shutouts': 1 if player['goalsAgainst'] == '0' else 0
                                }
                            else:
                                players_live_stats[position_type][name] = {
                                    'goals_against': player['goalsAgainst'],
                                    'saves': int(player['saveShotsAgainst'].split('/')[0]),
                                    'wins': 0,
                                    'losses': 0,
                                    'shutouts': 0
                                }
                        else:
                            # skaters
                            players_live_stats[position_type][name] = {
                                'goals': player['goals'],
                                'assists': player['assists'],
                                'plus_minus': player['plusMinus'],
                            }
            
            # do comparison here
            for player_type in baseline:
                positional_baseline = baseline[player_type]
                for player in players_live_stats[player_type]:
                    if player in positional_baseline:
                        if player_type == 'goalies':
                            sub_baseline = {
                                    "wins": int(current_state[player_type][player]['wins']) - int(positional_baseline[player]['wins']),
                                    "losses": int(current_state[player_type][player]['losses']) - int(positional_baseline[player]['losses']),
                                    "goals_against": int(current_state[player_type][player]['goals_against']) - int(positional_baseline[player]['goals_against']),
                                    "saves": int(current_state[player_type][player]['saves']) - int(positional_baseline[player]['saves']),
                                    "shutouts": int(current_state[player_type][player]['shutouts']) - int(positional_baseline[player]['shutouts']),
                                }
                        else:
                            sub_baseline = {
                                "goals": int(current_state[player_type][player]['goals']) - int(positional_baseline[player]['goals']),
                                "assists": int(current_state[player_type][player]['assists']) - int(positional_baseline[player]['assists']),
                                "plus_minus": int(current_state[player_type][player]['plus_minus']) - int(positional_baseline[player]['plus_minus']),
                            }
                        
                        # do we need to update
                        if (players_live_stats[player_type][player] == sub_baseline) or all(int(value) == 0 for value in players_live_stats[player_type][player].values()):
                            pass
                        else:
                            print('updating....')
                            print(player)
                            print(players_live_stats[player_type][player])
                            print(sub_baseline)
                            print('---------------------------------------------')
                            if player_type == 'goalies':
                                update = [
                                    int(positional_baseline[player]['wins']) + int(players_live_stats[player_type][player]['wins']),
                                    int(positional_baseline[player]['losses']) + int(players_live_stats[player_type][player]['losses']),
                                    int(positional_baseline[player]['shutouts']) + int(players_live_stats[player_type][player]['shutouts']), 
                                    int(positional_baseline[player]['saves']) + int(players_live_stats[player_type][player]['saves']),
                                    int(positional_baseline[player]['goals_against']) + int(players_live_stats[player_type][player]['goals_against']),
                                ]
                                updates[range_mapping[player_type][player]] = update
                            else:
                                update = [
                                    int(positional_baseline[player]['goals']) + int(players_live_stats[player_type][player]['goals']),
                                    int(positional_baseline[player]['assists']) + int(players_live_stats[player_type][player]['assists']),
                                    int(positional_baseline[player]['plus_minus']) + int(players_live_stats[player_type][player]['plus_minus']),
                                    int(positional_baseline[player]['ot_goal']),
                                ]
                                updates[range_mapping[player_type][player]] = update
                set_update(updates)


if __name__=="__main__":
    baseline_file = f'/home/groos1/nhl-playoff-pool/{datetime.today().strftime("%Y-%m-%d")}/baseline.pkl'

    if os.path.exists(baseline_file):
        print(f'baseline detected at {baseline_file}, loading...')
        with open(baseline_file, 'rb') as f:
            baseline = pickle.load(f)
    else:
        print(f'no baseline detectred at {baseline_file}, generating...')
        baseline = get_nightly_baseline()
        os.makedirs(os.path.dirname(baseline_file), exist_ok=True)
        with open(baseline_file, 'wb') as f:
            pickle.dump(baseline, f)

    while True:
        try:
            run(baseline)
        except Exception as e:
            print(e)
        print('sleeping for 1 min...')
        time.sleep(60)