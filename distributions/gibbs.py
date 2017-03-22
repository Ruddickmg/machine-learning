from __future__ import division
from math import log, exp
from plotly.graph_objs import Scatter, Layout
import plotly
import random

def incAvg(q, r, t):

	return q + ((1 / t) * (r - q))

def error(reward, avg, alpha):
	
	return alpha * (reward - avg)

def updateCurrent(preference, probability, reward, avg, alpha):

	return preference + (error(reward, avg, alpha) * (1 - probability))

def updateRest(preference, probability, reward, avg, alpha):

	return preference - (error(reward, avg, alpha) * probability)

def calculateProbability(actions, action):

	return exp(action) / sum(list(map(exp, actions)))

def updateSoftMax(actions, probabilities, current, avg, alpha):

	preferences = []

	for action, value in enumerate(actions):

		probability = probabilities[action]

		reward = actions[current]
		
		preferences.append(

			updateCurrent(value, probability, reward, avg, alpha) if (action == current) 
		 	else updateRest(value, probability, reward, avg, alpha)
		)

	return preferences

def chose (probabilities):

	r = random.random()
	current = 0

	for action, probability in enumerate(probabilities):

		current += probability

		if (r <= current):

			return action

def test (rewards, alpha, steps, baseline):

	preferences = [list(map(lambda x: 0, rewards))]
	percentages = []
	best = rewards.index(max(rewards))

	timesChoseBest = 0
	avg = 0

	for t in range(1, steps):

		preference = preferences[-1]
		probabilities = list(map(lambda p: calculateProbability(preference, p), preference))
		current = chose(probabilities)

		if (baseline):

			avg = incAvg(avg, rewards[current], t)

		if (current == best):

			timesChoseBest += 1

		percentages.append((timesChoseBest/t) * 100)
		preferences.append(updateSoftMax(rewards, probabilities, current, avg, alpha))

		alpha -= 0.001

	return {

		"preference":preferences, 
		"percentage":percentages
	}

def getPreferences(rewards, alpha, steps, baseline):

	return test(rewards, alpha, steps, baseline)['preference']

def getPercentageChoseBest(rewards, alpha, steps, baseline):

	return test(rewards, alpha, steps, baseline)['percentage']

def trace(xAxis, yAxis):

	return Scatter(x=xAxis, y=yAxis, fill='tozeroy')

def plotPreferences (results):

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

data = plotPercentage(getPercentageChoseBest(rewardSeed, 0.1, 1000, True))

# data = plotPreferences(getPreferences(rewardSeed, 0.1, 200, True))

plotly.offline.plot({

    "data": data,
    "layout": Layout(title="Soft Max: Percentage highest value was chosen")
})