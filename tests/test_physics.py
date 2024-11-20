import unittest
import physics
import random


class numTests(unittest.TestCase):
    numTests = 1000
    tolerance = 1e-4


class test_length(numTests):

    def test_0turn(self):
        """
        We test that when the string is not turned,
        the length remains the same.
        """
        ogLengths = [random.uniform(0, 100) for _ in range(self.numTests)]
        lengths = [i + random.uniform(0, 100) for i in ogLengths]

        for i in range(self.numTests):
            self.assertEqual(
                physics.calculateNewLength(ogLengths[i], lengths[i], 0), lengths[i]
            )

    def test_positiveTurn(self):
        """
        We test that when the string is turned positively,
        the length increases.
        """
        ogLengths = [random.uniform(0, 100) for _ in range(self.numTests)]
        lengths = [i + random.uniform(0, 100) for i in ogLengths]
        turns = [random.uniform(0, 5) for _ in range(self.numTests)]

        for i in range(self.numTests):
            self.assertGreater(
                physics.calculateNewLength(ogLengths[i], lengths[i], turns[i]),
                lengths[i],
            )

    def test_negativeTurn(self):
        """
        We test that when the string is turned negatively,
        the length decreases.
        """
        ogLengths = [random.uniform(0, 100) for _ in range(self.numTests)]
        lengths = [i + random.uniform(0, 100) for i in ogLengths]
        turns = [random.uniform(-5, 0) for _ in range(self.numTests)]

        for i in range(self.numTests):
            self.assertLess(
                physics.calculateNewLength(ogLengths[i], lengths[i], turns[i]),
                lengths[i],
            )

    def test_neverSmallerThanOriginal(self):
        """
        We test that the new length is never smaller than the original length
        no matter how negative the turn is.
        """
        ogLengths = [random.uniform(0, 100) for _ in range(self.numTests)]
        lengths = [i + random.uniform(0, 100) for i in ogLengths]
        turns = [random.uniform(-100, 0) for _ in range(self.numTests)]

        for i in range(self.numTests):
            self.assertGreaterEqual(
                physics.calculateNewLength(ogLengths[i], lengths[i], turns[i]),
                ogLengths[i],
            )


