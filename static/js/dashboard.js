// UAP Signal Generator Dashboard JavaScript

let currentFilename = null;
let currentWaveform = null;
let loadingModal = null;
let progressInterval = null;
let audioPlayer = null;

// Web Audio API variables
let audioContext = null;
let analyserNode = null;
let sourceNode = null;
let animationId = null;

document.addEventListener('DOMContentLoaded', function () {
    loadingModal = new bootstrap.Modal(document.getElementById('loadingModal'));
    audioPlayer = document.getElementById('audioPlayer');

    initializeEventListeners();
    loadMusicFiles();
});

function initializeEventListeners() {
    // Preset selector
    document.getElementById('presetSelector').addEventListener('change', handlePresetChange);

    // Music switch
    document.getElementById('useMusicSwitch').addEventListener('change', handleMusicSwitchChange);

    // Upload music button
    document.getElementById('uploadMusicBtn').addEventListener('click', handleMusicUpload);
    
    // Download YouTube button
    document.getElementById('downloadYoutubeBtn').addEventListener('click', handleYoutubeDownload);

    // Tremolo depth slider
    document.getElementById('tremoloDepth').addEventListener('input', function (e) {
        document.getElementById('tremoloDepthValue').textContent = e.target.value;
    });

    // Tremolo switch
    document.getElementById('tremoloSwitch').addEventListener('change', function (e) {
        document.getElementById('tremoloSettings').style.display = e.target.checked ? 'block' : 'none';
    });

    // Generate button
    document.getElementById('generateBtn').addEventListener('click', handleGenerateSignal);

    // Playback controls
    document.getElementById('playBtn').addEventListener('click', handlePlay);
    document.getElementById('pauseBtn').addEventListener('click', handlePause);
    document.getElementById('stopBtn').addEventListener('click', handleStop);

    // Download button
    document.getElementById('downloadBtn').addEventListener('click', handleDownload);

    // Audio player events
    if (audioPlayer) {
        audioPlayer.addEventListener('play', function () {
            document.getElementById('playBtn').disabled = true;
            document.getElementById('pauseBtn').disabled = false;
            document.getElementById('stopBtn').disabled = false;
            startRealtimeVisualization();
        });

        audioPlayer.addEventListener('pause', function () {
            document.getElementById('playBtn').disabled = false;
            document.getElementById('pauseBtn').disabled = true;
            stopRealtimeVisualization();
        });

        audioPlayer.addEventListener('ended', function () {
            handleStop();
        });
    }
}

function handlePresetChange(e) {
    const presetName = e.target.value;
    if (!presetName) {
        document.getElementById('presetDescription').classList.add('d-none');
        return;
    }

    fetch(`/api/preset/${presetName}`)
        .then(response => response.json())
        .then(preset => {
            // Update description
            const descDiv = document.getElementById('presetDescription');
            descDiv.innerHTML = `<strong>${preset.name}</strong><br>${preset.description}`;
            descDiv.classList.remove('d-none');

            // Update configuration
            const config = preset.config;
            document.getElementById('baseToneFreq').value = config.base_tone_freq;
            document.getElementById('schumannFreq').value = config.schumann_freq;
            document.getElementById('dnaRepairFreq').value = config.dna_repair_freq;
            document.getElementById('ambientFreq').value = config.ambient_freq;
            document.getElementById('chirpFreq').value = config.chirp_freq;
            document.getElementById('ultrasonicFreq').value = config.ultrasonic_freq;

            document.getElementById('useMusicSwitch').checked = config.use_music_modulation;
            handleMusicSwitchChange({ target: document.getElementById('useMusicSwitch') });

            document.getElementById('tremoloSwitch').checked = config.use_tremolo;
            document.getElementById('tremoloDepth').value = config.tremolo_depth * 100;
            document.getElementById('tremoloDepthValue').textContent = Math.round(config.tremolo_depth * 100);
        })
        .catch(error => console.error('Error loading preset:', error));
}

