from gsheet import range_mappings, set_update
from api import get_json


# TODO: this is ugly
def reconcile():
    # get the box scores
    # get the playoff stats from those box scores per player ID
    # update the sheet accordingly
    name_to_range = range_mappings()
    skater_ids = [{"id": entry['person']['id'], "name": entry['person']['fullName']} for entry in
        get_json('https://statsapi.web.nhl.com/api/v1/stats/leaders?leaderCategories=[points,goals,assists]&season=20222023&limit=500&leaderGameTypes=P')['leagueLeaders'][0]['leaders']]
    updates = {}
    for entry in skater_ids:

        if entry["name"] in ['Nathan MacKinnon']:
            entry["name"] = 'Nathan Mackinnon'
        if entry["name"] in ['Valeri Nichushkin']:
            entry["name"] = 'Valeri Nichsukin'
        if entry["name"] in ["Brad Marchand"]:
            entry["name"] = "Rat Brad"
        if entry["name"] in name_to_range:
            stats = get_json(f"https://statsapi.web.nhl.com/api/v1/people/{entry['id']}/stats?stats=statsSingleSeasonPlayoffs&season=20222023")['stats'][0]['splits'][0]['stat']
            print(entry["name"])
            updates[name_to_range[entry["name"]]] = [
                stats['goals'],
                stats['assists'],
                stats["plusMinus"],
                stats["overTimeGoals"]
            ]
    goalie_ids = [{"id": entry['person']['id'], "name": entry['person']['fullName']} for entry in
            get_json('https://statsapi.web.nhl.com/api/v1/stats/leaders?leaderCategories=savePct&season=20222023&limit=100&leaderGameTypes=P')['leagueLeaders'][0]['leaders']]
    for entry in goalie_ids:
        if entry["name"] in ['Andrei Vasilevskiy']:
            entry["name"] = 'Andrei Vasilevsky'
        if entry["name"] in ['Sergei Bobrovsky']:
            entry["name"] = 'Sergei Bobrovski'
        if entry["name"] in name_to_range:
            print(entry["name"])
            stats = get_json(f"https://statsapi.web.nhl.com/api/v1/people/{entry['id']}/stats?stats=statsSingleSeasonPlayoffs&season=20222023")['stats'][0]['splits'][0]['stat']
            updates[name_to_range[entry["name"]]] = [
                stats['wins'],
                stats['losses'],
                stats["shutouts"],
                stats["saves"],
                stats["goalsAgainst"]
            ]
    if updates:
        set_update(updates)

if __name__ == '__main__':
    reconcile()