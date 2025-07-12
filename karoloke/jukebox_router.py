import os

from flask import (
    Flask,
    render_template,
    render_template_string,
    request,
    send_from_directory,
)

from karoloke.jukebox_controller import get_background_img, get_video_file
from karoloke.settings import (
    BACKGROUND_DIR,
    PLAYER_TEMPLATE,
    VIDEO_DIR,
    VIDEO_PATH_SETUP_TEMPLATE,
)
from karoloke.utils import collect_playlist

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    bg_img = get_background_img(BACKGROUND_DIR)
    if not bg_img or not os.path.isfile(os.path.join(BACKGROUND_DIR, bg_img)):
        bg_img = None
    video = None
    if request.method == 'POST':
        stop_recurring = True
        while stop_recurring:
            song_num = request.form.get('song')
            if song_num:
                video = get_video_file(song_num, VIDEO_DIR)

            if video:
                stop_recurring = False

    video_files = collect_playlist(VIDEO_DIR)
    total_videos = len(video_files)
    return render_template(
        PLAYER_TEMPLATE, bg_img=bg_img, video=video, total_videos=total_videos
    )


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
    return render_template('video_path_setup.html', bg_img=background_img)