function handleMusicSwitchChange(e) {
    const musicSection = document.getElementById('musicSection');
    musicSection.classList.toggle('d-none', !e.target.checked);
}

function loadMusicFiles() {
    return fetch('/api/list_music')
        .then(response => response.json())
        .then(data => {
            const selector = document.getElementById('musicFileSelector');
            selector.innerHTML = '';

            if (data.files && data.files.length > 0) {
                data.files.forEach(file => {
                    const option = document.createElement('option');
                    option.value = file.filename;
                    option.textContent = `${file.filename} (${Math.round(file.duration_seconds)}s)`;
                    selector.appendChild(option);
                });
            } else {
                selector.innerHTML = '<option value="">No music files available</option>';
            }
        })
        .catch(error => {
            console.error('Error loading music files:', error);
            throw error;
        });
}

function handleMusicUpload() {
    const fileInput = document.getElementById('musicUpload');
    const file = fileInput.files[0];

    if (!file) {
        alert('Please select a file to upload');
        return;
    }

    const formData = new FormData();
    formData.append('file', file);

    loadingModal.show();

    fetch('/api/upload_music', {
        method: 'POST',
        body: formData
    })
        .then(response => response.json())
        .then(data => {
            loadingModal.hide();
            if (data.status === 'success') {
                alert(`Music file uploaded successfully!\nDuration: ${Math.round(data.duration_seconds)} seconds`);
                loadMusicFiles();
                fileInput.value = '';
            } else {
                alert('Error uploading file: ' + data.message);
            }
        })
        .catch(error => {
            loadingModal.hide();
            console.error('Error uploading music:', error);
            alert('Error uploading file');
        });
}

function handleYoutubeDownload() {
    const urlInput = document.getElementById('youtubeUrl');
    const url = urlInput.value.trim();

    if (!url) {
        alert('Please enter a YouTube URL');
        return;
    }

    if (!url.includes('youtube.com') && !url.includes('youtu.be')) {
        alert('Please enter a valid YouTube URL');
        return;
    }

    loadingModal.show();
    document.getElementById('progressText').textContent = 'Downloading audio from YouTube...';

    fetch('/api/download_youtube', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ url: url })
    })
        .then(response => response.json())
        .then(data => {
            loadingModal.hide();
            if (data.status === 'success') {
                const cacheMsg = data.cached ? ' (from cache)' : '';
                const title = data.title ? `"${data.title}"` : 'Audio';
                alert(`${title} downloaded successfully!${cacheMsg}\nDuration: ${Math.round(data.duration_seconds)} seconds`);
                
                // Reload music files and auto-select the new one
                loadMusicFiles().then(() => {
                    const selector = document.getElementById('musicFileSelector');
                    selector.value = data.filename;
                    
                    // Enable music switch if not already enabled
                    const musicSwitch = document.getElementById('useMusicSwitch');
                    if (!musicSwitch.checked) {
                        musicSwitch.checked = true;
                        handleMusicSwitchChange({ target: musicSwitch });
                    }
                });
                
                urlInput.value = '';
            } else {
                alert('Error downloading YouTube audio: ' + data.message);
            }
        })
        .catch(error => {
            loadingModal.hide();
            console.error('Error downloading YouTube audio:', error);
            alert('Error downloading YouTube audio: ' + error.message);
        });
}

