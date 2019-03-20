from random import randint as random
from my_stuff.misc import init
from my_stuff.lists import delete_from_list, find_in_list
from math import inf as infinity

def a_star (initial_state, goal_cost = 0):
	"""
		A full, batteries-included A* search AI!
		To use, provide: 
			- a State class with: 
				- a "cost" attribute
				- an "expand" method -- must return State[]
				- a (unique!) format method
				- comparative methods
				- equality methods
			- an instance of the initial state
			- If the goal's cost is not 0, provide the cost
	"""
	from textwrap import dedent
	from trie import Trie
	from my_stuff.lists import Queue

	def Node (state, parent): return (state, parent)

	def expand_node (node):
		state, parent = node
		return [Node (change, node) for change in state.expand()]

	initial_node = Node (initial_state, parent = None)
	explored = Trie()
	frontier = Queue(initial_node, reverse = True)
	counter = 0
	while frontier:
		node = frontier.pop()
		for state, parent in expand_node (node):
			counter += 1
			if not counter % 1_000: print (dedent (f"""\
				Possibility number {counter:,}:
					Frontier: {len (frontier):,}.
					Explored: {len (explored):,}.
					Depth: {state.depth}.
					Current cost: {state.cost}.
			"""))
			if state.cost == goal_cost: return state, parent
			elif format (state) in explored: continue
			else: frontier.push (Node (state, parent))
		explored + format (node [0])
	return None

def a_star_no_path (
			initial_state, 
			goal_cost = 0, 
			print_self = False, 
			frequency = 1_000
		):
	from textwrap import dedent
	from trie import Trie
	from my_stuff.lists import Queue

	explored = Trie()
	frontier = Queue (initial_state, reverse = True)
	counter = 0
	while frontier:
		state = frontier.pop()
		for new_state in state.expand():
			counter += 1
			if not counter % frequency: 
				if not print_self: print (dedent (f"""\
					Possibility number {counter:,}:
						Frontier: {len (frontier):,}.
						Explored: {len (explored):,}.
						Current cost: {state.cost}.
				"""))
				else: print (new_state, end = "\r")

			if new_state.cost == goal_cost: return new_state
			elif format (new_state) in explored: continue
			else: frontier.push (new_state)
		explored + format (state)
	return None

def genetic_algorithm (State, size = 50, generations = 5_000, perfect = True):
	""" 
		Genetic algorithm, batteries included!
		State must be a class with following methods:
			total ordering based on cost: < is better!
			__bool__: is solution state
			random (no self): generate a random instance of the class
			cross (self, other): cross self with other
			mutate: mutate self
		size is the starting generation size
		generations is how many generations to do
			ignored if perfect
		perfect is whether or not there is a definite solution

	"""
	from random import randint as random
	from math import inf as infinity
	from bisect import insort_left as sorted_insert

	def generate_population(): return [
		State.random() 
		for _ in range (size)
	]

	def choose_random (population): return population [
		random (0, len (population) // 3)
	]

	if perfect: generations = infinity
	population = generate_population()
	population.sort()
	counter = 0
	while True:
		for _ in range (size // 2):
			state1 = choose_random (population)
			state2 = choose_random (population)
			state1, state2 = state1.cross (state2)
			if state1: return state1
			elif state2: return state2
			state1.mutate()
			state2.mutate()
			if state1: return state1
			elif state2: return state2
			sorted_insert (population, state1)
			sorted_insert (population, state2)
		counter += 1
		if counter == generations: break
	result = min (population)
	if perfect and not result: raise RecursionError
	else: return result

def genetic_cross (one, two):
	index = random (1, len (one) - 2)
	one_first, one_last = one [:index], one [index:]
	two_first, two_last = two [:index], two [index:]
	return one_first + two_last, two_first + one_last

def _minimax_search (state, max_: bool, alpha, beta, override, depth = 0):
	if state.finished: return state.utility()
	elif depth > override: return state.heuristic()
	else: 
		result = -infinity if max_ else infinity
		for child in state.expand():
			if max_: beta = result
			else: alpha = result
			value = _minimax_search (child, not max_, alpha, beta, override, depth + 1)
			if max_ and value > result: result = value
			elif not max_ and value < result: result = value
			if max_ and result > alpha: break
			elif not max_ and result < beta: break
		return result

def minimax (starter_state, override = infinity):
	"""
		Requires a State class to be passed in
		State must include the following: 
			
			- finished: attr, bool
			- expand():=> List <State>
			- utility() => int V float
			- optional heuristic() => int V float (maybe large range)
	"""
	running_max = -infinity
	result = None
	for child in starter_state.expand():
		value = _minimax_search (child, False, infinity, -infinity, override = override)
		if value > running_max: 
			running_max = value
			result = child
	return result

class Node:
	@init
	def __init__(self, id, domain = None): 
		self.neighbors = []
		self.arcs = 0
	def __eq__(self, other): type (other) is Node and other.id == self.id
	def __repr__(self): return f"Node ({self.id})"
	def before(self, *nodes): 
		for node in nodes: 
			self.neighbors.append (node)
			node.arcs += 1

class OrderedCSP:
	
	def get_node(nodes, id_): 
		for node in nodes: 
			if node.id == id_: return node
		else: raise ValueError(f"Cannot find node {id_} in {nodes}")

	def __new__(cls, names, constraints): 
		if type (names) is int: nodes = [Node (n + 1) for n in range (names)]
		else: nodes = [Node (name) for name in names]

		for before, after in constraints: 
			first_node = cls.get_node (nodes, before)
			second_node = cls.get_node (nodes, after)
			first_node.before (second_node)

		csp = object.__new__(cls)
		csp.__init__(nodes, range (len (nodes)))
		return [node.id for node in csp.solve()]

	@init
	def __init__ (self, nodes, domain = None): 
		self.result = []
		if domain is not None: 
			domain = list (domain)
			for node in nodes:
				node.domain = domain.copy()

	def get_arc_count(self, node: Node): 
		return len ([
			node2
			for node2 in self.nodes 
			if node in node2.neighbors
		])

	def detach (self, nodes): 
		for node in nodes: 
			for neighbor in node.neighbors: 
				neighbor.arcs -= 1

	def get_nodes(self, num_arcs): 

		arcs = {}
		for node in self.nodes:
			if node in self.result: continue
			if node.arcs in arcs: 
				arcs [node.arcs].append (node)
			else: arcs [node.arcs] = [node]

		if not arcs: return []

		result = arcs [min (arcs)]
		self.detach (result)
		return result

	def solve(self): 
		for arc_count in range (len (self.nodes)): 
			nodes = self.get_nodes (arc_count)
			self.result.extend (nodes)
		return self.result
