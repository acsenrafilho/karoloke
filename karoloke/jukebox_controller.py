import os
import random

from karoloke.settings import VIDEO_FORMATS


def get_background_img(background_dir: str = 'backgrounds'):
    images = [
        f
        for f in os.listdir(background_dir)
        if f.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp', '.gif'))
    ]
    if not images:
        raise FileNotFoundError(
            "No background images found in the 'background' directory."
        )

    if images:
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
