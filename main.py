import sound
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import numpy as np


if __name__ == "__main__":
    # https://en.wikipedia.org/wiki/Guitar_tunings
    frequencies = [329.63, 246.94, 196.00, 146.83, 110.00, 82.41]

    # for f in frequencies:
    #     sound.playCordFrequency(f)

    # https://en.wikipedia.org/wiki/Audio_frequency
    maxFrecuency = 20000
    minFrecuency = 20

    # https://en.wikipedia.org/wiki/Psychoacoustics
    frequencyDiscrimination = 3.6

    # https://en.wikipedia.org/wiki/Scale_length_(string_instruments)
    guitarLength = 65

    # https://www.harpsatsang.com/harp_design/data/stringcalculator.html
    maxLength = 120.5
    minLength = 8

    frequencyDifference = ctrl.Antecedent(
        np.arange(minFrecuency - maxFrecuency, maxFrecuency - minFrecuency, 1),
        "quality",
    )
    stringLength = ctrl.Antecedent(np.arange(minLength, maxLength, 1), "stringLength")

    turn = ctrl.Consequent(np.arange(-5, 5, 1), "turn")
