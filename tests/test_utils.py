import os
import shutil
import tempfile

import pytest

from karoloke.settings import VIDEO_FORMATS
from karoloke.utils import collect_playlist


@pytest.fixture
def temp_video_dir():
    """Fixture to create a temporary directory with video files."""
    temp_dir = tempfile.mkdtemp()
    files = [
        'song1.mp4',
        'song2.webm',
        'song3.avi',
        'not_a_video.txt',
        'duplicate.mp4',
    ]
    # Create files in root
    for fname in files:
        with open(os.path.join(temp_dir, fname), 'w') as f:
            f.write('dummy')
    # Create subdirectory with more files
    sub_dir = os.path.join(temp_dir, 'sub')
    os.makedirs(sub_dir)
    with open(os.path.join(sub_dir, 'song4.mp4'), 'w') as f:
        f.write('dummy')
    with open(os.path.join(sub_dir, 'duplicate.mp4'), 'w') as f:
        f.write('dummy')
    yield temp_dir
    shutil.rmtree(temp_dir)


def test_collect_playlist_finds_supported_formats(temp_video_dir):
    """Test that only supported video formats are collected."""
    playlist = collect_playlist(temp_video_dir)
    expected_exts = tuple(VIDEO_FORMATS)
    assert all(
        os.path.splitext(f)[1].lower() in expected_exts for f in playlist
    )
    assert any('song1.mp4' in f for f in playlist)
    assert any('song2.webm' in f for f in playlist)
    assert any('song4.mp4' in f for f in playlist)
    assert not any('not_a_video.txt' in f for f in playlist)


def test_collect_playlist_empty_dir():
    """Test that an empty directory returns an empty list."""
    temp_dir = tempfile.mkdtemp()
    try:
        playlist = collect_playlist(temp_dir)
        assert playlist == []
    finally:
        shutil.rmtree(temp_dir)


def test_collect_playlist_nonexistent_dir():
    """Test that a nonexistent directory returns an empty list."""
    playlist = collect_playlist('/nonexistent/path/for/karoloke')
    assert playlist == []
