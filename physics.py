import numpy as np


def calculateNewLength(
    origLength: float, actualLength: float, turnAngle: float
) -> float:
    """
    This function calculates the new length of a string given its original length,
    the actual length and the turn angle.

    If the turnAngle is positive, the new length will be greater than the actual length.
    If the turnAngle is negative, the new length will be less than the actual length.

    We estimate that the string peg to be 3 mm in radius.
    We use a photo that Lucas gave us. It is in the documentation file.

    We do not allow the new length to be less than the original length.

    Args:
        - origLength (float): The original length of the string in meters.
        - actualLength (float): The actual length of the string in meters.
        - turnAngle (float): The turn angle of the string in revolutions.

    Returns:
        - float: The new length of the string in meters.
    """

    newLength = actualLength + (2 * np.pi * 0.003 * turnAngle)

    return max(origLength, newLength)


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


def calculateStringFrequencyMersenne(
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


def calculateStringNewFrequency(
    origLength: float,
    actualLength: float,
    turnAngle: float,
    youngModulus: float,
    density: float,
) -> float:
    """
    We calculate the new frequency of the string.

    We use a formula that we derived from the other formulas.


    Args:
        - origLength (float): The original length of the string in meters.
        - actualLength (float): The actual length of the string in meters.
        - turnAngle (float): The turn angle of the string in degrees.
        - youngModulus (float): The Young's modulus of the string in pascals.
        - density (float): The density of the string in kilograms per cubic meter.

    Returns:
        - float: The new frequency of the string in hertz.
    """

    newLength = calculateNewLength(origLength, actualLength, turnAngle)
    lengthDifference = newLength - origLength
    return (
        ((youngModulus * lengthDifference * newLength) / (density * origLength**2))
        ** (1 / 2)
    ) / (2 * origLength)


def calculateNewLengthByFrequency(
    initialLength: float, frequency: float, youngModulus: float, density: float
) -> float:
    """
    We calculate the length of the stretched string so it gives a certain frequency.

    The formula is derived from calculateStringNewFrequency() solving for the new length.


    Args:
        - initialLength (float): The initial length of the string in meters.
        - frequency (float): The frequency of the string in hertz.
        - youngModulus (float): The Young's modulus of the string in pascals.
        - density (float): The density of the string in kilograms per cubic meter.

    Returns:
        - float: The new length of the string in meters.
    """
    return (
        initialLength
        + (
            initialLength**2
            + (16 * density * frequency**2 * initialLength**4) / youngModulus
        )
        ** (1 / 2)
    ) / 2
