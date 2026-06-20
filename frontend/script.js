// API Base URL
const API_BASE_URL = 'http://localhost:5000/api';

// Tab Navigation
document.querySelectorAll('.nav-link').forEach(link => {
    link.addEventListener('click', (e) => {
        e.preventDefault();
        const tabName = link.getAttribute('data-tab');
        switchTab(tabName);
    });
});

function switchTab(tabName) {
    // Hide all tabs
    document.querySelectorAll('.tab-content').forEach(tab => {
        tab.classList.remove('active');
    });

    // Remove active class from all nav links
    document.querySelectorAll('.nav-link').forEach(link => {
        link.classList.remove('active');
    });

    // Show selected tab
    document.getElementById(tabName).classList.add('active');
    document.querySelector(`[data-tab="${tabName}"]`).classList.add('active');
}

// Video Options
document.querySelectorAll('.option-btn').forEach(btn => {
    btn.addEventListener('click', () => {
        const option = btn.getAttribute('data-option');
        document.querySelectorAll('.video-option').forEach(opt => {
            opt.style.display = 'none';
        });
        document.getElementById(option).style.display = 'block';
    });
});

// Loading Indicator
function showLoading() {
    document.getElementById('loadingIndicator').style.display = 'flex';
}

function hideLoading() {
    document.getElementById('loadingIndicator').style.display = 'none';
}

// API Calls
async function apiCall(endpoint, method = 'GET', data = null) {
    try {
        const options = {
            method: method,
            headers: {
                'Content-Type': 'application/json',
            }
        };

        if (data) {
            options.body = JSON.stringify(data);
        }

        const response = await fetch(`${API_BASE_URL}${endpoint}`, options);
        
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.error || 'API Error');
        }

        return await response.json();
    } catch (error) {
        console.error('API Error:', error);
        showError(error.message);
        throw error;
    }
}

// Notifications
function showError(message) {
    alert('Error: ' + message);
}

function showSuccess(message) {
    alert('Success: ' + message);
}

// ==================== SCRIPT GENERATION ====================

document.getElementById('generateScriptBtn').addEventListener('click', async () => {
    const topic = document.getElementById('topic').value;
    const duration = parseInt(document.getElementById('duration').value);
    const style = document.getElementById('style').value;
    const audience = document.getElementById('audience').value;

    if (!topic) {
        showError('Please enter a topic');
        return;
    }

    try {
        showLoading();
        const result = await apiCall('/generate-script', 'POST', {
            topic: topic,
            duration: duration,
            style: style,
            target_audience: audience
        });

        if (result.status === 'success') {
            document.getElementById('scriptContent').textContent = result.script;
            document.getElementById('scriptResult').style.display = 'block';
            showSuccess('Script generated successfully!');
        }
    } catch (error) {
        console.error('Error:', error);
    } finally {
        hideLoading();
    }
});

document.getElementById('copyScriptBtn').addEventListener('click', () => {
    const scriptContent = document.getElementById('scriptContent').textContent;
    navigator.clipboard.writeText(scriptContent).then(() => {
        showSuccess('Script copied to clipboard!');
    });
});

document.getElementById('generateCaptionsBtn').addEventListener('click', async () => {
    const script = document.getElementById('scriptContent').textContent;

    try {
        showLoading();
        const result = await apiCall('/generate-captions', 'POST', {
            script: script
        });

        if (result.status === 'success') {
            alert('Captions generated:\n\n' + result.captions.join('\n\n'));
        }
    } catch (error) {
        console.error('Error:', error);
    } finally {
        hideLoading();
    }
});

// ==================== VIDEO CREATION ====================

document.getElementById('composeBtn').addEventListener('click', async () => {
    const clipPathsString = document.getElementById('clipPaths').value;
    const clipPaths = clipPathsString.split(',').map(p => p.trim()).filter(p => p);
    const transition = document.getElementById('transition').value;

    if (clipPaths.length === 0) {
        showError('Please enter at least one clip path');
        return;
    }

    try {
        showLoading();
        const result = await apiCall('/compose-video', 'POST', {
            clip_paths: clipPaths,
            transition: transition
        });

        if (result.status === 'success') {
            document.getElementById('videoPath').textContent = 'Output: ' + result.output_path;
            document.getElementById('videoResult').style.display = 'block';
            showSuccess('Video composed successfully!');
        }
    } catch (error) {
        console.error('Error:', error);
    } finally {
        hideLoading();
    }
});

