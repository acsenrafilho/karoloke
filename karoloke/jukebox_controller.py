import os
import random

from flask import session

from karoloke.settings import VIDEO_FORMATS


def get_background_subfolders(background_dir: str) -> list[str]:
    """List all subfolders in the backgrounds directory.

    Parameters
    ----------
    background_dir : str
        Base backgrounds directory

    Returns
    -------
    list[str]
        List of subfolder names
    """
    if not os.path.exists(background_dir):
        return ['default']

    subfolders = [
        f
        for f in os.listdir(background_dir)
        if os.path.isdir(os.path.join(background_dir, f))
        and not f.startswith('.')
    ]

    # Ensure 'default' is always first if it exists
    if 'default' in subfolders:
        subfolders.remove('default')
        subfolders.insert(0, 'default')

    return subfolders if subfolders else ['default']


def validate_song_for_queue(song_num: str, video_dir: str) -> dict:
    """Validate if a song can be added to the queue.

    Checks if:
    - Song file exists in supported format
    - File size is greater than 0
    - Song is not already in the queue

    Parameters
    ----------
    song_num : str
        Song number to validate
    video_dir : str
        Path to video directory

    Returns
    -------
    dict
        Status dict with keys:
        - 'valid' (bool): Whether song is valid
        - 'reason' (str): Reason if invalid
    """
    # Check if song is already in queue
    queue = session.get('queue', [])
    if song_num in queue:
        return {'valid': False, 'reason': 'duplicate'}

    # Check if video file exists and has supported format
    video_file = None
    for ext in VIDEO_FORMATS:
        candidate = f'{song_num}{ext}'
        for root, _, files in os.walk(video_dir):
            if candidate in files:
                video_path = os.path.join(root, candidate)
                # Check file size is greater than 0
                try:
                    if os.path.getsize(video_path) > 0:
                        video_file = video_path
                        break
                except (OSError, IOError):
                    continue
        if video_file:
            break

    if not video_file:
        return {'valid': False, 'reason': 'error'}

    return {'valid': True, 'reason': None}


def get_background_img(
    background_dir: str = 'backgrounds', subfolder: str = 'default'
):
    """Get a random background image from the specified subfolder.

    Parameters
    ----------
    background_dir : str
        Base backgrounds directory
    subfolder : str
        Subfolder name within background_dir (default: 'default')

    Returns
    -------
    str
        Relative path to background image (subfolder/filename)
    """
    folder_path = os.path.join(background_dir, subfolder)
    if not os.path.exists(folder_path):
        # Fallback to default if subfolder doesn't exist
        folder_path = os.path.join(background_dir, 'default')
        subfolder = 'default'
        if not os.path.exists(folder_path):
            # If even default doesn't exist, use the base directory
            folder_path = background_dir
            subfolder = ''

    if not os.path.exists(folder_path):
        raise FileNotFoundError(
            "No background images found in the 'background' directory."
        )

    images = [
        f
        for f in os.listdir(folder_path)
        if f.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp', '.gif'))
    ]
    if not images:
        raise FileNotFoundError(
            "No background images found in the 'background' directory."
        )

    # Return relative path with subfolder (or just filename if no subfolder)
    if subfolder:
        return os.path.join(subfolder, random.choice(images))
    else:
        return random.choice(images)


def get_video_file(song_num, video_dir):
    video_file = None
    for ext in VIDEO_FORMATS:
        candidate = f'{song_num}{ext}'
        # Recursively search for candidate in video_dir and subdirectories
        for root, _, files in os.walk(video_dir):
            if candidate in files:
                video_file = os.path.relpath(
                    os.path.join(root, candidate), video_dir
                )
                break
        if video_file:
            break

    if video_file:
        # Return the relative path from video_dir
        return video_file
    return None