class test_tension(numTests):

    def test_equalLength(self):
        """
        We test that there is no tension
        when the string isn't stretched.
        """
        elasticModulus = [random.uniform(0, 10**10) for _ in range(self.numTests)]
        crossSection = [random.uniform(0, 1) for _ in range(self.numTests)]
        lengths = [random.uniform(0, 100) for _ in range(self.numTests)]

        for i in range(self.numTests):
            self.assertEqual(
                physics.calculateStringTension(
                    elasticModulus[i], crossSection[i], lengths[i], lengths[i]
                ),
                0,
            )

    def test_proportionalPositive(self):
        """
        We test that the tension is proportional to the length
        change when the string is stretched.
        """
        elasticModulus = [
            random.uniform(0, 10**10) for _ in range(int(self.numTests ** (1 / 2)))
        ]
        crossSection = [
            random.uniform(0, 1) for _ in range(int(self.numTests ** (1 / 2)))
        ]
        lengths = [random.uniform(0, 100) for _ in range(int(self.numTests ** (1 / 2)))]

        for i in range(int(self.numTests ** (1 / 2))):
            newLengths = [
                lengths[i] + random.uniform(0, 100)
                for i in range(int(self.numTests ** (1 / 2)))
            ]

            proportions = [
                physics.calculateStringTension(
                    elasticModulus[i], crossSection[i], lengths[i], newLength
                )
                / (newLength - lengths[i])
                for newLength in newLengths
            ]

            average = sum(proportions) / len(proportions)

            self.assertTrue(
                all([abs(i - average) < self.tolerance for i in proportions])
            )

    def test_bigModulus(self):
        """
        The function should work with big modulus.
        """
        elasticModulus = [random.uniform(10**10, 10**20) for i in range(self.numTests)]
        crossSection = [random.uniform(0, 1) for i in range(self.numTests)]
        lengths = [random.uniform(0, 100) for i in range(self.numTests)]
        newLengths = [i + random.uniform(0, 100) for i in range(self.numTests)]

        for i in range(self.numTests):
            physics.calculateStringTension(
                elasticModulus[i], crossSection[i], lengths[i], newLengths[i]
            )

    def test_smallModulus(self):
        """
        The function should work with small modulus.
        """
        elasticModulus = [random.uniform(0, 10) for i in range(self.numTests)]
        crossSection = [random.uniform(0, 1) for i in range(self.numTests)]
        lengths = [random.uniform(0, 100) for i in range(self.numTests)]
        newLengths = [i + random.uniform(0, 100) for i in range(self.numTests)]

        for i in range(self.numTests):
            physics.calculateStringTension(
                elasticModulus[i], crossSection[i], lengths[i], newLengths[i]
            )

    def test_bigCrossSection(self):
        """
        The function should work with big cross section.
        """
        elasticModulus = [random.uniform(0, 10**10) for i in range(self.numTests)]
        crossSection = [random.uniform(10**10, 10**20) for i in range(self.numTests)]
        lengths = [random.uniform(0, 100) for i in range(self.numTests)]
        newLengths = [i + random.uniform(0, 100) for i in range(self.numTests)]

        for i in range(self.numTests):
            physics.calculateStringTension(
                elasticModulus[i], crossSection[i], lengths[i], newLengths[i]
            )

    def test_smallCrossSection(self):
        """
        The function should work with small cross section.
        """
        elasticModulus = [random.uniform(0, 10**10) for i in range(self.numTests)]
        crossSection = [random.uniform(0, 0.01) for i in range(self.numTests)]
        lengths = [random.uniform(0, 100) for i in range(self.numTests)]
        newLengths = [i + random.uniform(0, 100) for i in range(self.numTests)]

        for i in range(self.numTests):
            physics.calculateStringTension(
                elasticModulus[i], crossSection[i], lengths[i], newLengths[i]
            )

    def test_ModulusAndCrossSection(self):
        """
        The function should work with extreme values of modulus and cross section.
        """
        elasticModulus = [random.uniform(0, 10**20) for i in range(self.numTests)]
        crossSection = [random.uniform(0, 10**20) for i in range(self.numTests)]
        lengths = [random.uniform(0, 100) for i in range(self.numTests)]
        newLengths = [i + random.uniform(0, 100) for i in range(self.numTests)]

        for i in range(self.numTests):
            physics.calculateStringTension(
                elasticModulus[i], crossSection[i], lengths[i], newLengths[i]
            )


class test_frecuency1(numTests):
    def test_0tension(self):
        """
        We test that when the string has no tension,
        the frequency is cero.
        """
        lengths = [random.uniform(0, 100) for _ in range(self.numTests)]
        massPerLengths = [random.uniform(0, 20000) for _ in range(self.numTests)]

        for i in range(self.numTests):
            self.assertEqual(
                physics.calculateStringFrequencyMersenne(
                    lengths[i], 0, massPerLengths[i]
                ),
                0,
            )

    def test_positiveInputs(self):
        """
        We test that the frequency is positive
        when the inputs are positive.
        """
        lengths = [random.uniform(0, 100) for _ in range(self.numTests)]
        tensions = [random.uniform(0, 100) for _ in range(self.numTests)]
        massPerLengths = [random.uniform(0, 20000) for _ in range(self.numTests)]

        for i in range(self.numTests):
            self.assertGreater(
                physics.calculateStringFrequencyMersenne(
                    lengths[i], tensions[i], massPerLengths[i]
                ),
                0,
            )

    def test_rangeOfInputs(self):
        """
        We test what happens when the inputs
        can be any value.
        """
        lengths = [random.uniform(-100, 100) for _ in range(self.numTests)]
        tensions = [random.uniform(-100, 100) for _ in range(self.numTests)]
        massPerLengths = [random.uniform(-20000, 20000) for _ in range(self.numTests)]

        for i in range(self.numTests):
            physics.calculateStringFrequencyMersenne(
                lengths[i], tensions[i], massPerLengths[i]
            )


