import io
import json
import os
import socket

import qrcode
from flask import (
    Flask,
    render_template,
    request,
    send_from_directory,
    url_for,
)

from karoloke.jukebox_controller import (
    calculate_average_score,
    get_background_img,
    get_video_file,
)
from karoloke.settings import (
    BACKGROUND_DIR,
    PLAYER_TEMPLATE,
    SINGERS,
    VIDEO_DIR,
    VIDEO_PATH_SETUP_TEMPLATE,
)
from karoloke.utils import collect_playlist

app = Flask(__name__)

playlist_path = os.path.join(
    os.path.dirname(__file__), 'static', 'playlist.json'
)
try:
    with open(playlist_path, 'r') as f:
        playlist_data = json.load(f)
except (FileNotFoundError, json.JSONDecodeError):
    # If the file doesn't exist or is invalid, start with an empty playlist.
    # This makes the app more resilient.
    playlist_data = []


@app.route('/', methods=['GET', 'POST'])
def index():
    bg_img = get_background_img(BACKGROUND_DIR)
    video = None
    selected_singer = None
    if request.method == 'POST':
        song_num = request.form.get('song')
        singer_name = request.form.get('singer')
        if song_num:
            video = get_video_file(song_num, VIDEO_DIR)
        if singer_name:
            selected_singer = singer_name
    total_videos = len(collect_playlist(VIDEO_DIR))
    playlist_url = url_for('playlist')
    playlist_qr_url = url_for('playlist_qr')
    return render_template(
        PLAYER_TEMPLATE,
        bg_img=bg_img,
        video=video,
        total_videos=total_videos,
        playlist_qr_url=playlist_qr_url,
        singers=list(SINGERS.values()),
        selected_singer=selected_singer,
    )


@app.route('/playlist')
def playlist():
    # Get available video files (filenames without extension)
    video_files = set(
        os.path.splitext(os.path.basename(f))[0]
        for f in collect_playlist(VIDEO_DIR)
    )
    # Filter playlist to only those with a matching video file
    filtered_playlist = [
        row for row in playlist_data if row['filename'] in video_files
    ]
    return render_template('playlist.html', playlist=filtered_playlist)


@app.route('/playlist_qr')
def playlist_qr():
    # Try to get the server's local IP address for the QR code

    try:
        hostname = socket.gethostname()
        local_ip = socket.gethostbyname(hostname)
        # If localhost, try to get a better IP
        if local_ip.startswith('127.') or local_ip == 'localhost':
            # Try to get the first non-localhost IP
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            try:
                # doesn't have to be reachable
                s.connect(('8.8.8.8', 80))
                local_ip = s.getsockname()[0]
            except Exception:
                pass
            finally:
                s.close()
    except socket.gaierror:
        local_ip = 'localhost'
    port = request.environ.get('SERVER_PORT', request.host.split(':')[-1])
    playlist_url = f"{request.scheme}://{local_ip}:{port}{url_for('playlist')}"
    img = qrcode.make(playlist_url)
    buf = io.BytesIO()
    img.save(buf, 'PNG')
    buf.seek(0)
    return app.response_class(buf.read(), mimetype='image/png')


@app.route('/background/<path:filename>')
def background(filename):
    return send_from_directory(BACKGROUND_DIR, filename)


@app.route('/video/<path:filename>')
def video(filename):
    return send_from_directory(VIDEO_DIR, filename)


@app.route('/setup_video_dir', methods=['GET', 'POST'])
def setup_video_dir():
    if request.method == 'POST':
        global VIDEO_DIR
        new_path = request.form.get('video_dir')
        if new_path and os.path.isdir(new_path):
            VIDEO_DIR = new_path
            return {'status': 'success', 'video_dir': VIDEO_DIR}, 200
        return {'status': 'error', 'message': 'Invalid directory'}, 400
    # GET request: show the setup page
    background_img = get_background_img(BACKGROUND_DIR)
    return render_template(VIDEO_PATH_SETUP_TEMPLATE, bg_img=background_img)


@app.route('/score')
def score():
    bg_img = get_background_img(BACKGROUND_DIR)
    return render_template('score.html', bg_img=bg_img)


@app.route('/singers', methods=['GET', 'POST'])
def singers():
    """
    Handles displaying and adding singers.
    """
    bg_img = get_background_img(BACKGROUND_DIR)
    error = None
    success = None

    if request.method == 'POST':
        singer_name = request.form.get('nickname')
        # Check for duplicate names
        if singer_name and singer_name.strip():
            if any(s['name'] == singer_name for s in SINGERS.values()):
                error = 'Nome/apelido já cadastrado. Tente outro.'
            else:
                singer_position = len(SINGERS) + 1
                SINGERS[singer_position] = {
                    'name': singer_name,
                    'average_score': 0,
                    'songs_counter': 0,
                }
                success = f"Cantor(a) '{singer_name}' cadastrado com sucesso!"
        else:
            error = 'Nome/apelido é obrigatório.'

    return render_template(
        'singers.html',
        bg_img=bg_img,
        singers=list(SINGERS.values()),
        error=error,
        success=success,
    )


@app.route('/submit_score', methods=['POST'])
def submit_score():
    data = request.get_json()
    score = data.get('score')
    name = data.get('singer')
    # Save the score into the SINGERS dictionary or process it as needed
    for singer in SINGERS.values():
        if singer['name'] == name:
            singer['average_score'] = calculate_average_score(
                singer.get('average_score', 0), score
            )
            singer['songs_counter'] += 1
            break
    return {'status': 'ok'}
