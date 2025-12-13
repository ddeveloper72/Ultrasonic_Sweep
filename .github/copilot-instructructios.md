---
description: Ultrasonic Sweep Project - UAP Contact Signal Generator
applyTo: '**'
---

# Ultrasonic Sweep Project Instructions

## Project Overview
This project generates composite audio signals combining various frequencies and sound effects for potential UAP (Unidentified Aerial Phenomena) contact attempts, based on research from the UAP Dog Whistle project.

### Reference Materials
- Primary Research: https://github.com/brycehelm/UAP_Dog_Whistle/blob/main/README.md
- Guide: https://uapwatchers.com/build-a-uap-dog-whistle-guide/
- Local research files stored in `source_files/` directory

### Key Technologies
- **Python 3.12.8** (Required - do not use Python 3.13+ due to audioop compatibility)
- **Flask Web Framework** for interactive dashboard
- **pydub** for audio manipulation (requires FFmpeg)
- **scipy 1.14.1** (stable version, avoid 1.16+ which has import issues)
- **numpy, matplotlib** for signal processing and visualization

## Directory Structure

### Required Directories
- **`source_files/`**: All source materials, reference documents, and input audio files
  - Music files (MP3, MP4, etc.)
  - Research PDFs and documentation
  - Mathematical references for sound generation
- **`static/`**: Static web assets for Flask applications
  - `static/js/` - JavaScript files (separate from HTML)
  - `static/css/` - CSS files (separate from HTML)
  - Images and other static resources
- **`templates/`**: Flask HTML templates
- **`generated_signals/`**: Output directory for generated audio files
- **`Pleiadian_frequencies/`**: Core frequency generation application
- **`BS_Pleiadian_frequencies/`**: Music-aligned frequency generation application
- **`.venv/`**: Python virtual environment (DO NOT MODIFY)

## Coding Standards

### Python Development
### Python Development
1. **Python Version**: Use Python 3.12.8 (installed on host machine)
   - Python 3.13+ has audioop compatibility issues
   - Python 3.14 has scipy import problems
2. **Always work within the `.venv` virtual environment**
   - Create with: `py -3.12 -m venv .venv`
   - Activate: `.venv\Scripts\Activate.ps1` (Windows PowerShell)
3. **Never install packages to the host machine** - use `pip install` within `.venv` only
4. **No emoji icons in Python scripts** - they cause script errors
5. **Use relative paths** for file references:
   ```python
   # Good
   music_file = AudioSegment.from_file("source_files/music_file.mp4", format="mp4")
   
   # Bad
   music_file = AudioSegment.from_file("C:\\Users\\Duncan\\...", format="mp4")
   ```
6. **Use `os.path.join()` for cross-platform paths**
### Audio Processing
1. **FFmpeg Configuration**: Always set FFmpeg path at the start of audio processing scripts:
   ```python
   import pydub
### Flask Applications
1. **Use latest Bootstrap 5 CDN** - do not download Bootstrap locally
2. **Separate static files**: 
   - JavaScript → `static/js/`
   - CSS → `static/css/`
   - Never inline JS/CSS in HTML templates
3. **UI/UX Design Principles**:
   - **Mobile-first design** - design for mobile, then scale up
   - **Responsive layouts** - use Bootstrap grid system
   - **Accessibility** - ensure text contrast meets WCAG standards
   - **Color scheme** - dark theme with high-contrast text
   - Text colors: Use `#c0c0c0` or lighter for muted text on dark backgrounds
