import unittest
import random
import instrument
import guitars
import harplike
import numpy as np
import random
import inspect


def getClasses() -> list:
    """
    Returns a list with all the classes defined in the current module.

    Args:
        - None

    Returns:
        - list: List with all the classes defined in the current module.
    """
    classes = []
    # Check globals for any types
    for obj in globals().values():
        # If it's a class defined or imported in the current module
        if isinstance(obj, type):
            classes.append(obj)  # Collect the class object
        # If it's a module, inspect its attributes for classes
        elif inspect.ismodule(obj):
            for attr_name in dir(obj):
                attr = getattr(obj, attr_name)
                if isinstance(attr, type):  # Check if the attribute is a class
                    classes.append(attr)
    return classes


def instrumentChildren() -> list:
    """
    Returns a list with all the classes that are children of the
    instrument.Instrument class.

    Args:
        - None

    Returns:
        - list: List with all the classes that are children of the
                instrument.Instrument class.
    """
    classes = getClasses()
    children = []
    for cls in classes:
        if issubclass(cls, instrument.Instrument) and cls is not instrument.Instrument:
            children.append(cls)
    return children


class numTests(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(numTests, self).__init__(*args, **kwargs)
        self.numTests = 100
        self.timelimit = 10
        self.instruments = instrumentChildren()


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

            averageTurns.append(sum(nTurns) / len(nTurns))

            nStringSuccess += np.sum(np.where(nTurns <= t, 1, 0))

        print(f"Success rate: {100*nSuccess/self.numTests}%")
        print(
            f"Success rate per string: {100*nStringSuccess/(self.numTests*len(objective))}%"
        )
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

        averageTurns.append(sum(nTurns) / len(nTurns))

        nStringSuccess += np.sum(np.where(nTurns <= t, 1, 0))

        print(f"Success rate: {100*nSuccess}%")
        print(f"Success rate per string: {100*nStringSuccess/len(harp.frequencies)}%")
        print(f"Average turns by string: {sum(averageTurns)/len(averageTurns)}")

    def test_veryCloseInstruments(self):
        """
        Checks that it doesn't tune the
        instruments if the strings are
        very close to the objective.
        """
        t = 0

        nSuccess = 0
        nTotalTurns = 0
        nStrings = 0
        nStringSuccess = 0

        for _ in range(self.numTests):
            inst = random.choice(self.instruments)()

            objective = inst.frequencies
            actual = inst.stringFrequencies

            nTurns = np.zeros(len(objective))

            for i in range(len(objective)):
                actual[i] = objective[i] + random.uniform(-3, 3)

            inst.calculateTightness()

            itTurns = inst.tune(timeLimit=self.timelimit)

            for turns in itTurns:
                nTurns += np.where(turns != 0, 1, 0)

            if np.all(nTurns <= t):
                nSuccess += 1

            nTotalTurns += sum(nTurns)
            nStrings += len(objective)
            nStringSuccess += np.sum(np.where(nTurns <= t, 1, 0))

        print(f"Success rate: {100*nSuccess/self.numTests}%")
        print(f"Success rate per string: {100*nStringSuccess/nStrings}%")
        print(f"Average turns by string: {nTotalTurns/nStrings}")

    def test_alternativeGuitar(self):
        """
        Checks that a guitar can be tuned
        in only 5 turns even when the objective
        frequencies are different.

        NOT POSSIBLE
        """
        t = 5

        nSuccess = 0
        averageTurns = []
        nStringSuccess = 0

        for _ in range(self.numTests):
            guitar = guitars.BassTuningGuitar()

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

            averageTurns.append(sum(nTurns) / len(nTurns))

            nStringSuccess += np.sum(np.where(nTurns <= t, 1, 0))

        print(f"Success rate: {100*nSuccess/self.numTests}%")
        print(
            f"Success rate per string: {100*nStringSuccess/(self.numTests*len(objective))}%"
        )
        print(f"Average turns by string: {sum(averageTurns)/len(averageTurns)}")
