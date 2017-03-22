from gridworld import GridWorld, Position

def value (value, targetValue, reward, alpha, discount):

	return value + (alpha * (reward + (discount * targetValue) - value))

def getValue (agent, position, action, state):

	alpha = agent.policy.alpha
	discount = agent.policy.discount
	target = agent.evaluate(action)
	target = target if state.inBounds(target) else position
	reward = agent.model.reward(target)
	currentValue = state.get(position).stateValue()
	targetValue = state.get(target).stateValue()

	return value(currentValue, targetValue, reward, alpha, discount)

def update (agent, state, action):

	position = agent.position()
	agent.policy.time.incriment(position)
	average = getValue(agent, position, action, state)
	agent.policy.updateEpsilonCount(state.get(position).stateValue(), average)
	state.get(position).updateState(average)

	return state

def td0 (agent, state):

	position = Position(3,3)

	while not position.on(Position(0,0)) and not position.on(Position(4,4)):
		
		action = agent.choseAction(state)
		
		update(agent, state, action)

		if state.inBounds(agent.evaluate(action)):

			agent.move(action)

		position = agent.position()

print GridWorld(5, 5, 0.01, .9, .1).episodic(td0, 2000).playOffStateValues(50)