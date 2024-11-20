import unittest
import random
import guitars
import harplike
import numpy as np


class numTests(unittest.TestCase):
    numTests = 100
    timelimit = 10


class test_instrument(numTests):

    def test_5TurnsGuitar(self):
        """
        Checks if a guitar can be tuned in only 5 turns
        for each string. Each string is very close to the
        objective or very far from it.

        NOT POSSIBLE
        """
        t = 5

        nSuccess = 0
        averageTurns = []
        nStringSuccess = 0

        for _ in range(self.numTests):
            guitar = guitars.ClassicalGuitar()

            objective = guitar.frequencies
            actual = guitar.stringFrequencies

            nTurns = np.zeros(len(objective))

            for i in range(len(objective)):
                if random.random() < 0.5:
                    actual[i] = max(0, objective[i] + random.uniform(-5, 5))
                else:
                    actual[i] = max(0, objective[i] + random.uniform(-500, 500))

            guitar.calculateTightness()

            itTurns = guitar.tune(timeLimit=self.timelimit)

            for turns in itTurns:
                nTurns += np.where(turns != 0, 1, 0)

            if np.all(nTurns <= t):
                nSuccess += 1

            averageTurns.append(sum(nTurns)/len(nTurns))

            nStringSuccess += np.sum(np.where(nTurns <= t, 1, 0))

        print(f"Success rate: {100*nSuccess/self.numTests}%")
        print(f"Success rate per string: {100*nStringSuccess/(self.numTests*len(objective))}%")
        print(f"Average turns by string: {sum(averageTurns)/len(averageTurns)}")


    def test_12TurnsHarp(self):
        """
        Checks if a harp can be tuned in only 12 turns.
        We start with a harp that doesn't have any of
        the strings tightened.
        """
        t = 12

        nSuccess = 0
        averageTurns = []
        nStringSuccess = 0

        harp = harplike.Harp36String()

        nTurns = np.zeros(len(harp.frequencies))

        itTurns = harp.tune(timeLimit=self.timelimit)

        for turns in itTurns:
            nTurns += np.where(turns != 0, 1, 0)

        if np.all(nTurns <= t):
            nSuccess += 1

        averageTurns.append(sum(nTurns)/len(nTurns))

        nStringSuccess += np.sum(np.where(nTurns <= t, 1, 0))

        print(f"Success rate: {100*nSuccess}%")
        print(f"Success rate per string: {100*nStringSuccess/len(harp.frequencies)}%")
        print(f"Average turns by string: {sum(averageTurns)/len(averageTurns)}")

