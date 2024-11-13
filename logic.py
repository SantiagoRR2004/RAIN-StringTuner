import skfuzzy as fuzz
from skfuzzy import control as ctrl
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os
from concurrent.futures import ProcessPoolExecutor
from tqdm import tqdm


class Tuner:

    def __init__(self) -> None:

        self.tuner = self.createController()

    def antecedentFrequency(self) -> ctrl.Antecedent:
        """
        Create the antecedent for the frequency difference.
        We use the data from this source:
        https://en.wikipedia.org/wiki/Audio_frequency

        Args:
            - None

        Returns:
            - ctrl.Antecedent: The antecedent for the frequency difference.
        """
        maxFrecuency = 20000
        minFrecuency = 20
        frequencyDifference = ctrl.Antecedent(
            np.arange(0, maxFrecuency - minFrecuency, 1),
            "frequency",
        )

        """frequencyDifference["very_very_close"] = fuzz.trapmf(
            frequencyDifference.universe, [0, 0, 10, 30]
        )        
        frequencyDifference["very_close"] = fuzz.trapmf(
            frequencyDifference.universe, [5, 5, 20, 80]"""

        frequencyDifference["very_close"] = fuzz.trapmf(
            frequencyDifference.universe, [0, 0, 20, 80]
        )
        frequencyDifference["close"] = fuzz.trapmf(
            frequencyDifference.universe, [20, 80, 100, 200]
        )
        frequencyDifference["medium"] = fuzz.trapmf(
            frequencyDifference.universe, [100, 250, 500, 1000]
        )
        frequencyDifference["far"] = fuzz.trapmf(
            frequencyDifference.universe,
            [500, 2000, maxFrecuency - minFrecuency, maxFrecuency - minFrecuency],
        )

        return frequencyDifference

    def antecedentLength(self) -> ctrl.Antecedent:
        """
        Create the antecedent for the string length.
        For the limits we use the data from this source:
        # https://www.harpsatsang.com/harp_design/data/stringcalculator.html

        Args:
            - None

        Returns:
            - ctrl.Antecedent: The antecedent for the string length.
        """
        maxLength = 1.2
        minLength = 0.08
        stringLength = ctrl.Antecedent(
            np.arange(minLength, maxLength, 0.01), "stringLength"
        )

        stringLength["small"] = fuzz.trapmf(
            stringLength.universe, [0.08, 0.08, 0.4, 0.7]
        )
        stringLength["medium"] = fuzz.trapmf(stringLength.universe, [0.4, 0.6, 0.8, 1])
        stringLength["long"] = fuzz.trapmf(stringLength.universe, [0.8, 1, 1.2, 1.2])

        return stringLength

    def consequentTurn(self) -> ctrl.Consequent:
        """
        Create the consequent for the turn.

        Args:
            - None

        Returns:
            - ctrl.Consequent: The consequent for the turn.
        """
        turn = ctrl.Consequent(np.arange(0, 1.1, 0.001), "turn")

        turn["very_very_little"] = fuzz.trapmf(turn.universe, [0, 0, 0.005, 0.01])
        turn["very_little"] = fuzz.trapmf(turn.universe, [0, 0, 0.05, 0.1])
        turn["little"] = fuzz.trapmf(turn.universe, [0.05, 0.1, 0.20, 0.4])
        turn["medium"] = fuzz.trapmf(turn.universe, [0.25, 0.4, 0.6, 0.8])
        turn["large"] = fuzz.trapmf(turn.universe, [0.6, 0.8, 1, 1])

        return turn

    def createRules(
        self,
        frequencyDifference: ctrl.Antecedent,
        stringLength: ctrl.Antecedent,
        turn: ctrl.Consequent,
    ) -> ctrl.ControlSystem:
        """
        Create the rules for the fuzzy controller.

        Args:
            - frequencyDifference (ctrl.Antecedent): The antecedent for the frequency difference.
            - stringLength (ctrl.Antecedent): The antecedent for the string length.
            - turn (ctrl.Consequent): The consequent for the turn.

        Returns:
            - ctrl.ControlSystem: The rules for the fuzzy controller.
        """
        # Reglas difusas
        rule1 = ctrl.Rule(
            frequencyDifference["very_close"] & stringLength["small"],
            turn["very_very_little"],
        )
        rule2 = ctrl.Rule(
            frequencyDifference["very_close"] & stringLength["medium"],
            turn["very_little"],
        )
        rule3 = ctrl.Rule(
            frequencyDifference["very_close"] & stringLength["long"], turn["little"]
        )
        rule4 = ctrl.Rule(
            frequencyDifference["close"] & stringLength["small"], turn["very_little"]
        )
        rule5 = ctrl.Rule(
            frequencyDifference["close"] & stringLength["medium"], turn["little"]
        )
        rule6 = ctrl.Rule(
            frequencyDifference["close"] & stringLength["long"], turn["medium"]
        )
        rule7 = ctrl.Rule(
            frequencyDifference["medium"] & stringLength["small"], turn["little"]
        )
        rule8 = ctrl.Rule(
            frequencyDifference["medium"] & stringLength["medium"], turn["medium"]
        )
        rule9 = ctrl.Rule(
            frequencyDifference["medium"] & stringLength["long"], turn["large"]
        )
        rule10 = ctrl.Rule(
            frequencyDifference["far"] & stringLength["small"], turn["medium"]
        )
        rule11 = ctrl.Rule(
            frequencyDifference["far"] & stringLength["medium"], turn["large"]
        )
        rule12 = ctrl.Rule(
            frequencyDifference["far"] & stringLength["long"], turn["large"]
        )

        turn_ctrl = ctrl.ControlSystem(
            [
                rule1,
                rule2,
                rule3,
                rule4,
                rule5,
                rule6,
                rule7,
                rule8,
                rule9,
                rule10,
                rule11,
                rule12,
            ]
        )
        return turn_ctrl

    def createRulesManually(
        self,
        frequencyDifference: ctrl.Antecedent,
        stringLength: ctrl.Antecedent,
        turn: ctrl.Consequent,
    ) -> ctrl.ControlSystem:
        """
        NOT CURRENTLY USED

        Create the rules for the fuzzy controller.
        The frequency and turn need to have the same number of terms
        and be in the same order.
        The lenght has three terms.

        Initially we choose the turn to be the same as the frequency.

        Then the length of the string will modify the turn.
        If the string is short, the turn will be changed to the previous turn.
        If the string is long, the turn will be changed to the next turn.

        Args:
            - frequencyDifference (ctrl.Antecedent): The antecedent for the frequency difference.
            - stringLength (ctrl.Antecedent): The antecedent for the string length.
            - turn (ctrl.Consequent): The consequent for the turn.

        Returns:
            - ctrl.ControlSystem: The rules for the fuzzy controller.
        """
        rules = []

        for idF, (_, freq) in enumerate(frequencyDifference.terms.items()):
            for idL, (_, length) in enumerate(stringLength.terms.items()):
                turnValue = idF
                if idL == 0:
                    turnValue = max(0, idF - 1)
                elif idL == 2:
                    turnValue = min(len(frequencyDifference.terms) - 1, idF + 1)

                rule = ctrl.Rule(
                    freq & length,
                    list(turn.terms.values())[turnValue],
                )
                rules.append(rule)

        turn_ctrl = ctrl.ControlSystem(rules)

        return turn_ctrl

    def createController(self) -> ctrl.ControlSystemSimulation:
        """
        Create a fuzzy controller to tune a string.

        Args:
            - None

        Returns:
            - ctrl.ControlSystemSimulation: A fuzzy controller to tune a string.
        """

        frequencyDifference = self.antecedentFrequency()
        stringLength = self.antecedentLength()
        turn = self.consequentTurn()

        # https://scikit-fuzzy.github.io/scikit-fuzzy/auto_examples/plot_defuzzify.html
        # tenemos centroid por defecto, además de mom, som, lom y bisector
        turn.defuzzify_method = "mom"  # medium of maximum

        turn_ctrl = self.createRules(frequencyDifference, stringLength, turn)

        turner = ctrl.ControlSystemSimulation(turn_ctrl)

        return turner

    def calculateTurn(self, difference: float, stringLength: float) -> float:
        """
        Calculate the turn to tune a string.

        Args:
            - difference (float): The difference between the objective frequency
                                and the current frequency of the string.
            - stringLength (float): The current length of the string.

        Returns:
            - float: The turn to tune the string.
        """
        self.tuner.input["frequency"] = abs(difference)
        self.tuner.input["stringLength"] = stringLength

        self.tuner.compute()

        return self.tuner.output["turn"]

    def tune(
        self,
        objFrecuency: float,
        frequency: float,
        stringLength: float,
        verbose: bool = False,
    ) -> float:
        """
        Calculate the turn to tune a string being positive if the string is
        below the objective frequency and negative if the string is above the
        objective frequency.

        Args:
            - objFrecuency (float): The objective frequency of the string.
            - frequency (float): The current frequency of the string.
            - stringLength (float): The current length of the string.
            - verbose (bool): A boolean that indicates if the tuning process is verbose.

        Returns:
            - float: The turn to tune the string.
        """
        difference = objFrecuency - frequency

        turn = self.calculateTurn(difference, stringLength)

        if difference < 0:
            turn *= -1

        if verbose:
            print(turn)
        return turn

    def showAntecedentFrequency(self) -> None:
        """
        Show the antecedent for the frequency difference.

        Args:
            - None

        Returns:
            - None
        """
        self.antecedentFrequency().view()
        plt.title("Frequency Difference")

    def showAntecedentLength(self) -> None:
        """
        Show the antecedent for the string length.

        Args:
            - None

        Returns:
            - None
        """
        self.antecedentLength().view()
        plt.title("String Length")

    def showConsequentTurn(self) -> None:
        """
        Show the consequent for the turn.

        Args:
            - None

        Returns:
            - None
        """
        self.consequentTurn().view()
        plt.title("Turn")

    def showAntecedentsAndConsequents(self) -> None:
        """
        Show the antecedents and consequents for the fuzzy controller.

        Args:
            - None

        Returns:
            - None
        """
        self.showAntecedentFrequency()
        self.showAntecedentLength()
        self.showConsequentTurn()

    def showControlSpace(self) -> None:
        """
        Show the control space for the fuzzy controller.

        Args:
            - None

        Returns:
            - None
        """

        if not os.path.exists("turns.parquet"):
            self.createDataframe()

        data = pd.read_parquet("turns.parquet")

        # We check that the Dataframe is up to date
        repeat = False

        if np.array_equal(self.antecedentFrequency().universe, data.index.values):
            diff = np.where(self.antecedentFrequency().universe != data.index.values)
            if diff[0].size > 0:
                repeat = True
                print(
                    "Not the same frequencyDifference range. Need to update the Dataframe."
                )

        if np.allclose(self.antecedentLength().universe, data.columns.values):
            diff = np.where(self.antecedentLength().universe != data.columns.values)
            if diff[0].size > 0:
                repeat = True
                print("Not the same stringLength range. Need to update the Dataframe.")

        # We check 100 values to see if they are correct
        for _ in range(100):
            frequency = np.random.choice(data.index.values)
            length = np.random.choice(data.columns.values)
            turn = self.calculateTurn(frequency, length)
            if turn != data.loc[frequency, length]:
                repeat = True
                print("Not the same calculations. Need to update the Dataframe.")
                break

        # # We create the Dataframe again if it is not up to date
        # if repeat:
        #     del data
        #     self.createDataframe()
        #     data = pd.read_parquet("turns.parquet")

        frequencyDifference = self.antecedentFrequency()
        fUni = frequencyDifference.universe

        for name, term in frequencyDifference.terms.items():

            self.createGraphs(
                data.loc[fUni[term.mf > 0]],
                title=f"Heatmap of Turns for Frequency {name} and Length",
            )

        self.createGraphs(data)

        plt.show()

    def createGraphs(
        self,
        dataFrame: pd.DataFrame,
        *,
        title: str = "Heatmap of Turns for Frequency and Length",
    ) -> None:
        """
        Create the graphs for the control space.

        Args:
            - dataFrame (pd.DataFrame): The DataFrame with the turns for all the possible
                                        combinations of frequencies and lengths.
        Returns:
            - None
        """
        # Extract frequency, length, and turns from the DataFrame
        frequencies = dataFrame.index.values
        lengths = dataFrame.columns.values
        turns = dataFrame.values

        # Create a meshgrid for 3D plotting
        # freq_grid, length_grid = np.meshgrid(frequencies, lengths)
        length_grid, freq_grid = np.meshgrid(lengths, frequencies)

        # Initialize a 3D plot
        fig = plt.figure()
        fig.canvas.manager.set_window_title(f"3D {title}")
        ax = fig.add_subplot(111, projection="3d")

        # Plot the surface
        ax.plot_surface(freq_grid, length_grid, turns, cmap="viridis")

        # Add labels
        ax.set_xlabel("Frequency")
        ax.set_ylabel("String Length")
        ax.set_zlabel("Turns")
        ax.set_title(title)

        # Initialize a 2D plot
        fig = plt.figure()
        fig.canvas.manager.set_window_title(f"2D {title}")
        plt.imshow(
            turns.T,
            extent=(
                frequencies.min(),
                frequencies.max(),
                lengths.min(),
                lengths.max(),
            ),
            origin="lower",
            aspect="auto",
            cmap="viridis",
        )
        plt.colorbar(label="Turns")
        plt.xlabel("Frequency")
        plt.ylabel("String Length")
        plt.title(title)

    def createDataframe(self) -> None:
        """
        Create a DataFrame with the turns for all the possible
        combinations of frequencies and lengths.

        Args:
            - None

        Returns:
            - None
        """

        frequencyDifference = self.antecedentFrequency()
        stringLength = self.antecedentLength()

        # Define the full range of frequencies and lengths
        frequenciesAll = frequencyDifference.universe
        lengths = stringLength.universe

        batchSize = 50
        nBatches = len(frequenciesAll) // batchSize
        all_turns = []

        for batch_index in tqdm(range(nBatches), desc="Processing Batches"):
            # Extract the current batch of 50 frequencies
            start = batch_index * batchSize
            end = start + batchSize
            frequencies = frequenciesAll[start:end]

            # Create a meshgrid of frequencies and lengths
            frequency_grid, length_grid = np.meshgrid(
                frequencies, lengths, indexing="ij"
            )

            # Create an array filled with zeros of the same shape as frequency_grid and length_grid
            turns = [0] * len(frequencies) * len(lengths)

            with ProcessPoolExecutor() as executor:
                for i, (f, l) in enumerate(
                    zip(frequency_grid.flatten(), length_grid.flatten())
                ):
                    turns[i] = executor.submit(self.calculateTurn, f, l)

            turns = [turn.result() for turn in turns]

            turns = np.array(turns).reshape(frequency_grid.shape)

            batch_df = pd.DataFrame(turns, index=frequencies, columns=lengths)
            all_turns.append(batch_df)

        # Concatenate all batches to form the full DataFrame
        full_df = pd.concat(all_turns, axis=0)

        # Save the DataFrame to a Parquet file
        full_df.to_parquet("turns.parquet")


if __name__ == "__main__":
    turner = Tuner()

    turner.showAntecedentsAndConsequents()

    turner.showControlSpace()
