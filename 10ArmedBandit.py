from __future__ import division
from math import log, exp, floor
from plotly.graph_objs import Scatter, Layout
import plotly
import random

def incAvg(q, r, t):

	return q + ((1 / t) * (r - q))

def best (estimates):

	return estimates.index(max(estimates))

def rand (arms):

	return int(floor(random.random() * float(arms)))

def chose (estimates, e, arms):

	return rand(arms) if (random.random() <= e) else best(estimates)

def test (rewards, e, steps):

	arms = len(rewards)
	maxReward = max(rewards)
	percentages = []
	allEstimates = []
	estimates = map(lambda x: maxReward + 1, rewards)
	taken = map(lambda x: 0, rewards)
	best = rewards.index(maxReward)

	timesChoseBest = 0

	for t in range(1, steps):

		current = chose(estimates, e, arms)
		estimate = estimates[current]
		taken[current] += 1

		estimates[current] = incAvg(estimate, rewards[current], taken[current])

		if (current == best):

			timesChoseBest += 1

		percentages.append((timesChoseBest / t) * 100)
		allEstimates.append(estimates)

		e -= 0.002

	print estimates
	print rewards

	return {

		"estimates":allEstimates, 
		"percentage":percentages
	}

def getEstimates(rewards, e, steps):

	return test(rewards, e, steps)['estimates']

def getPercentageChoseBest(rewards, e, steps):

	return test(rewards, e, steps)['percentage']

def trace(xAxis, yAxis):

	return Scatter(x=xAxis, y=yAxis, fill='tozeroy')

def plotEstimates (results):

	x = range(1, len(results) + 1)

	lines = list(map(lambda x: [], results[0]))
	points = []

	for result in results:

		for i, value in enumerate(result):

			lines[i].append(value)

	for y in lines:

		points.append(trace(x, y))

	return points

def plotPercentage (percentages):

	return [trace(range(1, len(percentages) + 1), percentages)]

rewardSeed = [15 * random.random() for _ in range(10)]

data = plotPercentage(getPercentageChoseBest(rewardSeed, 0.1, 1000))

# data = plotEstimates(getPreferences(rewardSeed, 0.1, 200, True))

plotly.offline.plot({

    "data": data,
    "layout": Layout(title="10 armed bandit: Percentage highest value was chosen")
})