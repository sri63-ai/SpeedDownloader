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
    if not video_url:
        return jsonify({"error": "URL cannot be empty!"}), 400

    # Combined single format selection to ensure audio + video are pre-merged
    ydl_opts = {
        'format': 'best[ext=mp4]/best',
        'quiet': True,
        'no_warnings': True,
        'cookiefile': 'cookies.txt',
        'nocheckcertificate': True,
        'geo_bypass': True,
        'extract_flat': False,
        'skip_download': True,
        'http_headers': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9',
            'Sec-Fetch-Mode': 'navigate'
        }
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=False)
            
            direct_url = None
            
            # Scan formats to guarantee both video and audio codecs exist
            if 'formats' in info:
                for f in reversed(info['formats']):
                    if f.get('vcodec') != 'none' and f.get('acodec') != 'none' and f.get('ext') == 'mp4':
                        direct_url = f.get('url')
                        break
                
                # Fallback to any extension with combined audio and video tracks
                if not direct_url:
                    for f in reversed(info['formats']):
                        if f.get('vcodec') != 'none' and f.get('acodec') != 'none':
                            direct_url = f.get('url')
                            break

            # Secondary fallback to main info URL
            if not direct_url:
                direct_url = info.get('url')

            # Final fallback to last available stream format
            if not direct_url and 'formats' in info:
                direct_url = info['formats'][-1].get('url')

            title = info.get('title', 'video')
            
        return jsonify({"success": True, "download_url": direct_url, "title": title})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, port=int(os.environ.get("PORT", 5000)))
