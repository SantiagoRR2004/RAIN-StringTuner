import unittest
import random
import guitars
import harplike


class numTests(unittest.TestCase):
    numTests = 100
    timelimit = 10


class test_instrument(numTests):

    def test_5TurnsGuitar(self):
        """
        Checks if a guitar can be tuned in only 5 turns
        for each string. Each string is very close to the
        objective or very far from it.
        """

        for _ in range(self.numTests):
            guitar = guitars.ClassicalGuitar()

            objective = guitar.frequencies
            actual = guitar.stringFrequencies

            for i in range(len(objective)):
                if random.random() < 0.5:
                    actual[i] = max(0, objective[i] + random.uniform(-5, 5))
                else:
                    actual[i] = max(0, objective[i] + random.uniform(-500, 500))

            guitar.calculateTightness()

            self.assertLessEqual(len(guitar.tune(timeLimit=self.timelimit)), 5)

    def test_12TurnsHarp(self):
        """
        Checks if a harp can be tuned in only 12 turns.
        We start with a harp that doesn't have any of
        the strings tightened.
        """

        harp = harplike.Harp36String()

        self.assertLessEqual(len(harp.tune(timeLimit=self.timelimit)), 12)
