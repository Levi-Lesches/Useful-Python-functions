from random import randrange as random

def xor (a, b): return a != b
def nand (a, b): return not (a and b)
def nor (a, b): return not (a or b)
def xnor (a, b): return a == b

def one_in_three (a, b, c): return (
	nand (a, b) and 
	xor (
		xor (a, b),
		c
	)
)

def rand_bool(): 
	return bool (random (2))