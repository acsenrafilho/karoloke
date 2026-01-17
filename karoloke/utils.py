import os
import shutil
import subprocess

from karoloke.settings import VIDEO_FORMATS


def collect_playlist(root_dir: str) -> list:
    """
    Collects all video files from the specified root directory and its subdirectories.

    Note:
        This function searches for files with the '.mp4' extension and it is not
        allowed to have duplicate filenames in the list. If a file with the same name
        already exists in the list, it will be skipped.

    Args:
        root_dir (str): The root directory to search for video files.

    Returns:
        list: A list of paths to video files.
    """
    video_files = []
    for dirpath, _, filenames in os.walk(root_dir):
        for filename in filenames:
            # Skip if the file is already in the list
            if filename in video_files:
                continue

            # Check for common HTML5 video extensions
            if filename.lower().endswith(VIDEO_FORMATS):
                video_files.append(os.path.join(dirpath, filename))

    return video_files


def is_playable(path: str) -> bool:
    """
    Perform a lightweight check that a video file is likely playable by the browser.

    The validation follows two steps:
    1. Basic file checks: existence and file size > 0.
    2. Optional ffprobe probe: if `ffprobe` is available in PATH, run a quick
       probe and ensure it returns success; otherwise, fall back to the basic check.

    Parameters
    ----------
    path : str
        Absolute path to the video file to validate.

    Returns
    -------
    bool
        True if the file passes the checks, False otherwise.
    """
    if not os.path.exists(path):
        return False

    try:
        if os.path.getsize(path) <= 0:
            return False
    except OSError:
        return False

    # If ffprobe is not available, accept based on size check
    if shutil.which('ffprobe') is None:
        return True

    try:
        result = subprocess.run(
            [
                'ffprobe', '-v', 'error', '-select_streams', 'v:0',
                '-show_entries', 'stream=codec_type', '-of', 'default=noprint_wrappers=1',
                path,
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=3,
            check=False,
        )
        return result.returncode == 0
    except Exception:
        return False
