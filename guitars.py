# https://en.wikipedia.org/wiki/Outline_of_guitars

import instrument


class ClassicalGuitar(instrument.Instrument):
    def __init__(self, length: float = 0.65):
        # https://en.wikipedia.org/wiki/Guitar_tunings
        self.frequencies = [329.63, 246.94, 196.00, 146.83, 110.00, 82.41][::-1]

        # https://en.wikipedia.org/wiki/Scale_length_(string_instruments)
        self.lengths = [length] * len(self.frequencies)

        # Nylon: https://en.wikipedia.org/wiki/Young%27s_modulus
        self.youngModulus = [2.93 * (10**9)] * len(self.frequencies)

        # https://en.wikipedia.org/wiki/Nylon_66
        self.density = [1140] * len(self.frequencies)

        super().__init__()


class ElectricGuitar(instrument.Instrument):
    def __init__(
        self, length: float = 0.648
    ):  # Standard electric guitar scale length in meters
        # Frequencies in standard tuning (EADGBE), same as classical guitar
        self.frequencies = [329.63, 246.94, 196.00, 146.83, 110.00, 82.41][::-1]

        # Electric guitars typically have steel or nickel strings

        # Steel: https://en.wikipedia.org/wiki/Young%27s_modulus
        self.youngModulus = [200 * (10**9)] * len(self.frequencies)  # For steel

        # Steel density: https://en.wikipedia.org/wiki/Density
        self.density = [7850] * len(self.frequencies)  # Steel density in kg/m^3

        # Scale length remains relatively uniform for electric guitars
        # Often slightly shorter than classical guitars
        self.lengths = [length] * len(self.frequencies)

        super().__init__()


class BassTuningGuitar(instrument.Instrument):
    def __init__(self, length: float = 0.864):
        # https://en.wikipedia.org/wiki/Bass_guitar_tuning
        self.frequencies = [130.81, 98.00, 73.42, 55.00, 41.20, 30.87][::-1]

        # https://en.wikipedia.org/wiki/Scale_length_(string_instruments)
        self.lengths = [length] * len(self.frequencies)

        # Nylon: https://en.wikipedia.org/wiki/Young%27s_modulus
        self.youngModulus = [2.93 * (10**9)] * len(self.frequencies)

        # https://en.wikipedia.org/wiki/Nylon_66
        self.density = [1140] * len(self.frequencies)

        super().__init__()
