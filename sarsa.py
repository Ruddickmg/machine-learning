from gridworld import GridWorld, Position

def value (value, targetValue, reward, alpha, discount):

	return value + (alpha * (reward + (discount * targetValue) - value))

def getValue (agent, position, action, state):

	policy = agent.policy
	currentValue = state.get(position).actionValue(action)
	tPosition = agent.evaluate(action)
	target = state.get(tPosition if state.inBounds(tPosition) else position)
	targetValue = target.actionValue(target.actions.eGreedy())

	return value(currentValue, targetValue, agent.model.reward(tPosition), policy.alpha, policy.discount)

def update (agent, state, action):

	position = agent.position()
	agent.policy.time.incriment(position)
	average = getValue(agent, position, action, state)
	agent.policy.updateEpsilonCount(state.get(position).actionValue(action), average)
	state.get(position).updateAction(action, average)

	return state

def sarsa (agent, state):

	position = Position(3,3)
	action = state.get(agent.position()).actions.eGreedy()

	while not position.on(Position(0,0)) and not position.on(Position(4,4)):
		
		update(agent, state, action)

		if state.inBounds(agent.evaluate(action)):

			agent.move(action)

		position = agent.position()
		action = state.get(position).actions.eGreedy()

print GridWorld(5, 5, 0.01, .9, .1).episodic(sarsa, 2000).playOffActionValues(50)