import json
import random
import math
from statistics import mean, pstdev

# ---- Elo update helpers ----
def expected_score(rating_a, rating_b):
    return 1 / (1 + 10 ** ((rating_b - rating_a) / 400))

def update_elo(rating, expected, score, k=32):
    return rating + k * (score - expected)

# ---- Dataset generator ----
def generate_dataset(num_teams=10, num_seasons=4, matches_per_season=40):
    dataset = {"seasons": []}
    teams = [f"Team_{chr(65+i)}" for i in range(num_teams)]
    players = {team: [f"{team[5]}{i+1}" for i in range(5)] for team in teams}

    match_id_counter = 1
    for season in range(1, num_seasons+1):
        season_data = {"season": season, "matches": []}
        for _ in range(matches_per_season):
            t1, t2 = random.sample(teams, 2)
            t1_stats = [{"id": pid, "adr": random.randint(60, 120)} for pid in players[t1]]
            t2_stats = [{"id": pid, "adr": random.randint(60, 120)} for pid in players[t2]]
            winner = random.choice([t1, t2])
            match = {
                "match_id": match_id_counter,
                "winner": winner,
                "teams": [
                    {"team_id": t1, "players": t1_stats},
                    {"team_id": t2, "players": t2_stats}
                ]
            }
            season_data["matches"].append(match)
            match_id_counter += 1
        dataset["seasons"].append(season_data)
    return dataset

# ---- Rating processor ----
def process_ratings(dataset):
    team_ratings = {}
    player_ratings = {}

    # initialize teams and players
    for season in dataset["seasons"]:
        for match in season["matches"]:
            for team in match["teams"]:
                tid = team["team_id"]
                if tid not in team_ratings:
                    team_ratings[tid] = {"rating": 1500, "wins": 0, "losses": 0}
                for p in team["players"]:
                    if p["id"] not in player_ratings:
                        player_ratings[p["id"]] = {"rating": 1500, "team": tid}

    # process matches
    for season in dataset["seasons"]:
        for match in season["matches"]:
            t1, t2 = match["teams"]
            tid1, tid2 = t1["team_id"], t2["team_id"]
            tr1, tr2 = team_ratings[tid1]["rating"], team_ratings[tid2]["rating"]

            expected1 = expected_score(tr1, tr2)
            expected2 = 1 - expected1

            if match["winner"] == tid1:
                score1, score2 = 1, 0
                team_ratings[tid1]["wins"] += 1
                team_ratings[tid2]["losses"] += 1
            else:
                score1, score2 = 0, 1
                team_ratings[tid1]["losses"] += 1
                team_ratings[tid2]["wins"] += 1

            # update team ratings
            team_ratings[tid1]["rating"] = update_elo(tr1, expected1, score1)
            team_ratings[tid2]["rating"] = update_elo(tr2, expected2, score2)

            # update individual ratings (based on ADR z-score)
            for team in [t1, t2]:
                adrs = [p["adr"] for p in team["players"]]
                avg, std = mean(adrs), pstdev(adrs) if pstdev(adrs) > 0 else 1
                for p in team["players"]:
                    z = (p["adr"] - avg) / std
                    player_ratings[p["id"]]["rating"] += z * 10  # scale factor
                    player_ratings[p["id"]]["team"] = team["team_id"]

    return team_ratings, player_ratings

# ---- Run demo ----
if __name__ == "__main__":
    dataset = generate_dataset()
    with open("cs2_dataset.json", "w") as f:
        json.dump(dataset, f, indent=2)

    team_ratings, player_ratings = process_ratings(dataset)

    print("\n=== Final Team Ratings ===")
    for tid, meta in team_ratings.items():
        print(tid, meta)

    print("\n=== Final Player Ratings (sample) ===")
    for pid, meta in list(player_ratings.items())[:10]:
        print(pid, meta)
