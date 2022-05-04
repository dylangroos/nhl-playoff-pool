from api import get_box_scores
from gsheet import get_players
from .stats import win, loss, shutout, fight, ot_goal

def generate_updates(baseline, active):
    # update is a dictionary with row_index then the values -- this is taken in by the gsheet stuff
    updates = {}
    for player_type in baseline:
        for i, player in enumerate(baseline[player_type]):
            if player['name'] == 'Vasilevsky':
                player['name'] = 'Vasilevskiy'
            if player['name'] == 'Bobrovski':
                player['name'] = 'Bobrovsky'
            if player['name'] == 'Brad':
                player['name'] = 'Marchand'
            if player['name'] == 'Mackinnon':
                player['name'] = 'MacKinnon' 
            if player['name'] == 'Nichsukin':
                player['name'] = 'Nichushkin'
            if player['name'] in active:
                if player_type in ['forwards', 'defense']:
                    update = [
                        active[player['name']]['goals'] + int(player['goals']),
                        active[player['name']]['assists'] + int(player['assists']),
                        int(active[player['name']]['plus_minus']) + int(player['plus_minus']),
                        active[player['name']]['ot_goal'] + int(player['ot_goal']),
                        active[player['name']]['fights'] + int(player['fights'])
                    ]
                elif player_type == 'goalies':
                    update = [
                        active[player['name']]['wins'],
                        active[player['name']]['losses'],
                        active[player['name']]['shutouts'],
                        active[player['name']]['saves'] + int(player['saves']),
                        active[player['name']]['goals_against'] + int(player['goals_against'])
                    ]
                if any(update):

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
    return _preprocess_box_scores(get_box_scores())


def _preprocess_box_scores(box_scores):
    out = {}
    active_players = get_players()
    # TODO: the ones that are ended are post game stats (how do we get post game stats?)
    for box_score in box_scores:
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
                        if player["person"]["lastName"] in active_players:
                            out[player["person"]["lastName"]] = {
                                'goals': stats[stat_type]['goals'],
                                'assists': stats[stat_type]['assists'],
                                'plus_minus': stats[stat_type]['plusMinus'],
                                'ot_goal': ot_goal(box_score, player_id),
                                'fights': fight(box_score, player_id)
                            }
                    elif stat_type == "goalieStats":
                        # set goalie stats
                        if player["person"]["lastName"] == 'Bobrovsky':
                            player["person"]["lastName"] == 'Bobrovski'
                        if player["person"]["lastName"] in active_players:
                            out[player["person"]["lastName"]] = {
                                    'wins': win(box_score, player_id),
                                    'losses': loss(box_score, player_id),
                                    'shutouts': shutout(box_score, player_id),
                                    'saves': stats[stat_type]['saves'],
                                    'goals_against': stats[stat_type]['shots'] - stats[stat_type]['saves']
                                }
    return out
