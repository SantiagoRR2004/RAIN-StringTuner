import unittest
import logic
import random


class numTests(unittest.TestCase):
    numTests = 1000


class test_turner(numTests):

    def test_lowerFrecuency(self):
        """
        We test that when the frequency is too low,
        the turn is positive.
        """

    def test_higherFrecuency(self):
        """
        We test that when the frequency is too high,
        the turn is negative.
        """

    def test_sameDifference(self):
        """
        We test that when the difference is the same,
        the absolute turn is the same.
        """

    def test_50Hz(self):
        """
        We test that when the difference is 50 Hz,
        the turn is 0.05 +/- 0.03.
        """

    def test_100Hz(self):
        """
        We test that when the difference is 300 Hz,
        the turn is 0.55 +/- 0.05.
        """
