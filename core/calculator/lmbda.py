def calcTeamFactor(team_mean: float, league_mean: float) -> float:
    return team_mean / league_mean

def calcLambda(attack_factor: float, opponent_defense_factor: float, league_mean: float) -> float:
    return attack_factor * opponent_defense_factor * league_mean
