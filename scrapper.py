import requests
import json
import os
import time

#Get Data from APi
HEADERS = {
	"x-rapidapi-key": "05c3b17ad3mshb9e532f242ede0cp1da70ajsnf1a0ece06868",
	"x-rapidapi-host": "cricbuzz-cricket.p.rapidapi.com",
	"Content-Type": "application/json"
}

BASE_URL = "https://cricbuzz-cricket.p.rapidapi.com"

os.makedirs("data", exist_ok=True)

# fetching data from API
def get_data(endpoint):
    try:
        #time.sleep(5)  # Add a delay of 1 second before making the request
        response = requests.get(
            BASE_URL + endpoint,
            headers=HEADERS
        )

        response.raise_for_status()

        return response.json()

    except Exception as e:
        print(f"Error in {endpoint}: {e}")
        return None



# SAVE data as JSON file
def save(filename, data):

    with open(
        f"data/{filename}",
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            data,
            f,
            indent=4,
            ensure_ascii=False
        )

# extracting data for Master tables 
players = {}
teams = {}
series = {}
matches = {}
venues = {}
scorecards = []

rankings = {
    "batsmen": [],
    "bowlers": [],
    "allrounders": []
}


#live matches data

live = get_data("/matches/v1/live")

match_ids = []

if live:

    for type_match in live.get("typeMatches", []):

        for series_match in type_match.get("seriesMatches", []):

            if "seriesAdWrapper" not in series_match:
                continue

            wrapper = series_match["seriesAdWrapper"]

            series_id = wrapper["seriesId"]

            series[series_id] = {
                "series_id": series_id,
                "series_name": wrapper["seriesName"]
            }

            for match in wrapper.get("matches", []):

                info = match["matchInfo"]

                match_id = info["matchId"]

                match_ids.append(match_id)

#matches details
for match_id in match_ids:

    data = get_data(f"/mcenter/v1/{match_id}")

    if data is None:
        continue

    # Teams
    team1 = data["team1"]
    team2 = data["team2"]

    teams[team1["teamid"]] = {
        "team_id": team1["teamid"],
        "team_name": team1["teamname"],
        "short_name": team1["teamsname"]
    }

    teams[team2["teamid"]] = {
        "team_id": team2["teamid"],
        "team_name": team2["teamname"],
        "short_name": team2["teamsname"]
    }

    # Venue
    venue = data['venueinfo']

    venues[venue["id"]] = {
        "venue_id": venue["id"],
        "ground": venue["ground"],
        "city": venue["city"],
        "timezone": venue["timezone"]
    }

    # Match
    matches[match_id] = {
        "match_id": match_id,
        "series_id": data["seriesid"],
        "team1_id": team1["teamid"],
        "team2_id": team2["teamid"],
        "venue_id": venue["id"],
        "status": data["status"]
    }


#player details and scorecards

for match_id in match_ids:

    scorecard = get_data(f"/mcenter/v1/{match_id}/scard")

    if scorecard is None:
        continue

    for innings in scorecard["scorecard"]:

        # Innings summary
        scorecards.append({

            "match_id": match_id,

            "innings_id": innings.get("inningsid"),

            "bat_team_name": innings.get("batteamname"),

            "bat_team_short_name": innings.get("batteamsname"),

            "score": innings.get("score"),

            "wickets": innings.get("wickets"),

            "overs": innings.get("overs"),

            "run_rate": innings.get("runrate")

        })

        # ======================
        # BATSMEN
        # ======================

        batsmen = innings["batsman"]

        for bat in batsmen:

            pid = bat["id"]

            if pid not in players:

                players[pid] = {

                    "player_id": pid,

                    "player_name": bat["name"],

                    "is_captain": bat["iscaptain"],

                    "is_keeper": bat["iskeeper"]

                }

        # ======================
        # BOWLERS
        # ======================

        bowlers = innings["bowler"]

        for bowl in bowlers:

            pid = bowl["id"]

            if pid not in players:

                players[pid] = {

                    "player_id": pid,

                    "player_name": bowl["name"],

                    "is_captain": bowl["iscaptain"],

                    "is_keeper": bowl["iskeeper"]

                }
#players info
for pid in list(players.keys()):

    player = get_data(f"/stats/v1/player/{pid}")

    if player is None:
        continue

    players[pid].update({

        "role": player.get("role"),

        "batting_style": player.get("battingStyle"),

        "bowling_style": player.get("bowlingStyle"),

        "birth_place": player.get("birthPlace"),

        "country": player.get("intlTeam")

    })
# rankings

rankings["batsmen"] = get_data("/stats/v1/rankings/batsmen")

rankings["bowlers"] = get_data("/stats/v1/rankings/bowlers")

rankings["allrounders"] = get_data("/stats/v1/rankings/allrounders")

# Save all data to JSON files
save("players.json",list(players.values()))
save("teams.json",list(teams.values()))
save("series.json",list(series.values()))
save("matches.json",list(matches.values()))
save("venues.json",list(venues.values()))
save("scorecards.json",scorecards)
save("rankings.json",rankings)
