# https://en.wikipedia.org/wiki/Outline_of_guitars

import instrument
import physics
import numpy as np


class ClassicalGuitar(instrument.Instrument):
    # https://en.wikipedia.org/wiki/Guitar_tunings
    frequencies = [329.63, 246.94, 196.00, 146.83, 110.00, 82.41]

    # https://en.wikipedia.org/wiki/Scale_length_(string_instruments)
    guitarLength = 65

    # Nylon: https://en.wikipedia.org/wiki/Young%27s_modulus
    youngModulus = 2.93

    # https://en.wikipedia.org/wiki/Nylon_66
    density = 1140

    stringLengths = (0.01 + guitarLength) * np.ones(len(frequencies))

    stringFrequencies = physics.calculateStringNewFrequency(
        guitarLength, 0.01 + guitarLength, 0, youngModulus, density
    ) * np.ones(len(frequencies))
