# -*- coding: utf-8 -*-
"""
UAP Signal Generator Flask Application
Interactive dashboard for customizing and generating UAP contact signals
"""
from flask import Flask, render_template, request, jsonify, send_file
from werkzeug.utils import secure_filename
import os
import json
import numpy as np
from uap_signal_generator import generate_hybrid_uap_signal, apply_amplitude_modulation, apply_tremolo
from signal_presets import get_all_presets, get_preset
from pydub import AudioSegment
import io

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB max file size
app.config['UPLOAD_FOLDER'] = 'source_files'
app.config['OUTPUT_FOLDER'] = 'generated_signals'

# Ensure output directory exists
os.makedirs(app.config['OUTPUT_FOLDER'], exist_ok=True)

ALLOWED_EXTENSIONS = {'mp3', 'mp4', 'wav', 'flac', 'm4a'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def index():
    """Main dashboard page"""
    presets = get_all_presets()
    return render_template('dashboard.html', presets=presets)


@app.route('/api/presets')
def api_presets():
    """Get all available presets"""
    return jsonify(get_all_presets())


@app.route('/api/preset/<preset_name>')
def api_preset(preset_name):
    """Get a specific preset configuration"""
    preset = get_preset(preset_name)
    return jsonify(preset)


@app.route('/api/generate', methods=['POST'])
def api_generate():
    """Generate signal based on configuration"""
    try:
        data = request.json
        config = data.get('config', {})
        use_music = data.get('use_music', False)
        music_file = data.get('music_file', None)
        
        # Determine music file path
        music_path = None
        if use_music and music_file:
            music_path = os.path.join(app.config['UPLOAD_FOLDER'], music_file)
            if not os.path.exists(music_path):
                music_path = None
        
        # Generate signal
        signal, metadata = generate_hybrid_uap_signal(
            music_file_path=music_path,
            duration_ms=int(data.get('duration', 10000)),
            config=config
        )
        
        # Save to file
        output_filename = f"UAP_Signal_{data.get('preset_name', 'custom')}.mp3"
        output_path = os.path.join(app.config['OUTPUT_FOLDER'], output_filename)
        signal.export(output_path, format="mp3")
        
        # Get waveform data for visualization
        waveform_data = get_waveform_data(signal, samples=1000)
        
        return jsonify({
            'status': 'success',
            'filename': output_filename,
            'metadata': metadata,
            'waveform': waveform_data,
            'duration_ms': len(signal)
        })
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500


@app.route('/api/download/<filename>')
def api_download(filename):
    """Download generated signal file"""
    file_path = os.path.join(app.config['OUTPUT_FOLDER'], secure_filename(filename))
    if os.path.exists(file_path):
        return send_file(file_path, as_attachment=True)
    return jsonify({'status': 'error', 'message': 'File not found'}), 404


@app.route('/api/upload_music', methods=['POST'])
def api_upload_music():
    """Upload music file for signal modulation"""
    if 'file' not in request.files:
        return jsonify({'status': 'error', 'message': 'No file provided'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'status': 'error', 'message': 'No file selected'}), 400
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Get file info
        audio = AudioSegment.from_file(filepath)
        duration_ms = len(audio)
        
        return jsonify({
            'status': 'success',
            'filename': filename,
            'duration_ms': duration_ms,
            'duration_seconds': duration_ms / 1000
        })
    
    return jsonify({'status': 'error', 'message': 'Invalid file type'}), 400


@app.route('/api/list_music')
def api_list_music():
    """List available music files"""
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        return jsonify({'files': []})
    
    files = []
    for filename in os.listdir(app.config['UPLOAD_FOLDER']):
        if allowed_file(filename):
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            try:
                audio = AudioSegment.from_file(filepath)
                files.append({
                    'filename': filename,
                    'duration_ms': len(audio),
                    'duration_seconds': len(audio) / 1000
                })
            except:
                pass
    
    return jsonify({'files': files})


@app.route('/api/waveform/<filename>')
def api_waveform(filename):
    """Get waveform data for visualization"""
    file_path = os.path.join(app.config['OUTPUT_FOLDER'], secure_filename(filename))
    
    if not os.path.exists(file_path):
        return jsonify({'status': 'error', 'message': 'File not found'}), 404
    
    try:
        audio = AudioSegment.from_file(file_path)
        waveform_data = get_waveform_data(audio, samples=2000)
        
        return jsonify({
            'status': 'success',
            'waveform': waveform_data,
            'duration_ms': len(audio)
        })
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500


def get_waveform_data(audio_segment, samples=1000):
    """Extract waveform data from AudioSegment for visualization"""
    audio_array = np.array(audio_segment.get_array_of_samples())
    
    # Downsample for visualization
    step = max(1, len(audio_array) // samples)
    downsampled = audio_array[::step]
    
    # Normalize to -1 to 1
    if downsampled.max() != downsampled.min():
        normalized = downsampled / max(abs(downsampled.max()), abs(downsampled.min()))
    else:
        normalized = downsampled
    
    return normalized.tolist()


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
