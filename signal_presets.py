# -*- coding: utf-8 -*-
"""
UAP Signal Presets Configuration
Defines preset signal types for the Flask dashboard
"""

SIGNAL_PRESETS = {
    "original_uap": {
        "name": "Original UAP Dog Whistle",
        "description": "Based on the original UAP Dog Whistle project with Schumann resonance",
        "config": {
            "base_tone_freq": 100,
            "schumann_freq": 7.83,
            "dna_repair_freq": 528,
            "ultrasonic_freq": 17000,
            "chirp_freq": 2500,
            "ambient_freq": 432,
            "use_music_modulation": False,
            "use_tremolo": True,
            "tremolo_depth": 0.5
        }
    },
    "schumann_pure": {
        "name": "Schumann Resonance (Pure)",
        "description": "Earth's natural electromagnetic frequency - pure 7.83 Hz foundation",
        "config": {
            "base_tone_freq": 7.83,
            "schumann_freq": 7.83,
            "dna_repair_freq": 528,
            "ultrasonic_freq": 15000,
            "chirp_freq": 1500,
            "ambient_freq": 432,
            "use_music_modulation": False,
            "use_tremolo": True,
            "tremolo_depth": 0.7
        }
    },
    "solfeggio_healing": {
        "name": "Solfeggio Healing Tones",
        "description": "Ancient healing frequencies - 396 Hz (liberation), 528 Hz (transformation), 852 Hz (intuition)",
        "config": {
            "base_tone_freq": 396,
            "schumann_freq": 7.83,
            "dna_repair_freq": 528,
            "ultrasonic_freq": 18000,
            "chirp_freq": 852,
            "ambient_freq": 432,
            "use_music_modulation": True,
            "use_tremolo": True,
            "tremolo_depth": 0.4
        }
    },
    "cosmic_alignment": {
        "name": "Cosmic Alignment",
        "description": "Planetary frequencies - Venus (221.23 Hz), Earth-Moon (210.42 Hz), higher harmonics",
        "config": {
            "base_tone_freq": 136.1,
            "schumann_freq": 7.83,
            "dna_repair_freq": 221.23,
            "ultrasonic_freq": 16500,
            "chirp_freq": 3000,
            "ambient_freq": 210.42,
            "use_music_modulation": False,
            "use_tremolo": True,
            "tremolo_depth": 0.5
        }
    },
    "alpha_theta_gateway": {
        "name": "Alpha-Theta Gateway",
        "description": "Brainwave entrainment - Alpha (10.5 Hz) meets Theta (6 Hz) for deep meditation",
        "config": {
            "base_tone_freq": 100,
            "schumann_freq": 6.0,
            "dna_repair_freq": 528,
            "ultrasonic_freq": 17500,
            "chirp_freq": 2000,
            "ambient_freq": 432,
            "use_music_modulation": True,
            "use_tremolo": True,
            "tremolo_depth": 0.6
        }
    },
    "golden_ratio": {
        "name": "Golden Ratio Harmonics",
        "description": "Fibonacci sequence frequencies - 89 Hz, 144 Hz, 233 Hz, 377 Hz (phi relationships)",
        "config": {
            "base_tone_freq": 89,
            "schumann_freq": 8.0,
            "dna_repair_freq": 233,
            "ultrasonic_freq": 17000,
            "chirp_freq": 377,
            "ambient_freq": 144,
            "use_music_modulation": False,
            "use_tremolo": True,
            "tremolo_depth": 0.3
        }
    }
}


def get_preset(preset_name):
    """Get a preset configuration by name"""
    return SIGNAL_PRESETS.get(preset_name, SIGNAL_PRESETS["original_uap"])


def get_all_presets():
    """Get all available presets"""
    return SIGNAL_PRESETS


def get_preset_names():
    """Get list of all preset names"""
    return list(SIGNAL_PRESETS.keys())
