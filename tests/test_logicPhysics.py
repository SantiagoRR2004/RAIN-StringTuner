import unittest
import logic
import physics
import random


class numTests(unittest.TestCase):
    numTests = 1000


class test_turnerPhysics(numTests):

    def test_lowerFrecuency(self):
        """
        We test that when the frequency is too low,
        the new frequency is higher.
        """

    def test_higherFrecuency(self):
        """
        We test that when the frequency is too high,
        the new frequency is lower.
        """

    def test_0Difference(self):
        """
        We test that when the difference is zero,
        the turn is around zero and the new
        frequency is almost the same.
        """

    def test_NegligibleDifference(self):
        """
        We test that when the difference is negligible,
        the turn is around zero and the new
        frequency is almost the same.
        """

    def test_MultipleTurns(self):
        """
        We test that when it does multiple turns,
        the frequency gets progressively closer to the
        desired frequency.
        """
