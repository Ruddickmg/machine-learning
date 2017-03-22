from gridworld import GridWorld, Position, incAvg
import math

def value(value, reward, discount):

	return reward + (discount * value)

def update (agent, state, action, currentValue):

	position = agent.evaluate(action)

	if not state.inBounds(position):

		position = agent.position()

	return value(
		state.get(position).stateValue(),
		agent.model.reward(position),
		agent.policy.discount
	)

def dp (agent, state):

	position = agent.position()
	time = agent.policy.time.incriment(position)
	current = state.get(position)
	currentValue = current.stateValue()
	average = 0

	for num, action in enumerate(agent.actions):

		average = incAvg(average, update(agent, state, action, currentValue), num + 1)

	average = incAvg(currentValue, average, time + 1)

	agent.policy.updateEpsilonCount(currentValue, average)

	return current.updateState(average)

print GridWorld(5, 5, 0.1, .9, .1).sweep(dp, 100).playOffStateValues(50)
