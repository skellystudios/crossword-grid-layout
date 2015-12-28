from random import *

def mutate(candidate):

	(grid, remaining_words) = item

	# either do a translation or an insertion
	if random:
		return translate(grid, remaining_words)

	else:
		return insertion(grid, remaining_words)


def insertion(grid, remaining_words):

	# select a random word from the list
	

	""" 
	
	HOW DO WE FIND OUT IF THERE IS 
	SOMEWHERE WE CAN INSERT A WORD? 
	
	"""
	pass

def translate(grid, remaining_words):

	# select a word to translate, and move it to a random location

	"""

	SHALL WE JUST MAKE ANY SORT OF TRANSLATION AND SEE WHAT HAPPENS?
	Is there ever a situation where a translation would be useful

	"""
	pass


def fitness(grid, remaining_words):

	"""

	Criteria: 
	- not enough blank spaces = fail
	- non-contiguous (is this an issue?)
	- words overlapping in an unacceptable way (will the represenation allow this?)

	- number of words used (good)
	- number of intersections (good)

	"""
	pass


def check_insertion():
	pass







	