function handleGenerateSignal() {
    const config = {
        base_tone_freq: parseInt(document.getElementById('baseToneFreq').value),
        schumann_freq: parseFloat(document.getElementById('schumannFreq').value),
        dna_repair_freq: parseInt(document.getElementById('dnaRepairFreq').value),
        ambient_freq: parseInt(document.getElementById('ambientFreq').value),
        chirp_freq: parseInt(document.getElementById('chirpFreq').value),
        ultrasonic_freq: parseInt(document.getElementById('ultrasonicFreq').value),
        use_music_modulation: document.getElementById('useMusicSwitch').checked,
        use_music_as_foundation: document.getElementById('musicFoundationSwitch').checked,
        use_tremolo: document.getElementById('tremoloSwitch').checked,
        tremolo_depth: parseFloat(document.getElementById('tremoloDepth').value) / 100
    };

    const useMusic = document.getElementById('useMusicSwitch').checked;
    const musicFile = useMusic ? document.getElementById('musicFileSelector').value : null;
    const presetName = document.getElementById('presetSelector').value || 'custom';

    const requestData = {
        config: config,
        use_music: useMusic,
        music_file: musicFile,
        preset_name: presetName,
        duration: 10000
    };

    const hasMusic = useMusic && musicFile;
    showProgressModal(hasMusic);

    fetch('/api/generate', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(requestData)
    })
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            if (data.status === 'started') {
                // Start listening to progress updates
                listenToProgress(data.task_id);
            } else if (data.status === 'error') {
                hideProgressModal();
                alert('Error starting generation: ' + data.message);
            }
        })
        .catch(error => {
            hideProgressModal();
            console.error('Error starting generation:', error);
            alert('Error starting generation: ' + error.message);
        });
}

function listenToProgress(taskId) {
    const eventSource = new EventSource(`/api/progress/${taskId}`);
    
    eventSource.onmessage = function(event) {
        const data = JSON.parse(event.data);
        updateProgressDisplay(data.progress, data.message);
        
        if (data.status === 'completed' && data.result) {
            eventSource.close();
            hideProgressModal();
            
            // Display the results
            currentFilename = data.result.filename;
            currentWaveform = data.result.waveform;
            displaySignalInfo(data.result);
            drawWaveform(data.result.waveform);
            drawSpectrum(data.result.fft);
            drawSpectrogram(data.result.waveform, data.result.duration_ms);
            showDownloadButton(data.result.filename);
            
        } else if (data.status === 'error') {
            eventSource.close();
            hideProgressModal();
            alert('Error generating signal: ' + data.error);
        }
    };
    
    eventSource.onerror = function(error) {
        console.error('SSE error:', error);
        eventSource.close();
        hideProgressModal();
        alert('Connection error during signal generation');
    };
}

function updateProgressDisplay(progress, message) {
    const progressBar = document.getElementById('progressBar');
    const progressSpinner = document.getElementById('progressSpinner');
    const progressText = document.getElementById('progressText');
    
    const opacity = 0.2 + (progress / 100) * 0.8;  // 20% to 100% opacity
    
    progressBar.style.width = progress + '%';
    progressBar.textContent = Math.round(progress) + '%';
    progressBar.setAttribute('aria-valuenow', progress);
    progressSpinner.style.opacity = opacity;
    progressText.textContent = message;
}

function showProgressModal(withMusic = false) {
    const progressBar = document.getElementById('progressBar');
    const progressSpinner = document.getElementById('progressSpinner');
    const progressText = document.getElementById('progressText');
    
    // Reset progress
    progressBar.style.width = '0%';
    progressBar.textContent = '0%';
    progressBar.setAttribute('aria-valuenow', '0');
    progressSpinner.style.opacity = '0.2';
    progressText.textContent = 'Initializing...';
    
    loadingModal.show();
    
    // Clear any existing simulated interval
    if (progressInterval) {
        clearInterval(progressInterval);
        progressInterval = null;
    }
}

function hideProgressModal() {
    if (progressInterval) {
        clearInterval(progressInterval);
        progressInterval = null;
    }
    
    // Complete the progress bar
    const progressBar = document.getElementById('progressBar');
    const progressSpinner = document.getElementById('progressSpinner');
    progressBar.style.width = '100%';
    progressBar.textContent = '100%';
    progressBar.setAttribute('aria-valuenow', '100');
    progressSpinner.style.opacity = '1';
    
    // Hide after a brief moment to show completion
    setTimeout(() => {
        loadingModal.hide();
    }, 300);
}

