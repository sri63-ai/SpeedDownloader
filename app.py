import os
from flask import Flask, render_template, request, jsonify
import yt_dlp

app = Flask(__name__)

# Copy cookies.txt into the /tmp folder to prevent Read-Only file system errors on cloud servers
cookie_source = 'cookies.txt'
cookie_dest = '/tmp/cookies.txt'

if os.path.exists(cookie_source):
    try:
        with open(cookie_source, 'r', encoding='utf-8') as f:
            cookie_data = f.read()
        with open(cookie_dest, 'w', encoding='utf-8') as f:
            f.write(cookie_data)
    except Exception as e:
        print("Cookie copy warning:", e)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/founder')
def founder():
    return render_template('founder.html')

@app.route('/terms')
def terms():
    return render_template('terms.html')

@app.route('/get_download_link', methods=['POST'])
def get_download_link():
    video_url = request.form.get('url')
    req_type = request.form.get('type', 'video')
    
    if not video_url:
        return jsonify({'success': False, 'error': 'URL cannot be empty!'}), 400

    # Automatically get the user's Desktop path
    desktop_path = os.path.join(os.path.expanduser("~"), "Desktop", "Downloaded_Videos")

    # Create the folder if it does not exist
    os.makedirs(desktop_path, exist_ok=True)

    # yt-dlp options
    ydl_opts = {
        'format': 'best',
        'verbose': True,  # ఇది యాడ్ చేయండి, అప్పుడు టెర్మినల్‌లో పూర్తి వివరాలు వస్తాయి
        'quiet': False,   # False చేస్తే ఎర్రర్స్ కనిపిస్తాయి
        'no_warnings': False,
    }

    # Use cookies file from /tmp if available
    if os.path.exists(cookie_dest):
        ydl_opts['cookiefile'] = cookie_dest

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            print("[*] Extracting media info and downloading to Desktop...")
            # download=True is required to save the file to the specified path
            info = ydl.extract_info(video_url, download=True)
            title = info.get('title', 'Media File')

            # 1. PHOTO download logic
            if req_type == 'photo':
                photo_url = info.get('thumbnail')
                if info.get('thumbnails') and isinstance(info['thumbnails'], list):
                    photo_url = info['thumbnails'][-1].get('url')
                
                if photo_url:
                    return jsonify({"success": True, "download_url": photo_url, "title": title})
                return jsonify({"success": False, "error": "Photo link not found!"}), 400

            # 2. VIDEO download success response
            return jsonify({
                "success": True, 
                "download_url": "#", 
                "title": title,
                "message": "Video downloaded successfully to your Desktop/Downloaded_Videos folder!"
            })

    except Exception as e:
        error_msg = str(e)
        print(f"[!] Error occurred: {error_msg}")
        return jsonify({"success": False, "error": "❌ This link is not supported, Please try again other links."}), 500

if __name__ == "__main__":
    app.run(debug=True, port=int(os.environ.get("PORT", 5000)))
