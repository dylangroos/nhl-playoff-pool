from urllib.parse import urljoin
from datetime import datetime

SCHEDULE = 'https://api-web.nhle.com/v1/schedule/now'

BOXSCORE = 'https://api-web.nhle.com/v1/gamecenter/%s/boxscore' # % game ID

LINESCORE = 'https://api-web.nhle.com/v1/score/now' # %  game ID

LIVE = 'https://statsapi.web.nhl.com/api/v1/game/%s/feed/live/diffPatch?startTimecode=%s' # % game ID, yyyymmdd_hhmmss


SCHEDULE_DATE = 'https://statsapi.web.nhl.com/api/v1/schedule?date=%s' # % date yyyy-m-d
