from flask import Flask, render_template, request, send_file, after_this_request
import subprocess
import os
import yt_dlp
import tempfile
from werkzeug.utils import secure_filename

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    url = request.form['url']
    file_format = request.form['format']

    try:
        # Get video title using yt_dlp
        with yt_dlp.YoutubeDL({'quiet': True}) as ydl:
            info = ydl.extract_info(url, download=False)
            title = info.get('title', 'downloaded_media')

        # Create a safe and clean filename
        safe_title = secure_filename(title)
        ext = 'mp4' if file_format == 'mp4' else 'mp3'
        filename = f"{safe_title}.{ext}"

        # Temp directory for download
        temp_dir = tempfile.gettempdir()
        output_path = os.path.join(temp_dir, filename)

        # yt-dlp command based on format
        command = (
            ['yt-dlp', '-f', 'mp4', '-o', output_path, url]
            if file_format == 'mp4'
            else ['yt-dlp', '-x', '--audio-format', 'mp3', '-o', output_path, url]
        )

        # Execute the download
        subprocess.run(command, check=True)

        # Schedule file deletion after sending
        @after_this_request
        def cleanup(response):
            try:
                os.remove(output_path)
            except Exception as e:
                print(f"Cleanup failed: {e}")
            return response

        # Send file to user
        return send_file(output_path, as_attachment=True, download_name=filename)

    except Exception as e:
        return f"Download failed: {e}", 500

if __name__ == '__main__':
    app.run(debug=True)
