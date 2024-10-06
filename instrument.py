import abc
import sound
import physics
import logic
import numpy as np


class Instrument(abc.ABC):
    # https://en.wikipedia.org/wiki/Psychoacoustics
    frequencyDiscrimination = 3.6

    turner = logic.createController()

    def tune(self, soundEnabled: bool = False) -> None:
        while np.any(
            np.abs(self.frequencies - self.stringFrequencies)
            > self.frequencyDiscrimination
        ):
            """
            """
            print(self.stringFrequencies)
            if soundEnabled:
                sound.playStrum(self.stringFrequencies)

            for i in range(len(self.frequencies)):
                difference = self.frequencies[i] - self.stringFrequencies[i]
                self.turner.input["frequency"] = difference
                self.turner.input["stringLength"] = self.guitarLength

                self.turner.compute()

                turn = self.turner.output["turn"]

                self.stringLengths[i] = physics.calculateNewLength(
                    self.guitarLength, self.stringLengths[i], turn
                )

                self.stringFrequencies[i] = physics.calculateStringNewFrequency(
                    self.guitarLength,
                    self.stringLengths[i],
                    turn,
                    self.youngModulus,
                    self.density,
                )


