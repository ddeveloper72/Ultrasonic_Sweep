# -*- coding: utf-8 -*-
"""
UAP Signal Generator Flask Application
Interactive dashboard for customizing and generating UAP contact signals
"""
from flask import Flask, render_template, request, jsonify, send_file, Response, stream_with_context
from werkzeug.utils import secure_filename
import os
import json
import numpy as np
from uap_signal_generator import generate_hybrid_uap_signal, apply_amplitude_modulation, apply_tremolo
from signal_presets import get_all_presets, get_preset
from pydub import AudioSegment
import io
import threading
import queue
import uuid
import yt_dlp
import re
import tempfile

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024  # 10MB max file size for music uploads
app.config['UPLOAD_FOLDER'] = 'source_files'
app.config['OUTPUT_FOLDER'] = 'generated_signals'
app.config['COOKIES_FILE'] = 'youtube_cookies.txt'

# Store progress data for each generation task
generation_progress = {}

# Store uploaded music files in memory (filename -> bytes)
uploaded_music_files = {}

# Ensure output directory exists
os.makedirs(app.config['OUTPUT_FOLDER'], exist_ok=True)
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

ALLOWED_EXTENSIONS = {'mp3', 'mp4', 'wav', 'flac', 'm4a'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/health')
def health():
    """Health check endpoint"""
    import shutil
    ffmpeg_status = shutil.which('ffmpeg') or 'not found'
    return jsonify({
        'status': 'ok',
        'ffmpeg': ffmpeg_status,
        'python': os.sys.version
    })


@app.route('/')
def index():
    """Main dashboard page"""
    presets = get_all_presets()
    return render_template('dashboard.html', presets=presets)


@app.route('/documentation')
def documentation():
    """Documentation page"""
    return render_template('documentation.html')


@app.route('/api/documentation')
def api_documentation():
    """Get markdown documentation content"""
    try:
        with open('README.md', 'r', encoding='utf-8') as f:
            content = f.read()
        return content, 200, {'Content-Type': 'text/plain; charset=utf-8'}
    except Exception as e:
        return f"Error loading documentation: {str(e)}", 500


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
    """Initiate signal generation and return task ID"""
    try:
        data = request.json
        print(f"[GENERATE] Received request: {data.get('preset_name', 'unknown')}")
        task_id = str(uuid.uuid4())
        print(f"[GENERATE] Created task ID: {task_id}")
        
        # Store task info
        generation_progress[task_id] = {
            'progress': 0,
            'message': 'Initializing...',
            'status': 'running',
            'result': None,
            'error': None
        }
        
        # Start generation in background thread
        thread = threading.Thread(target=generate_signal_task, args=(task_id, data))
        thread.daemon = True
        thread.start()
        
        return jsonify({
            'status': 'started',
            'task_id': task_id
        })
        
    except Exception as e:
        import traceback
        error_trace = traceback.format_exc()
        print(f"Error starting generation: {error_trace}")
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500


def generate_signal_task(task_id, data):
    """Background task to generate signal with progress updates"""
    try:
        print(f"[TASK {task_id}] Starting generation task")
        config = data.get('config', {})
        use_music = data.get('use_music', False)
        music_file = data.get('music_file', None)
        
        # Determine music file path or data
        music_path = None
        temp_music_file = None
        if use_music and music_file:
            # Check if file exists in memory
            if music_file in uploaded_music_files:
                # Write to temporary file for processing (generator expects file path)
                temp_music_file = tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(music_file)[1])
                temp_music_file.write(uploaded_music_files[music_file])
                temp_music_file.close()
                music_path = temp_music_file.name
                print(f"[TASK {task_id}] Using music file from memory: {music_file} (temp: {music_path})")
            else:
                print(f"[TASK {task_id}] Music file not found in memory: {music_file}")
                music_path = None
        
        # Progress callback
        def update_progress(progress, message):
            generation_progress[task_id]['progress'] = progress
            generation_progress[task_id]['message'] = message
        
        # Generate signal with progress tracking
        signal, metadata = generate_hybrid_uap_signal(
            music_file_path=music_path,
            duration_ms=int(data.get('duration', 10000)),
            config=config,
            progress_callback=update_progress
        )
        
        # Clean up temporary music file if created
        if temp_music_file and music_path and os.path.exists(music_path):
            try:
                os.unlink(music_path)
                print(f"[TASK {task_id}] Cleaned up temporary music file: {music_path}")
            except Exception as cleanup_error:
                print(f"[TASK {task_id}] Warning: Failed to cleanup temp file: {cleanup_error}")
        
        # Export to in-memory buffer instead of file
        update_progress(97, 'Exporting to MP3...')
        output_filename = f"UAP_Signal_{data.get('preset_name', 'custom')}.mp3"
        
        # Create in-memory buffer
        mp3_buffer = io.BytesIO()
        signal.export(mp3_buffer, format="mp3")
        mp3_buffer.seek(0)  # Reset buffer position to start
        
        # Get visualization data
        update_progress(99, 'Generating visualizations...')
        waveform_data = get_waveform_data(signal, samples=1000)
        fft_data = get_fft_data(signal, bins=512)
        
        print(f"[TASK {task_id}] Generation complete!")
        
        # Update task with result (store buffer instead of filename)
        generation_progress[task_id]['status'] = 'completed'
        generation_progress[task_id]['progress'] = 100
        generation_progress[task_id]['message'] = 'Complete!'
        generation_progress[task_id]['result'] = {
            'filename': output_filename,
            'metadata': metadata,
            'waveform': waveform_data,
            'fft': fft_data,
            'mp3_data': mp3_buffer.getvalue(),  # Store raw bytes
            'duration_ms': len(signal)
        }
        
    except Exception as e:
        import traceback
        error_trace = traceback.format_exc()
        print(f"[TASK {task_id}] ERROR: {error_trace}")
        
        # Clean up temporary music file if created
        if temp_music_file and music_path and os.path.exists(music_path):
            try:
                os.unlink(music_path)
                print(f"[TASK {task_id}] Cleaned up temporary music file after error: {music_path}")
            except Exception as cleanup_error:
                print(f"[TASK {task_id}] Warning: Failed to cleanup temp file: {cleanup_error}")
        
        generation_progress[task_id]['status'] = 'error'
        generation_progress[task_id]['error'] = str(e)
        generation_progress[task_id]['message'] = f'Error: {str(e)}'


