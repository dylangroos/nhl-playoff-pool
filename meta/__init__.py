from api import get_scores
from gsheet import get_players
from .stats import win, loss, fight, ot_goal

def generate_updates(baseline, active):
    # update is a dictionary with row_index then the values -- this is taken in by the gsheet stuff
    updates = {}
    for player_type in baseline:
        for i, player in enumerate(baseline[player_type]):
        
            if player['name'] in active:
                if player_type in ['forwards', 'defense']:
                    update = [
                        active[player['name']]['goals'] + int(player['goals']),
                        active[player['name']]['assists'] + int(player['assists']),
                        int(active[player['name']]['plus_minus']) + int(player['plus_minus']),
                        active[player['name']]['ot_goal'] + int(player['ot_goal']),
                        active[player['name']]['fights'] + int(player['fights'])
                    ]
                    base = [
                        int(player['goals']),
                        int(player['assists']),
                        int(player['plus_minus']),
                        int(player['ot_goal']),
                        int(player['fights'])
                    ]
                elif player_type == 'goalies':
                    update = [
                        active[player['name']]['wins'] + int(player['wins']),
                        active[player['name']]['losses'] + int(player['losses']),
                        active[player['name']]['shutouts'] + int(player['shutouts']),
                        active[player['name']]['saves'] + int(player['saves']),
                        active[player['name']]['goals_against'] + int(player['goals_against'])
                    ]
                    base = [
                        int(player['wins']),
                        int(player['losses']),
                        int(player['shutouts']),
                        int(player['saves']),
                        int(player['goals_against'])
                    ]
                if any([a_i - b_i for a_i, b_i in zip(update, base)]):

                    if player_type == 'forwards':
                        print(f'        G|A|+-|OT|F')
                        updates[f'Home Page Test!B{i+14}:F{i+14}'] = update
                    if player_type == 'defense':
                        print(f'       G|A|+-|OT|F')
                        updates[f'Home Page Test!I{i+14}:M{i+14}'] = update
                    if player_type == 'goalies':
                        print(f'        W|L|Sh|Sa|GA')
                        updates[f'Home Page Test!P{i+14}:T{i+14}'] = update
                    print(f'Updates for {player["name"]}: {update}')

    return updates


def get_active_stats():
    # returns dict with keys as last name
    return _preprocess_box_scores(get_scores())


def _preprocess_box_scores(scores):
    out = {}
    active_players = get_players()
    box_scores = scores['box']
    line_scores = scores['line']
    # iterate through active box scores
    for i, box_score in enumerate(box_scores):
        is_over = _ended(line_scores[i])  # is the game over?
        for team_id in box_score["teams"]:
            team = box_score["teams"][team_id]
            for player_id in team["players"]:
                player = team["players"][player_id]
                stats = player["stats"]
                for stat_type in stats:
                    # set player stats
                    if stat_type == "skaterStats":
                        if player["person"]["lastName"] == 'Marchand':
                            player["person"]["lastName"] = 'Brad'
                        if player["person"]["lastName"] == 'MacKinnon':
                            player["person"]["lastName"] = 'Mackinnon'
                        if player["person"]["lastName"] == 'Nichushkin':
                            player["person"]["lastName"] = 'Nichsukin'
                        if player["person"]["lastName"] == 'Eriksson Ek':
                            player["person"]["lastName"] = 'Ek'
                        if player["person"]["lastName"] in active_players:
                            out[player["person"]["lastName"]] = {
                                'goals': stats[stat_type]['goals'],
                                'assists': stats[stat_type]['assists'],
                                'plus_minus': stats[stat_type]['plusMinus'],
                                'ot_goal': ot_goal(box_score, line_scores[i], player_id) if is_over else 0,
                                'fights': fight(box_score, player_id)
                            }
                    elif stat_type == "goalieStats":
                        # set goalie stats
                        if player["person"]["lastName"] == 'Bobrovsky':
                            player["person"]["lastName"] = 'Bobrovski'
                        if player["person"]["lastName"] == 'Vasilevsky':
                            player["person"]["lastName"] = 'Vasilevskiy'
                        if player["person"]["lastName"] in active_players:
                            out[player["person"]["lastName"]] = {
                                    'wins': win(box_score, player_id) if is_over else 0,
                                    'losses': loss(box_score, player_id) if is_over else 0,
                                    'shutouts': 1 if is_over and stats[stat_type]['shots'] == stats[stat_type]['saves'] else 0,
                                    'saves': stats[stat_type]['saves'],
                                    'goals_against': stats[stat_type]['shots'] - stats[stat_type]['saves']
                                }
    return out


def _ended(ls):
    # is the game over?
    if 'currentPeriodTimeReamining' in ls:
        return (ls['currentPeriodTimeRemaining'] == "Final")
    else:
        return False