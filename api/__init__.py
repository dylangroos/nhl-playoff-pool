import requests
from .urls import SCHEDULE, BOXSCORE


def get_box_scores():
    # return list of box scores from todays games
    return [get_json(BOXSCORE % id) for id in get_game_ids()]

# get game ids
def get_game_ids():
    sched = get_todays_schedule()
    return [game["gamePk"] for date in sched["dates"] for game in date["games"]]

# get schedule
def get_todays_schedule():
    return get_json(SCHEDULE)

# get json from nhl api
def get_json(url):
    response = requests.get(url)
    return response.json()