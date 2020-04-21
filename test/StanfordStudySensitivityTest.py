import unittest
import math
from StanfordStudySensitivity import *

class TestMethods(unittest.TestCase):

	s = StanfordStudySensitivity()

	def test_adjust_to_implied_fatality_rate(self):
		self.assertEqual(self.s.adjust_to_implied_fatality_rate(10,100,1000,25),25)
		self.assertEqual(self.s.adjust_to_implied_fatality_rate(0,100,1000,25),0)

	def test_id(self):
		self.assertEqual(self.s.id(10,100,1000,25),10)
		self.assertEqual(self.s.id(0,100,1000,25),0)

	def test_adjust_to_implied_cases(self):
		self.assertEqual(self.s.adjust_to_implied_cases(10,100,1000),100)
		self.assertEqual(self.s.adjust_to_implied_cases(0,100,1000),0)

	def test_adjust_to_implied_us_deaths(self):
		self.assertEqual(self.s.adjust_to_implied_us_deaths(10,100,1000,25,10000),2500)
		self.assertEqual(self.s.adjust_to_implied_us_deaths(0,100,1000,25,10000),None)

	def test_determine_adjusted_cases(self):
		self.assertEqual(self.s.determine_adjusted_cases(1000,10,1,1),10)
		self.assertEqual(self.s.determine_adjusted_cases(1000,10,0.5,1),20)
		self.assertEqual(int(round(self.s.determine_adjusted_cases(1000,10,1,0.995))),5)
		self.assertEqual(int(round(self.s.determine_adjusted_cases(1000,10,0.5,0.995))),10)

	def test_compute_binomial_variance_normal(self):
		self.assertEqual(self.s.compute_binomial_variance_normal(100,0.5),25)

	def test_compute_binomial_ci_normal(self):
		self.assertEqual(map(round,self.s.compute_binomial_ci_normal(100,0.5,0.95)),[40,60])


if __name__ == '__main__':
    unittest.main()