function displaySignalInfo(data) {
    const infoDiv = document.getElementById('signalInfo');
    const metadata = data.metadata;

    // Format layer names for display
    const foundationDesc = metadata.modulation.music_as_foundation
        ? 'Music (primary carrier with subtle Schumann resonance overlay)'
        : 'Base tone (100 Hz) + Schumann resonance (7.83 Hz)';

    const humanEnhancementDesc = metadata.modulation.music_modulation
        ? 'Music-modulated DNA repair (528 Hz) + Ambient pad (432 Hz)'
        : 'DNA repair (528 Hz) + Ambient pad (432 Hz)';

    let html = `
        <h6>Signal Generated Successfully</h6>
        <p><strong>Duration:</strong> ${(data.duration_ms / 1000).toFixed(2)} seconds</p>
        <p><strong>Layers:</strong></p>
        <ul>
            <li><strong>Foundation Layer:</strong> ${foundationDesc}</li>
            <li><strong>Human Enhancement:</strong> ${humanEnhancementDesc}</li>
            <li><strong>Attention Layer:</strong> Chirps (2500 Hz) + Ultrasonic pings (17 kHz)</li>
            <li><strong>Life Indicator:</strong> Filtered breath layer with tremolo</li>
        </ul>
        <p><strong>Modulation:</strong></p>
        <ul>
            <li>Music Modulation: ${metadata.modulation.music_modulation ? 'Enabled' : 'Disabled'}</li>
            <li>Music as Foundation: ${metadata.modulation.music_as_foundation ? 'Enabled' : 'Disabled'}</li>
            <li>Tremolo: ${metadata.modulation.tremolo ? 'Enabled (' + metadata.modulation.tremolo_rate + ' Hz)' : 'Disabled'}</li>
        </ul>
    `;

    infoDiv.innerHTML = html;
}

function drawWaveform(waveformData) {
    const canvas = document.getElementById('waveformCanvas');
    const ctx = canvas.getContext('2d');

    // Clear canvas
    ctx.fillStyle = '#000';
    ctx.fillRect(0, 0, canvas.width, canvas.height);

    // Draw grid
    ctx.strokeStyle = '#333';
    ctx.lineWidth = 1;

    // Horizontal lines
    for (let i = 0; i <= 4; i++) {
        const y = (canvas.height / 4) * i;
        ctx.beginPath();
        ctx.moveTo(0, y);
        ctx.lineTo(canvas.width, y);
        ctx.stroke();
    }

    // Vertical lines
    for (let i = 0; i <= 8; i++) {
        const x = (canvas.width / 8) * i;
        ctx.beginPath();
        ctx.moveTo(x, 0);
        ctx.lineTo(x, canvas.height);
        ctx.stroke();
    }

    // Draw waveform
    ctx.strokeStyle = '#0f0';
    ctx.lineWidth = 2;
    ctx.beginPath();

    const midY = canvas.height / 2;
    const xStep = canvas.width / waveformData.length;

    for (let i = 0; i < waveformData.length; i++) {
        const x = i * xStep;
        const y = midY - (waveformData[i] * midY * 0.9);

        if (i === 0) {
            ctx.moveTo(x, y);
        } else {
            ctx.lineTo(x, y);
        }
    }

    ctx.stroke();
}

