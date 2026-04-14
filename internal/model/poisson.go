package model

import (
	"math"
)

type poissonCacheKey struct {
	lambda float64 
	k      int
}

func newPoissonCache(lambda float64, k int) poissonCacheKey {
	return poissonCacheKey{lambda: lambda, k: k}
}

type PoissonModel struct {
	MaxGoals      int
	HomeAdvantage float64
	Cache          map[poissonCacheKey]float64	
}

func NewPoissonModel(MaxGoals int, HomeAdvantage float64) *PoissonModel {
	return &PoissonModel{
		MaxGoals:      MaxGoals,
		HomeAdvantage: HomeAdvantage,
		Cache: make(map[poissonCacheKey]float64),
	}
}

func factorial(n int) int {
	result := 1
	for i := 2; i <= n; i++ {
	    result *= i
	}
	return result
  }

func (pm *PoissonModel) CalcProb(lambda float64, k int) float64 {
	key := newPoissonCache(lambda, k)
	if value, exists := pm.Cache[key]; exists{
		return value
	}

	p := (math.Pow(lambda, float64(k)) * math.Exp(-lambda)) / float64(factorial(k))
	pm.Cache[key] = p

	return p
}

func (pm *PoissonModel) GoalDistribution(lambda float64) []float64{
	probs := make([]float64, pm.MaxGoals+1)
	for k := 0; k <= pm.MaxGoals; k++ {
		probs[k] = pm.CalcProb(lambda, k)
	}

	total := 0.0
	for _, p := range probs {
		total += p
	}

	normalized := make([]float64, len(probs))
	for i, p := range probs {
		normalized[i] = p / total
	}

	return normalized
}
