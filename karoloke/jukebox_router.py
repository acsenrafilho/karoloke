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
    session,
    url_for,
)

from karoloke.jukebox_controller import (
    get_background_img,
    get_video_file,
    validate_song_for_queue,
)
from karoloke.settings import (
    BACKGROUND_DIR,
    PLAYER_TEMPLATE,
    VIDEO_DIR,
    VIDEO_PATH_SETUP_TEMPLATE,
)
from karoloke.utils import collect_playlist

app = Flask(__name__)
app.secret_key = 'karoloke-secret-key-2024'  # Secret key for session management

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
    # Initialize queue if not present
    if 'queue' not in session:
        session['queue'] = []
        session['current_song'] = None
        session.modified = True
    
    bg_img = get_background_img(BACKGROUND_DIR)
    video = None
    current_song = None
    queue_position = None
    queue_length = None
    queue = session.get('queue', [])
    
    if request.method == 'POST':
        song_num = request.form.get('song')
        if song_num:
            video = get_video_file(song_num, VIDEO_DIR)
            if video:
                current_song = song_num
    else:
        # GET request: check if there's a song in the queue to auto-load
        if queue and len(queue) > 0:
            song_num = queue[0]
            video = get_video_file(song_num, VIDEO_DIR)
            if video:
                current_song = song_num
                session['current_song'] = song_num
                session.modified = True
    
    # Calculate queue position if video is playing
    if current_song and queue:
        if current_song in queue:
            queue_position = queue.index(current_song) + 1
            queue_length = len(queue)
    
    total_videos = len(collect_playlist(VIDEO_DIR))
    playlist_url = url_for('playlist')
    playlist_qr_url = url_for('playlist_qr')
    return render_template(
        PLAYER_TEMPLATE,
        bg_img=bg_img,
        video=video,
        current_song=current_song,
        queue_position=queue_position,
        queue_length=queue_length,
        queue=queue,
        total_videos=total_videos,
        playlist_qr_url=playlist_qr_url,
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


@app.route('/add_to_queue', methods=['POST'])
def add_to_queue():
    """Add a song to the queue after validation."""
    song_num = request.form.get('song', '').strip()
    
    if not song_num:
        return {'status': 'error', 'message': 'Erro nesta musica, escolha outra'}, 400
    
    # Validate song
    validation = validate_song_for_queue(song_num, VIDEO_DIR)
    
    if not validation['valid']:
        if validation['reason'] == 'duplicate':
            return {'status': 'duplicate', 'message': 'Música já selecionada'}, 409
        else:
            return {'status': 'error', 'message': 'Erro nesta musica, escolha outra'}, 400
    
    # Add to queue
    if 'queue' not in session:
        session['queue'] = []
    
    session['queue'].append(song_num)
    session.modified = True
    
    return {'status': 'ok', 'message': 'OK', 'queue': session['queue']}, 200


@app.route('/get_queue', methods=['GET'])
def get_queue():
    """Get current queue."""
    queue = session.get('queue', [])
    return {'queue': queue}, 200


@app.route('/next_song', methods=['GET'])
def next_song():
    """Remove current song from queue and load next one."""
    if 'queue' not in session:
        session['queue'] = []
    
    # Remove current song from queue if it exists
    current_song = session.get('current_song')
    if current_song and current_song in session['queue']:
        session['queue'].remove(current_song)
        session.modified = True
    
    # Check if there are more songs in queue
    if session['queue'] and len(session['queue']) > 0:
        # Redirect to index to auto-load next song
        return {'status': 'next', 'next_song': session['queue'][0]}, 200
    else:
        # Queue is empty, redirect to score
        return {'status': 'empty'}, 200


@app.route('/score')
def score():
    bg_img = get_background_img(BACKGROUND_DIR)
    return render_template('score.html', bg_img=bg_img)
