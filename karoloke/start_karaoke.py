import os
import threading
import webbrowser

from karoloke.jukebox_router import app
from karoloke.settings import BACKGROUND_DIR, VIDEO_DIR


def open_browser():
    webbrowser.open_new('http://localhost:5000/')


def main():
    # Ensure video and backgrounds folders exist
    os.makedirs(BACKGROUND_DIR, exist_ok=True)
    os.makedirs(VIDEO_DIR, exist_ok=True)
    threading.Timer(1.0, open_browser).start()
    app.run(host='0.0.0.0', port=5000, debug=True, use_reloader=False)


if __name__ == '__main__':
    main()
