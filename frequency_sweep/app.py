import numpy as np
from scipy.io.wavfile import write

START_FREQ = 18000
END_FREQ = 24000
DURATION = 60
SAMPLE_RATE = 44100

# Time and frequency data
t = np.linspace(0, DURATION, int(SAMPLE_RATE * DURATION), endpoint=False)
frequencies = np.linspace(START_FREQ, END_FREQ, t.size)
waveform = 0.5 * np.sin(2 * np.pi * frequencies * t)
audio = np.int16(waveform * 32767)

write("uap_dog-whistle.wav", SAMPLE_RATE, audio)
print("Dog whistle sound generated and saved as 'uap_dog-whistle.wav'.")
