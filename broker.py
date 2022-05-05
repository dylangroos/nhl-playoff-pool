from gsheet import get_nightly_baseline, set_update
from meta import get_active_stats, generate_updates
import time
import pickle
import os
from datetime import date, datetime

def broker():
    # todays path
    todays_path = f'nightly_baseline_{datetime.today().strftime("%Y-%m-%d")}.pkl'
    print('getting nightly baseline...')
    if os.path.isfile(todays_path):
        # load it
        with open(todays_path, 'rb') as f: 
             baseline = pickle.load(f)
    else:
        # generate it
        baseline = get_nightly_baseline()
        # save it
        with open(todays_path, 'wb') as f: 
             pickle.dump(baseline, f)
    while True:
        print('fetching active stats from nhl api...')
        active = get_active_stats()
        updates = generate_updates(baseline, active)
        if updates:
            set_update(updates)
        else:
            print('no stat changes!')
        print("sleeping for 1 min...")
        time.sleep(60)


# do the boxscore from any date
def reconcile(date):
    pass 


if __name__ == "__main__":
    broker()