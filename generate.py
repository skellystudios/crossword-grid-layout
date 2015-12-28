import numpy as np
import operator

"""

OK, so we want 

unchecked_letters :: grid -> [(letter, position)]

merge :: grid -> position -> grid -> position -> Maybe grid

words :: grid -> [words]


"""


class Grid():

	# ok, we'll start off by representing it as a NxM array, and a list of words. 
	# We'll see what needs to be changed from there
	def __init__(self):
		pass

	def set_word(self, word):
		self.words = [word]
		self.matrix = np.array([map(lambda x: Letter(x), list(word))])
		return self

	def __repr__(self):
		return str(self.matrix)

	def rotated(self):
		"""
		
		Returns a version of the grid rotated 90 degrees clockwise. 
		Should only be done for single word arrays that haven't already been rotated
		
		"""

		grid = Grid()
		grid.words = self.words
		grid.matrix = np.rot90(self.matrix, 3) # Rotates 270 counter-clockwise
		return grid


	def merge(self, a_location, b_grid, b_location):
		"""
		
		Merges two grids together, joining them together at the two locations

		TODO: Performs checks to ensure
		- All the overlapping letters are correct
		- No words end up adjacent and parallel

		For example, joining target on (1,1) with source on (2,1)

		target = 00  01  02 03       
		         10 [11] 12 13
		         20  21  22 24
		         30  31  32 34

		source = 00  01 02 03
		         10  11 12 13
		        [20] 21 22 24
		         30  31 32 34

		 should give

		 result = 
				 	 00  01 02 03
		         00	 10  11 12 13
		         10	[20] 21 22 24
		         20	 30  31 32 34
		         30  31  32 34
		
		"""	
		a = self.matrix
		b = b_grid.matrix
		result = Grid()

		# Calculate the words section
		if set(self.words) & set(b_grid.words):
			raise UnallowableMerge("Two grids already have words used in common")
		result.words = list(set(self.words) & set(b_grid.words))

		# calculate how much to offset each call for B by
		offset = a_location - b_location
		print offset
		# for each item in a (TODO: optimise to only use the overlapping portions) 
		# check that the letters match

		# for (x,y), a_val in np.ndenumerate(a):
		# 	adjusted = Point(x,y) + offset

		# 	try:
		# 		b_val = b[adjusted.x][adjusted.y]
		# 	except IndexError:
		# 		continue
		# 	if b_val != a_val:
		# 		raise UnallowableMerge()


		# Now we create the new array. There's probably a smarter way of doing this, but there you go.
		# calculate the bounds of the new array
		(a_w, a_h) = a.shape
		(b_w, b_h) = b.shape
		b_x_min = offset.x 
		b_x_max = b_w + offset.x
		b_y_min = offset.y
		b_y_max = b_h + offset.y

		x_min = min(0, b_x_min)
		x_max = max(a_w, b_x_max)
		y_min = min(0, b_y_min)
		y_max = max(a_h, b_y_max)

		height = x_max - x_min
		width = y_max - y_min

		a_offset = Point(min(0, offset.x) * -1, min(0,offset.y) * -1) 
		b_offset = a_offset + offset
		
		a_holder = np.full((height,width), Letter(None), object)
		b_holder = np.full((height,width), Letter(None), object)

		# Add a onto the holder
		a_holder[a_offset.x:a_offset.x+a_w, a_offset.y:a_offset.y+a_h] = a_holder[a_offset.x:a_offset.x+a_w, a_offset.y:a_offset.y+a_h] + a
		b_holder[b_offset.x:b_offset.x+b_w, b_offset.y:b_offset.y+b_h] = b_holder[b_offset.x:b_offset.x+b_w, b_offset.y:b_offset.y+b_h] + b
		result.matrix = a_holder + b_holder
		print a_holder
		print b_holder
		print result
		return result 



class UnallowableMerge(Exception):
		pass


class Point():

	def __init__(self, x, y):
		self.x = x
		self.y = y

	def __repr__(self):
		return "{self.x}, {self.y}".format(**locals())

	def __add__(self, p):
		return Point(self.x+p.x, self.y+p.y)

	def __sub__(self, p):
		return Point(self.x-p.x, self.y-p.y)


class Letter():

	def __init__(self, letter):
		self.string = letter
		self.checked = False

	def __repr__(self):
		if self.string is None:
			return "_"
		return str(self.string)

	def __add__(self, other):
		if self.string is None:
			return other
		if other.string is None:
			return self
		if self.string == other.string:
			self.checked = True
			return self
		raise UnallowableMerge("Can't merge letters1")


	def __radd__(self, other):
		if self.string is None:
			return other
		if other.string is None:
			return self
		if self.string == other.string:
			self.checked = True
			return self
		raise UnallowableMerge("Can't merge letters1")


a = Grid().set_word("hello")
b = Grid().set_word("lol")
merged = a.merge(Point(0,2),b.rotated(),Point(2,0))

c = Grid().set_word("rofl")
d = Grid().set_word("ree")
merged_2 = c.merge(Point(0,0), d.rotated(), Point(0,0))


merged_2.merge(Point(0,3), merged, Point(0,2))

