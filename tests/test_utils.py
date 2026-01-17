import os
import shutil
import tempfile
from unittest import mock

import pytest

from karoloke.settings import VIDEO_FORMATS
from karoloke.utils import collect_playlist, is_playable


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


def test_is_playable_nonexistent_file():
    """Test that is_playable returns False for nonexistent file."""
    assert is_playable('/nonexistent/file.mp4') is False


def test_is_playable_empty_file():
    """Test that is_playable returns False for empty file."""
    with tempfile.NamedTemporaryFile(suffix='.mp4', delete=False) as f:
        temp_path = f.name
    try:
        # File exists but is empty (size 0)
        assert is_playable(temp_path) is False
    finally:
        os.remove(temp_path)


def test_is_playable_valid_file_no_ffprobe():
    """Test is_playable with valid file when ffprobe is not available."""
    with tempfile.NamedTemporaryFile(suffix='.mp4', delete=False) as f:
        f.write(b'fake video content')
        temp_path = f.name
    
    try:
        with mock.patch('shutil.which', return_value=None):
            # Should return True based on size check alone
            assert is_playable(temp_path) is True
    finally:
        os.remove(temp_path)


def test_is_playable_with_ffprobe_success():
    """Test is_playable when ffprobe is available and succeeds."""
    with tempfile.NamedTemporaryFile(suffix='.mp4', delete=False) as f:
        f.write(b'fake video content')
        temp_path = f.name
    
    try:
        # Mock ffprobe being available and returning success
        with mock.patch('shutil.which', return_value='/usr/bin/ffprobe'):
            mock_result = mock.Mock()
            mock_result.returncode = 0
            with mock.patch('subprocess.run', return_value=mock_result):
                assert is_playable(temp_path) is True
    finally:
        os.remove(temp_path)


def test_is_playable_with_ffprobe_failure():
    """Test is_playable when ffprobe is available but fails."""
    with tempfile.NamedTemporaryFile(suffix='.mp4', delete=False) as f:
        f.write(b'fake video content')
        temp_path = f.name
    
    try:
        with mock.patch('shutil.which', return_value='/usr/bin/ffprobe'):
            mock_result = mock.Mock()
            mock_result.returncode = 1
            with mock.patch('subprocess.run', return_value=mock_result):
                assert is_playable(temp_path) is False
    finally:
        os.remove(temp_path)


def test_is_playable_with_ffprobe_exception():
    """Test is_playable when ffprobe raises an exception."""
    with tempfile.NamedTemporaryFile(suffix='.mp4', delete=False) as f:
        f.write(b'fake video content')
        temp_path = f.name
    
    try:
        with mock.patch('shutil.which', return_value='/usr/bin/ffprobe'):
            with mock.patch('subprocess.run', side_effect=Exception('ffprobe error')):
                assert is_playable(temp_path) is False
    finally:
        os.remove(temp_path)


def test_is_playable_os_error_on_size():
    """Test is_playable when os.path.getsize raises OSError."""
    with tempfile.NamedTemporaryFile(suffix='.mp4', delete=False) as f:
        f.write(b'content')
        temp_path = f.name
    
    try:
        with mock.patch('os.path.getsize', side_effect=OSError('Permission denied')):
            assert is_playable(temp_path) is False
    finally:
        os.remove(temp_path)
