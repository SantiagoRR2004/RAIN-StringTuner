import skfuzzy as fuzz
from skfuzzy import control as ctrl
import numpy as np


class Tuner:

    def __init__(self) -> None:

        self.tuner = self.createController()

    def createController(self) -> ctrl.ControlSystemSimulation:
        """
        Create a fuzzy controller to tune a string.

        Args:
            - None

        Returns:
            - ctrl.ControlSystemSimulation: A fuzzy controller to tune a string.
        """

        # https://en.wikipedia.org/wiki/Audio_frequency
        maxFrecuency = 20000
        minFrecuency = 20
        frequencyDifference = ctrl.Antecedent(
            np.arange(0, maxFrecuency - minFrecuency, 1),
            "frequency",
        )

        # https://www.harpsatsang.com/harp_design/data/stringcalculator.html
        maxLength = 1.2
        minLength = 0.08
        stringLength = ctrl.Antecedent(
            np.arange(minLength, maxLength, 0.01), "stringLength"
        )

        turn = ctrl.Consequent(np.arange(0, 1.1, 0.01), "turn")

        frequencyDifference["very_close"] = fuzz.trimf(
            frequencyDifference.universe, [0, 0, 50]
        )
        frequencyDifference["close"] = fuzz.trimf(
            frequencyDifference.universe, [0, 150, 300]
        )
        frequencyDifference["medium"] = fuzz.trimf(
            frequencyDifference.universe, [150, 300, 600]
        )
        frequencyDifference["far"] = fuzz.trimf(
            frequencyDifference.universe, [500, 1000, 19800]
        )

        stringLength["small"] = fuzz.trimf(stringLength.universe, [0.08, 0.08, 0.7])
        stringLength["medium"] = fuzz.trimf(stringLength.universe, [0.4, 0.80, 1.0])
        stringLength["long"] = fuzz.trimf(stringLength.universe, [0.8, 1.20, 1.20])

        turn["very_little"] = fuzz.trimf(turn.universe, [0, 0, 0.05])
        turn["little"] = fuzz.trimf(turn.universe, [0.05, 0.2, 0.4])
        turn["medium"] = fuzz.trimf(turn.universe, [0.3, 0.5, 0.8])
        turn["a_lot"] = fuzz.trimf(turn.universe, [0.6, 1, 1])

        rule1 = ctrl.Rule(
            frequencyDifference["very_close"] & stringLength["small"],
            turn["very_little"],
        )
        rule2 = ctrl.Rule(
            frequencyDifference["close"] & stringLength["small"], turn["very_little"]
        )
        rule3 = ctrl.Rule(
            frequencyDifference["far"] & stringLength["small"], turn["medium"]
        )
        rule4 = ctrl.Rule(
            frequencyDifference["very_close"] & stringLength["medium"],
            turn["very_little"],
        )
        rule5 = ctrl.Rule(
            frequencyDifference["close"] & stringLength["medium"], turn["little"]
        )
        rule5 = ctrl.Rule(
            frequencyDifference["medium"] & stringLength["medium"], turn["medium"]
        )
        rule6 = ctrl.Rule(
            frequencyDifference["far"] & stringLength["medium"], turn["a_lot"]
        )
        rule7 = ctrl.Rule(
            frequencyDifference["very_close"] & stringLength["long"], turn["little"]
        )
        rule8 = ctrl.Rule(
            frequencyDifference["close"] & stringLength["long"], turn["medium"]
        )
        rule9 = ctrl.Rule(
            frequencyDifference["far"] & stringLength["long"], turn["a_lot"]
        )

        turn_ctrl = ctrl.ControlSystem(
            [rule1, rule2, rule3, rule4, rule5, rule6, rule7, rule8, rule9]
        )
        turner = ctrl.ControlSystemSimulation(turn_ctrl)

        return turner

    def calculateTurn(self, difference: float, stringLength: float) -> float:
        """
        Calculate the turn to tune a string.

        Args:
            - difference (float): The difference between the objective frequency
                                and the current frequency of the string.
            - stringLength (float): The current length of the string.

        Returns:
            - float: The turn to tune the string.
        """
        self.tuner.input["frequency"] = abs(difference)
        self.tuner.input["stringLength"] = stringLength

        self.tuner.compute()

        return self.tuner.output["turn"]

    def tune(self, objFrecuency: float, frequency: float, stringLength: float) -> float:
        """
        Calculate the turn to tune a string being positive if the string is
        below the objective frequency and negative if the string is above the
        objective frequency.

        Args:
            - objFrecuency (float): The objective frequency of the string.
            - frequency (float): The current frequency of the string.
            - stringLength (float): The current length of the string.

        Returns:
            - float: The turn to tune the string.
        """
        difference = objFrecuency - frequency

        turn = self.calculateTurn(difference, stringLength)

        if difference < 0:
            turn *= -1

        return turn
