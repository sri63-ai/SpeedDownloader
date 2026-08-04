let currentPlatform = 'facebook';
let currentServiceMode = 'video';

function switchServiceMode(mode) {
    currentServiceMode = mode;
    document.getElementById('btnModeVideo').classList.toggle('active', mode === 'video');
    document.getElementById('btnModePhoto').classList.toggle('active', mode === 'photo');
    updateLabels();
}

function switchTab(platform, btnElement) {
    currentPlatform = platform;
    document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
    if (btnElement) btnElement.classList.add('active');
    updateLabels();
}

function updateLabels() {
    const mainTitle = document.getElementById('mainTitle');
    const urlInput = document.getElementById('videoUrl');
    const actionBtn = document.getElementById('actionBtn');
    let displayPlatform = currentPlatform.charAt(0).toUpperCase() + currentPlatform.slice(1);

    if (currentServiceMode === 'video') {
        mainTitle.innerText = `⚡ ${displayPlatform} Video Downloader`;
        urlInput.placeholder = `Please paste your ${displayPlatform} video link here...`;
        actionBtn.innerText = "Get Video Link";
        actionBtn.style.background = "#6c5ce7";
    } else {
        mainTitle.innerText = `📸 ${displayPlatform} Photo Downloader`;
        urlInput.placeholder = `Please paste your ${displayPlatform} photo/post link here...`;
        actionBtn.innerText = "Get Photo Link";
        actionBtn.style.background = "#0984e3";
    }
}

async function startDownload() {
    const urlInput = document.getElementById('videoUrl').value.trim();
    const statusDiv = document.getElementById('status');
    const spinner = document.getElementById('loadingSpinner');
    
    if (!urlInput) {
        statusDiv.innerHTML = "<p style='color: #ff7675;'>URL cannot be empty!</p>";
        return;
    }

    // Loading message and spinner activation
    statusDiv.innerHTML = "<div style='color: #a29bfe; font-weight: bold; margin: 15px 0;'>⏳ Downloading / Processing, Please wait...</div>";
    if (spinner) spinner.style.display = "block";

    try {
        const formData = new FormData();
        formData.append('url', urlInput);
        
        // Handles both naming styles safely
        const mode = typeof currentServiceMode !== 'undefined' ? currentServiceMode : (typeof selectedMode !== 'undefined' ? selectedMode : 'video');
        formData.append('type', mode);
        
        if (typeof currentPlatform !== 'undefined') {
            formData.append('platform', currentPlatform);
        }

        const response = await fetch('/get_download_link', {
            method: 'POST',
            body: formData
        });

        const textResponse = await response.text();
        if (spinner) spinner.style.display = "none";

        let data;
        try {
            data = JSON.parse(textResponse);
        } catch (err) {
            statusDiv.innerHTML = `<p style='color: #ff7675;'>Server Raw Response: ${textResponse}</p>`;
            return;
        }

        if (data.success && data.download_url) {
            const btnColor = mode === 'video' ? '#2ecc71' : '#0984e3';
            const btnLabel = mode === 'video' ? 'Click Here to Download Video' : 'Click Here to Download Photo';

            statusDiv.innerHTML = `
                <p style='color: #2ecc71; margin-bottom: 10px;'>Success: ${data.title || 'Media'}</p>
                <a href="${data.download_url}" target="_blank" rel="noopener noreferrer">
                    <button class="btn" style="background: ${btnColor}; width: 100%; padding: 12px; color: white; border: none; border-radius: 8px; cursor: pointer; font-weight: bold;">${btnLabel}</button>
                </a>`;
        } else {
            statusDiv.innerHTML = `<p style='color: #ff7675;'>Error: ${data.error || 'This link is not supported.'}</p>`;
        }
    } catch (error) {
            if (spinner) spinner.style.display = "none";
            statusDiv.innerHTML = `<p style='color: #ff7675; margin-top: 15px;'>❌ This link is not supported, Please try again other links.</p>`;
        }
}

function openModal() {
    const modal = document.getElementById('complaintModal');
    if (modal) modal.style.display = 'flex';
    const mainUrl = document.getElementById('videoUrl').value;
    const modalUrlInput = document.getElementById('modalVideoUrl');
    if (mainUrl && modalUrlInput) {
        modalUrlInput.value = mainUrl;
    }
}

function closeModal() {
    const modal = document.getElementById('complaintModal');
    if (modal) modal.style.display = 'none';
}

function switchServiceMode(mode) {
    currentServiceMode = mode;
    console.log("Mode switched to:", mode);
}