4. **Template structure**:
   ```html
   <!DOCTYPE html>
   <html>
   <head>
       <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
       <link href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.0/font/bootstrap-icons.css" rel="stylesheet">
       <link href="{{ url_for('static', filename='css/dashboard.css') }}" rel="stylesheet">
   </head>
   <body>
       <!-- content -->
       <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
       <script src="{{ url_for('static', filename='js/dashboard.js') }}"></script>
   </body>
   </html>
   ```dy>
       <!-- content -->
       <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
       <script src="{{ url_for('static', filename='js/custom.js') }}"></script>
   </body>
   </html>
   ```

### Bash and PowerShell Scripts
1. **No emoji icons** - they cause encoding errors
2. **Use comments** for clarity instead of decorative characters
3. **Cross-platform compatibility**: Consider both Windows and Unix-style paths when applicable

## Git Workflow
1. **Commit changes regularly** using git
2. **Local storage only** - changes are stored locally in this repository
3. **Meaningful commit messages**: Describe what changed and why
4. **Example commit workflow**:
   ```bash
   git add .
   git commit -m "feat: Update app to use source_files directory for music input"
   ```
### Music Integration
- Music files provide the carrier wave for modulation
- Supported formats: MP3, MP4, WAV, FLAC, M4A
- Schumann resonance should align/track with the music duration
- All generated tones should match the music file duration

### Signal Modulation Techniques
- **Amplitude Modulation (AM)**: Music modulates carrier frequencies for organic quality
- **Tremolo**: 7.83 Hz pulsing creates Earth's "heartbeat" effect
- **Hybrid Multi-Layer**: Combines steady carriers, music-modulated tones, and tremolo effects
- Purpose: Demonstrates intelligent beings enhancing natural frequencies
The composite signal should include:
- **Base Tone**: 100 Hz (grounding frequency)
- **Schumann Resonance**: 7.83 Hz (Earth's natural frequency)
- **DNA Repair Tone**: 528 Hz (Solfeggio frequency)
- **Ultrasonic Ping**: 17,000 Hz (high-frequency marker)
## Dependencies
Key Python packages (install in `.venv` with `pip install -r requirements.txt`):
- `flask>=3.0.0` - Web framework for dashboard
- `pydub>=0.25.1` - Audio manipulation (requires FFmpeg)
- `numpy>=1.24.0` - Numerical processing
- `scipy==1.14.1` - Signal processing (use 1.14.1, NOT 1.16+ due to import issues)
- `werkzeug>=3.0.0` - WSGI utilities
- `matplotlib>=3.7.0` - Plotting and visualization

**Important**: Python 3.12.8 required. Do NOT use Python 3.13+ (audioop missing) or 3.14 (scipy issues)uration
- All generated tones should match the music file duration

## Data Visualization
- Use `matplotlib` for waveform, frequency spectrum, and amplitude envelope plots
- Downsample data for performance (factor of 10 recommended)
- Export plots as high-resolution PNG files (300 DPI minimum)

## Dependencies
Key Python packages (install in `.venv`):
- `pydub` - Audio manipulation
- `numpy` - Numerical processing
- `scipy` - Signal processing
- `matplotlib` - Plotting
- `flask` - Web framework (when building web interfaces)

## Best Practices
1. **Error Handling**: Always handle file not found and audio processing errors gracefully
2. **Path Handling**: Use `os.path.join()` or `pathlib.Path` for cross-platform compatibility
3. **Documentation**: Comment complex audio processing algorithms
## Dashboard Features
The Flask dashboard (`app.py`) provides:
- **6 Signal Presets**: Original UAP, Music Enhanced, Harmonic Focus, Earth Heartbeat, Pure Carriers, Biological Mimic
- **Custom Frequency Controls**: Adjust all tone frequencies individually
- **Music Upload/Selection**: Integrate user-provided music files
- **Modulation Settings**: Enable/disable tremolo and music modulation
- **Live Oscilloscope**: Real-time waveform visualization
- **Signal Download**: Export generated signals as MP3 files
- **Signal Information**: View layer architecture and modulation details

## Running the Application
```powershell
# Ensure Python 3.12 venv is activated
.venv\Scripts\Activate.ps1

# Start Flask server
python app.py

# Access dashboard at http://localhost:5000
```

## Troubleshooting
- **scipy import hangs**: Use scipy==1.14.1, not 1.16+
- **audioop errors**: Use Python 3.12.8, not 3.13+
- **Flask not found**: Ensure `.venv` is activated before running
- **Text not visible**: Use `#c0c0c0` or lighter colors for text on dark backgrounds
- **FFmpeg errors**: Verify FFmpeg path in audio processing scripts

## Prohibited Actions
- Installing packages outside `.venv`
- Using absolute file paths (use `os.path.join()` instead)
- Inline JavaScript/CSS in Flask templates
- Emoji characters in any scripts
- Modifying `.venv` directory contents directly
- Using Python 3.13+ or 3.14 (compatibility issues)
- Installing scipy 1.16+ (has import problems)appropriately)
3. Document any new frequency additions with their purpose
4. Test the output audio file for quality and duration
5. Update visualization code to include new layers

## Prohibited Actions
- Installing packages outside `.venv`
- Using absolute file paths
- Inline JavaScript/CSS in Flask templates
- Emoji characters in any scripts
- Modifying `.venv` directory contents directly