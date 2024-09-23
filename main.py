import numpy as np
import sounddevice as sd


def calculateStringFrequency(
    length: float, tension: float, massPerLegth: float
) -> float:
    """
    This formula is extracted from the following link:
    https://en.wikipedia.org/wiki/Mersenne%27s_laws

    It calculates the frequency of a string given its length, tension and mass per length.

    Args:
        - length (float): The length of the string in meters.
        - tension (float): The tension or force of the string in newtons.
        - massPerLegth (float): The mass per length of the string in
            kilograms per meter. https://en.wikipedia.org/wiki/Linear_density

    Returns:
        - float: The frequency of the string in hertz.
    """
    return np.sqrt(tension / massPerLegth) / (2 * length)


def playCordFrequency(frequency: float) -> None:
    """
    Play a sound with the given frequency using the Karplus-Strong algorithm.
    https://en.wikipedia.org/wiki/Karplus%E2%80%93Strong_string_synthesis

    We also got this code from the following link:
    https://github.com/earthspecies/intro-to-DSP-with-python/blob/main/02_Generate_a_sound_that_resembles_violin.ipynb
    and had ChatGPT modify it to change the frecuency of the sound.

    Args:
        - frequency (float): The frequency of the sound to play.

    Returns:
        - None
    """
    sr = 16000  # Sample rate
    decay = 0.99  # Feedback decay factor
    duration = 2  # Duration in seconds

    # Calculate delay length based on frequency
    delay_length = int(sr / frequency)  # Samples
    delay_line = np.random.rand(delay_length) * 2 - 1  # Initialize with random values

    # Initialize the output signal
    signal = np.zeros(int(sr * duration))

    # Fill the output signal with the initial noise
    for i in range(delay_length):
        signal[i] = delay_line[i]

    # Generate the signal using the Karplus-Strong method
    for i in range(delay_length, len(signal)):
        # Average the first two samples of the delay line
        avg = 0.5 * (delay_line[i % delay_length] + delay_line[(i + 1) % delay_length])
        # Apply decay
        output = avg * decay
        # Store in the delay line and signal
        delay_line[i % delay_length] = output
        signal[i] = output

    # Play the synthesized sound
    sd.play(signal, samplerate=sr)
    sd.wait()  # Wait until the audio is done playing


def calculateStringTension(
    elasticModulus: float, crossSection: float, originalLength: float, newLength: float
) -> float:
    """
    This formula appears in the "Tensional stress of a uniform bar"
    of the following link:
    https://en.wikipedia.org/wiki/Hooke%27s_law#Tensional_stress_of_a_uniform_bar

    Args:
        - elasticModulus (float): The elastic modulus of the string in pascals.
            Specifically it is the Young's modulus:
            https://en.wikipedia.org/wiki/Elastic_modulus
            https://en.wikipedia.org/wiki/Young%27s_modulus
        - crossSection (float): The cross section of the string in square meters.
        - originalLength (float): The original length of the string in meters.
        - newLength (float): The new length of the string in meters.

    Returns:
        - float: The tension of the string in newtons.
    """
    return elasticModulus * crossSection * (newLength - originalLength) / originalLength


if __name__ == "__main__":
    # https://en.wikipedia.org/wiki/Guitar_tunings
    frecuencies = [329.63, 246.94, 196.00, 146.83, 110.00, 82.41]

    for f in frecuencies:
        playCordFrequency(f)

    # https://en.wikipedia.org/wiki/Audio_frequency
    maxFrecuency = 20000
    minFrecuency = 20

    # https://en.wikipedia.org/wiki/Psychoacoustics
    frequencyDiscrimination = 3.6

    # https://en.wikipedia.org/wiki/Scale_length_(string_instruments)
    guitarLength = 0.65
