import os
from flask import Flask, render_template, request, jsonify
import yt_dlp

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_info', methods=['POST'])
def get_info():
    video_url = request.form.get('url')
    
    # Cookie file check kora jate error na hoy
    cookie_path = 'cookies.txt'
    
   ydl_opts = {
    'quiet': True,
    'no_warnings': True,
    'format': 'best',
    'cookiefile': 'cookies.txt',  # Ei line-ti error solve korbe
    'extractor_args': {
        'youtube': {
            'player_client': ['android', 'web']
        }
    }
}
    
    # Jodi cookies.txt file thake tobe seta use korbe
    if os.path.exists(cookie_path):
        ydl_opts['cookiefile'] = cookie_path

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # ... baki code ager motoi thakbe ...
            info = ydl.extract_info(video_url, download=False)
            
            # Format list filter: Shudhu MP4 ebong video+audio ache emon formats
            formats = []
            for f in info.get('formats', []):
                # MP4 format ebong jekhane video o audio duiti-i ache
                if f.get('ext') == 'mp4' and f.get('acodec') != 'none' and f.get('vcodec') != 'none':
                    formats.append({
                        'url': f['url'],
                        'quality': f.get('format_note', 'HD'),
                        'extension': f.get('ext')
                    })
            
            return jsonify({
                'title': info.get('title'),
                'thumbnail': info.get('thumbnail'),
                'duration': info.get('duration_string'),
                'formats': formats
            })
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    # Render ba onno hosting-er jonno port dynamic kora
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)


