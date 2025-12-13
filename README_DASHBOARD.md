# UAP Signal Generator Dashboard

## Complete Implementation with Hybrid Multi-Layer Approach

### What's Been Built

1. **Enhanced Signal Generation** (`uap_signal_generator.py`)
   - Amplitude modulation (AM) functions
   - Tremolo effects at Schumann resonance (7.83 Hz)
   - Hybrid multi-layer signal architecture
   - Music integration for intelligent signaling

2. **Signal Presets** (`signal_presets.py`)
   - 6 preset configurations:
     - Original UAP Dog Whistle
     - Music Enhanced Signal
     - Harmonic Focus
     - Earth Heartbeat
     - Pure Carrier Waves
     - Biological Mimic

3. **Flask Dashboard** (`app.py`)
   - Interactive web interface
   - Real-time signal generation
   - Music file upload and management
   - Custom tone configuration
   - Live oscilloscope visualization

4. **User Interface** (`templates/dashboard.html`)
   - Bootstrap 5 responsive design
   - Preset selection
   - Frequency controls
   - Modulation settings
   - Real-time waveform display
   - Download capabilities

## Installation

1. Ensure you're in the `.venv` environment:
   ```cmd
   .venv\Scripts\activate
   ```

2. Install required packages:
   ```cmd
   pip install -r requirements.txt
   ```

## Running the Dashboard

1. Start the Flask server:
   ```cmd
   python app.py
   ```

2. Open your browser to:
   ```
   http://localhost:5000
   ```

## Usage Guide

### Quick Start
1. Select a preset from the dropdown (e.g., "Music Enhanced Signal")
2. Optionally upload a music file or select from available files
3. Enable "Use Music Modulation" to integrate music
4. Click "Generate Signal" to create your UAP contact signal
5. View the waveform in the oscilloscope display
6. Download the generated MP3 file

### Custom Configuration
- **Frequencies**: Adjust individual tone frequencies
  - Base Tone: 100 Hz (grounding)
  - Schumann: 7.83 Hz (Earth's heartbeat)
  - DNA Repair: 528 Hz (Solfeggio)
  - Ambient: 432 Hz (harmonic tuning)
  - Chirp: 2500 Hz (attention)
  - Ultrasonic: 17000 Hz (non-human detection)

- **Modulation Settings**:
  - Enable/disable tremolo (Earth heartbeat pulsing)
  - Adjust tremolo depth (0-100%)
  - Enable music modulation for organic quality

### Signal Architecture Explained

**Layer 1: Foundation (Steady, Natural)**
- Base tone and Schumann carrier with optional slow tremolo
- Represents Earth's natural frequencies

**Layer 2: Human Enhancement (Music-Modulated)**
- DNA repair tone and ambient pad modulated by music
- Shows intelligent creative enhancement

**Layer 3: Attention (Pulsing/Organic)**
- Chirps with tremolo and ultrasonic pings
- Creates "alive" signaling quality

**Layer 4: Life Indicator (Breath Layer)**
- Filtered white noise with tremolo
- Mimics biological breathing

## Features

- **6 Signal Presets**: Pre-configured for different contact strategies
- **Music Integration**: Upload MP3, MP4, WAV, FLAC, or M4A files
- **Real-time Visualization**: Live oscilloscope display
- **Custom Frequency Control**: Adjust all tone frequencies
- **Modulation Options**: Tremolo and amplitude modulation
- **Download Signals**: Save generated signals as MP3
- **Responsive Design**: Works on desktop and mobile

## Technical Details

### Amplitude Modulation
Music modulates carrier frequencies, creating a pulsing effect that demonstrates intelligent enhancement of natural Earth frequencies.

### Tremolo at 7.83 Hz
Applies Earth's Schumann resonance as a tremolo rate, creating the "heartbeat" effect that shows awareness of planetary frequencies.

### Hybrid Approach Benefits
- Multiple modulation types for broader detection
- Combines natural and artificial signals
- Creates organic "alive" quality
- Demonstrates intelligent technological capability

## File Structure

```
Ultrasonic_Sweep/
├── app.py                      # Flask application
├── uap_signal_generator.py     # Signal generation engine
├── signal_presets.py           # Preset configurations
├── requirements.txt            # Python dependencies
├── templates/
│   └── dashboard.html          # Main UI template
├── static/
│   ├── css/
│   │   └── dashboard.css       # Custom styles
│   └── js/
│       └── dashboard.js        # Dashboard logic
├── source_files/               # Music files go here
├── generated_signals/          # Output signals saved here
└── .venv/                      # Virtual environment
```

## Next Steps

You can now:
1. Add more preset configurations
2. Implement advanced visualization (FFT spectrum, 3D plots)
3. Add batch generation for multiple signals
4. Create scheduling for automated signal broadcasting
5. Add export formats (WAV, FLAC, etc.)
6. Implement real-time audio playback in browser

## Research References

- UAP Dog Whistle Project: https://github.com/brycehelm/UAP_Dog_Whistle
- Schumann Resonance: Earth's fundamental electromagnetic frequency (7.83 Hz)
- Solfeggio Frequencies: 528 Hz (DNA repair), 432 Hz (harmonic tuning)
