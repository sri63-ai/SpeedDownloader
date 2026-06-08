from flask import Flask, render_template, request, send_from_directory
import yt_dlp
import os

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

# New Route to display Terms and Conditions Page safely
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
        'outtmpl': f'{output_folder}/%(title)s.%(ext)s',
        'noplaylist': True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([video_url])
        return "<h1>⚡ Success! Video downloaded successfully into the server 'downloads' folder.</h1>"
    except Exception as e:
        return f"<h1>Error: {e}</h1>", 500

if __name__ == "__main__":
    app.run(debug=True, port=5000)
