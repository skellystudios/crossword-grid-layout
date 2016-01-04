import unittest
import generate
import numpy as np


class TestGenerateLayout(unittest.TestCase):

	def setUp(self):
		pass


	def tearDown(self):
		pass

	def test_neighbours(self):

		height, width = 3, 2
		matrix = np.full((height,width), None, object)

		self.assertEqual(
			set(generate.Grid.neighbours(matrix,0,0)),
			set([(0,1),(1,0)])
			)

		self.assertEqual(
			set(generate.Grid.neighbours(matrix,0,1)),
			set([(0,0),(1,1),(0,2)])
			)

		self.assertEqual(
			set(generate.Grid.neighbours(matrix,1,1)),
			set([(0,1),(1,0),(1,2),(2,1)])
			)





if __name__ == '__main__':
	unittest.main()