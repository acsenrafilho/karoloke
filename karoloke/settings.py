import os

# Settings for the Karoloke application
VIDEO_FORMATS = ('.mp4', '.webm', '.ogg')

# Path to backgrounds and videos
BACKGROUND_DIR = os.path.join(os.path.dirname(__file__), 'backgrounds')
VIDEO_DIR = os.path.join(os.path.dirname(__file__), 'videos')
PLAYER_TEMPLATE = 'player.html'
VIDEO_PATH_SETUP_TEMPLATE = 'video_path_setup.html'