class test_frecuency2(numTests):

    def test_0turn(self):
        """
        We test that when the string is not turned,
        the frequency remains the same.
        """
        ogLengths = [random.uniform(0, 100) for _ in range(self.numTests)]
        lengths = [i + random.uniform(0, 100) for i in ogLengths]
        elasticModulus = [random.uniform(0, 10**10) for _ in range(self.numTests)]
        densities = [random.uniform(0, 20000) for _ in range(self.numTests)]

        for i in range(self.numTests):
            self.assertEqual(
                physics.calculateStringNewFrequency(
                    ogLengths[i], lengths[i], 0, elasticModulus[i], densities[i]
                ),
                physics.calculateStringNewFrequency(
                    ogLengths[i], lengths[i], 0, elasticModulus[i], densities[i]
                ),
            )

    def test_positiveTurn(self):
        """
        We test that when the string is turned positively,
        the frequency increases.
        """
        ogLengths = [random.uniform(0, 100) for _ in range(self.numTests)]
        lengths = [i + random.uniform(0, 100) for i in ogLengths]
        elasticModulus = [random.uniform(0, 10**10) for _ in range(self.numTests)]
        densities = [random.uniform(0, 20000) for _ in range(self.numTests)]
        turns = [random.uniform(0, 5) for _ in range(self.numTests)]

        for i in range(self.numTests):
            self.assertGreater(
                physics.calculateStringNewFrequency(
                    ogLengths[i], lengths[i], turns[i], elasticModulus[i], densities[i]
                ),
                physics.calculateStringNewFrequency(
                    ogLengths[i], lengths[i], 0, elasticModulus[i], densities[i]
                ),
            )

    def test_0Modulus(self):
        """
        We test that when the string has no modulus,
        the frequency is cero.
        """
        ogLengths = [random.uniform(0, 100) for _ in range(self.numTests)]
        lengths = [i + random.uniform(0, 100) for i in ogLengths]
        densities = [random.uniform(0, 20000) for _ in range(self.numTests)]
        turns = [random.uniform(-5, 5) for _ in range(self.numTests)]

        for i in range(self.numTests):
            self.assertEqual(
                physics.calculateStringNewFrequency(
                    ogLengths[i], lengths[i], turns[i], 0, densities[i]
                ),
                0,
            )

    def test_negativeTurn(self):
        """
        We test that when the string is turned negatively,
        the frequency decreases.
        """
        ogLengths = [random.uniform(0, 100) for _ in range(self.numTests)]
        lengths = [i + random.uniform(0, 100) for i in ogLengths]
        elasticModulus = [random.uniform(0, 10**10) for _ in range(self.numTests)]
        densities = [random.uniform(0, 20000) for _ in range(self.numTests)]
        turns = [random.uniform(-5, 0) for _ in range(self.numTests)]

        for i in range(self.numTests):
            self.assertLess(
                physics.calculateStringNewFrequency(
                    ogLengths[i], lengths[i], turns[i], elasticModulus[i], densities[i]
                ),
                physics.calculateStringNewFrequency(
                    ogLengths[i], lengths[i], 0, elasticModulus[i], densities[i]
                ),
            )

    def test_rangeOfInputs(self):
        """
        We test what happens when the inputs
        can be any value.
        """
        ogLengths = [random.uniform(-100, 100) for _ in range(self.numTests)]
        lengths = [random.uniform(-100, 100) for _ in ogLengths]
        elasticModulus = [random.uniform(-10**10, 10**10) for _ in range(self.numTests)]
        densities = [random.uniform(-20000, 20000) for _ in range(self.numTests)]
        turns = [random.uniform(-5, 5) for _ in range(self.numTests)]

        for i in range(self.numTests):
            physics.calculateStringNewFrequency(
                ogLengths[i], lengths[i], turns[i], elasticModulus[i], densities[i]
            )