@app.route('/api/progress/<task_id>')
def api_progress(task_id):
    """Stream progress updates via Server-Sent Events"""
    def generate():
        import time
        
        # Wait for task to be registered (max 2 seconds)
        wait_time = 0
        while task_id not in generation_progress and wait_time < 2:
            time.sleep(0.1)
            wait_time += 0.1
        
        # Check if task exists after waiting
        if task_id not in generation_progress:
            print(f"[SSE] Task {task_id} not found after waiting")
            yield f"data: {json.dumps({'status': 'error', 'error': 'Task not found', 'progress': 0, 'message': 'Task not found'})}\n\n"
            return
        
        print(f"[SSE] Connected to task {task_id}")
        
        # Send keep-alive and check status
        max_wait = 120  # 2 minutes max
        start_time = time.time()
        
        while task_id in generation_progress:
            # Check timeout
            if time.time() - start_time > max_wait:
                yield f"data: {json.dumps({'status': 'error', 'error': 'Generation timeout', 'progress': 0, 'message': 'Timeout'})}\n\n"
                break
            
            task_data = generation_progress[task_id]
            
            # Create a copy without mp3_data (bytes not JSON serializable)
            sse_data = task_data.copy()
            if 'result' in sse_data and sse_data['result']:
                sse_data['result'] = sse_data['result'].copy()
                sse_data['result'].pop('mp3_data', None)  # Remove bytes from SSE
            
            yield f"data: {json.dumps(sse_data)}\n\n"
            
            if task_data['status'] in ['completed', 'error']:
                # Clean up after 30 seconds to allow client to retrieve result
                threading.Timer(30.0, lambda: generation_progress.pop(task_id, None)).start()
                break
            
            time.sleep(0.5)  # Update every 500ms
    
    try:
        return Response(stream_with_context(generate()), 
                       mimetype='text/event-stream',
                       headers={
                           'Cache-Control': 'no-cache',
                           'X-Accel-Buffering': 'no',
                           'Connection': 'keep-alive'
                       })
    except Exception as e:
        print(f"SSE error: {str(e)}")
        return jsonify({'status': 'error', 'error': str(e)}), 500


@app.route('/api/download/<task_id>')
def api_download(task_id):
    """Download generated signal file from memory"""
    # Check if task exists and has completed
    if task_id not in generation_progress:
        return jsonify({'status': 'error', 'message': 'Task not found'}), 404
    
    task = generation_progress[task_id]
    if task['status'] != 'completed':
        return jsonify({'status': 'error', 'message': 'Generation not complete'}), 400
    
    if not task.get('result') or 'mp3_data' not in task['result']:
        return jsonify({'status': 'error', 'message': 'File data not available'}), 404
    
    # Create BytesIO from stored data
    mp3_buffer = io.BytesIO(task['result']['mp3_data'])
    mp3_buffer.seek(0)
    
    filename = task['result'].get('filename', 'UAP_Signal.mp3')
    
    return send_file(
        mp3_buffer,
        mimetype='audio/mpeg',
        as_attachment=True,
        download_name=filename
    )


