import datetime
from api import get_live

def ot_goal(box_score, line_score, player_id):
    # check the end time and get the timestamped -30 live feed
    try:
        if line_score["periods"][-1]['periodType'] == 'OVERTIME':
            game_id = line_score['game_id']
            delta = datetime.timedelta(minutes=2)
            check = (datetime.datetime.now() - delta).strftime("%Y%m%D_%H%M%S")
            live = get_live(game_id, check)
            play_i = int(live['liveData']['plays']['scoringPlays'])
            play =  live['liveData']['plays']['allPlays'][play_i]
            scorer_id = play["players"][0]['player']['id']
    except Exception as e:
        print(e)
    return int(scorer_id == player_id)

def fight(box_score, player_id):
    return 0

def win(box_score, player_id):
    try:
        game_id = box_score['game_id']
        delta = datetime.timedelta(minutes=2)
        check = (datetime.datetime.now() - delta).strftime("%Y%m%D_%H%M%S")
        live = get_live(game_id, check)
    
    except Exception as e:
        print(e)
        
    return int(live['liveData']['decisions']['winner']['id'] == player_id)

def loss(box_score, player_id):
    try:
        game_id = box_score['game_id']
        delta = datetime.timedelta(minutes=2)
        check = (datetime.datetime.now() - delta).strftime("%Y%m%D_%H%M%S")
        live = get_live(game_id, check)
    except Exception as e:
        print(e)
    return int(live['liveData']['decisions']['loser']['id'] == player_id)