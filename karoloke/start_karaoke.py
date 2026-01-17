import os
import threading
import webbrowser
import sys

from karoloke.jukebox_router import app
from karoloke.settings import BACKGROUND_DIR, VIDEO_DIR


def open_browser():
    """
    Open the application in the default browser.
    Falls back to supported browsers if default fails.
    """
    url = 'http://localhost:5000/'
    
    try:
        # Try to open with system default browser
        webbrowser.open_new(url)
    except Exception as e:
        # If default browser fails, try to open with specific browsers
        print(f"Could not open default browser: {e}")
        print("Attempting to open with supported browsers...")
        
        # Try Chrome, Firefox, Edge in order
        browsers = [
            'chrome',
            'chromium',
            'firefox',
            'mozilla',
            'microsoft-edge',
        ]
        
        opened = False
        for browser_name in browsers:
            try:
                browser = webbrowser.get(browser_name)
                browser.open_new(url)
                opened = True
                print(f"Successfully opened in {browser_name}")
                break
            except Exception:
                continue
        
        if not opened:
            print("\n" + "="*60)
            print("ERROR: Could not open browser automatically")
            print("="*60)
            print("Please install one of the following browsers:")
            print("  - Google Chrome")
            print("  - Mozilla Firefox")
            print("  - Microsoft Edge")
            print("\nOr manually open this URL in your browser:")
            print(f"  {url}")
            print("="*60 + "\n")


def main():
    # Ensure video and backgrounds folders exist
    os.makedirs(BACKGROUND_DIR, exist_ok=True)
    os.makedirs(VIDEO_DIR, exist_ok=True)
    threading.Timer(1.0, open_browser).start()
    app.run(host='0.0.0.0', port=5000, debug=True, use_reloader=False)


if __name__ == '__main__':
    main()