function drawSpectrum(fftData) {
    const canvas = document.getElementById('spectrumCanvas');
    const ctx = canvas.getContext('2d');

    // Clear canvas
    ctx.fillStyle = '#000';
    ctx.fillRect(0, 0, canvas.width, canvas.height);

    const frequencies = fftData.frequencies;
    const magnitudes = fftData.magnitudes;

    // Draw frequency grid lines
    ctx.strokeStyle = '#333';
    ctx.lineWidth = 1;

    // Horizontal lines
    for (let i = 0; i <= 4; i++) {
        const y = (canvas.height / 4) * i;
        ctx.beginPath();
        ctx.moveTo(0, y);
        ctx.lineTo(canvas.width, y);
        ctx.stroke();
    }

    // Draw spectrum bars
    const barWidth = canvas.width / magnitudes.length;
    
    for (let i = 0; i < magnitudes.length; i++) {
        const barHeight = magnitudes[i] * canvas.height * 0.9;
        const x = i * barWidth;
        const y = canvas.height - barHeight;

        // Color gradient based on frequency
        const hue = (i / magnitudes.length) * 240; // Blue to red
        ctx.fillStyle = `hsl(${hue}, 100%, 50%)`;
        ctx.fillRect(x, y, barWidth - 1, barHeight);
    }

    // Draw frequency labels
    ctx.fillStyle = '#0f0';
    ctx.font = '12px monospace';
    const labelFreqs = [100, 500, 1000, 5000, 10000, 15000];
    labelFreqs.forEach(freq => {
        const index = frequencies.findIndex(f => f >= freq);
        if (index > 0) {
            const x = (index / magnitudes.length) * canvas.width;
            ctx.fillText(`${freq}Hz`, x, canvas.height - 5);
        }
    });
}

function drawSpectrogram(waveformData, durationMs) {
    const canvas = document.getElementById('spectrogramCanvas');
    const ctx = canvas.getContext('2d');

    // Clear canvas
    ctx.fillStyle = '#000';
    ctx.fillRect(0, 0, canvas.width, canvas.height);

    // Simple spectrogram: divide signal into time slices and show frequency content
    const numSlices = 100;
    const sliceSize = Math.floor(waveformData.length / numSlices);
    const freqBins = 64;

    for (let slice = 0; slice < numSlices; slice++) {
        const start = slice * sliceSize;
        const end = Math.min(start + sliceSize, waveformData.length);
        const sliceData = waveformData.slice(start, end);

        // Simple FFT approximation (rolling average for frequency bands)
        for (let bin = 0; bin < freqBins; bin++) {
            let energy = 0;
            const binSize = Math.floor(sliceData.length / freqBins);
            const binStart = bin * binSize;
            
            for (let i = 0; i < binSize && binStart + i < sliceData.length; i++) {
                energy += Math.abs(sliceData[binStart + i]);
            }
            energy = energy / binSize;

            // Draw pixel
            const x = (slice / numSlices) * canvas.width;
            const y = canvas.height - ((bin / freqBins) * canvas.height);
            const intensity = Math.min(255, energy * 500);
            
            // Color map: blue (low) to yellow (medium) to red (high)
            let r, g, b;
            if (intensity < 128) {
                r = 0;
                g = 0;
                b = intensity * 2;
            } else {
                r = (intensity - 128) * 2;
                g = (intensity - 128) * 2;
                b = 255 - ((intensity - 128) * 2);
            }
            
            ctx.fillStyle = `rgb(${r}, ${g}, ${b})`;
            ctx.fillRect(x, y, canvas.width / numSlices + 1, canvas.height / freqBins + 1);
        }
    }

    // Add labels
    ctx.fillStyle = '#0f0';
    ctx.font = '12px monospace';
    ctx.fillText('Frequency →', 10, 20);
    ctx.save();
    ctx.rotate(-Math.PI / 2);
    ctx.fillText('Time →', -canvas.height + 10, 20);
    ctx.restore();
}


function handlePlay() {
    if (audioPlayer) {
        // Only set src if it's not already loaded
        if (!audioPlayer.src || !audioPlayer.src.includes(currentFilename)) {
            audioPlayer.src = `/api/download/${currentFilename}`;
        }
        audioPlayer.play();
    }
}

function handlePause() {
    if (audioPlayer) {
        audioPlayer.pause();
    }
}

function handleStop() {
    if (audioPlayer) {
        audioPlayer.pause();
        audioPlayer.currentTime = 0;
        // Reset button states
        document.getElementById('playBtn').disabled = false;
        document.getElementById('pauseBtn').disabled = true;
        document.getElementById('stopBtn').disabled = true;
        // Stop visualization and clear spectrogram
        stopRealtimeVisualization();
        spectrogramData = [];
    }
}

