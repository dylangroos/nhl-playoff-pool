from gsheet import get_nightly_baseline, set_update
from meta import get_active_stats, generate_updates
import time

def broker():
    print('getting nightly baseline...')
    baseline = get_nightly_baseline()
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

if __name__ == "__main__":
    broker()