@app.route('/api/upload_music', methods=['POST'])
def api_upload_music():
    """Upload music file for signal modulation (stored in memory)"""
    if 'file' not in request.files:
        return jsonify({'status': 'error', 'message': 'No file provided'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'status': 'error', 'message': 'No file selected'}), 400
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        
        # Read file into memory
        file_data = file.read()
        
        # Check file size (already enforced by MAX_CONTENT_LENGTH, but double-check)
        file_size_mb = len(file_data) / (1024 * 1024)
        if file_size_mb > 10:
            return jsonify({
                'status': 'error', 
                'message': f'File too large ({file_size_mb:.1f}MB). Maximum size is 10MB.'
            }), 400
        
        # Store in memory
        uploaded_music_files[filename] = file_data
        
        # Get file info by loading from memory
        audio = AudioSegment.from_file(io.BytesIO(file_data))
        duration_ms = len(audio)
        
        return jsonify({
            'status': 'success',
            'filename': filename,
            'duration_ms': duration_ms,
            'duration_seconds': duration_ms / 1000,
            'size_mb': round(file_size_mb, 2)
        })
    
    return jsonify({'status': 'error', 'message': 'Invalid file type. Supported: MP3, WAV, OGG, FLAC, M4A'}), 400


@app.route('/api/upload_cookies', methods=['POST'])
def api_upload_cookies():
    """Upload YouTube cookies file for bypassing bot detection"""
    try:
        if 'cookies' not in request.files:
            return jsonify({'status': 'error', 'message': 'No cookies file provided'}), 400
        
        file = request.files['cookies']
        if file.filename == '':
            return jsonify({'status': 'error', 'message': 'No file selected'}), 400
        
        # Save the cookies file
        cookies_path = app.config['COOKIES_FILE']
        file.save(cookies_path)
        
        # Validate it's a proper cookies file (should contain youtube.com)
        try:
            with open(cookies_path, 'r', encoding='utf-8') as f:
                content = f.read()
                if 'youtube.com' not in content.lower():
                    os.remove(cookies_path)
                    return jsonify({
                        'status': 'error', 
                        'message': 'Invalid cookies file - must contain YouTube cookies'
                    }), 400
        except Exception as e:
            if os.path.exists(cookies_path):
                os.remove(cookies_path)
            return jsonify({'status': 'error', 'message': f'Invalid file format: {str(e)}'}), 400
        
        return jsonify({
            'status': 'success',
            'message': 'Cookies uploaded successfully. YouTube downloads will now use these cookies.'
        })
        
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500


@app.route('/api/check_cookies', methods=['GET'])
def api_check_cookies():
    """Check if cookies file exists"""
    cookies_path = app.config['COOKIES_FILE']
    return jsonify({
        'has_cookies': os.path.exists(cookies_path)
    })


