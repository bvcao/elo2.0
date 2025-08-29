def process_matches_dual(json_file, start_rating=1500, K_team=20, K_indiv=15, alpha=0.6):
    with open(json_file, "r") as f:
        data = json.load(f)

    team_rating = {}
    indiv_rating = {}

    for match in data["matches"]:
        adrs = [p["adr"] for p in match["players"]]
        teams = [p["team"] for p in match["players"]]
        winner = match["winner"]

        # init ratings
        for p in match["players"]:
            if p["id"] not in team_rating:
                team_rating[p["id"]] = start_rating
                indiv_rating[p["id"]] = start_rating

        # --- TEAM RATING UPDATE (Elo classic) ---
        team0 = [p["id"] for p in match["players"] if p["team"] == 0]
        team1 = [p["id"] for p in match["players"] if p["team"] == 1]
        avg0 = np.mean([team_rating[p] for p in team0])
        avg1 = np.mean([team_rating[p] for p in team1])

        expected0 = 1 / (1 + 10 ** ((avg1 - avg0) / 400))
        expected1 = 1 - expected0
        actual0, actual1 = (1, 0) if winner == 0 else (0, 1)

        delta0 = K_team * (actual0 - expected0)
        delta1 = K_team * (actual1 - expected1)

        for p in team0: team_rating[p] += delta0
        for p in team1: team_rating[p] += delta1

        # --- INDIVIDUAL RATING UPDATE (ADR-based) ---
        indiv_deltas = elo_plus_curved_adr(adrs, teams, winner, K=K_indiv)
        for i, p in enumerate(match["players"]):
            indiv_rating[p["id"]] += indiv_deltas[i]

    # --- Final Blended Rating ---
    results = {}
    for p in team_rating:
        blended = alpha * team_rating[p] + (1 - alpha) * indiv_rating[p]
        results[p] = {
            "TeamRating": round(team_rating[p], 1),
            "IndivRating": round(indiv_rating[p], 1),
            "FinalRating": round(blended, 1),
            "Rank": rating_to_rank(blended)
        }
    return results
