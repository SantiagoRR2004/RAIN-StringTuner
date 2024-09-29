import sound
import physics
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
        np.arange(minFrecuency - maxFrecuency, maxFrecuency - minFrecuency, 1),
        "frequency",
    )

    # https://www.harpsatsang.com/harp_design/data/stringcalculator.html
    maxLength = 120.5
    minLength = 8
    stringLength = ctrl.Antecedent(np.arange(minLength, maxLength, 1), "stringLength")

    turn = ctrl.Consequent(np.arange(-5, 5, 1), "turn")

    frequencyDifference.automf(names=["higher", "perfect", "lower"])
    stringLength.automf(names=["small", "long"])

    turn["loosen2"] = fuzz.trimf(turn.universe, [-5, -5, 0])
    turn["loosen1"] = fuzz.trimf(turn.universe, [-2.5, -2.5, 0])
    turn["tighten1"] = fuzz.trimf(turn.universe, [0, 2.5, 2.5])
    turn["tighten2"] = fuzz.trimf(turn.universe, [0, 5, 5])

    rule1 = ctrl.Rule(
        frequencyDifference["higher"] & stringLength["long"], turn["loosen2"]
    )
    rule2 = ctrl.Rule(
        frequencyDifference["higher"] & stringLength["small"], turn["loosen1"]
    )
    rule3 = ctrl.Rule(
        frequencyDifference["lower"] & stringLength["small"], turn["tighten1"]
    )
    rule4 = ctrl.Rule(
        frequencyDifference["lower"] & stringLength["long"], turn["tighten2"]
    )

    turn_ctrl = ctrl.ControlSystem([rule1, rule2, rule3, rule4])
    turner = ctrl.ControlSystemSimulation(turn_ctrl)

    return turner


if __name__ == "__main__":
    # https://en.wikipedia.org/wiki/Guitar_tunings
    frequencies = [329.63, 246.94, 196.00, 146.83, 110.00, 82.41]

    # for f in frequencies:
    #     sound.playCordFrequency(f)

    # https://en.wikipedia.org/wiki/Psychoacoustics
    frequencyDiscrimination = 3.6

    # https://en.wikipedia.org/wiki/Scale_length_(string_instruments)
    guitarLength = 65

    # Nylon: https://en.wikipedia.org/wiki/Young%27s_modulus
    youngModulus = 2.93

    # https://en.wikipedia.org/wiki/Nylon_66
    density = 1140

    turner = createController()

    stringLengths = (0.01 + guitarLength) * np.ones(len(frequencies))

    stringFrequencies = physics.calculateStringNewFrequency(
        guitarLength, 0.01 + guitarLength, 0, youngModulus, density
    ) * np.ones(len(frequencies))

    while np.any(np.abs(frequencies - stringFrequencies) > frequencyDiscrimination):
        print(stringFrequencies)
        for i in range(len(frequencies)):
            difference = frequencies[i] - stringFrequencies[i]
            turner.input["frequency"] = difference
            turner.input["stringLength"] = guitarLength

            turner.compute()

            turn = turner.output["turn"]

            stringLengths[i] = physics.calculateNewLength(
                guitarLength, stringLengths[i], turn
            )

            stringFrequencies[i] = physics.calculateStringNewFrequency(
                guitarLength, stringLengths[i], turn, youngModulus, density
            )
