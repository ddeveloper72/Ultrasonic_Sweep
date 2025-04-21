# This script generates a composite audio signal that combines various frequencies and sound effects
from pydub.generators import Sine, WhiteNoise
from pydub import AudioSegment
from pydub.effects import low_pass_filter

base_tone = Sine(100).to_audio_segment(duration=10000).apply_gain(-6)
schumann_carrier = Sine(7.83).to_audio_segment(duration=10000).apply_gain(-12)
dna_repair_tone = Sine(528).to_audio_segment(duration=10000).apply_gain(-6)
ultrasonic_ping = Sine(17000).to_audio_segment(duration=500).apply_gain(-3)
chirps = Sine(2500).to_audio_segment(duration=300).apply_gain(-3)
ambient_pad = Sine(432).to_audio_segment(duration=10000).apply_gain(-9)
breath_layer = (
    low_pass_filter(
        WhiteNoise().to_audio_segment(duration=10000),
        cutoff=300
    )
    .apply_gain(-18)
)

chirp_sequence = AudioSegment.silent(duration=10000)
chirp_sequence = chirp_sequence.overlay(chirps, position=0)
chirp_sequence = chirp_sequence.overlay(chirps, position=10000)

composite_signal = base_tone.overlay(schumann_carrier)
composite_signal = composite_signal.overlay(dna_repair_tone)
composite_signal = composite_signal.overlay(ambient_pad)
composite_signal = composite_signal.overlay(breath_layer)
composite_signal = composite_signal.overlay(chirp_sequence)
composite_signal = composite_signal.overlay(ultrasonic_ping, position=5000)

composite_signal.export("Pleiadian_Contact_Signal.mp3", format="mp3")
print("Pleiadian Contact Signal generated and saved as 'Pleiadian_Contact_Signal.mp3'")
