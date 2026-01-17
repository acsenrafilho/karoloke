import os
import pathlib
import random
import tempfile
from unittest import mock

import pytest

from karoloke.jukebox_controller import (
    get_background_img,
    get_background_subfolders,
    get_video_file,
    validate_song_for_queue,
)

BACKGROUND_FOLDER = os.path.join(
    pathlib.Path(__file__).parents[1], 'karoloke', 'backgrounds'
)


def test_get_background_img_raise_error_for_empty_image_list(tmpdir):
    with pytest.raises(
        FileNotFoundError,
        match="No background images found in the 'background' directory.",
    ):
        get_background_img(background_dir=tmpdir)


def test_get_background_img_returns_image():
    # Call the function and check if it returns the correct image
    result = get_background_img(background_dir=str(BACKGROUND_FOLDER))
    assert len(result) > 0   # type: ignore


def test_get_background_img_with_subfolder(tmpdir):
    # Create subfolder with image
    subfolder = tmpdir.mkdir('custom')
    subfolder.join('test.png').write('fake')
    result = get_background_img(background_dir=str(tmpdir), subfolder='custom')
    assert 'custom' in result
    assert result.endswith('.png')


def test_get_background_img_fallback_to_default(tmpdir):
    # Create default subfolder with image
    default_folder = tmpdir.mkdir('default')
    default_folder.join('test.jpg').write('fake')
    # Request non-existent subfolder, should fall back to default
    result = get_background_img(background_dir=str(tmpdir), subfolder='nonexistent')
    assert 'default' in result


def test_get_background_img_no_subfolder(tmpdir):
    # Image in base directory (no subfolder)
    tmpdir.join('test.png').write('fake')
    result = get_background_img(background_dir=str(tmpdir), subfolder='missing')
    assert result.endswith('.png')


def test_get_background_subfolders_returns_list(tmpdir):
    tmpdir.mkdir('default')
    tmpdir.mkdir('custom')
    tmpdir.mkdir('.hidden')  # Should be ignored
    tmpdir.join('file.txt').write('not a folder')
    
    result = get_background_subfolders(str(tmpdir))
    assert 'default' in result
    assert 'custom' in result
    assert '.hidden' not in result
    # default should be first
    assert result[0] == 'default'


def test_get_background_subfolders_nonexistent_dir():
    result = get_background_subfolders('/nonexistent/path')
    assert result == ['default']


def test_get_background_subfolders_no_folders(tmpdir):
    tmpdir.join('file.txt').write('not a folder')
    result = get_background_subfolders(str(tmpdir))
    assert result == ['default']


def test_validate_song_for_queue_valid(tmpdir):
    # Create a valid video file
    video_file = tmpdir.join('123.mp4')
    video_file.write('fake video content')
    
    from karoloke import jukebox_router
    with jukebox_router.app.test_request_context():
        from flask import session
        session['queue'] = []
        result = validate_song_for_queue('123', str(tmpdir))
        assert result['valid'] is True
        assert result['reason'] is None


def test_validate_song_for_queue_duplicate(tmpdir):
    video_file = tmpdir.join('123.mp4')
    video_file.write('fake video content')
    
    from karoloke import jukebox_router
    with jukebox_router.app.test_request_context():
        from flask import session
        session['queue'] = ['123']
        result = validate_song_for_queue('123', str(tmpdir))
        assert result['valid'] is False
        assert result['reason'] == 'duplicate'


def test_validate_song_for_queue_not_found(tmpdir):
    from karoloke import jukebox_router
    with jukebox_router.app.test_request_context():
        from flask import session
        session['queue'] = []
        result = validate_song_for_queue('999', str(tmpdir))
        assert result['valid'] is False
        assert result['reason'] == 'error'


def test_validate_song_for_queue_empty_file(tmpdir):
    # Create an empty file (size 0)
    video_file = tmpdir.join('123.mp4')
    video_file.write('')
    
    from karoloke import jukebox_router
    with jukebox_router.app.test_request_context():
        from flask import session
        session['queue'] = []
        result = validate_song_for_queue('123', str(tmpdir))
        assert result['valid'] is False
        assert result['reason'] == 'error'


def test_get_video_file_found(tmpdir):
    video_file = tmpdir.join('456.mp4')
    video_file.write('fake video')
    
    result = get_video_file('456', str(tmpdir))
    assert result is not None
    assert '456.mp4' in result


def test_get_video_file_in_subdirectory(tmpdir):
    subdir = tmpdir.mkdir('subdir')
    video_file = subdir.join('789.webm')
    video_file.write('fake video')
    
    result = get_video_file('789', str(tmpdir))
    assert result is not None
    assert '789.webm' in result


def test_get_video_file_not_found(tmpdir):
    result = get_video_file('999', str(tmpdir))
    assert result is None
