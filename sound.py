import numpy as np
import sounddevice as sd


def createCordFrequency(frequency: float) -> np.ndarray:
    """
    Create a sound with the given frequency using the Karplus-Strong algorithm.
    https://en.wikipedia.org/wiki/Karplus%E2%80%93Strong_string_synthesis

    We also got this code from the following link:
    https://github.com/earthspecies/intro-to-DSP-with-python/blob/main/02_Generate_a_sound_that_resembles_violin.ipynb
    and had ChatGPT modify it to change the frecuency of the sound.

    Args:
        - frequency (float): The frequency of the sound to play.

    Returns:
        - np.ndarray: The sound signal. The sample rate is 16000 Hz.
    """
    sr = 16000  # Sample rate
    decay = 0.99  # Feedback decay factor
    duration = 2  # Duration in seconds

    if frequency <= 0:
        signal = np.zeros(int(sr * duration))

    else:
        # Calculate delay length based on frequency
        delay_length = int(sr / frequency)  # Samples
        delay_line = (
            np.random.rand(delay_length) * 2 - 1
        )  # Initialize with random values

        # Initialize the output signal
        signal = np.zeros(int(sr * duration))

        # Fill the output signal with the initial noise
        for i in range(delay_length):
            signal[i] = delay_line[i]

        # Generate the signal using the Karplus-Strong method
        for i in range(delay_length, len(signal)):
            # Average the first two samples of the delay line
            avg = 0.5 * (
                delay_line[i % delay_length] + delay_line[(i + 1) % delay_length]
            )
            # Apply decay
            output = avg * decay
            # Store in the delay line and signal
            delay_line[i % delay_length] = output
            signal[i] = output

    return signal


def playSound(signal: np.ndarray, sr: int = 16000) -> None:
    """
    Play the given sound using the sounddevice library.

    Args:
        - signal (np.ndarray): The sound signal to play.
        - sr (int): The sample rate of the sound signal.

    Returns:
        - None
    """
    # Play the synthesized sound
    sd.play(signal, samplerate=sr)
    sd.wait()  # Wait until the audio is done playing


def combineSounds(signals: list, soundLength: int = 2000) -> np.ndarray:
    """
    Combine a list of sound signals into a single sound signal.

    The lengths calculations are to check what the length of the final
    sound is going to be. It is going to be at least the sound length
    times the number of sounds plus the remaining time.

    Args:
        - signals (list): A list of sound signals.
        - soundLength (int): The length from the start of one sound
                            to the start of the next sound.

    Returns:
        - np.ndarray: The concatenated sound signal.
    """
    lengths = [len(s) for s in signals]
    lengths = [
        lengths[i] - soundLength * (len(lengths) - i) for i in range(len(lengths))
    ]

    finalSignalLength = soundLength * len(signals) + max(lengths + [0])

    finalSignal = np.zeros(finalSignalLength)

    for i in range(len(signals)):
        finalSignal[i * soundLength : i * soundLength + len(signals[i])] += signals[i]

    return finalSignal


def playStrum(frequencies: list) -> None:
    """
    Play a strum of sounds with the given frequencies.

    Args:
        - frequencies (list): A list of frequencies to play.

    Returns:
        - None
    """
    signals = [createCordFrequency(f) for f in frequencies]
    playSound(combineSounds(signals))


if __name__ == "__main__":
    frequencies = [329.63, 246.94, 196.00, 146.83, 110.00, 82.41]
    playStrum(frequencies)
