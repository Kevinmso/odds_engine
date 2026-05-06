import math
from dataclasses import dataclass, field

@dataclass
class PoissonModel:
    max_goals: int
    cache: dict[tuple[float, int], float] = field(default_factory=dict)

    def calcProb(self, lmbda: float, k: int) -> float:
        key = (round(lmbda, 4), k)
        if key in self.cache:
            return self.cache[key]

        log_p = k * math.log(lmbda) - lmbda - math.lgamma(k + 1)
        p = math.exp(log_p)
        self.cache[key] = p
        return p

    def goalDistribution(self, lmbda: float) -> list[float]:
        probs = [self.calcProb(lmbda, k) for k in range(self.max_goals + 1)]
        total = sum(probs)
        return [p / total for p in probs]
    
    def scoreMatrix(self, lambda_home: float, lambda_away: float) -> list[list[float]]:
        home_probs = self.goalDistribution(lambda_home)
        away_probs = self.goalDistribution(lambda_away)

        matrix = [[home_probs[i] * away_probs[j] for j in range(self.max_goals + 1)] for i in range(self.max_goals + 1)]
        return matrix
    
    def matchOutcome(self, lambda_home: float, lambda_away: float) -> dict[str, float]:
        matrix = self.scoreMatrix(lambda_home, lambda_away)
        outcome = {
            "home": 0.0,
            "draw": 0.0,
            "away": 0.0,
        }

        for i in range(self.max_goals + 1):
            for j in range(self.max_goals + 1):
                if i > j:
                    outcome["home"] += matrix[i][j]
                elif i == j:
                    outcome["draw"] += matrix[i][j]
                else:
                    outcome["away"] += matrix[i][j]
        return outcome
    
    def probToOdd(self, p: float) -> float:
        return 1.0 / p
    
    def getMatchOdds(self, lambda_home: float, lambda_away: float) -> dict[str, float]:
        probs = self.matchOutcome(lambda_home, lambda_away)
        
        odds = {
            label: self.probToOdd(p) if p > 0 else float('inf') 
            for label, p in probs.items()
        }
        
        return odds