document.getElementById('textToVideoBtn').addEventListener('click', async () => {
    const text = document.getElementById('videoText').value;
    const duration = parseFloat(document.getElementById('videoDuration').value);
    const style = document.getElementById('videoStyle').value;

    if (!text) {
        showError('Please enter text');
        return;
    }

    try {
        showLoading();
        const result = await apiCall('/text-to-video', 'POST', {
            text: text,
            duration: duration,
            style: style
        });

        if (result.status === 'success') {
            document.getElementById('videoPath').textContent = 'Output: ' + result.output_path;
            document.getElementById('videoResult').style.display = 'block';
            showSuccess('Video created successfully!');
        }
    } catch (error) {
        console.error('Error:', error);
    } finally {
        hideLoading();
    }
});

// ==================== EFFECTS ====================

document.getElementById('applyEffectsBtn').addEventListener('click', async () => {
    const videoPath = document.getElementById('effectVideoPath').value;
    const effects = Array.from(document.querySelectorAll('input[name="effect"]:checked')).map(e => e.value);
    const musicPath = document.getElementById('musicPath').value;

    if (!videoPath) {
        showError('Please enter video path');
        return;
    }

    try {
        showLoading();
        let result;

        if (effects.length > 0) {
            result = await apiCall('/add-effects', 'POST', {
                video_path: videoPath,
                effects: effects
            });
        }

        if (musicPath) {
            result = await apiCall('/add-music', 'POST', {
                video_path: videoPath,
                music_path: musicPath,
                music_volume: parseFloat(document.getElementById('musicVolume').value)
            });
        }

        if (result && result.status === 'success') {
            document.getElementById('effectsPath').textContent = 'Output: ' + result.output_path;
            document.getElementById('effectsResult').style.display = 'block';
            showSuccess('Effects applied successfully!');
        }
    } catch (error) {
        console.error('Error:', error);
    } finally {
        hideLoading();
    }
});

// ==================== SUBTITLES ====================

document.getElementById('generateSubtitlesBtn').addEventListener('click', async () => {
    const videoPath = document.getElementById('subtitleVideoPath').value;
    const language = document.getElementById('subtitleLanguage').value;

    if (!videoPath) {
        showError('Please enter video path');
        return;
    }

    try {
        showLoading();
        const result = await apiCall('/generate-subtitles', 'POST', {
            video_path: videoPath,
            language: language
        });

        if (result.status === 'success') {
            const subtitleText = result.subtitles
                .map(s => `${s.start.toFixed(2)}s - ${s.end.toFixed(2)}s: ${s.text}`)
                .join('\n');
            document.getElementById('subtitlesContent').textContent = subtitleText;
            document.getElementById('subtitlesResult').style.display = 'block';
            showSuccess('Subtitles generated successfully!');
        }
    } catch (error) {
        console.error('Error:', error);
    } finally {
        hideLoading();
    }
});

// ==================== FACEBOOK ====================

document.getElementById('validateFacebookBtn').addEventListener('click', async () => {
    try {
        showLoading();
        const result = await apiCall('/validate-facebook', 'GET');
        const statusBox = document.getElementById('facebookStatus');

        if (result.status === 'success') {
            statusBox.innerHTML = `<div style="color: green;">✓ Credentials Valid</div>`;
            statusBox.classList.remove('error');
        } else {
            statusBox.innerHTML = `<div style="color: red;">✗ ${result.message}</div>`;
            statusBox.classList.add('error');
        }
        statusBox.style.display = 'block';
    } catch (error) {
        console.error('Error:', error);
    } finally {
        hideLoading();
    }
});

document.getElementById('uploadFacebookBtn').addEventListener('click', async () => {
    const videoPath = document.getElementById('fbVideoPath').value;
    const title = document.getElementById('fbTitle').value;
    const description = document.getElementById('fbDescription').value;

    if (!videoPath || !title) {
        showError('Please enter video path and title');
        return;
    }

    try {
        showLoading();
        const result = await apiCall('/post-facebook', 'POST', {
            video_path: videoPath,
            title: title,
            description: description
        });

        if (result.status === 'success') {
            document.getElementById('facebookMessage').textContent = result.message;
            document.getElementById('facebookLink').href = result.facebook_url;
            document.getElementById('facebookResult').style.display = 'block';
            showSuccess('Video uploaded successfully!');
        }
    } catch (error) {
        console.error('Error:', error);
    } finally {
        hideLoading();
    }
});