function showDownloadButton(filename) {
    document.getElementById('noSignal').classList.add('d-none');
    document.getElementById('downloadSection').classList.remove('d-none');
    document.getElementById('downloadFilename').textContent = `File: ${filename}`;

    // Enable playback controls and load audio
    if (audioPlayer) {
        audioPlayer.src = `/api/download/${filename}`;
        document.getElementById('playBtn').disabled = false;
        document.getElementById('pauseBtn').disabled = true;
        document.getElementById('stopBtn').disabled = true;
    }
}

function handleDownload() {
    if (currentFilename) {
        window.location.href = `/api/download/${currentFilename}`;
    }
}

// ========== Real-time Visualization with Web Audio API ==========

function startRealtimeVisualization() {
    // Initialize Web Audio API if not already done
    if (!audioContext) {
        audioContext = new (window.AudioContext || window.webkitAudioContext)();
        analyserNode = audioContext.createAnalyser();
        analyserNode.fftSize = 2048;
        
        // Connect audio element to analyser
        if (!sourceNode) {
            sourceNode = audioContext.createMediaElementSource(audioPlayer);
            sourceNode.connect(analyserNode);
            analyserNode.connect(audioContext.destination);
        }
    }
    
    // Resume audio context if suspended
    if (audioContext.state === 'suspended') {
        audioContext.resume();
    }
    
    // Start animation loop
    animateVisualizations();
}

function stopRealtimeVisualization() {
    if (animationId) {
        cancelAnimationFrame(animationId);
        animationId = null;
    }
}

function animateVisualizations() {
    animationId = requestAnimationFrame(animateVisualizations);
    
    // Get current active tab
    const activeTab = document.querySelector('#visualizationTabs .nav-link.active');
    const activeTabId = activeTab ? activeTab.id : 'waveform-tab';
    
    // Update only the active visualization for performance
    if (activeTabId === 'waveform-tab') {
        drawRealtimeWaveform();
    } else if (activeTabId === 'spectrum-tab') {
        drawRealtimeSpectrum();
    } else if (activeTabId === 'spectrogram-tab') {
        drawRealtimeSpectrogram();
    }
}

function drawRealtimeWaveform() {
    const canvas = document.getElementById('waveformCanvas');
    const ctx = canvas.getContext('2d');
    
    const bufferLength = analyserNode.fftSize;
    const dataArray = new Uint8Array(bufferLength);
    analyserNode.getByteTimeDomainData(dataArray);
    
    // Clear canvas
    ctx.fillStyle = '#000';
    ctx.fillRect(0, 0, canvas.width, canvas.height);
    
    // Draw grid
    ctx.strokeStyle = '#333';
    ctx.lineWidth = 1;
    for (let i = 0; i <= 4; i++) {
        const y = (canvas.height / 4) * i;
        ctx.beginPath();
        ctx.moveTo(0, y);
        ctx.lineTo(canvas.width, y);
        ctx.stroke();
    }
    for (let i = 0; i <= 8; i++) {
        const x = (canvas.width / 8) * i;
        ctx.beginPath();
        ctx.moveTo(x, 0);
        ctx.lineTo(x, canvas.height);
        ctx.stroke();
    }
    
    // Draw waveform
    ctx.strokeStyle = '#0f0';
    ctx.lineWidth = 2;
    ctx.beginPath();
    
    const sliceWidth = canvas.width / bufferLength;
    let x = 0;
    
    for (let i = 0; i < bufferLength; i++) {
        const v = dataArray[i] / 128.0;
        const y = v * canvas.height / 2;
        
        if (i === 0) {
            ctx.moveTo(x, y);
        } else {
            ctx.lineTo(x, y);
        }
        
        x += sliceWidth;
    }
    
    ctx.stroke();
}

