# https://en.wikipedia.org/wiki/Harp

import instrument


class Harp36String(instrument.Instrument):
    # https://www.harpsatsang.com/harp_design/data/stringcalculator.html

    frequencies = [
        1864.655,
        1760.000,
        1567.982,
        1396.913,
        1318.510,
        1174.659,
        1046.502,
        932.328,
        880.000,
        783.991,
        698.456,
        659.255,
        587.330,
        523.251,
        466.164,
        440.000,
        391.995,
        349.228,
        329.628,
        293.665,
        261.626,
        233.082,
        220.000,
        195.998,
        174.614,
        164.814,
        146.832,
        130.813,
        116.541,
        110.000,
        97.999,
        87.307,
        82.407,
        73.416,
        65.406,
        58.270,
    ]

    lengths = [
        0.080,
        0.100,
        0.123,
        0.145,
        0.165,
        0.175,
        0.190,
        0.225,
        0.240,
        0.260,
        0.275,
        0.295,
        0.315,
        0.330,
        0.348,
        0.370,
        0.390,
        0.415,
        0.445,
        0.477,
        0.510,
        0.545,
        0.585,
        0.628,
        0.675,
        0.728,
        0.785,
        0.850,
        0.900,
        0.950,
        1.000,
        1.045,
        1.090,
        1.130,
        1.168,
        1.205,
    ]

    # https://en.wikipedia.org/wiki/Silver
    youngModulus = [83 * (10**9)] * len(frequencies)
    density = [10503] * len(frequencies)
