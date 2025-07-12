import os

from jukebox_router import app
from settings import BACKGROUND_DIR, VIDEO_DIR

if __name__ == '__main__':
    # Ensure video and backgrounds folders exist
    os.makedirs(BACKGROUND_DIR, exist_ok=True)
    os.makedirs(VIDEO_DIR, exist_ok=True)
    app.run(host='0.0.0.0', port=5000, debug=True)
