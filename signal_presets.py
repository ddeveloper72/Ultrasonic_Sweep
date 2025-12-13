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
    "music_enhanced": {
        "name": "Music Enhanced Signal",
        "description": "Combines music modulation with Schumann tremolo for intelligent signaling",
        "config": {
            "base_tone_freq": 100,
            "schumann_freq": 7.83,
            "dna_repair_freq": 528,
            "ultrasonic_freq": 17000,
            "chirp_freq": 2500,
            "ambient_freq": 432,
            "use_music_modulation": True,
            "use_tremolo": True,
            "tremolo_depth": 0.5
        }
    },
    "harmonic_focus": {
        "name": "Harmonic Focus",
        "description": "Emphasizes Solfeggio frequencies (528 Hz, 432 Hz) with subtle modulation",
        "config": {
            "base_tone_freq": 100,
            "schumann_freq": 7.83,
            "dna_repair_freq": 528,
            "ultrasonic_freq": 17000,
            "chirp_freq": 2500,
            "ambient_freq": 432,
            "use_music_modulation": True,
            "use_tremolo": True,
            "tremolo_depth": 0.3
        }
    },
    "earth_heartbeat": {
        "name": "Earth Heartbeat",
        "description": "Strong Schumann resonance with deep tremolo pulsing",
        "config": {
            "base_tone_freq": 100,
            "schumann_freq": 7.83,
            "dna_repair_freq": 528,
            "ultrasonic_freq": 17000,
            "chirp_freq": 2500,
            "ambient_freq": 432,
            "use_music_modulation": False,
            "use_tremolo": True,
            "tremolo_depth": 0.7
        }
    },
    "pure_carriers": {
        "name": "Pure Carrier Waves",
        "description": "Unmodulated carrier frequencies for maximum clarity",
        "config": {
            "base_tone_freq": 100,
            "schumann_freq": 7.83,
            "dna_repair_freq": 528,
            "ultrasonic_freq": 17000,
            "chirp_freq": 2500,
            "ambient_freq": 432,
            "use_music_modulation": False,
            "use_tremolo": False,
            "tremolo_depth": 0.0
        }
    },
    "biological_mimic": {
        "name": "Biological Mimic",
        "description": "Maximum organic 'alive' quality with music and tremolo",
        "config": {
            "base_tone_freq": 100,
            "schumann_freq": 7.83,
            "dna_repair_freq": 528,
            "ultrasonic_freq": 17000,
            "chirp_freq": 2500,
            "ambient_freq": 432,
            "use_music_modulation": True,
            "use_tremolo": True,
            "tremolo_depth": 0.6
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
