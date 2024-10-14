import abc
import sound
import physics
import logic
import numpy as np


class Instrument(abc.ABC):
    # https://en.wikipedia.org/wiki/Psychoacoustics
    frequencyDiscrimination = 3.6

    turner = logic.createController()

    def __init__(self) -> None:
        """
        Initialize the instrument.

        All the strings are placed with zero tension
        so their frequencies are zero.

        It requires the following attributes to be already defined:
            - frequencies (list): The frequencies of the strings in hertz.
            - lengths (list): The lengths of the strings in meters.

        Args:
            - None

        Returns:
            - None
        """
        self.stringFrequencies = np.zeros(len(self.frequencies))
        self.stringLengths = self.lengths.copy()
        self.checker()

    def checker(self) -> None:
        """
        Check if the lists that represent different attributes
        of the strings have the same length.

        It raises a ValueError if the lengths are different.

        It requires the following attributes to be already defined:
            - frequencies (list): The frequencies of the strings in hertz.
            - lengths (list): The lengths of the strings in meters.

        Args:
            - None

        Returns:
            - None
        """
        if len(self.frequencies) != len(self.lengths):
            raise ValueError("The number of frequencies and lengths must be the same.")
        elif len(self.frequencies) != len(self.stringFrequencies):
            raise ValueError(
                "The number of frequencies and string frequencies must be the same."
            )
        elif len(self.lengths) != len(self.stringLengths):
            raise ValueError(
                "The number of lengths and string lengths must be the same."
            )

    def play(self) -> None:
        """
        Play the instrument.

        Args:
            - None

        Returns:
            - None
        """
        self.checker()
        sound.playStrum(self.stringFrequencies)

    def playPerfect(self) -> None:
        """
        Play the perfect sound of the instrument.

        It requires the following attributes to be already defined:
            - frequencies (list): The frequencies of the strings in hertz.

        Args:
            - None

        Returns:
            - None
        """
        self.checker()
        sound.playStrum(self.frequencies)

    def tune(self, soundEnabled: bool = False) -> None:
        while np.any(
            np.abs(self.frequencies - self.stringFrequencies)
            > self.frequencyDiscrimination
        ):
            """
            Document this method.
            """
            print(self.stringFrequencies)
            if soundEnabled:
                self.play()

            for i in range(len(self.frequencies)):
                difference = self.frequencies[i] - self.stringFrequencies[i]
                if abs(difference) > self.frequencyDiscrimination:
                    self.turner.input["frequency"] = abs(difference)
                    self.turner.input["stringLength"] = self.lengths[i]

                    self.turner.compute()

                    turn = self.turner.output["turn"]

                    if difference < 0:
                        # The string is too tight
                        turn *= -1
                    print(turn)
                    self.stringLengths[i] = physics.calculateNewLength(
                        self.lengths[i], self.stringLengths[i], turn
                    )

                    self.stringFrequencies[i] = physics.calculateStringNewFrequency(
                        self.lengths[i],
                        self.stringLengths[i],
                        turn,
                        self.youngModulus,
                        self.density,
                    )
