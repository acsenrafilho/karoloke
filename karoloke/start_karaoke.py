import os

from karoloke.jukebox_router import app
from karoloke.settings import BACKGROUND_DIR, VIDEO_DIR


def main():
    # Ensure video and backgrounds folders exist
    os.makedirs(BACKGROUND_DIR, exist_ok=True)
    os.makedirs(VIDEO_DIR, exist_ok=True)
    app.run(host='0.0.0.0', port=5000, debug=True)


if __name__ == '__main__':
    main()
