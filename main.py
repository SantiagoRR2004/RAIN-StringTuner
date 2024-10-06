import sound
import physics
import logic
import numpy as np

if __name__ == "__main__":
    # https://en.wikipedia.org/wiki/Guitar_tunings
    frequencies = [329.63, 246.94, 196.00, 146.83, 110.00, 82.41]

    # https://en.wikipedia.org/wiki/Psychoacoustics
    frequencyDiscrimination = 3.6

    # https://en.wikipedia.org/wiki/Scale_length_(string_instruments)
    guitarLength = 65

    # Nylon: https://en.wikipedia.org/wiki/Young%27s_modulus
    youngModulus = 2.93

    # https://en.wikipedia.org/wiki/Nylon_66
    density = 1140

    turner = logic.createController()

    stringLengths = (0.01 + guitarLength) * np.ones(len(frequencies))

    stringFrequencies = physics.calculateStringNewFrequency(
        guitarLength, 0.01 + guitarLength, 0, youngModulus, density
    ) * np.ones(len(frequencies))

    while np.any(np.abs(frequencies - stringFrequencies) > frequencyDiscrimination):
        print(stringFrequencies)
        # sound.playStrum(stringFrequencies)
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
