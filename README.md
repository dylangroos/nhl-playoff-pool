# NHL Playoff Pool
This project connects the real-time stats endpoints from the National Hockey League (hosted by Major League Baseball) to our 2022 NHL Playoff Pool fantasy Google Sheet.


# Sample Sheet
https://docs.google.com/spreadsheets/d/1WuK3vSut4oyWxDPYN0f4Lig9xkU-sOLa7c4WHfkIwXg/edit?usp=sharing

# Explanation
`broker.py` pings the NHL endpoints and updates the google sheet in real time.  `reconcile.py` accounts runs the morning after all games have completed and corrects for any inconcistencies in micro stat calculations. The project can be configured to execute on ECS Spot Instances (for price)

# TO DO
*Swap to an event based live tracking model rather than parsing the full boxscores each time.
*Query google sheet using [ROAPI](https://roapi.github.io/docs/index.html)
*Deploy on GCP App Engine
