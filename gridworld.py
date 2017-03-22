from __future__ import division
from math import floor
import random

def incAvg(q, r, t):

	return q + ((1 / t) * (r - q))

def matrix(x, y, n = 0):

	return [[n for j in range(y)] for i in range(x)]

def rand (amount):

	return int(floor(random.random() * float(amount)))

class Actions:

	def __init__(self, actions, epsilon=0):

		self.list = actions
		self.actions = {}
		self.epsilon = epsilon

		for action in actions:

			self.actions[action] = 0

	def __repr__(self):

		return "Actions(%s)" % self.actions

	def __str__(self):

		return "{\n    list: %s,\n    values: %s\n}" % (self.list, self.actions)

	def value(self, action):

		return self.actions[action]

	def update(self, action, value):

		self.actions[action] = value

	def max(self):

		array = self.list
		actions = self.actions
		values = list(map(lambda a: actions[a], array))
		index = values.index(max(values))

		return array[index] if any(actions[a] != actions['north'] for a in array) else self.random() 

	def random(self):

		return self.list[rand(len(self.list))]

	def eGreedy(self):

		return self.max() if random.random() <= self.epsilon else self.random()

class State:

	def __init__(self, actions, epsilon=0):

		self.actions = Actions(actions, epsilon)
		self.val = 0
		self.epsilon = epsilon

	def __repr__(self):

		return "State(%s)" % str(self.actions.list)

	def __str__(self):

		return "{\n    value: %s,\n    actions: %s\n}" % (self.val, self.actions)

	def stateValue(self):

		return self.val

	def updateState(self, value):

		self.val = value

	def updateAction(self, action, value):

		self.actions.update(action, value)

	def actionValue(self, action):

		return self.actions.value(action)

	def actions(self):

		return self.actions.list

class Position:

	def __init__(self, x, y):
		self.x = x
		self.y = y

	def __repr__(self):

		return "Position(%s, %s)" % (self.x, self.y)

	def __str__(self):

		return "{x: %s, y: %s}" % (self.x, self.y)

	def on (self, position):

		return self.x == position.x and self.y == position.y

	def copy (self):

		return Position(self.x, self.y)

class E_Greedy:

	def __init__ (self, e):

		self.e = e

	def __repr__ (self):

		return "E_Greedy(%s)" % self.e

	def __str__(self):
		
		return "{epsilon: %s}" % self.e

	def best (self, values):

		return values.index(max(values))

	def chose (self, values):

		if random.random() <= self.e or not any(x != values[0] for x in values):

			return rand(len(values))

	 	else:

	 	 	return self.best(values)

class Matrix:

	def __init__(self, x, y, n = 0):

		self.matrix = matrix(x, y, n)
		self.x = x
		self.y = y
		self.n = n

	def __repr__(self):

		return "Matrix(%s, %s, %s)" % (self.x, self.y, self.n)

	def __str__(self):

		formatted = matrix(self.x, self.y)

		for x, row in enumerate(self.matrix):
			
			for y, value in enumerate(row):

				formatted[y][x] = "%s" % value

		string = ""

		for row in formatted:

			string += "[" + ", ".join(map(str, row)) + "]\n"

		return string

	def get (self, position):

		return self.matrix[position.x][position.y]

	def set (self, position, value):

		self.matrix[position.x][position.y] = value

		return self

	def reset (self):

		self.matrix = matrix(self.x, self.y, self.n)

	def inBounds (self, position):

		x = position.x
		y = position.y

		return x >= 0 and x < self.x and y >= 0 and y < self.y

class Time (Matrix):

	def incriment (self, position):

		time = self.get(position)

		self.set(position, self.get(position) + 1)

		return time

class Agent:

	def __init__ (self, x, y, policy, actions):

		self.score = 0
		self.actions = actions
		self.start = Position(x, y)
		self.current = Position(x, y)
		self.policy = policy
		self.model = Model()

	def __repr__(self):

		p = self.start

		return "Agent(%s, %s, %s)" % (p.x, p.y, repr(self.policy))

	def __str__(self):

		s = "\n    "

		actions = "[" + ", ".join(map(str, self.actions)) + "]"
		string = "{"+s+"score: %s,"+s+"actions: %s,"+s+"starting position: %s,"+s+"position: %s"+s+"policy: %s,"+s+"model: %s\n}"
		return string % (self.score, actions, str(self.start), str(self.current), str(self.policy).replace("\n", s), str(self.model).replace("\n", s))

	def reset (self, position, epsilon=0):

		self.epsilon = epsilon
		self.current = position
		self.score = 0
		self.policy.time.reset()

		return self

	def training (self):

		return self.policy.changeAboveEpsilon()

	def setPosition(self, position):

		self.current = position

		return self

	def position (self):

		return self.current.copy() 

	def evaluate (self, direction):

		position = self.position()

		if direction == "south":

			position.y += 1

		if direction == "north":

			position.y -= 1

		if direction == "east":

			position.x += 1

		if direction == "west":

			position.x -= 1

		return position
	
	def move (self, direction):

		self.current = self.evaluate(direction)

		return self

	def reward (self, position=None):

		self.score += self.model.reward(self.position())

	def choseAction(self, state):

		actions = self.actions

		return actions[self.policy.chose(self, state)]

	def choseBestAction (self, state):

		actions = self.actions

		return actions[self.policy.greedy(self, state)]

