# -*- coding: utf-8 -*-
"""
UAP Signal Generator - Enhanced Multi-Layer Approach
Combines amplitude modulation, tremolo, and carrier waves for intelligent contact signaling
"""
from pydub.generators import Sine, WhiteNoise
from pydub import AudioSegment
from pydub.effects import low_pass_filter
import numpy as np
from scipy.fftpack import fft
from scipy.signal import hilbert
import pydub
import os
import shutil

# Configure FFmpeg - check for system ffmpeg first, then Windows path
ffmpeg_path = shutil.which('ffmpeg')
if not ffmpeg_path:
    # Try Windows path if on Windows
    windows_path = "C:\\Users\\Duncan\\FFmpeg\\bin\\ffmpeg.exe"
    if os.path.exists(windows_path):
        ffmpeg_path = windows_path
    else:
        # Default to system ffmpeg (Heroku installs it in /usr/bin)
        ffmpeg_path = '/usr/bin/ffmpeg'

AudioSegment.converter = ffmpeg_path
AudioSegment.ffmpeg = ffmpeg_path
AudioSegment.ffprobe = ffmpeg_path.replace('ffmpeg', 'ffprobe')


def apply_amplitude_modulation(carrier, modulator):
    """
    Apply amplitude modulation using modulator signal
    
    Args:
        carrier: AudioSegment to be modulated
        modulator: AudioSegment used as modulation source
    
    Returns:
        AudioSegment with amplitude modulation applied
    """
    # Convert both to mono to ensure compatibility
    carrier = carrier.set_channels(1)
    modulator = modulator.set_channels(1)
    
    # Ensure both signals have same sample rate
    if carrier.frame_rate != modulator.frame_rate:
        modulator = modulator.set_frame_rate(carrier.frame_rate)
    
    # Ensure both signals are same length
    min_length = min(len(carrier), len(modulator))
    carrier = carrier[:min_length]
    modulator = modulator[:min_length]
    
    # Convert to numpy arrays
    carrier_array = np.array(carrier.get_array_of_samples(), dtype=np.float32)
    mod_array = np.array(modulator.get_array_of_samples(), dtype=np.float32)
    
    # Normalize modulator to 0-1 range
    if mod_array.max() != mod_array.min():
        mod_normalized = (mod_array - mod_array.min()) / (mod_array.max() - mod_array.min())
    else:
        mod_normalized = np.ones_like(mod_array) * 0.5
    
    # Apply modulation (scale carrier by modulator)
    modulated = carrier_array * mod_normalized
    
    # Convert back to AudioSegment
    modulated_int16 = np.clip(modulated, -32768, 32767).astype(np.int16)
    
    return AudioSegment(
        modulated_int16.tobytes(),
        frame_rate=carrier.frame_rate,
        sample_width=carrier.sample_width,
        channels=carrier.channels
    )


def apply_tremolo(audio, rate=7.83, depth=0.5):
    """
    Apply tremolo effect at specified rate (Hz)
    
    Args:
        audio: AudioSegment to apply tremolo to
        rate: Tremolo rate in Hz (default 7.83 for Schumann resonance)
        depth: Tremolo depth 0-1 (default 0.5)
    
    Returns:
        AudioSegment with tremolo applied
    """
    duration_ms = len(audio)
    sample_rate = audio.frame_rate
    
    # Generate tremolo LFO (Low Frequency Oscillator)
    num_samples = int((duration_ms / 1000.0) * sample_rate)
    t = np.linspace(0, duration_ms / 1000.0, num_samples)
    lfo = 1 - depth + depth * np.sin(2 * np.pi * rate * t)
    
    # Apply to audio
    audio_array = np.array(audio.get_array_of_samples(), dtype=np.float32)
    
    # Match lengths
    min_len = min(len(audio_array), len(lfo))
    tremolo_audio = audio_array[:min_len] * lfo[:min_len]
    
    # Convert back to int16
    tremolo_int16 = np.clip(tremolo_audio, -32768, 32767).astype(np.int16)
    
    return AudioSegment(
        tremolo_int16.tobytes(),
        frame_rate=audio.frame_rate,
        sample_width=audio.sample_width,
        channels=audio.channels
    )


