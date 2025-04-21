from matplotlib import pyplot as plt
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

# Plot the charts
plt.figure(figsize=(12, 6))

# Waveform chart
plt.subplot(3, 1, 1)
plt.plot(t, waveform, label="Dog Whistle Waveform", color="blue")
plt.title("Dog Whistle Waveform")
plt.xlabel("Time [s]")
plt.ylabel("Amplitude")
plt.grid()
plt.legend(loc="upper right")
plt.subplots_adjust()

# Frequency spectrum chart
plt.subplot(3, 1, 2)
plt.specgram(waveform, Fs=SAMPLE_RATE, NFFT=1024, noverlap=512, cmap="viridis")
plt.title("Dog Whistle Frequency Spectrum")
plt.xlabel("Time [s]")
plt.ylabel("Frequency [Hz]")
plt.colorbar(label="Intensity [dB]", orientation="horizontal", pad=0.5)
plt.ylim(START_FREQ, END_FREQ)  # Limit y-axis to the whistle frequency range

plt.grid()
plt.legend(loc="upper right")
plt.subplots_adjust(hspace=1, bottom=0.1)


# Save the plot as an image file
plt.savefig("Dog_Whistle_Plots.png", dpi=300)
print("Plots saved as 'Dog_Whistle_Plots.png'")
# Show the plots
plt.show()
