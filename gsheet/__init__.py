from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from .constants import SCOPE, SHEET_ID, FORWARD_RANGES, DEFENSE_RANGES, GOALIE_RANGES, STARTING_ROW, SHEET_NAME
import time

def set_update(updates):
    for i, range in enumerate(updates):
        print(f'UPDATING States at {range}')
        print(updates[range])
        get_sheet().values().update(spreadsheetId=SHEET_ID, 
                                    range=range, valueInputOption='RAW', 
                                    body={'values': [updates[range]]}).execute()
        if i % 20 == 0 and i != 0:
            print('sleeping...')
            time.sleep(60)

# TODO: the path of the token has to be reac
def get_sheet():
    creds = service_account.Credentials.from_service_account_file('gsheet/token.json', scopes=SCOPE)
    return build('sheets', 'v4', credentials=creds).spreadsheets()


def get(RANGE):
    result = get_sheet().values().get(spreadsheetId=SHEET_ID, range=RANGE).execute()
    return result.get('values', [])


def get_players():
    return  [name[0].split('(')[0].strip() for name in get(FORWARD_RANGES['names'])] + \
    [name[0].split('(')[0].strip() for name in get(DEFENSE_RANGES['names'])] + \
    [name[0].split('(')[0].strip() for name in get(GOALIE_RANGES['names'])]


def range_mappings():
    out = {}
    out['forwards'] = {name[0].split('(')[0].strip().split(' ')[-1] : f'{SHEET_NAME}!B{i+ STARTING_ROW}:F{i+ STARTING_ROW}'
                       for i, name in enumerate(get(FORWARD_RANGES["names"]))}
    out['defense'] = {name[0].split('(')[0].strip().split(' ')[-1] : f'{SHEET_NAME}!I{i+ STARTING_ROW}:L{i+ STARTING_ROW}' 
                      for i, name in enumerate(get(DEFENSE_RANGES["names"]))}
    out['goalies'] = {name[0].split('(')[0].strip().split(' ')[-1] : f'{SHEET_NAME}!P{i+ STARTING_ROW}:T{i+ STARTING_ROW}' 
                      for i, name in enumerate(get(GOALIE_RANGES["names"]))}
    [out['defense'].update({
        name[0].split('(')[0].strip().split(' ')[-1] : f'{SHEET_NAME}!I{i+ STARTING_ROW}:L{i+ STARTING_ROW}'
    }) for i, name in enumerate(get(DEFENSE_RANGES["names"]))]
    [out['goalies'].update({
        name[0].split('(')[0].strip().split(' ')[-1] : f'{SHEET_NAME}!P{i+ STARTING_ROW}:T{i+ STARTING_ROW}'
    }) for i, name in enumerate(get(GOALIE_RANGES["names"]))]
    return out

def get_nightly_baseline():
    return {
                "forwards":{ entry[0].split('(')[0].strip().split(' ')[-1]:
                           {
                               "goals": entry[1],
                                "assists": entry[2],
                                "plus_minus": entry[3],
                                "ot_goal": entry[4],
                                "fights": entry[5]
                            }
                        
                        for entry in get(FORWARD_RANGES["all"])},
                "defense":{ entry[0].split('(')[0].strip().split(' ')[-1]:
                           {
                               "goals": entry[1],
                                "assists": entry[2],
                                "plus_minus": entry[3],
                                "ot_goal": entry[4],
                                "fights": entry[5]
                            }
                        
                        for entry in get(DEFENSE_RANGES["all"])},
                "goalies":{entry[0].split('(')[0].strip().split(' ')[-1]: 
                            {
                                "wins": entry[1],
                                "losses": entry[2],
                                "shutouts": entry[3],
                                "saves": entry[4],
                                "goals_against": entry[5]
                            }
                        for entry in get(GOALIE_RANGES["all"])},
                }


def get_sheet_state():
    return {
                "forwards":[{
                            "name": entry[0].split('(')[0].strip(),
                            "goals": entry[1],
                            "assists": entry[2],
                            "plus_minus": entry[3],
                            "ot_goal": entry[4],
                            "fights": entry[5]
                        }
                        for entry in get(FORWARD_RANGES["all"])],
                "defense":[{
                            "name": entry[0].split('(')[0].strip(),
                            "goals": entry[1],
                            "assists": entry[2],
                            "plus_minus": entry[3],
                            "ot_goal": entry[4],
                            "fights": entry[5]
                        }
                        for entry in get(DEFENSE_RANGES["all"])],
                "goalies":[{
                            "name":entry[0].split('(')[0].strip(),
                            "wins": entry[1],
                            "losses": entry[2],
                            "shutouts": entry[3],
                            "saves": entry[4],
                            "goals_against": entry[5]
                        }
                        for entry in get(GOALIE_RANGES["all"])],
                }