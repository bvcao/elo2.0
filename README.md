# elo2.0

🔹 Dual-Rating Elo System (Team + Individual)

We’re combining two layers of rating:

Team Rating (TR)

Each distinct 5-player team has its own Elo rating.

Updated like classic Elo:

If the team wins → TR goes up.

If the team loses → TR goes down.

Magnitude depends on opponent TR and expected win probability.

A “team” is treated as a unique combination of players (so if you change rosters, it’s a new team with a fresh rating).

Individual Rating (IR)

Each player has their own personal rating.

Independent of team results.

Updated per match based on ADR (Average Damage per Round):

Compare each player’s ADR to their own team’s ADR average.

Convert that difference into a z-score (relative performance within team).

Players above average gain IR, below average lose IR.

This way, even in a losing team, the top performer can climb, while underperformers drop.

🔹 Match Processing (Step by Step)

Start ratings:

TR = 1500 for all teams.

IR = 1500 for all players.

When a match is played:

Determine winning team.

Update both teams’ TR using Elo formula.

For each team, calculate ADR average + standard deviation.

For each player:

Compute z-score = (ADR - team_avg) / team_std.

Adjust IR by z * scale_factor (e.g., ±10 points).

After many matches:

Teams sort into rankings (like CS2 leagues).

Players’ IR shows personal skill consistency, independent of win/loss streaks.

🔹 What This Captures

Team performance matters:

TR tracks group success and synergy.

Individual performance matters:

IR tracks skill, consistency, and contribution.

Balance between them:

You can be a high-IR player stuck on a low-TR team.

Or you can ride on strong teammates (high TR, low IR).

Metadata links them:

A player’s profile can show:

Current team(s) they’re tied to.

Their own IR.

The TR of their current/past teams.

🔹 Advantages Over Pure Elo

Prevents “hard carrying” from being invisible.

Keeps team skill and individual skill distinct.

Provides a more granular ladder:

Leaderboards for top teams.

Leaderboards for top players (even across different teams).

👉 So in short:

Team Rating (TR) = How good the team unit is.

Individual Rating (IR) = How good you are, relative to your teammates.

Both update each match, so over time you can see who carries, who coasts, and which teams are strongest.
