import unittest
import physics
import random


class numTests(unittest.TestCase):
    numTests = 1000


class test_length(numTests):

    def test_0turn(self):
        """
        We test that when the string is not turned,
        the length remains the same.
        """
        ogLengths = [random.uniform(0, 100) for i in range(self.numTests)]
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

    def test_negativeTurn(self):
        """
        We test that when the string is turned negatively,
        the length decreases.
        """

    def test_neverSmallerThanOriginal(self):
        """
        We test that the new length is never smaller than the original length
        no matter how negative the turn is.
        """


class test_tension(numTests):

    def test_equalLength(self):
        """
        We test that there is no tension
        when the string isn't stretched.
        """

    def test_proportionalPositive(self):
        """
        We test that the tension is proportional to the length
        change when the string is stretched.
        """

    def test_bigModulus(self):
        """ """

    def test_smallModulus(self):
        """ """

    def test_bigCrossSection(self):
        """ """

    def test_smallCrossSection(self):
        """ """

    def test_ModulusAndCrossSection(self):
        """ """


class test_frecuency1(numTests):
    def test_0tension(self):
        """
        We test that when the string has no tension,
        the frequency is cero.
        """

    def test_positiveInputs(self):
        """
        We test that the frequency is positive
        when the inputs are positive.
        """

    def test_rangeOfInputs(self):
        """
        We test what happens when the inputs
        can be any value.
        """


class test_frecuency2(numTests):

    def test_0turn(self):
        """
        We test that when the string is not turned,
        the frequency remains the same.
        """

    def test_positiveTurn(self):
        """
        We test that when the string is turned positively,
        the frequency increases.
        """

    def test_0Modulus(self):
        """
        We test that when the string has no modulus,
        the frequency is cero.
        """

    def test_negativeTurn(self):
        """
        We test that when the string is turned negatively,
        the frequency decreases.
        """

    def test_rangeOfInputs(self):
        """
        We test what happens when the inputs
        can be any value.
        """
