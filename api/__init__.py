import requests
from .urls import SCHEDULE, BOXSCORE, LINESCORE, LIVE

def get_live(game_id, time):
    return get_json(LIVE % (game_id, time))


def get_scores():
    # return list of box scores from todays games
    return {
        'box': [get_json_game_id(BOXSCORE % id) for id in get_game_ids()],
        'line':  [get_json_game_id(LINESCORE % id) for id in get_game_ids()]
    }

# get game ids
def get_game_ids():
    sched = get_todays_schedule()
    return [game["gamePk"] for date in sched["dates"] for game in date["games"]]

# get schedule
def get_todays_schedule():
    return get_json(SCHEDULE)


# get and append id (lazy i know, but need this for unplanned functionality)
def get_json_game_id(url):
    response = requests.get(url)
    out = response.json()
    out["game_id"] = url.split('/')[-2]
    return out


# get json from nhl api
def get_json(url):
    response = requests.get(url)
    return response.json()