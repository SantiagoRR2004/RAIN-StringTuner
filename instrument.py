import abc
import sound
import physics
import logic
import numpy as np
import time
import random
import matplotlib.pyplot as plt
from typing import List


class Instrument(abc.ABC):
    # https://en.wikipedia.org/wiki/Psychoacoustics
    frequencyDiscrimination = 3.6

    turner = logic.Tuner()

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
        # self.stringFrequencies.fill(100)
        self.calculateTightness()
        self.checker()

    def calculateTightness(self) -> None:
        """
        Calculate the tightness of the strings.

        It requires the following attributes to be already defined:
            - stringFrequencies (list): The frequencies of the strings in hertz.
            - lengths (list): The initial lengths of the strings in meters.
            - youngModulus (list): The young modulus of the strings in pascals.
            - density (list): The densities of the strings in kilograms per cubic meter.

        Args:
            - None

        Returns:
            - None
        """
        self.stringLengths = [
            physics.calculateNewLengthByFrequency(
                self.lengths[i],
                self.stringFrequencies[i],
                self.youngModulus[i],
                self.density[i],
            )
            for i in range(len(self.frequencies))
        ]

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
        elif len(self.frequencies) != len(self.stringLengths):
            raise ValueError(
                "The number of frequencies and string lengths must be the same."
            )
        elif len(self.frequencies) != len(self.density):
            raise ValueError("The number of frequencies and density must be the same.")
        elif len(self.frequencies) != len(self.youngModulus):
            raise ValueError(
                "The number of frequencies and young modulus must be the same."
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

    def tune(
        self,
        *,
        soundEnabled: bool = False,
        timeLimit: int = 0,
        verbose: bool = False,
        showGraph: bool = False,
    ) -> list:
        """
        Tune the instrument.

        It requires the following attributes to be already defined:
            - frequencies (list): The frequencies of the strings in hertz.
            - lengths (list): The lengths of the strings in meters.
            - youngModulus (list): The young modulus of the strings in pascals.
            - density (list): The densities of the strings in kilograms per cubic meter.

        Args:
            - soundEnabled (bool): A boolean that indicates if the sound is enabled.
            - timeLimit (int): The time limit for the tuning process in seconds.
            - verbose (bool): A boolean that indicates if the tuning process is verbose.
            - showGraph (bool): A boolean that indicates if the tuning process is graphed.

        Returns:
            - list: A list of the turns that were made to tune the instrument.
                    This is a list of lists where each list represents an iteration
                    of string tunning.
        """
        turns = []
        frequenciesIter = []

        if timeLimit:
            startTime = time.time()

        while np.any(
            np.abs(self.frequencies - self.stringFrequencies)
            > self.frequencyDiscrimination
        ):
            # Show the frequencies of the strings
            if verbose:
                print(self.stringFrequencies)

            # Play the sound of the current strings
            if soundEnabled:
                self.play()

            # We add the actual frequencies for the graph
            if showGraph:
                frequenciesIter.append(self.stringFrequencies.copy())

            turnIteration = np.zeros(len(self.frequencies))

            for i in range(len(self.frequencies)):
                difference = self.frequencies[i] - self.stringFrequencies[i]
                if abs(difference) > self.frequencyDiscrimination:

                    turn = self.turner.tune(
                        self.frequencies[i],
                        self.stringFrequencies[i],
                        self.lengths[i],
                    )

                    turnIteration[i] = turn

                    newLength = physics.calculateNewLength(
                        self.lengths[i], self.stringLengths[i], turn
                    )

                    self.stringFrequencies[i] = physics.calculateStringNewFrequency(
                        self.lengths[i],
                        self.stringLengths[i],
                        turn,
                        self.youngModulus[i],
                        self.density[i],
                    )

                    self.stringLengths[i] = newLength

            if verbose:
                for i in range(len(turnIteration)):
                    if turnIteration[i] != 0:
                        print(f"Turn string {i+1}: {turnIteration[i]}")
                print("---------------------------------------------")
            
            turns.append(turnIteration)
            if timeLimit:
                if time.time() - startTime > timeLimit:
                    raise TimeoutError("Time limit exceeded")

        if verbose:
            print("Tuning finished")
            print(f"Results: {self.frequencies}")
        
        if showGraph:
            frequenciesIter.append(self.stringFrequencies.copy())
            self.graphsFromTuning(turns, frequenciesIter)

        return turns

    def graphsFromTuning(
        self, turns: List[List[float]], frequencies: List[List[float]]
    ) -> None:
        """
        Show the graphs of the tuning process.

        It shows two graphs:

            - The first one shows the turns that were made to tune the instrument.

            - The second one shows the difference between the objective and the actual frequency
                for each iteration.

        Args:
            - turns (List[List[float]]): A list of the turns that were made to tune the instrument.
            - frequencies (List[List[float]]): A list of the frequencies of the strings in each iteration.

        Returns:
            - None
        """
        turns = np.array(turns)
        frequencies = np.array(frequencies)

        # First the we represent the turns by string
        fig = plt.figure()
        fig.canvas.manager.set_window_title("Revolutions by string")

        # Draw line at 0 Hz
        plt.axhline(0, color="black", linewidth=0.5)

        # Draw the turns
        plt.plot(turns, label=[f"{obj} Hz" for obj in self.frequencies])

        plt.xlabel("Iteration")
        plt.xticks(range(len(turns)))
        plt.ylabel("Revolution")
        plt.legend()
        plt.title("Revolutions by string")

        # The difference between the objective and the actual frequency
        # for each iteration
        frequencies = [fr - self.frequencies for fr in frequencies]

        # Then we represent the difference between the objective and the actual frequency
        fig = plt.figure()
        fig.canvas.manager.set_window_title("Difference by string")

        # Draw the frequency discrimination zone
        plt.axhspan(
            -self.frequencyDiscrimination, self.frequencyDiscrimination, color="black"
        )

        # Draw the differences
        plt.plot(
            frequencies, label=[f"String {i+1}" for i in range(len(self.frequencies))]
        )
        plt.xlabel("Iteration")
        plt.xticks(range(len(frequencies)))
        plt.ylabel("Difference (Hz)")
        plt.legend()
        plt.title("Difference by string")

        plt.show()


class RandomInstrument(Instrument):
    def __init__(
        self, nStrings: int = random.randint(1, 40), length: float = 0.65
    ) -> None:

        maxFrequency = 1000
        minFrequency = 100

        self.frequencies = list(
            np.random.uniform(minFrequency, maxFrequency, nStrings)
        )[::-1]

        self.lengths = [length] * len(self.frequencies)

        # Steel: https://en.wikipedia.org/wiki/Young%27s_modulus
        maxYoungModulus = 200 * (10**9)
        # Nylon: https://en.wikipedia.org/wiki/Young%27s_modulus
        minYoungModulus = 2.93 * (10**9)

        self.youngModulus = [
            random.uniform(minYoungModulus, maxYoungModulus) for _ in range(nStrings)
        ]

        # Steel density: https://en.wikipedia.org/wiki/Density
        maxDensity = 7850
        # Nylon: https://en.wikipedia.org/wiki/Nylon_66
        minDensity = 1140

        self.density = [random.uniform(minDensity, maxDensity) for _ in range(nStrings)]

        super().__init__()
