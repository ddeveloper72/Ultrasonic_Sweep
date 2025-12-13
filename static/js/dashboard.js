// UAP Signal Generator Dashboard JavaScript

let currentFilename = null;
let currentWaveform = null;
let loadingModal = null;
let audioPlayer = null;

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
        });

        audioPlayer.addEventListener('pause', function () {
            document.getElementById('playBtn').disabled = false;
            document.getElementById('pauseBtn').disabled = true;
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
    fetch('/api/list_music')
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
        .catch(error => console.error('Error loading music files:', error));
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

function handleGenerateSignal() {
    const config = {
        base_tone_freq: parseInt(document.getElementById('baseToneFreq').value),
        schumann_freq: parseFloat(document.getElementById('schumannFreq').value),
        dna_repair_freq: parseInt(document.getElementById('dnaRepairFreq').value),
        ambient_freq: parseInt(document.getElementById('ambientFreq').value),
        chirp_freq: parseInt(document.getElementById('chirpFreq').value),
        ultrasonic_freq: parseInt(document.getElementById('ultrasonicFreq').value),
        use_music_modulation: document.getElementById('useMusicSwitch').checked,
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

    loadingModal.show();

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
            loadingModal.hide();
            console.log('Generation response:', data);
            if (data.status === 'success') {
                currentFilename = data.filename;
                currentWaveform = data.waveform;

                displaySignalInfo(data);
                drawWaveform(data.waveform);
                showDownloadButton(data.filename);
            } else {
                alert('Error generating signal: ' + data.message);
            }
        })
        .catch(error => {
            loadingModal.hide();
            console.error('Error generating signal:', error);
            alert('Error generating signal: ' + error.message);
        });
}

function displaySignalInfo(data) {
    const infoDiv = document.getElementById('signalInfo');
    const metadata = data.metadata;

    let html = `
        <h6>Signal Generated Successfully</h6>
        <p><strong>Duration:</strong> ${(data.duration_ms / 1000).toFixed(2)} seconds</p>
        <p><strong>Layers:</strong></p>
        <ul>
            <li>Foundation: ${metadata.layers.foundation.join(', ')}</li>
            <li>Human Enhancement: ${metadata.layers.human_enhancement.join(', ')}</li>
            <li>Attention: ${metadata.layers.attention.join(', ')}</li>
            <li>Life Indicator: ${metadata.layers.life_indicator.join(', ')}</li>
        </ul>
        <p><strong>Modulation:</strong></p>
        <ul>
            <li>Music Modulation: ${metadata.modulation.music_modulation ? 'Enabled' : 'Disabled'}</li>
            <li>Tremolo: ${metadata.modulation.tremolo ? 'Enabled (' + metadata.modulation.tremolo_rate + ' Hz)' : 'Disabled'}</li>
        </ul>
    `;

    infoDiv.innerHTML = html;
}

function drawWaveform(waveformData) {
    const canvas = document.getElementById('oscilloscope');
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
