# https://en.wikipedia.org/wiki/Outline_of_guitars

import instrument


class ClassicalGuitar(instrument.Instrument):
    def __init__(self, length: float = 0.65):
        # https://en.wikipedia.org/wiki/Guitar_tunings
        self.frequencies = [329.63, 246.94, 196.00, 146.83, 110.00, 82.41]

        # https://en.wikipedia.org/wiki/Scale_length_(string_instruments)
        self.lengths = [length] * len(self.frequencies)

        # Nylon: https://en.wikipedia.org/wiki/Young%27s_modulus
        self.youngModulus = 2.93 * (10 ** 9)

        # https://en.wikipedia.org/wiki/Nylon_66
        self.density = 1140

        super().__init__()
