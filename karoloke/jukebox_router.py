import io
import json
import math
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
    get_background_subfolders,
    get_video_file,
    validate_song_for_queue,
)
from karoloke.settings import (
    BACKGROUND_DIR,
    PLAYER_TEMPLATE,
    SETTINGS_TEMPLATE,
    VIDEO_DIR,
    VIDEO_FORMATS,
    VIDEO_PATH_SETUP_TEMPLATE,
)
from karoloke.utils import collect_playlist, is_playable

app = Flask(__name__)
app.secret_key = (
    'karoloke-secret-key-2024'  # Secret key for session management
)

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
    # Initialize session variables if not present
    if 'queue' not in session:
        session['queue'] = []
        session['current_song'] = None
        session.modified = True
    if 'background_folder' not in session:
        session['background_folder'] = 'default'
        session.modified = True

    bg_img = get_background_img(
        BACKGROUND_DIR, session.get('background_folder', 'default')
    )
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
    # Reload playlist JSON each request for freshness
    try:
        with open(playlist_path, 'r', encoding='utf-8') as f:
            current_playlist = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        current_playlist = []

    # Use shared is_playable from utils

    # Discover available videos (first basename wins)
    valid_videos = {}
    scan_errors = 0
    for root, _, files in os.walk(VIDEO_DIR):
        for fname in files:
            _, ext = os.path.splitext(fname)
            if ext.lower() not in VIDEO_FORMATS:
                continue
            basename = os.path.splitext(fname)[0]
            full_path = os.path.join(root, fname)
            if basename in valid_videos:
                scan_errors += 1  # duplicate basename
                continue
            if is_playable(full_path):
                valid_videos[basename] = full_path
            else:
                scan_errors += 1

    # Filter playlist entries to those with valid videos
    filtered_playlist = [
        row for row in current_playlist if row.get('filename') in valid_videos
    ]
    missing_errors = len(current_playlist) - len(filtered_playlist)
    error_count = scan_errors + missing_errors
    ok_count = len(filtered_playlist)

    # Pagination
    page = max(int(request.args.get('page', 1)), 1)
    allowed_page_sizes = [100, 200, 500]
    try:
        page_size = int(request.args.get('page_size', allowed_page_sizes[0]))
    except ValueError:
        page_size = allowed_page_sizes[0]
    if page_size not in allowed_page_sizes:
        page_size = allowed_page_sizes[0]

    total_pages = max(math.ceil(ok_count / page_size), 1)
    if page > total_pages:
        page = total_pages

    start_idx = (page - 1) * page_size
    end_idx = start_idx + page_size
    page_items = filtered_playlist[start_idx:end_idx]

    pages_list = list(range(1, total_pages + 1))

    return render_template(
        'playlist.html',
        playlist=page_items,
        page=page,
        total_pages=total_pages,
        page_size=page_size,
        page_sizes=allowed_page_sizes,
        pages_list=pages_list,
        ok_count=ok_count,
        error_count=error_count,
    )


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
    
    # Original playlist route logic (commented for future use)
    # playlist_url = f"{request.scheme}://{local_ip}:{port}{url_for('playlist')}"
    
    # Temporary solution: QR code points to a PDF file
    playlist_url = "https://drive.google.com/file/d/1Mv06a6NNCY1udz38Q2fYjKdg57lI1hJr/view?usp=sharing"
    
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
    bg_folder = session.get('background_folder', 'default')
    background_img = get_background_img(BACKGROUND_DIR, bg_folder)
    return render_template(VIDEO_PATH_SETUP_TEMPLATE, bg_img=background_img)


@app.route('/add_to_queue', methods=['POST'])
def add_to_queue():
    """Add a song to the queue after validation."""
    song_num = request.form.get('song', '').strip()

    if not song_num:
        return {
            'status': 'error',
            'message': 'Erro nesta musica, escolha outra',
        }, 400

    # Validate song
    validation = validate_song_for_queue(song_num, VIDEO_DIR)

    if not validation['valid']:
        if validation['reason'] == 'duplicate':
            return {
                'status': 'duplicate',
                'message': 'Música já selecionada',
            }, 409
        else:
            return {
                'status': 'error',
                'message': 'Erro nesta musica, escolha outra',
            }, 400

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
    bg_folder = session.get('background_folder', 'default')
    bg_img = get_background_img(BACKGROUND_DIR, bg_folder)
    return render_template('score.html', bg_img=bg_img)


@app.route('/settings')
def settings():
    """Settings page for background folder and video directory configuration."""
    bg_folder = session.get('background_folder', 'default')
    bg_img = get_background_img(BACKGROUND_DIR, bg_folder)
    folders = get_background_subfolders(BACKGROUND_DIR)
    return render_template(
        SETTINGS_TEMPLATE,
        bg_img=bg_img,
        background_folders=folders,
        current_background=bg_folder,
    )


@app.route('/get_background_folders', methods=['GET'])
def get_background_folders():
    """List available background subfolders."""
    folders = get_background_subfolders(BACKGROUND_DIR)
    current = session.get('background_folder', 'default')
    return {'folders': folders, 'current': current}, 200


@app.route('/set_background_folder', methods=['POST'])
def set_background_folder():
    """Set the active background folder in session."""
    folder = request.form.get('folder', '').strip()

    if not folder:
        return {'status': 'error', 'message': 'No folder specified'}, 400

    # Validate folder exists
    available_folders = get_background_subfolders(BACKGROUND_DIR)
    if folder not in available_folders:
        return {'status': 'error', 'message': 'Invalid folder'}, 400

    session['background_folder'] = folder
    session.modified = True

    return {'status': 'ok', 'folder': folder}, 200
