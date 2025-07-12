import os

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
        list: A dictionay of paths to video files.
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
