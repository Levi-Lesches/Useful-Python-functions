def censor (text, sensitive): return text.lower().replace (
	key.lower(), "*" * len (key)
)

def pig_latin (word): return word [1:] + word [0].lower() + "ay"

def remove_vowels (text):
	from my_stuff.lists import vowels
	return "".join (filter (lambda char: char not in vowels, text))

def insert_word (text, word, index):
	words = text.split()
	words.insert (index, word)
	return " ".join (words)

def palindrome (word):
	from my_stuff.nums import is_even
	word = word.lower()
	middle = len (word) // 2
	if not is_even (len (word)): 
		new_word = list (word)
		new_word.pop (middle)
		word = "".join (new_word)
		middle = len (word) // 2
	return word [:middle] == "".join (reversed (word [middle:]))

def find_closing_paren (word: str, starting_index: int) -> int: 
	count = 1
	for index, letter in enumerate (word [starting_index + 1:]):
		if letter == "(": count += 1
		elif letter == ")":
			count -= 1
			if not count: return index + starting_index + 1

def find_opening_paren (word: str, starting_index: int) -> int:
	count = 1
	for index, letter in enumerate (word [starting_index - 1::-1]):
		if letter == ")": count += 1
		elif letter == "(": 
			count -= 1
			if not count: return starting_index - index - 1

def consume_int (string, starting_index) -> (int, int):
	result = ""
	index = starting_index
	while True:
		try: letter = string [index]
		except IndexError: break
		else: 
			if letter.isdigit(): result += letter
			else: break
		index += 1
	if not result: result = None
	else: result = int (result)
	return result, index