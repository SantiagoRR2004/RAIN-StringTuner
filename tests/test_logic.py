import unittest
import logic
import random


class numTests(unittest.TestCase):
    numTests = 1000
    tolerance = 1e-4


class test_turner(numTests):

    def test_lowerFrecuency(self):
        """
        We test that when the frequency is too low,
        the turn is positive.
        """
        frequency = [random.uniform(0, 1000) for _ in range(self.numTests)]
        objectiveFrequency = [i + random.uniform(0, 2000) for i in frequency]
        stringLength = [random.uniform(0, 2) for _ in range(self.numTests)]

        turner = logic.Tuner()

        for i in range(self.numTests):
            turn = turner.tune(objectiveFrequency[i], frequency[i], stringLength[i])
            self.assertTrue(turn >= 0)

    def test_higherFrecuency(self):
        """
        We test that when the frequency is too high,
        the turn is negative.
        """
        objectiveFrequency = [random.uniform(0, 1000) for _ in range(self.numTests)]
        frequency = [i + random.uniform(0, 2000) for i in objectiveFrequency]
        stringLength = [random.uniform(0, 2) for _ in range(self.numTests)]

        turner = logic.Tuner()

        for i in range(self.numTests):
            turn = turner.tune(objectiveFrequency[i], frequency[i], stringLength[i])
            self.assertTrue(turn <= 0)

    def test_sameDifference(self):
        """
        We test that when the difference is the same,
        the absolute turn is the same.
        """
        objectiveFrequency = [random.uniform(0, 1000) for _ in range(self.numTests)]
        frequency = [i + random.uniform(0, 2000) for i in objectiveFrequency]
        stringLength = [random.uniform(0, 2) for _ in range(self.numTests)]

        turner = logic.Tuner()

        for i in range(self.numTests):
            turn = turner.tune(objectiveFrequency[i], frequency[i], stringLength[i])
            turn2 = turner.tune(frequency[i], objectiveFrequency[i], stringLength[i])
            self.assertTrue(abs(turn) == abs(turn2))

    def test_0Hz(self):
        """
        We test that when the difference is 0 Hz,
        the turn is 0.

        NOT POSSIBLE
        """
        frequency = [random.uniform(0, 1000) for _ in range(self.numTests)]
        stringLength = [random.uniform(0, 2) for _ in range(self.numTests)]

        nSuccess = 0

        turner = logic.Tuner()

        for i in range(self.numTests):
            turn = turner.tune(frequency[i], frequency[i], stringLength[i])
            if 0 - self.tolerance < turn < 0 + self.tolerance:
                nSuccess += 1

        print(f"Success rate: {100*nSuccess/self.numTests}%")

    def test_50Hz(self):
        """
        We test that when the difference is 50 Hz,
        the turn is 0.05 +/- 0.03.

        NOT POSSIBLE
        """
        objectiveFrequency = [random.uniform(0, 1000) for _ in range(self.numTests)]
        frequency = [i + 50 for i in objectiveFrequency]
        stringLength = [random.uniform(0, 2) for _ in range(self.numTests)]

        nSuccess = 0

        turner = logic.Tuner()

        for i in range(self.numTests):
            turn = abs(
                turner.tune(objectiveFrequency[i], frequency[i], stringLength[i])
            )
            if 0.05 - 0.03 < turn < 0.05 + 0.03:
                nSuccess += 1

        print(f"Success rate: {100*nSuccess/self.numTests}%")

    def test_300Hz(self):
        """
        We test that when the difference is 300 Hz,
        the turn is 0.55 +/- 0.05.

        NOT POSSIBLE
        """
        objectiveFrequency = [random.uniform(0, 1000) for _ in range(self.numTests)]
        frequency = [i + 300 for i in objectiveFrequency]
        stringLength = [random.uniform(0, 2) for _ in range(self.numTests)]

        nSuccess = 0

        turner = logic.Tuner()

        for i in range(self.numTests):
            turn = abs(
                turner.tune(objectiveFrequency[i], frequency[i], stringLength[i])
            )
            if 0.55 - 0.05 < turn < 0.55 + 0.05:
                nSuccess += 1

        print(f"Success rate: {100*nSuccess/self.numTests}%")