def generate_hybrid_uap_signal(music_file_path=None, duration_ms=10000, config=None, progress_callback=None):
    """
    Generate hybrid multi-layer UAP contact signal
    
    Args:
        music_file_path: Path to music file (optional)
        duration_ms: Duration in milliseconds if no music file
        config: Dictionary with tone configurations
        progress_callback: Optional callback function(progress, message) for progress updates
    
    Returns:
        Tuple of (composite_signal, metadata)
    """
    # Default configuration
    if config is None:
        config = {
            'base_tone_freq': 100,
            'schumann_freq': 7.83,
            'dna_repair_freq': 528,
            'ultrasonic_freq': 17000,
            'chirp_freq': 2500,
            'ambient_freq': 432,
            'use_music_modulation': True,
            'use_music_as_foundation': False,
            'use_tremolo': True,
            'tremolo_depth': 0.5
        }
    
    # Load music file if provided
    if progress_callback:
        progress_callback(5, 'Loading music file...')
    
    if music_file_path and os.path.exists(music_file_path):
        music_file = AudioSegment.from_file(music_file_path)
        music_duration = len(music_file)
    else:
        music_file = None
        music_duration = duration_ms
    
    if progress_callback:
        progress_callback(15, 'Generating foundation layers...')
    
    # LAYER 1: Foundation (Steady, Natural)
    if config.get('use_music_as_foundation') and music_file:
        # Use music as the foundation layer - keep it prominent
        base_tone = music_file.apply_gain(-3)
        schumann_carrier = Sine(config['schumann_freq']).to_audio_segment(duration=music_duration).apply_gain(-18)
    else:
        # Use synthetic tones as foundation
        base_tone = Sine(config['base_tone_freq']).to_audio_segment(duration=music_duration).apply_gain(-6)
        schumann_carrier = Sine(config['schumann_freq']).to_audio_segment(duration=music_duration).apply_gain(-12)
    
    # Apply slow tremolo to Schumann if enabled
    if config['use_tremolo']:
        schumann_carrier = apply_tremolo(schumann_carrier, rate=config['schumann_freq'], depth=0.3)
    
    if progress_callback:
        progress_callback(30, 'Creating human enhancement layers...')
    
    # LAYER 2: Human Enhancement (Music-Modulated)
    dna_repair_tone = Sine(config['dna_repair_freq']).to_audio_segment(duration=music_duration).apply_gain(-9)
    ambient_pad = Sine(config['ambient_freq']).to_audio_segment(duration=music_duration).apply_gain(-9)
    
    if music_file and config['use_music_modulation']:
        if progress_callback:
            progress_callback(45, 'Applying music modulation...')
        # Music modulates DNA repair and ambient pad - showing human creativity
        dna_repair_tone = apply_amplitude_modulation(dna_repair_tone, music_file)
        ambient_pad = apply_amplitude_modulation(ambient_pad, music_file)
    
    if progress_callback:
        progress_callback(60, 'Generating attention signals...')
    
    # LAYER 3: Attention Signals (Pulsing/Organic)
    ultrasonic_ping = Sine(config['ultrasonic_freq']).to_audio_segment(duration=500).apply_gain(-3)
    chirps = Sine(config['chirp_freq']).to_audio_segment(duration=300).apply_gain(-3)
    
    # Apply tremolo to chirps
    if config['use_tremolo']:
        chirps = apply_tremolo(chirps, rate=config['schumann_freq'], depth=config['tremolo_depth'])
    
    # Create chirp sequence - repeat throughout the duration
    chirp_sequence = AudioSegment.silent(duration=music_duration)
    chirp_interval = 2000  # Place a chirp every 2 seconds
    position = 0
    while position < music_duration:
        chirp_sequence = chirp_sequence.overlay(chirps, position=position)
        position += chirp_interval
    
    if progress_callback:
        progress_callback(70, 'Creating life indicator layer...')
    
    # LAYER 4: Breath Layer (Life Indicator)
    breath_layer = low_pass_filter(
        WhiteNoise().to_audio_segment(duration=music_duration),
        cutoff=300
    ).apply_gain(-18)
    
    if config['use_tremolo']:
        breath_layer = apply_tremolo(breath_layer, rate=config['schumann_freq'], depth=0.4)
    
    # Create ultrasonic ping sequence - repeat throughout the duration
    ultrasonic_sequence = AudioSegment.silent(duration=music_duration)
    ping_interval = 3500  # Place an ultrasonic ping every 3.5 seconds
    position = 0
    while position < music_duration - 500:  # Ensure last ping fits
        ultrasonic_sequence = ultrasonic_sequence.overlay(ultrasonic_ping, position=position)
        position += ping_interval
    
    if progress_callback:
        progress_callback(80, 'Mixing all signal layers...')
    
    # Combine all layers
    composite_signal = base_tone.overlay(schumann_carrier)
    composite_signal = composite_signal.overlay(dna_repair_tone)
    composite_signal = composite_signal.overlay(ambient_pad)
    composite_signal = composite_signal.overlay(breath_layer)
    composite_signal = composite_signal.overlay(chirp_sequence)
    composite_signal = composite_signal.overlay(ultrasonic_sequence)
    
    # Overlay music if present and not used as foundation
    if music_file and not config.get('use_music_as_foundation'):
        composite_signal = composite_signal.overlay(music_file.apply_gain(-3))
    
    if progress_callback:
        progress_callback(95, 'Finalizing signal...')
    
    # Metadata
    foundation_layers = ['music_base', 'schumann_carrier'] if config.get('use_music_as_foundation') and music_file else ['base_tone', 'schumann_carrier']
    metadata = {
        'duration_ms': music_duration,
        'layers': {
            'foundation': foundation_layers,
            'human_enhancement': ['dna_repair_tone', 'ambient_pad'],
            'attention': ['chirps', 'ultrasonic_ping'],
            'life_indicator': ['breath_layer']
        },
        'modulation': {
            'music_modulation': config['use_music_modulation'] and music_file is not None,
            'music_as_foundation': config.get('use_music_as_foundation', False),
            'tremolo': config['use_tremolo'],
            'tremolo_rate': config['schumann_freq']
        }
    }
    
    return composite_signal, metadata


if __name__ == "__main__":
    # Example usage - generate signal without music
    # To use music, provide path to your audio file or use the web dashboard
    
    signal, meta = generate_hybrid_uap_signal(duration_ms=10000)
    
    signal.export("UAP_Hybrid_Contact_Signal.mp3", format="mp3")
    print("Hybrid UAP Contact Signal generated!")
    print(f"Metadata: {meta}")
