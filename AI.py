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

# class CSP_Node: 
# 	@init
# 	def __init__ (self, name, constraint = lambda a, b, c: True, domains = None): self.neighbors = []
# 	def __eq__ (self, other): return self.name == other.name
# 	def __repr__ (self): return f"Node ({self.name})"
# 	def set_neighbors (self, *nodes): 
# 		self.neighbors.extend (nodes)
# 		for node in nodes: 
# 			if self not in node.neighbors: node.set_neighbors(self)

class CSP: 
	@init
	def __init__ (self, nodes, domain = None):
		if domain is not None: 
			if type (domain) is not list: 
				raise TypeError ("my_stuff.ai.CSP: 'domain' must be of type 'list'")
			for node in nodes: node.domain = domain.copy()
		self.arcs = self.get_arcs()
		self.verify_arcs()

	def verify_arcs(self): 
		for node in self.nodes: 
			for neighbor in node.neighbors: 
				if node not in neighbor.neighbors:
					raise ValueError (
						f"{node} is not recognized as a neighbor of {neighbor}!"
					)

	def get_arcs (self): 
		arcs = []
		for node in self.nodes: 
			for other_node in node.neighbors:
				arcs.append ( (node, other_node) )
		return arcs

	def ac3 (self): 
		queue = list (self.arcs)

		while queue: 
			node_one, node_two = queue.pop(0)
			if self.filter (node_one, node_two): 
				if not node_one.domains: return False
				else: # double check against everyone else
					for node in node_one.neighbors:
						if node == node_two: continue
						queue.append ( (node_one, node) )
		return True

	def filter (self, node_one, node_two): 
		filtered = False
		to_remove = []
		for index, value in enumerate (node_one.domains):
			if not find_in_list (
					node_two.domains,
					lambda val: node_one.constraint(node_two.name, value, val)
					# lambda val: self.test_constraint (node_one, node_two, value, val)
					# lambda val: node_one.test_constraint (node_two, (value, val) )
			): 
					to_remove.append (index)
					filtered = True

		delete_from_list (node_one.domains, to_remove)
		return filtered

	def show_values (self):
		for node in self.nodes: 
			print (f"Possible values for {node.name}: {node.domains}")

	def _choose (self, chosen_node, value):
		set_later = []
		for node in self.nodes: 
			if node == chosen_node or value not in node.domains: 
				set_later.append (node.domains)
				continue
			temp_domains = set (node.domains)
			temp_domains.remove (value)
			if len (temp_domains) == 0: return False
			else: set_later.append (temp_domains)
		else: 
			for node, domain in zip (self.nodes, set_later):
				if node == chosen_node: continue
				else: node.domains = domain 
			return True

	def select_path (self, first_node = None, first_value = None):
		if first_node is not None and first_value is not None: 
			self._choose (first_node, first_value)
			starting_index = 1
		else: starting_index = 0

		for node in self.nodes [starting_index:]:
			for value in node.domains: 
				if self._choose (node, value): break
				else: continue

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
	def __init__(self, id, test, domain = None): 
		self.neighbors = []
		self.arcs = 0
	def __eq__(self, other): type (other) is Node and other.id == self.id
	def __repr__(self): return f"Node ({self.id})"
	def set_neighbors(self, *nodes): 
		for node in nodes: 
			self.neighbors.append (node)
			self.arcs += 1

class CSP:
	@init
	def __init__ (self, nodes, domain = None): 
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

	def get_node(self, num_arcs): 
		result = min (self.nodes, key = lambda node: node.arcs)
		if result.arcs > num_arcs: 
			raise ValueError(
				f"{result} has {result.arcs} arcs, expected {num_arcs} arcs."
			)
		else: return result

	