@app.route('/api/download_youtube', methods=['POST'])
def api_download_youtube():
    """Download audio from YouTube URL"""
    try:
        data = request.json
        youtube_url = data.get('url', '').strip()
        
        if not youtube_url:
            return jsonify({'status': 'error', 'message': 'No URL provided'}), 400
        
        # Validate YouTube URL
        youtube_regex = r'(https?://)?(www\.)?(youtube|youtu|youtube-nocookie)\.(com|be)/'
        if not re.match(youtube_regex, youtube_url):
            return jsonify({'status': 'error', 'message': 'Invalid YouTube URL'}), 400
        
        # Generate unique filename
        video_id = extract_video_id(youtube_url)
        output_filename = f"youtube_{video_id}.mp3"
        output_path = os.path.join(app.config['UPLOAD_FOLDER'], output_filename)
        
        # Check if already downloaded
        if os.path.exists(output_path):
            audio = AudioSegment.from_file(output_path)
            return jsonify({
                'status': 'success',
                'filename': output_filename,
                'duration_ms': len(audio),
                'duration_seconds': len(audio) / 1000,
                'cached': True
            })
        
        # Download audio using yt-dlp
        import shutil
        import platform
        
        # Detect if running on Heroku
        is_heroku = os.environ.get('DYNO') is not None
        
        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'outtmpl': os.path.join(app.config['UPLOAD_FOLDER'], f'youtube_{video_id}.%(ext)s'),
            'quiet': False,  # Enable output for debugging
            'no_warnings': False,
            # Use web client when we have cookies
            'extractor_args': {
                'youtube': {
                    'player_client': ['web'],
                    'skip': ['hls', 'dash'],
                }
            },
        }
        
        # Check for uploaded cookie file first (works on both local and Heroku)
        cookies_path = app.config['COOKIES_FILE']
        
        # Check for cookies from Heroku environment variable
        heroku_cookies = os.environ.get('YOUTUBE_COOKIES')
        if heroku_cookies and is_heroku:
            # Write environment variable cookies to temp file with proper format
            with open(cookies_path, 'w', encoding='utf-8', newline='\n') as f:
                f.write(heroku_cookies)
            ydl_opts['cookiefile'] = cookies_path
            print(f"Using cookies from YOUTUBE_COOKIES environment variable")
        elif os.path.exists(cookies_path):
            ydl_opts['cookiefile'] = cookies_path
            print(f"Using cookie file: {cookies_path}")
        # Fallback to browser cookies if local and no cookie file
        elif not is_heroku:
            try:
                ydl_opts['cookiesfrombrowser'] = ('chrome',)
                print("Using Chrome browser cookies")
            except:
                print("No cookies available - may encounter bot detection")
                pass
        
        # Add ffmpeg location if not in PATH
        ffmpeg_path = shutil.which('ffmpeg')
        if not ffmpeg_path and os.path.exists('C:\\Users\\Duncan\\FFmpeg\\bin'):
            ydl_opts['ffmpeg_location'] = 'C:\\Users\\Duncan\\FFmpeg\\bin'
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(youtube_url, download=True)
            title = info.get('title', 'Unknown')
        
        # Get audio duration
        audio = AudioSegment.from_file(output_path)
        duration_ms = len(audio)
        
        return jsonify({
            'status': 'success',
            'filename': output_filename,
            'title': title,
            'duration_ms': duration_ms,
            'duration_seconds': duration_ms / 1000,
            'cached': False
        })
        
    except Exception as e:
        import traceback
        error_trace = traceback.format_exc()
        print(f"Error downloading YouTube audio: {error_trace}")
        return jsonify({
            'status': 'error',
            'message': f'Failed to download audio: {str(e)}'
        }), 500


def extract_video_id(url):
    """Extract video ID from YouTube URL"""
    patterns = [
        r'(?:v=|\/)([0-9A-Za-z_-]{11}).*',
        r'(?:embed\/)([0-9A-Za-z_-]{11})',
        r'(?:watch\?v=)([0-9A-Za-z_-]{11})'
    ]
    
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    
    return 'unknown'


@app.route('/api/list_music')
def api_list_music():
    """List available music files from memory"""
    files = []
    
    for filename, file_data in uploaded_music_files.items():
        try:
            audio = AudioSegment.from_file(io.BytesIO(file_data))
            files.append({
                'filename': filename,
                'duration_ms': len(audio),
                'duration_seconds': len(audio) / 1000,
                'size_mb': round(len(file_data) / (1024 * 1024), 2)
            })
        except Exception as e:
            print(f"Error reading music file {filename}: {e}")
            continue
    
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


def get_fft_data(audio_segment, bins=512):
    """Extract FFT data from AudioSegment for spectrum visualization"""
    from scipy.fft import rfft, rfftfreq
    
    audio_array = np.array(audio_segment.get_array_of_samples(), dtype=np.float32)
    sample_rate = audio_segment.frame_rate
    
    # Take a chunk from the middle for analysis
    chunk_size = min(8192, len(audio_array))
    start = len(audio_array) // 2 - chunk_size // 2
    chunk = audio_array[start:start + chunk_size]
    
    # Apply window function to reduce spectral leakage
    window = np.hanning(len(chunk))
    windowed = chunk * window
    
    # Compute FFT
    fft_vals = rfft(windowed)
    fft_freqs = rfftfreq(len(chunk), 1.0 / sample_rate)
    
    # Get magnitude
    magnitudes = np.abs(fft_vals)
    
    # Downsample to bins
    step = max(1, len(magnitudes) // bins)
    freq_bins = fft_freqs[::step][:bins]
    mag_bins = magnitudes[::step][:bins]
    
    # Normalize
    if mag_bins.max() > 0:
        mag_bins = mag_bins / mag_bins.max()
    
    return {
        'frequencies': freq_bins.tolist(),
        'magnitudes': mag_bins.tolist()
    }


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)