class Model: 

	def __repr__(self):
		
		return "Model()"

	def reward(self, position):

		return 0 if position.on(Position(0,0)) or position.on(Position(4,4)) else -1

class Policy:

	def __init__ (self, epsilon, discount, alpha, time, iterations=100):

		self.eGreedy = E_Greedy(epsilon)
		self.iterations = iterations
		self.discount = discount
		self.epsilon = epsilon
		self.alpha = alpha
		self.time = time
		self.range = 0

	def __repr__ (self):

		return "Policy(%s, %s, %s, %s)" % (self.epsilon, self.discount, repr(self.time), self.iterations)

	def __str__(self):

		tab = "    "
		s = "\n"+tab
		string = "{"+s+"eGreedy: %s,"+s+"iterations: %s,"+s+"discount: %s,"+s+"epsilon: %s,"+s+"range: %s,"+s+"time:\n%s\n}"
		return string % (str(self.eGreedy), self.iterations, self.discount, self.epsilon, self.range, tab + tab + str(self.time).replace("\n", s + tab))

	def changeAboveEpsilon (self):

		return self.range <= self.iterations

	def updateEpsilonCount(self, value, reward):

		self.range = (self.range + 1) if abs(value - reward) < self.epsilon else 0

	def chose (self, agent, state):

		return self.eGreedy.chose(list(map(lambda a: state.get(agent.evaluate(a) if state.inBounds(agent.evaluate(a)) else agent.position()).stateValue(), agent.actions)))
	
	def greedy(self, agent, state):

		return self.eGreedy.best(list(map(lambda a: state.get(agent.evaluate(a) if state.inBounds(agent.evaluate(a)) else agent.position()).stateValue(), agent.actions)))

class GridWorld:

	def __init__ (self, x, y, epsilon, discount, alpha=1, i=None):

		actions = ['north', 'south', 'east', 'west']
		policy = Policy(epsilon, discount, alpha, Time(x, y), i if (i != None) else (x * y))

		self.alpha = alpha
		self.dimensions = Position(x,y)
		self.discount = discount
		self.epsilon = epsilon
		self.agent = Agent(rand(x), rand(y), policy, actions)
		self.state = Matrix(x, y)

		for a in range(x):
			for b in range(y):
				self.state.set(Position(a,b), State(actions, epsilon))

		self.iteration = 0

	def __repr__(self):

		d = self.dimensions
		policy = self.agent.policy

		return "GridWorld(%s, %s, %s, %s, %s)" % (d.x, d.y, self.epsilon, policy.discount, policy.iterations)

	def __str__(self):

		tab = "    "
		s = "\n" + tab
		string = "GridWorld: {\n\ndimensions: %s,\nepsilon: %s,\niterations: %s,\nagent: %s\nstate: \n%s"

		return string.replace("\n", s) % (str(self.dimensions), self.epsilon, self.iteration, str(self.agent).replace("\n", s), tab + str(self.state).replace("\n", s + tab)) + "\n}"

	def randomPosition(self):

		d = self.dimensions

		return Position(rand(d.x), rand(d.y))

	def sweep (self, algorithm, times=0):

		agent = self.agent.reset(self.randomPosition(), self.epsilon)
		state = self.state

		for _ in range(times):

			for x, row in enumerate(state.matrix):

				for y, value in enumerate(row):

					algorithm(agent, state)
					agent.setPosition(Position(x, y))

		self.iteration = times

		return self

	def episodic(self, algorithm, times):

		agent = self.agent.reset(self.randomPosition())
		state = self.state

		for _ in range(times):
			
			algorithm(agent, state)

			agent.setPosition(self.randomPosition())

		self.iteration = times

		return self

	def train (self, algorithm):

		agent = self.agent.reset(self.randomPosition())
		iterations = 0

		while agent.training():

			iterations += 1
			
			algorithm(agent, state)

			agent.setPosition(self.randomPosition())

		self.iteration = iterations

		return self

	def playOffStateValues (self, iterations):

		iteration = 0
		agent = self.agent.reset(self.randomPosition())
		state = self.state

		chosenMoves = []

		while iteration < iterations:

			iteration += 1

			direction = agent.choseBestAction(state)

			chosenMoves.append(direction)

			if state.inBounds(agent.evaluate(direction)):
				
				agent.move(direction)

			agent.policy.time.incriment(agent.position())
			agent.reward()

		self.iteration = iteration

		return self

	def playOffActionValues (self, iterations=float("inf")):

		iteration = 0
		agent = self.agent.reset(self.randomPosition())
		state = self.state
		position = Position(3,3)
		chosenMoves = []

		while not position.on(Position(0,0)) and not position.on(Position(4,4)) and iteration < iterations:

			iteration += 1

			direction = state.get(agent.position()).actions.max()

			chosenMoves.append(direction)

			if state.inBounds(agent.evaluate(direction)):
				
				agent.policy.time.incriment(position)
				agent.move(direction)

			agent.reward()
			position = agent.position()

		self.iteration = iteration

		print "moves: %s" % chosenMoves

		return self