from flask import Flask, render_template, request, jsonify
import yt_dlp
import os

app = Flask(__name__)

app.wsgi_app = app.wsgi_app 

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

    ydl_opts = {
        'format': 'best[ext=mp4]/best',
        'quiet': True,
        'no_warnings': True,
        'cookiefile': 'cookies.txt',
        'http_headers': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        }
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=False)
            direct_url = info.get('url')
            title = info.get('title', 'video')
            
        return jsonify({"success": True, "download_url": direct_url, "title": title})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500
