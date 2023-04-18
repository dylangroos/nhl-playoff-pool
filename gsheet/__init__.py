from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from .constants import SCOPE, SHEET_ID, FORWARD_RANGES, DEFENSE_RANGES, GOALIE_RANGES
import time

def set_update(updates):
    for i, range in enumerate(updates):
        print(f'UPDATING States at {range}')
        print(updates[range])
        get_sheet().values().update(spreadsheetId=SHEET_ID, 
                                    range=range, valueInputOption='RAW', 
                                    body={'values': [updates[range]]}).execute()
        if i % 20 == 0:
            time.sleep(10)

# TODO: the path of the token has to be reac
def get_sheet():
    creds = service_account.Credentials.from_service_account_file('gsheet/token.json', scopes=SCOPE)
    return build('sheets', 'v4', credentials=creds).spreadsheets()


def get(RANGE):
    result = get_sheet().values().get(spreadsheetId=SHEET_ID, range=RANGE).execute()
    return result.get('values', [])


def get_players():
    return  [name[0].split('(')[0].split(' ')[1].strip() for name in get(FORWARD_RANGES['names'])] + \
    [name[0].split('(')[0].split(' ')[1].strip() for name in get(DEFENSE_RANGES['names'])] + \
    [name[0].split('(')[0].split(' ')[1].strip() for name in get(GOALIE_RANGES['names'])]


def range_mappings():
    out = {}
    [out.update({
        name[0].split('(')[0].strip() : f'Home Page Test!B{i+14}:E{i+14}'
    }) for i, name in enumerate(get(FORWARD_RANGES["names"]))]
    [out.update({
        name[0].split('(')[0].strip() : f'Home Page Test!I{i+14}:L{i+14}'
    }) for i, name in enumerate(get(DEFENSE_RANGES["names"]))]
    [out.update({
        name[0].split('(')[0].strip() : f'Home Page Test!P{i+14}:T{i+14}'
    }) for i, name in enumerate(get(GOALIE_RANGES["names"]))]
    return out

def get_nightly_baseline():
    print(get(FORWARD_RANGES["all"]))
    return {
                "forwards":[{
                            "name": entry[0].split('(')[0].split(' ')[1].strip(),
                            "goals": entry[1],
                            "assists": entry[2],
                            "plus_minus": entry[3],
                            "ot_goal": entry[4],
                            "fights": entry[5]
                        }
                        for entry in get(FORWARD_RANGES["all"])],
                "defense":[{
                            "name": entry[0].split('(')[0].split(' ')[1].strip(),
                            "goals": entry[1],
                            "assists": entry[2],
                            "plus_minus": entry[3],
                            "ot_goal": entry[4],
                            "fights": entry[5]
                        }
                        for entry in get(DEFENSE_RANGES["all"])],
                "goalies":[{
                            "name":entry[0].split('(')[0].split(' ')[1].strip(),
                            "wins": entry[1],
                            "losses": entry[2],
                            "shutouts": entry[3],
                            "saves": entry[4],
                            "goals_against": entry[5]
                        }
                        for entry in get(GOALIE_RANGES["all"])],
                }