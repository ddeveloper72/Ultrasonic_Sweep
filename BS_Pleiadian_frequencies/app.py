# -*- coding: utf-8 -*-
from pydub.generators import Sine, WhiteNoise
from pydub import AudioSegment
from pydub.effects import low_pass_filter
import numpy as np
from scipy.fftpack import fft
from scipy.signal import hilbert

# Removed redundant import of matplotlib.pyplot

# Load the music file
music_file = AudioSegment.from_file(
    "Gerry_Rafferty_Baker_Street_(UK).mp4", format="mp4"
)  # Replace with the actual path
music_duration = len(music_file)  # Get the duration of the music file in milliseconds

# Generate other tones and layers with scaled durations
base_tone = Sine(100).to_audio_segment(duration=music_duration).apply_gain(-6)
schumann_carrier = Sine(7.83).to_audio_segment(duration=music_duration).apply_gain(-12)
dna_repair_tone = Sine(528).to_audio_segment(duration=10000).apply_gain(-6)
ultrasonic_ping = Sine(17000).to_audio_segment(duration=500).apply_gain(-3)
chirps = Sine(2500).to_audio_segment(duration=300).apply_gain(-3)
ambient_pad = Sine(432).to_audio_segment(duration=music_duration).apply_gain(-9)	

# Align the music file with the breath layer
breath_layer_duration = music_duration
breath_layer = low_pass_filter(
    WhiteNoise().to_audio_segment(duration=breath_layer_duration), cutoff=300
).apply_gain(-18)
aligned_breath_layer = breath_layer[:music_duration]  # Align with music duration


# Create chirp sequence
chirp_sequence = AudioSegment.silent(duration=music_duration)
chirp_sequence = chirp_sequence.overlay(chirps, position=0)
chirp_sequence = chirp_sequence.overlay(chirps, position=music_duration - 10000)

# Combine all layers
composite_signal = base_tone.overlay(schumann_carrier)
composite_signal = composite_signal.overlay(aligned_breath_layer)
composite_signal = composite_signal.overlay(chirp_sequence)
composite_signal = composite_signal.overlay(ultrasonic_ping, position=5000)

# Export the final composite signal
composite_signal.export("Pleiadian_Contact_Signal_With_Music.mp3", format="mp3")
print(
    "Pleiadian Contact Signal with music generated and saved as 'Pleiadian_Contact_Signal_With_Music.mp3'"
)

# Plot the waveform, frequency spectrum, and amplitude envelope of the final composite signal
import matplotlib.pyplot as plt


# Convert AudioSegment to numpy array for processing
def audio_segment_to_array(audio_segment):
    return np.array(audio_segment.get_array_of_samples())


# Compute the frequency spectrum
def compute_frequency_spectrum(audio_array, sample_rate):
    n = len(audio_array)
    freq = np.fft.rfftfreq(n, d=1 / sample_rate)
    magnitude = np.abs(fft(audio_array)[: len(freq)])
    return freq, magnitude


# Compute the amplitude envelope
def compute_amplitude_envelope(audio_array):
    analytic_signal = hilbert(audio_array)
    envelope = np.abs(analytic_signal)
    return envelope


# Convert composite signal to numpy array
sample_rate = composite_signal.frame_rate
composite_array = audio_segment_to_array(composite_signal)

# Compute frequency spectrum and amplitude envelope
freq, magnitude = compute_frequency_spectrum(composite_array, sample_rate)
amplitude_envelope = compute_amplitude_envelope(composite_array)

# Downsample data for plotting
downsample_factor = 10  # Take every 10th data point
downsampled_composite_array = composite_array[::downsample_factor]
downsampled_amplitude_envelope = amplitude_envelope[::downsample_factor]
downsampled_freq = freq[::downsample_factor]
downsampled_magnitude = magnitude[::downsample_factor]

# Plot the charts
plt.figure(figsize=(18, 12))

# Waveform chart
plt.subplot(3, 1, 1)
plt.plot(
    downsampled_composite_array,
    label="Composite Waveform (downsampled)",
    color="blue",
    linewidth=1,
)
plt.plot(
    audio_segment_to_array(base_tone)[::downsample_factor],
    label="Base Tone",
    color="green",
    linewidth=1,
)
plt.plot(
    audio_segment_to_array(schumann_carrier)[::downsample_factor],
    label="Schumann Carrier",
    color="orange",
    linewidth=1,
)
plt.plot(
    audio_segment_to_array(dna_repair_tone)[::downsample_factor],
    label="DNA Repair Tone",
    color="purple",
    linewidth=1,
)
plt.plot(
    audio_segment_to_array(ambient_pad)[::downsample_factor],
    label="Ambient Pad",
    color="cyan",
    linewidth=1,
)
plt.plot(
    audio_segment_to_array(breath_layer)[::downsample_factor],
    label="Breath Layer",
    color="magenta",
    linewidth=1,
)
plt.plot(
    audio_segment_to_array(chirp_sequence)[::downsample_factor],
    label="Chirp Sequence",
    color="brown",
    linewidth=1,
)
plt.plot(
    audio_segment_to_array(ultrasonic_ping)[::downsample_factor],
    label="Ultrasonic Ping",
    color="red",
    linewidth=1,
)
plt.title("Waveform of Pleiadian Contact Signal with Music")
plt.xlabel("Sample Number (downsampled)")
plt.ylabel("Amplitude")
plt.grid()
plt.legend(loc="upper right")  # Specify a fixed location for the legend

# Frequency spectrum chart
plt.subplot(3, 1, 2)
plt.plot(
    downsampled_freq,
    downsampled_magnitude,
    label="Frequency Spectrum (downsampled)",
    color="black",
    linewidth=1,
)
plt.title("Frequency Spectrum of Pleiadian Contact Signal with Music")
plt.xlabel("Frequency (Hz)")
plt.ylabel("Magnitude")
plt.grid()
plt.legend()

# Amplitude envelope chart
plt.subplot(3, 1, 3)
plt.plot(
    downsampled_amplitude_envelope,
    label="Amplitude Envelope (downsampled)",
    color="red",
    linewidth=1,
)
plt.title("Amplitude Envelope of Pleiadian Contact Signal with Music")
plt.xlabel("Sample Number (downsampled)")
plt.ylabel("Amplitude")
plt.grid()
plt.legend()

plt.tight_layout()
plt.show()
