# Analyse the amplitude of the various frequencies in the audion file provided by the user
# Visualize the data in graphical form using matplotlib

import numpy as np
import matplotlib.pyplot as plt

# Read the audio file
import librosa
import os

# Prompt the user to select the audio directory to be analyzed
print("Select the audio directory to analyze:")
print("1. Pleiadian_frequencies")
print("2. BS_Pleiadian_frequencies")
print("3. Frequency_Sweep")

choice = input("Enter the number corresponding to your choice (1, 2, or 3): ")

if choice == "1":
    AUDIO_SOURCE_DIRECTORY = "../Pleiadian_frequencies/"
elif choice == "2":
    AUDIO_SOURCE_DIRECTORY = "../BS_Pleiadian_frequencies/"
elif choice == "3":
    AUDIO_SOURCE_DIRECTORY = "../Frequency_Sweep/"
else:
    raise ValueError("Invalid choice. Please select 1, 2, or 3.")


# # Define the directory containing the audio files
# AUDIO_SOURCE_DIRECTORY = "../Pleiadian_frequencies/"

# Check if the directory exists
if not os.path.exists(AUDIO_SOURCE_DIRECTORY):
    raise FileNotFoundError(f"The directory {AUDIO_SOURCE_DIRECTORY} does not exist.")

# Select the .mp3 file to be analyzed
AUDIO_FILE = None
for file in os.listdir(AUDIO_SOURCE_DIRECTORY):
    if file.endswith(".mp3") or file.endswith(".wav"):
        AUDIO_FILE = os.path.join(AUDIO_SOURCE_DIRECTORY, file)
        break

if AUDIO_FILE is None:
    raise FileNotFoundError(f"No .mp3 file found in the directory {AUDIO_SOURCE_DIRECTORY}. Please ensure the directory contains an .mp3 file.")


# Read the audio file
data, sample_rate = librosa.load(AUDIO_FILE, sr=None)

# If stereo, take only one channel
if len(data.shape) == 2:
    data = data[:, 0]

# Normalize the data
data = data / np.max(np.abs(data))

# Time axis for the waveform
time = np.linspace(0, len(data) / sample_rate, num=len(data))

# Perform FFT
fft_data = np.fft.fft(data)
frequencies = np.fft.fftfreq(len(fft_data), 1 / sample_rate)

# Only keep the positive frequencies
positive_frequencies = frequencies[: len(frequencies) // 2]
positive_fft_data = np.abs(fft_data[: len(fft_data) // 2])

# Plot the waveform
plt.figure(figsize=(12, 6))

plt.subplot(2, 1, 1)
plt.plot(time, data)
plt.title("Waveform")
plt.xlabel("Time [s]")
plt.ylabel("Amplitude")

# Plot the frequency spectrum
plt.subplot(2, 1, 2)
plt.plot(positive_frequencies, positive_fft_data)
plt.title("Frequency Spectrum")
plt.xlabel("Frequency [Hz]")
plt.ylabel("Amplitude")

plt.tight_layout()

# Save the plot as an image file
plot_output_file = os.path.join(AUDIO_SOURCE_DIRECTORY, "frequency_analysis_plot.png")
plt.savefig(plot_output_file)
print(f"Plot saved to {plot_output_file}")

plt.show()


# Save the frequency spectrum data to a file
output_file = os.path.join(AUDIO_SOURCE_DIRECTORY, "frequency_analysis.csv")
np.savetxt(
    output_file,
    np.column_stack((positive_frequencies, positive_fft_data)),
    delimiter=",",
    header="Frequency(Hz),Amplitude",
    comments="",
)

print(f"Frequency analysis saved to {output_file}")

# Save the waveform data to a file
output_file_waveform = os.path.join(AUDIO_SOURCE_DIRECTORY, "waveform.csv")
np.savetxt(
    output_file_waveform,
    np.column_stack((time, data)),
    delimiter=",",
    header="Time(s),Amplitude",
    comments="",
)
print(f"Waveform data saved to {output_file_waveform}")
