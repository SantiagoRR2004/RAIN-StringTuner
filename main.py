import numpy as np
import sounddevice as sd

frecuencies = [329.63, 246.94, 196.00, 146.83, 110.00, 82.41]

for frequency in frecuencies:
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
