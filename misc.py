from os import chdir as cd, system

def pause (message = "Press Enter to continue"): input (message + " ")
def cwd(): system ("cd")

def military_time (time): 
	suffix = -2
	minutes = 2
	if time [suffix] == "A": return time [:suffix]
	else: return str (int (time [:minutes]) + 12) + time [minutes:suffix]

def cls(): 
	from os import system
	system ("cls")
	
def get_letter_grade (score):
	if score >= 90: return "A"
	elif score >= 80: return "B"
	elif score >= 70: return "C"
	elif score >= 60: return "D"
	else: return "F"

def scrabble_score(word):
	score = {"a": 1, "c": 3, "b": 3, "e": 1, "d": 2, "g": 2, "f": 4, "i": 1, "h": 4, "k": 5, "j": 8, "m": 3, "l": 1, "o": 1, "n": 1, "q": 10,"p": 3, "s": 1, "r": 1, "u": 1, "t": 1, "w": 4, "v": 4, "y": 4, "x": 8, "z": 10, " ": 0}
	return sum ([score [letter] for letter in word.lower()])

def veripy (category, message, List = None, errorMessage = None):
	if category not in [bool, str, int, float]: raise ValueError (f"argument category for Veripy was invalid: {category}. Change it to one of: bool, str, int, float")
	starting = True
	if category is bool:
		types = ["yes", "y", "no", "n"]
		while starting or response not in types:
			if starting: starting = not starting
			else: print ("Please choose either yes or no. (y or n)\n")
			try: response = input (message + " ")
			except KeyboardInterrupt: quit()
			else:
				if response in types [:2]: return True
				elif response in types [2:]: return False
				else: continue
	while True:
		try: response = category (input (message + " "))
		except KeyboardInterrupt: 
			print ()
			quit()
		except: continue
		else: 
			if List is not None:
				if response in List: break
				else: 
					print (
						errorMessage 
						if errorMessage is not None 
						else 
						f"Please choose one of: {', '.join (map (str, List))}.")
					continue
			if category is str:
				if all (word.isalpha() for word in response.split()): break
				else: continue
			break
	return response

def format_time (seconds):
	minutes, seconds = divmod (seconds, 60)
	hours, minutes = divmod (minutes, 60)
	if hours > 12: 
		hours -= 12
		suffix = "PM"
	else: suffix = "AM"
	return ":".join ([str (num).zfill (2) for num in (hours, minutes, seconds)]) + suffix

def init (func):
	"""This decorator automatically applies args to the object"""
	from inspect import signature
	def dec (*args, **kwargs):
		new_args = signature (func).bind (*args, **kwargs)
		new_args.apply_defaults()
		new_args = new_args.arguments
		self = new_args.popitem (last=False) [1]
		# for arg in new_args: self.__dict__ [arg] = new_args [arg]
		for arg in new_args: setattr (self, arg, new_args [arg])
		func (*args, **kwargs)
	return dec

def _loading (condition, globals, locale = None):
	from itertools import cycle
	from time import sleep
	loading = cycle (["|", "/", "-", "\\"])
	while not eval (condition, globals, locale):
		print (next (loading), end = "\r")
		sleep (.1)

def wait (seconds): 
	from time import time
	old = int (time()) + seconds
	_loading ("old < int (time())", globals = {}, locale = {"old": old, "time": time})
