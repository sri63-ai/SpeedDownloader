from flask import Flask, render_template, request, send_file
import yt_dlp
import os
import time

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/terms')
def terms():
    return render_template('terms.html')

@app.route('/download', methods=['POST'])
def download():
    video_url = request.form.get('url')
    
    if not video_url:
        return "Error: URL cannot be empty!", 400

    output_folder = "downloads"
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    ydl_opts = {
        'format': 'best[ext=mp4]/best',
        'outtmpl': f'{output_folder}/video_%(timestamp)s.%(ext)s',
        'noplaylist': True,
        'quiet': True,
        'http_headers': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-us,en;q=0.5',
        }
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=True)
            filename = ydl.prepare_filename(info)
        
        return send_file(filename, as_attachment=True)

    except Exception as e:
        return f"<h1>Error: {e}</h1><p>YouTube might be blocking this request. Please try another link or try again after 1 minute.</p>", 500

if __name__ == "__main__":
    app.run(debug=True, port=5000)
