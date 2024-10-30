import skfuzzy as fuzz
from skfuzzy import control as ctrl
import numpy as np


class Tuner:

    def __init__(self) -> None:

        self.tuner = self.createController()

    def antecedentFrequency(self) -> ctrl.Antecedent:
        """
        Create the antecedent for the frequency difference.
        We use the data from this source:
        https://en.wikipedia.org/wiki/Audio_frequency

        Args:
            - None

        Returns:
            - ctrl.Antecedent: The antecedent for the frequency difference.
        """
        maxFrecuency = 20000
        minFrecuency = 20
        frequencyDifference = ctrl.Antecedent(
            np.arange(0, maxFrecuency - minFrecuency, 1),
            "frequency",
        )

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

        return frequencyDifference

    def antecedentLength(self) -> ctrl.Antecedent:
        """
        Create the antecedent for the string length.
        For the limits we use the data from this source:
        # https://www.harpsatsang.com/harp_design/data/stringcalculator.html

        Args:
            - None

        Returns:
            - ctrl.Antecedent: The antecedent for the string length.
        """
        maxLength = 1.2
        minLength = 0.08
        stringLength = ctrl.Antecedent(
            np.arange(minLength, maxLength, 0.01), "stringLength"
        )

        stringLength["small"] = fuzz.trimf(stringLength.universe, [0.08, 0.08, 0.7])
        stringLength["medium"] = fuzz.trimf(stringLength.universe, [0.4, 0.80, 1.0])
        stringLength["long"] = fuzz.trimf(stringLength.universe, [0.8, 1.20, 1.20])

        return stringLength

    def consequentTurn(self) -> ctrl.Consequent:
        """
        Create the consequent for the turn.

        Args:
            - None

        Returns:
            - ctrl.Consequent: The consequent for the turn.
        """
        turn = ctrl.Consequent(np.arange(0, 1.1, 0.01), "turn")

        turn["very_little"] = fuzz.trimf(turn.universe, [0, 0, 0.05])
        turn["little"] = fuzz.trimf(turn.universe, [0.05, 0.2, 0.4])
        turn["medium"] = fuzz.trimf(turn.universe, [0.3, 0.5, 0.8])
        turn["a_lot"] = fuzz.trimf(turn.universe, [0.6, 1, 1])

        return turn

    def createRules(
        self,
        frequencyDifference: ctrl.Antecedent,
        stringLength: ctrl.Antecedent,
        turn: ctrl.Consequent,
    ) -> ctrl.ControlSystem:
        """
        Create the rules for the fuzzy controller.
        The frequency and turn need to have the same number of terms
        and be in the same order.
        The lenght has three terms.

        Initially we choose the turn to be the same as the frequency.

        Then the length of the string will modify the turn.
        If the string is short, the turn will be changed to the previous turn.
        If the string is long, the turn will be changed to the next turn.

        Args:
            - frequencyDifference (ctrl.Antecedent): The antecedent for the frequency difference.
            - stringLength (ctrl.Antecedent): The antecedent for the string length.
            - turn (ctrl.Consequent): The consequent for the turn.

        Returns:
            - ctrl.ControlSystem: The rules for the fuzzy controller.
        """
        rules = []

        for idF, (_, freq) in enumerate(frequencyDifference.terms.items()):
            for idL, (_, length) in enumerate(stringLength.terms.items()):
                turnValue = idF
                if idL == 0:
                    turnValue = max(0, idF - 1)
                elif idL == 2:
                    turnValue = min(len(frequencyDifference.terms) - 1, idF + 1)

                rule = ctrl.Rule(
                    freq & length,
                    list(turn.terms.values())[turnValue],
                )
                rules.append(rule)

        turn_ctrl = ctrl.ControlSystem(rules)

        return turn_ctrl

    def createController(self) -> ctrl.ControlSystemSimulation:
        """
        Create a fuzzy controller to tune a string.

        Args:
            - None

        Returns:
            - ctrl.ControlSystemSimulation: A fuzzy controller to tune a string.
        """

        frequencyDifference = self.antecedentFrequency()
        stringLength = self.antecedentLength()
        turn = self.consequentTurn()

        turn_ctrl = self.createRules(frequencyDifference, stringLength, turn)

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


if __name__ == "__main__":
    turner = Tuner()
    turner.createRules(
        turner.antecedentFrequency(), turner.antecedentLength(), turner.consequentTurn()
    )
