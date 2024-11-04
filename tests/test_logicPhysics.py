import unittest
import logic
import physics
import random


class numTests(unittest.TestCase):
    numTests = 1000
    tolerance = 1e-4


class test_turnerPhysics(numTests):

    def test_lowerFrecuency(self):
        """
        We test that when the frequency is too low,
        the new frequency is higher.
        """
        stringLength = [random.uniform(0, 2) for _ in range(self.numTests)]
        elasticModulus = [random.uniform(0, 10**10) for i in range(self.numTests)]
        densities = [random.uniform(0, 20000) for i in range(self.numTests)]
        stringTight = [i + random.uniform(0, 1) for i in stringLength]

        frequency = [
            physics.calculateStringNewFrequency(
                stringLength[i], stringTight[i], 0, elasticModulus[i], densities[i]
            )
            for i in range(self.numTests)
        ]
        objectiveFrequency = [i + random.uniform(0, 2000) for i in frequency]

        turner = logic.Tuner()

        for i in range(self.numTests):
            newFrequency = physics.calculateStringNewFrequency(
                stringLength[i],
                stringTight[i],
                turner.tune(objectiveFrequency[i], frequency[i], stringLength[i]),
                elasticModulus[i],
                densities[i],
            )
            self.assertTrue(newFrequency >= frequency[i])

    def test_higherFrecuency(self):
        """
        We test that when the frequency is too high,
        the new frequency is lower.
        """
        stringLength = [random.uniform(0, 2) for _ in range(self.numTests)]
        elasticModulus = [random.uniform(0, 10**10) for i in range(self.numTests)]
        densities = [random.uniform(0, 20000) for i in range(self.numTests)]
        stringTight = [i + random.uniform(0, 1) for i in stringLength]

        frequency = [
            physics.calculateStringNewFrequency(
                stringLength[i], stringTight[i], 0, elasticModulus[i], densities[i]
            )
            for i in range(self.numTests)
        ]
        objectiveFrequency = [min(i - random.uniform(0, 1000), 0) for i in frequency]

        turner = logic.Tuner()

        for i in range(self.numTests):
            newFrequency = physics.calculateStringNewFrequency(
                stringLength[i],
                stringTight[i],
                turner.tune(objectiveFrequency[i], frequency[i], stringLength[i]),
                elasticModulus[i],
                densities[i],
            )
            self.assertTrue(newFrequency <= frequency[i])

    def test_0Difference(self):
        """
        We test that when the difference is zero,
        the turn is around zero and the new
        frequency is almost the same.
        """
        stringLength = [random.uniform(0, 2) for _ in range(self.numTests)]
        elasticModulus = [random.uniform(0, 10**10) for i in range(self.numTests)]
        densities = [random.uniform(0, 20000) for i in range(self.numTests)]
        stringTight = [i + random.uniform(0, 1) for i in stringLength]

        frequency = [
            physics.calculateStringNewFrequency(
                stringLength[i], stringTight[i], 0, elasticModulus[i], densities[i]
            )
            for i in range(self.numTests)
        ]

        turner = logic.Tuner()

        for i in range(self.numTests):
            turn = turner.tune(frequency[i], frequency[i], stringLength[i])
            self.assertAlmostEqual(turn, 0, delta=self.tolerance)
            newFrequency = physics.calculateStringNewFrequency(
                stringLength[i],
                stringTight[i],
                turn,
                elasticModulus[i],
                densities[i],
            )
            self.assertAlmostEqual(newFrequency, frequency[i], delta=self.tolerance)

    def test_NegligibleDifference(self):
        """
        We test that when the difference is negligible,
        the turn is around zero and the new
        frequency is almost the same.
        """
        stringLength = [random.uniform(0, 2) for _ in range(self.numTests)]
        elasticModulus = [random.uniform(0, 10**10) for i in range(self.numTests)]
        densities = [random.uniform(0, 20000) for i in range(self.numTests)]
        stringTight = [i + random.uniform(0, 1) for i in stringLength]

        frequency = [
            physics.calculateStringNewFrequency(
                stringLength[i], stringTight[i], 0, elasticModulus[i], densities[i]
            )
            for i in range(self.numTests)
        ]
        objectiveFrequency = [i + random.uniform(0, self.tolerance) for i in frequency]

        turner = logic.Tuner()

        for i in range(self.numTests):
            turn = turner.tune(objectiveFrequency[i], frequency[i], stringLength[i])
            self.assertAlmostEqual(turn, 0, delta=self.tolerance * 10)
            newFrequency = physics.calculateStringNewFrequency(
                stringLength[i],
                stringTight[i],
                turn,
                elasticModulus[i],
                densities[i],
            )
            self.assertAlmostEqual(
                newFrequency, frequency[i], delta=self.tolerance * 10
            )

    def test_MultipleTurns(self):
        """
        We test that when it does multiple turns,
        the frequency gets progressively closer to the
        desired frequency.
        """
        elasticModulus = [
            random.uniform(0, 10**10) for i in range(int(self.numTests / 10))
        ]
        densities = [random.uniform(0, 20000) for i in range(int(self.numTests / 10))]
        stringLength = [random.uniform(0, 2) for _ in range(int(self.numTests / 10))]
        stringTight = [i + random.uniform(0, 1) for i in stringLength]

        frequency = [
            physics.calculateStringNewFrequency(
                stringLength[i], stringTight[i], 0, elasticModulus[i], densities[i]
            )
            for i in range(int(self.numTests / 10))
        ]
        objectiveFrequency = [i + random.uniform(0, 2000) for i in frequency]

        turner = logic.Tuner()

        for i in range(int(self.numTests / 10)):
            frequencies = [frequency[i]]

            for _ in range(10):
                turn = turner.tune(frequency[i], frequency[i], stringLength[i])
                frequency[i] = physics.calculateStringNewFrequency(
                    stringLength[i],
                    stringTight[i],
                    turn,
                    elasticModulus[i],
                    densities[i],
                )
                stringTight[i] = physics.calculateNewLength(
                    stringLength[i], stringTight[i], turn
                )
                frequencies.append(frequency[i])

            absolute = [abs(j - objectiveFrequency[i]) for j in frequencies]

            self.assertEqual(absolute, sorted(absolute, reverse=True))
