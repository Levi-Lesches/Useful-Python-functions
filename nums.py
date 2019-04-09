def is_even (num): return not num % 2
def factorial (num):
	from my_stuff.lists import product
	return product (range (1, num + 1))
def nCr (n, r): return factorial (n) / factorial (r) * factorial (n - r)
def distance (a, b): return abs (a - b)
def sum_digits (num): return sum (map (int, str (num)))

def is_prime (num): return not any (
	not num % n 
	for n in range (2, int (num ** 0.5) + 1)
)
def digit_analysis (num):
	num = str (num) [::-1]
	bases = []
	for index, digit in enumerate (num): 
		base = int ("1" + "0" * index)
		value = int (digit) * base
		bases.append (value)
	return bases [::-1]

def add (a, b): # got a, b to be bools
	a, b = [map (bool, bin (num) [:1:-1]) for num in (a, b)] 
	result = ""
	carry = False
	for bit in range (max ([len (a), len (b)]) + 1): 
		bit_a = False if len (a) - 1 < bit else bool (int (a [bit]))
		bit_b = False if len (b) - 1 < bit else bool (int (b [bit]))
		result += str (int (a ^ b ^ carry))
		carry = a & b | (a ^ b) & carry
	return int (result [::-1], 2)

def _subtract (a, b): #needs improvement
	if a < b: raise ValueError (f"{a} needs to be bigger than {b}.")
	a, b = [bin (num) [:1:-1] for num in [a, b]]
	result = ""
	carry = False
	for bit in range (max ([len (a), len (b)])):
		bit_a, bit_b = [False if len (num) - 1 < bit else bool (int (num [bit])) for num in [a, b]]
		result += str (int (xor (xor (bit_a, bit_b), carry)))
		# carry = (bit_a and bit_b and carry) or (not bit_a and bit_b)
		carry = (not a or carry) and b
	return int (result [::-1], 2)

def _test(): #tests subtraction
	from itertools import product
	nums = remove_duplicates (product (range (1, 10), repeat = 2))
	for num in nums:
		Max = max (num)
		Min = min (num)
		if subtract (Max, Min) != Max - Min: print (f"{Max} - {Min} = {subtract (Max, Min)}")

def clock_angle (hours, minutes):
	angle = abs (30 * (hours - ((11 * minutes) / 60)))
	return 360 - angle if angle > 180 else angle

def circle_segment (r, c):
	from math import pi, asin, degrees, radians, sqrt
	angle = round (degrees (asin (c / (2 * r)))) # gonna be an int anyway
	triangle_area = (c * sqrt (r ** 2 - ((c / 2) ** 2))) / 2
	sector_area = pi * (r ** 2) * angle / 180
	area = sector_area - triangle_area
	return area 

def triples (n):
	assert n % 2, f"n ({n}) must be odd"
	return n, (n ** 2 - 1) // 2, (n ** 2 + 1) // 2

def quadratic (a, b, c):
	from math import sqrt
	return (
		(-b + sqrt (
			b ** 2 - (4 * a * c)
		)) / 2 * a
	,
		(-b - sqrt (
			b ** 2 - (4 * a * c)
		)) / 2 * a)
