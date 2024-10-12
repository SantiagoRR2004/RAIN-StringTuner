import skfuzzy as fuzz
from skfuzzy import control as ctrl
import numpy as np


def createController() -> ctrl.ControlSystemSimulation:
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
    maxLength = 120.5
    minLength = 8
    stringLength = ctrl.Antecedent(np.arange(minLength, maxLength, 1), "stringLength")

    turn = ctrl.Consequent(np.arange(0, 1.1, 0.1), "turn")

    frequencyDifference.automf(names=["close", "far"])
    stringLength.automf(names=["small", "long"])

    turn["very_little"] = fuzz.trimf(turn.universe, [0, 0.1, 0.1])
    turn["little"] = fuzz.trimf(turn.universe, [0.5, 0.5, 1])
    turn["medium"] = fuzz.trimf(turn.universe, [0, 0.5, 1])
    turn["a_lot"] = fuzz.trimf(turn.universe, [1, 1, 1])

    rule1 = ctrl.Rule(
        frequencyDifference["close"] & stringLength["small"], turn["very_little"]
    )
    rule2 = ctrl.Rule(
        frequencyDifference["close"] & stringLength["long"], turn["little"]
    )
    rule3 = ctrl.Rule(
        frequencyDifference["far"] & stringLength["small"], turn["medium"]
    )
    rule4 = ctrl.Rule(frequencyDifference["far"] & stringLength["long"], turn["a_lot"])

    turn_ctrl = ctrl.ControlSystem([rule1, rule2, rule3, rule4])
    turner = ctrl.ControlSystemSimulation(turn_ctrl)

    return turner
