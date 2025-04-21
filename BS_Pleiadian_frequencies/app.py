# -*- coding: utf-8 -*-
from pydub.generators import Sine, WhiteNoise
from pydub import AudioSegment
from pydub.effects import low_pass_filter

# Load the music file
music_file = AudioSegment.from_file(
    "Gerry_Rafferty_Baker_Street_(UK).mp4", format="mp4"
)  # Replace with the actual path
music_duration = len(music_file)  # Get the duration of the music file in milliseconds

# Calculate the scaling factor based on the original 60s duration
scaling_factor = music_duration / 60000  # 60000 ms = 60 seconds

# Generate the dna repair tone with the scaled duration
dna_repair_tone = (
    Sine(528).to_audio_segment(duration=music_duration).apply_gain(-6)
)

# Generate the ambient pad with the scaled duration
ambient_pad = (
    Sine(432).to_audio_segment(duration=music_duration).apply_gain(-9)
)

# Align the dna repair tone with the music file
aligned_dna_repair = music_file.overlay(dna_repair_tone)

# Align the ambient pad with the music file
aligned_ambient_pad = music_file.overlay(ambient_pad)

# Generate other tones and layers with scaled durations
schumann_carrier = (
    Sine(7.83).to_audio_segment(duration=music_duration).apply_gain(-12)
)
base_tone = (
    Sine(100).to_audio_segment(duration=music_duration).apply_gain(-6)
)
ultrasonic_ping = (
    Sine(17000).to_audio_segment(duration=500).apply_gain(-3)
)
chirps = Sine(2500).to_audio_segment(duration=300).apply_gain(-3)
breath_layer = low_pass_filter(
    WhiteNoise().to_audio_segment(duration=music_duration), cutoff=300
).apply_gain(-18)

# Create chirp sequence
chirp_sequence = AudioSegment.silent(duration=music_duration)
chirp_sequence = chirp_sequence.overlay(chirps, position=0)
chirp_sequence = chirp_sequence.overlay(chirps, position=music_duration - 10000)

# Combine all layers
composite_signal = base_tone.overlay(schumann_carrier)
composite_signal = composite_signal.overlay(aligned_ambient_pad)
composite_signal = composite_signal.overlay(aligned_ambient_pad)
composite_signal = composite_signal.overlay(breath_layer)
composite_signal = composite_signal.overlay(chirp_sequence)
composite_signal = composite_signal.overlay(ultrasonic_ping, position=5000)

# Export the final composite signal
composite_signal.export("Pleiadian_Contact_Signal_With_Music.mp3", format="mp3")
print(
    "Pleiadian Contact Signal with music generated and saved as 'Pleiadian_Contact_Signal_With_Music.mp3'"
)
