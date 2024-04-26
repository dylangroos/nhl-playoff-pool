SCOPE = ['https://www.googleapis.com/auth/spreadsheets']


STARTING_ROW = 22

SHEET_NAME = "Copy of Home Page Test"


SHEET_ID = '1zSw0K2QcwHiCZ0nf8c2XeCr5gEnjkhcNToZGVmBsY7g'
FORWARD_RANGES = {
    "names": f"{SHEET_NAME}!A{STARTING_ROW}:A121",
    "goals": f"{SHEET_NAME}!B{STARTING_ROW}:B121",
    "assists": f"{SHEET_NAME}!C{STARTING_ROW}:C121",
    "plus_minus": f"{SHEET_NAME}!D{STARTING_ROW}:D121",
    "ot_goals": f"{SHEET_NAME}!E{STARTING_ROW}:E121",
    "fights": f"{SHEET_NAME}!F{STARTING_ROW}:F121",
    "all": f"{SHEET_NAME}!A{STARTING_ROW}:F121"
}
DEFENSE_RANGES = {
    "names": f"{SHEET_NAME}!H{STARTING_ROW}:H76",
    "goals": f"{SHEET_NAME}!I{STARTING_ROW}:I76",
    "assists": f"{SHEET_NAME}!J{STARTING_ROW}:J76",
    "plus_minus": f"{SHEET_NAME}!K{STARTING_ROW}:K76",
    "ot_goals": f"{SHEET_NAME}!L{STARTING_ROW}:L76",
    "fights": f"{SHEET_NAME}!M{STARTING_ROW}:M76",
    "all": f"{SHEET_NAME}!H{STARTING_ROW}:M76"
}
GOALIE_RANGES = {
    "names": f"{SHEET_NAME}!O{STARTING_ROW}:O43",
    "wins": f"{SHEET_NAME}!P{STARTING_ROW}:P43",
    "losses": f"{SHEET_NAME}!Q{STARTING_ROW}:Q43",
    "shutouts": f"{SHEET_NAME}!R{STARTING_ROW}:R43",
    "saves": f"{SHEET_NAME}!S{STARTING_ROW}:S43",
    "goals_against": f"{SHEET_NAME}!T{STARTING_ROW}:T43",
    "assists": f"{SHEET_NAME}!U{STARTING_ROW}:U43",
    "all": f"{SHEET_NAME}!O{STARTING_ROW}:U43"
}