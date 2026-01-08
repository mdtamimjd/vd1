from flask import Flask, render_template, request, jsonify
import yt_dlp

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_info', methods=['POST'])
def get_info():
    video_url = request.form.get('url')
    
    # yt-dlp options
    ydl_opts = {'quiet': True}
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # Video-r tottho fetch kora
            info = ydl.extract_info(video_url, download=False)
            
            # Shudhu proyojoniyo tottho pathano
            video_data = {
                'title': info.get('title'),
                'thumbnail': info.get('thumbnail'),
                'formats': [
                    {'url': f['url'], 'format_note': f.get('format_note')}
                    for f in info.get('formats', []) 
                    if f.get('ext') == 'mp4' and f.get('vcodec') != 'none'
                ]
            }
            return jsonify(video_data)
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)