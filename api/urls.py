from urllib.parse import urljoin
from datetime import datetime

SCHEDULE = 'https://statsapi.web.nhl.com/api/v1/schedule'

BOXSCORE = 'https://statsapi.web.nhl.com/api/v1/game/%s/boxscore' # % game ID

LINESCORE = 'https://statsapi.web.nhl.com/api/v1/game/%s/linescore' # %  game ID

LIVE = 'https://statsapi.web.nhl.com/api/v1/game/%s/feed/live/diffPatch?startTimecode=%s' # % game ID, yyyymmdd_hhmmss


SCHEDULE_DATE = 'https://statsapi.web.nhl.com/api/v1/schedule?date=%s' # % date yyyy-m-d
