from operator import mul as multiply
from functools import reduce

ALPHABET = list ("abcdefghijklmnopqrstuvwxyz")
VOWELS = list ("aeiou")

def average (*nums): return sum (nums) / len (nums)
def product (List): return reduce (multiply, List)
def consecutive (List): return List == list (
	range (List [0], List [0] + len (List))
)

def evens_of_list (List): 
	from my_stuff.nums import is_even
	return list (filter (is_even, List))

def flatten (List):
	temp = []
	for thing in List:
		if type (thing) is list: temp.extend (thing)
		else: temp.append (thing)
	return temp

def median (List):
	List = sorted (List)
	if even (len (List)): return average (List [len (List) // 2], List [len (List) // 2 - 1])
	else: return List [len (List) // 2]

def remove_duplicates (List):
	newList = []
	[newList.append (x) for x in List if x not in newList]
	return newList

def delete_from_list (List, indices):
	for i, index in enumerate (indices): List.pop (index - i)

def _next (List, index):
	if index == len (List) - 1: index = -1
	return List [index + 1], index + 1

def bubble_sort (List):
	for index in range (len (List)):
		for index2 in range (len (List) - 1, -1 + index, -1):
			if index2 - index and List [index2] < List [index2 - 1]: 
				List [index2], List [index2 - 1] = List [index2 - 1], List [index2]

def insertion_sort (List):
	insertion_sort.__annotations__ ["runtime"] = f"O({((len (List) ** 2) / 2) + (len (List) / 2)})"
	for index, num in enumerate (List):
		if not index: continue
		while List [index] < List [index - 1]: 
			if not index: break
			List [index], List [index - 1] = List [index - 1], List [index]
			index -= 1

def merge_sort (List): 
	if len (List) == 1: return List
	middle = len (List) // 2
	left = merge_sort (List [:middle])
	right = merge_sort (List [middle:])
	return _merge (left, right)

def _merge (left, right):
	result = []
	left_index = 0
	right_index = 0
	while True:
		if left_index > len (left) - 1: 
			result.extend (right [right_index:])
			break
		elif right_index > len (right) - 1: 
			result.extend (left [left_index:])
			break

		a = left [left_index] 
		b = right [right_index]
		if a < b: 
			result.append (a)
			left_index += 1
		else: 
			result.append (b)
			right_index += 1

	return result

def remove_adjacent(List):
	indices = [
		index 
		for index, num in enumerate (List, 1) 
		if index < len (List) and List [index - 1] == num
	]
	delete_from_list (List, indices)
	return List

def binary_search (List, thing, start = 0, end = None, reverse = False):
	"""The reverse kwarg is for if the list is sorted in reverse"""
	if end is None: end = len (List) - 1
	middle = (start + end) // 2
	element = List [middle]
	if element == thing: return middle
	elif (element > thing and not reverse) or (element < thing and reverse):
		try: return binary_search (List, thing, start = start, end = middle, reverse = reverse)
		except RecursionError: return None
	elif (element < thing and not reverse) or (element > thing and reverse): 
		try: return binary_search (List, thing, start = middle + 1, end = end, reverse = reverse)
		except RecursionError: return None

def ternary_search (List, thing, start = 0, end = None, reverse = False):
	if end is None: end = len (List)
	if end - start == 1: 
		element = List [start]
		if reverse: 
			if element > thing: return end
			elif element < thing: return start
		else: 
			if element < thing: return end 
			elif element > thing: return start
	if end - start == 2:
		if reverse: 
			if List [start] <= thing: return start
			elif List [start] >= thing >= List [start + 1]: return start + 1
			elif List [start + 1] >= thing >= List [end - 1]: return end - 1
			elif List [end - 1] >= thing: return end
			else: raise ValueError (f"{List [start : end]} \n {thing}")
		else: 
			if List [start] >= thing: return start
			elif List [start] <= thing <= List [start + 1]: return start + 1
			elif List [start + 1] <= thing <= List [end]: return end - 1
			elif List [end] <= thing: return end
			else: raise ValueError (f"{List [start : end]} \n {thing}")
	distance = (end - start) // 3
	one = start + distance
	two = one + distance
	element_one = List [one]
	element_two = List [two]
	if List [start] == thing: return start
	elif List [end - 1] == thing: return end
	elif element_one == thing: 
		move = 1 if reverse else -1
		while element_one == thing: 
			one += move
			try: element_one = List [one]
			except IndexError: return one - move
		return one
	elif element_two == thing: 
		move = 1 if reverse else -1
		while element_two == thing: 
			two += move
			try: element_two = List [two]
			except IndexError: return two - move
		return two
	elif reverse: 
		if thing > element_one: return ternary_search (List, thing, start = start, end = one, reverse = reverse)
		elif element_one > thing > element_two: return ternary_search (List, thing, start = one, end = two, reverse = reverse)
		elif element_two > thing: return ternary_search (List, thing, start = two, end = end, reverse = reverse)
	else: 
		if List [start] < thing < element_one: return ternary_search (List, thing, start = start, end = one, reverse = reverse)
		elif element_one < thing < element_two: return ternary_search (List, thing, start = one, end = two, reverse = reverse)
		elif element_two < thing < List [end - 1]: return ternary_search (List, thing, start = two, end = end, reverse = reverse)

def sorted_insert (List, thing, reverse = False):
	if not List: return List.append (thing)
	assert List
	index = ternary_search (List, thing, reverse)
	assert type (thing) is type (List [0]), f"{List}, {thing}"
	List.insert (index, thing)	

def find_in_list (List, condition, value = "value"):
	if type (List) is not list: 
		raise TypeError (
			"Arguments to 'my_stuff.lists.find_in_list' should be of the format:"
			" List, condition (func), value = {value | index | both}"
		)
	for index, thing in enumerate (List): 
		if condition (thing):
			if value == "value": return thing
			elif value == "index": return index
			elif value == "both": return index, thing
			else: raise ValueError (f"find_in_list got incorrect value: {value}")

class Queue:
	"""
		We need three operations from this class: push, pop, and find. 
		I think the quickest way to do this is with a sorted list
		However, the list will have to be reversed to mantain constant pop time
			Push: ternary search for index -- O (log (n, base = 3))
			Pop: regular pop -- constant time
			Find: binary search -- logarithmic time

		Attributes: 
			- elements: a sorted list of all the nods
			- reverse: Should the list be sorted in reverse?
		Methods: 
			- bool: check for emptiness
			- push: Insert element, maintain sortedness
			- pop: regular pop
			- thing in self: binary search for element
	"""
	def __init__ (self, element, reverse): 
		self.elements = [element]
		self.reverse = reverse

	def __iter__ (self): return iter (self.elements)
	def __len__ (self): return len (self.elements)
	def __bool__ (self): return bool (len (self))
	def __repr__ (self): return " | ".join (map (repr, self.elements))

	def __contains__ (self, other):
		"""Since we are maintaining a sorted list, a binary search will work"""
		if not len (self.elements): return False
		return binary_search (self.elements, other, reverse = self.reverse) is not None

	def pop (self): 
		return self.elements.pop()

	def push (self, other):
		"""Find the index to insert the element"""
		if not self.elements: return self.elements.append (other)
		index = ternary_search (self.elements, other, reverse = self.reverse)
		self.elements.insert (index, other)

	def replace (self, index, replacement):
		self.elements.pop (index)
		self.push (replacement)

def contains_more_than (List, element, n):
	"""Short-circuiting replacement for List.count (element) > n"""
	count = 0
	for thing in List:
		if thing == element: count += 1
		if count > n: return True
	else: return False

def split_list (List, n, fill = None):
	"""grouper(3, 'ABCDEFG', 'x') --> ABC DEF Gxx"""
	from itertools import zip_longest
	args = [iter(List)] * n
	return list (zip_longest(fillvalue=fill, *args))


def get_subsets(List: list, target, length: int = None): 
	from itertools import product
	smallest: int = abs (min (List))
	new_list: int = [num + smallest for num in List]
	results: list = []
	for instruction in product ( (1, 0), repeat = len (List)): 
		copy = [
			(index, num)
			for index, (keep, num) in enumerate (
				zip (instruction, new_list)
			)
			if keep
		]
		new_target = target + (smallest * len (copy))
		result = 0
		for index, num in copy: 
			result += num
			if result > new_target: break
		else: 
			if result == new_target: results.append (
				[List [index] for index, num in copy]
			)
	return results
