import sound


if __name__ == "__main__":
    # https://en.wikipedia.org/wiki/Guitar_tunings
    frecuencies = [329.63, 246.94, 196.00, 146.83, 110.00, 82.41]

    for f in frecuencies:
        sound.playCordFrequency(f)

    # https://en.wikipedia.org/wiki/Audio_frequency
    maxFrecuency = 20000
    minFrecuency = 20

    # https://en.wikipedia.org/wiki/Psychoacoustics
    frequencyDiscrimination = 3.6

    # https://en.wikipedia.org/wiki/Scale_length_(string_instruments)
    guitarLength = 0.65
