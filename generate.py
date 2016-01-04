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

	def num_intersections(self):
		intersections = 0
		w, h = self.matrix.shape
		for x in range(w):
			for y in range(h):
				if self.matrix[x][y].checked:
					intersections += 1
		return intersections

	def unchecked_letters(self):
		unchecked = []
		w, h = self.matrix.shape
		for x in range(w):
			for y in range(h):
				if self.matrix[x][y].string and not self.matrix[x][y].checked:
					unchecked.append((self.matrix[x][y].string,x,y))
		return unchecked

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

		# calculate the offset between a and b
		offset = a_location - b_location

		# Now we create the new array. 
		height, width = Grid.calculate_grid_size(a, b, offset)
		a_holder = np.full((height,width), Letter(None), object)
		b_holder = np.full((height,width), Letter(None), object)

		# Calculate how much each grid should be offset against the new grid
		a_offset = Point(min(0, offset.x) * -1, min(0,offset.y) * -1) 
		b_offset = a_offset + offset

		(a_w, a_h) = a.shape
		(b_w, b_h) = b.shape
		
		# Add and b into their holders
		a_holder[a_offset.x:a_offset.x+a_w, a_offset.y:a_offset.y+a_h] = a_holder[a_offset.x:a_offset.x+a_w, a_offset.y:a_offset.y+a_h] + a
		b_holder[b_offset.x:b_offset.x+b_w, b_offset.y:b_offset.y+b_h] = b_holder[b_offset.x:b_offset.x+b_w, b_offset.y:b_offset.y+b_h] + b
		
		# We do two passes: the first to work out where there are going to be checked squares so we can 
		pass_one = a_holder + b_holder

		print pass_one

		# We now want to make sure that squares next to an already taken square are reserved white space
		# (Unless they're next to a square that becomes checked - will need to deal with that later)

		for x in range(height):
			for y in range(width):
				print "__________"
				print "__________"
				print "__________"
				print a_holder
				print b_holder
				print "" + str(x) + ", " + str(y)
				print a_holder[x][y]
				print Grid.neighbours(a_holder, x, y)
				neighbours = Grid.neighbours(a_holder, x, y)
				for x1, y1 in neighbours:
					if a_holder[x1][y1].string and not a_holder[x][y].string:
						a_holder[x][y] = a_holder[x][y].get_reserved()
						print "bingo a"
					if b_holder[x1][y1].string and not b_holder[x][y].string:
						b_holder[x][y] = b_holder[x][y].get_reserved()
						print b_holder[x][y]
						print "bingo b"
				for x1, y1 in neighbours:
					if pass_one[x1][y1].checked:
						print "wowzer"
						a_holder[x][y] = a_holder[x][y].get_unreserved()
						b_holder[x][y] = b_holder[x][y].get_unreserved()

		print ""
		print ""

		print a_holder
		print b_holder

		# Add them together, and save in result.
		# The add methods of Letter will deal with most of the matching work
		result.matrix = a_holder + b_holder

		return result 

	@staticmethod
	def calculate_grid_size(a, b, offset):
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

		return (height, width)

	@staticmethod
	def neighbours(matrix, x, y):
		X, Y = matrix.shape
		print X, Y
		return [(x2, y2) for x2 in range(x-1, x+2)
           for y2 in range(y-1, y+2)
           if (-1 < x <= X and
               -1 < y <= Y and
               (x != x2 or y != y2) and
               (x == x2 or y == y2) and # Not diagonal neighbours
               (0 <= x2 < X) and
               (0 <= y2 < Y))]


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
		self.reserved = False

	def __eq__(self, other):
		if not self.string or not other.string:
			return False
		else:
			return self.string == other.string

	def __repr__(self):
		if self.checked:
			return "@"
		if self.reserved and self.string:
			return "!"
		if self.reserved and not self.string:
			return "#"
		if self.string is None:
			return "_"
		return str(self.string)

	def __add__(self, other):
		if (self.reserved or other.reserved) and (self.string or other.string):
			raise UnallowableMerge("Can't merge next to each other")
		if self.string is None:
			return other.clone()
		if other.string is None:
			return self.clone()
		if self.string == other.string:
			result = self.clone()
			result.checked = True
			return result
		raise UnallowableMerge("Can't merge letters1")

	def __radd__(self, other):
		if (self.reserved or other.reserved) and (self.string or other.string):
			raise UnallowableMerge("Can't merge next to each other")
		if self.string is None:
			return other
		if other.string is None:
			return self
		if self.string == other.string:
			result = self.clone()
			result.checked = True
			return result
		raise UnallowableMerge("Can't merge letters2")

	def clone(self):
		letter = Letter(self.string)
		letter.reserved = self.reserved
		letter.checked = self.checked
		return letter

	def get_reserved(self):
		letter = self.clone()
		letter.reserved = True
		return letter

	def get_unreserved(self):
		letter = self.clone()
		letter.reserved = False
		return letter


def matching_points(a,b):
	return [
	 ((x1,y1),(x2,y2)) 
	 for (l1, x1, y1) in a.unchecked_letters() 
	 for (l2, x2, y2) in b.unchecked_letters()
	 if l1 == l2
	]





a = Grid().set_word("hello")
b = Grid().set_word("lol")
merged = a.merge(Point(0,2),b.rotated(),Point(2,0))

c = Grid().set_word("rofl")
d = Grid().set_word("ree")
merged_2 = c.merge(Point(0,0), d.rotated(), Point(0,0))

merged_2.merge(Point(0,3), merged, Point(0,2))




