from flask import Flask, render_template, request, jsonify
import yt_dlp
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/terms')
def terms():
    return render_template('terms.html')

@app.route('/get_download_link', methods=['POST'])
def get_download_link():
    video_url = request.form.get('url')
    req_type = request.form.get('type', 'video')

    if not video_url:
        return jsonify({"success": False, "error": "URL cannot be empty!"}), 400

    print(f"[*] Processing request for URL: {video_url} [Mode: {req_type}]")

    ydl_opts = {
        'format': 'best/bestvideo+bestaudio/best',
        'quiet': True,
        'no_warnings': True,
        'nocheckcertificate': True,
        'geo_bypass': True,
        # Helps bypass youtube bot detection even if cookies are missing
        'extractor_args': {
            'youtube': {
                'player_client': ['android', 'web']
            }
        }
    }

    # Automatically checks for cookies.txt in the project directory
    cookie_path = os.path.join(os.path.dirname(__file__), 'cookies.txt')
    if os.path.exists(cookie_path):
        ydl_opts['cookiefile'] = cookie_path

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            print("[*] Extracting media info via yt-dlp...")
            info = ydl.extract_info(video_url, download=False)
            title = info.get('title', 'Media')

            # 1. PHOTO download logic
            if req_type == 'photo':
                photo_url = info.get('thumbnail')
                if info.get('thumbnails') and isinstance(info['thumbnails'], list):
                    photo_url = info['thumbnails'][-1].get('url')
                
                if photo_url:
                    print("[*] Photo thumbnail link extracted successfully!")
                    return jsonify({"success": True, "download_url": photo_url, "title": title})
                return jsonify({"success": False, "error": "Photo link not found!"}), 400

            # 2. VIDEO download logic
            direct_url = None

            if 'url' in info and info['url']:
                direct_url = info['url']

            if not direct_url and 'formats' in info:
                for f in reversed(info['formats']):
                    if f.get('vcodec') != 'none' and f.get('acodec') != 'none' and f.get('url'):
                        direct_url = f.get('url')
                        break

            if not direct_url and 'formats' in info and len(info['formats']) > 0:
                direct_url = info['formats'][-1].get('url')

            if direct_url:
                print("[*] Video download link generated successfully!")
                return jsonify({"success": True, "download_url": direct_url, "title": title})
            else:
                return jsonify({"success": False, "error": "Could not extract video stream. Platform might be blocking requests!"}), 400

    except Exception as e:
        error_msg = str(e)
        print(f"[!] Error occurred: {error_msg}")
        if "Sign in to confirm" in error_msg or "bot" in error_msg.lower():
            error_msg = "Platform blocked this request. Please add 'cookies.txt' to bypass bot detection."
        return jsonify({"success": False, "error": error_msg}), 500

if __name__ == "__main__":
    app.run(debug=True, port=int(os.environ.get("PORT", 5000)))