function drawRealtimeSpectrum() {
    const canvas = document.getElementById('spectrumCanvas');
    const ctx = canvas.getContext('2d');
    
    const bufferLength = analyserNode.frequencyBinCount;
    const dataArray = new Uint8Array(bufferLength);
    analyserNode.getByteFrequencyData(dataArray);
    
    // Clear canvas
    ctx.fillStyle = '#000';
    ctx.fillRect(0, 0, canvas.width, canvas.height);
    
    // Draw grid
    ctx.strokeStyle = '#333';
    ctx.lineWidth = 1;
    for (let i = 0; i <= 4; i++) {
        const y = (canvas.height / 4) * i;
        ctx.beginPath();
        ctx.moveTo(0, y);
        ctx.lineTo(canvas.width, y);
        ctx.stroke();
    }
    
    // Draw spectrum bars
    const barWidth = canvas.width / bufferLength;
    
    for (let i = 0; i < bufferLength; i++) {
        const barHeight = (dataArray[i] / 255) * canvas.height * 0.9;
        const x = i * barWidth;
        const y = canvas.height - barHeight;
        
        // Color gradient based on frequency
        const hue = (i / bufferLength) * 240;
        ctx.fillStyle = `hsl(${hue}, 100%, 50%)`;
        ctx.fillRect(x, y, barWidth - 1, barHeight);
    }
    
    // Draw frequency labels in waterfall/stepped pattern
    ctx.fillStyle = '#0f0';
    ctx.font = '12px monospace';
    const sampleRate = audioContext.sampleRate;
    const labelFreqs = [100, 500, 1000, 5000, 10000, 15000];
    labelFreqs.forEach((freq, idx) => {
        if (freq < sampleRate / 2) {
            const index = Math.floor((freq / (sampleRate / 2)) * bufferLength);
            const x = (index / bufferLength) * canvas.width;
            // Stagger labels vertically in steps
            const yOffset = (idx % 3) * 15; // 3-level waterfall
            ctx.fillText(`${freq >= 1000 ? freq/1000 + 'kHz' : freq + 'Hz'}`, x, canvas.height - 5 - yOffset);
        }
    });
}

let spectrogramData = [];
const spectrogramMaxSlices = 100;

function drawRealtimeSpectrogram() {
    const canvas = document.getElementById('spectrogramCanvas');
    const ctx = canvas.getContext('2d');
    
    const bufferLength = analyserNode.frequencyBinCount;
    const dataArray = new Uint8Array(bufferLength);
    analyserNode.getByteFrequencyData(dataArray);
    
    // Add new frequency data slice
    const slice = Array.from(dataArray);
    spectrogramData.push(slice);
    
    // Keep only recent slices
    if (spectrogramData.length > spectrogramMaxSlices) {
        spectrogramData.shift();
    }
    
    // Clear canvas
    ctx.fillStyle = '#000';
    ctx.fillRect(0, 0, canvas.width, canvas.height);
    
    // Draw spectrogram
    const sliceWidth = canvas.width / spectrogramData.length;
    const binHeight = canvas.height / bufferLength;
    
    for (let i = 0; i < spectrogramData.length; i++) {
        for (let j = 0; j < bufferLength; j++) {
            const value = spectrogramData[i][j];
            const intensity = value / 255;
            
            // Color map: blue (low) to yellow (medium) to red (high)
            let r, g, b;
            if (intensity < 0.5) {
                r = 0;
                g = 0;
                b = intensity * 2 * 255;
            } else {
                r = (intensity - 0.5) * 2 * 255;
                g = (intensity - 0.5) * 2 * 255;
                b = 255 - ((intensity - 0.5) * 2 * 255);
            }
            
            ctx.fillStyle = `rgb(${r}, ${g}, ${b})`;
            const x = i * sliceWidth;
            const y = canvas.height - (j * binHeight);
            ctx.fillRect(x, y, sliceWidth + 1, binHeight + 1);
        }
    }
    
    // Add labels
    ctx.fillStyle = '#0f0';
    ctx.font = '12px monospace';
    ctx.fillText('Time →', canvas.width - 60, canvas.height - 15);
    ctx.save();
    ctx.rotate(-Math.PI / 2);
    ctx.fillText('Frequency →', -canvas.height + 10, 15);
    ctx.restore();
}

