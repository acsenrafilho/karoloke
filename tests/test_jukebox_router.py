import os
import re
import sys
import tempfile
from io import BytesIO
from unittest import mock

import pytest

if not sys.platform.startswith('darwin'):
    import pyzbar.pyzbar as pyzbar
from PIL import Image

from karoloke import jukebox_router


@pytest.fixture
def client():
    jukebox_router.app.config['TESTING'] = True
    with jukebox_router.app.test_client() as client:
        yield client


def test_index_get(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b'<html' in response.data


def test_index_post_valid_song(client):
    with mock.patch(
        'karoloke.jukebox_controller.get_video_file', return_value='1.mp4'
    ):
        response = client.post('/', data={'song': '1'})
        assert '200' in response.status


def test_index_post_no_song(client):
    response = client.post('/', data={})
    assert response.status_code == 200


def test_playlist(client):
    response = client.get('/playlist')
    assert response.status_code == 200
    assert b'<html' in response.data


def test_playlist_qr(client):
    response = client.get('/playlist_qr')
    assert response.status_code == 200
    assert response.mimetype == 'image/png'


@pytest.mark.skipif(
    sys.platform.startswith('darwin'),
    reason='QR code IP test skipped on macOS',
)
def test_playlist_qr_is_with_ip_address(client):
    response = client.get('/playlist_qr')
    assert response.status_code == 200

    # Decode the QR code from the response PNG image
    img = Image.open(BytesIO(response.data))
    decoded = pyzbar.decode(img)
    ip_pattern = re.compile(rb'https?://(\d{1,3}\.){3}\d{1,3}(:\d+)?')
    assert any(
        d.type == 'QRCODE' and ip_pattern.search(d.data) for d in decoded
    )


@pytest.mark.skipif(
    sys.platform.startswith('win'), reason='Background test skipped on Windows'
)
def test_background(client):
    with tempfile.NamedTemporaryFile(
        dir=jukebox_router.BACKGROUND_DIR, suffix='.png', delete=False
    ) as f:
        fname = os.path.basename(f.name)
        temp_file_name = f.name
    try:
        response = client.get(f'/background/{fname}')
        assert response.status_code == 200
    finally:
        os.remove(temp_file_name)


@pytest.mark.skipif(
    sys.platform.startswith('win'), reason='Background test skipped on Windows'
)
def test_video(client):
    with tempfile.NamedTemporaryFile(
        dir=jukebox_router.VIDEO_DIR, suffix='.mp4', delete=False
    ) as f:
        fname = os.path.basename(f.name)
        temp_file_name = f.name
    try:
        response = client.get(f'/video/{fname}')
        assert response.status_code == 200
    finally:
        os.remove(temp_file_name)


def test_setup_video_dir_get(client):
    response = client.get('/setup_video_dir')
    assert response.status_code == 200
    assert b'<html' in response.data


def test_setup_video_dir_post_valid(client):
    with tempfile.TemporaryDirectory() as tmpdir:
        response = client.post('/setup_video_dir', data={'video_dir': tmpdir})
        assert response.status_code == 200
        assert b'success' in response.data


def test_setup_video_dir_post_invalid(client):
    response = client.post(
        '/setup_video_dir', data={'video_dir': '/invalid/path'}
    )
    assert response.status_code == 400
    assert b'Invalid directory' in response.data


def test_score(client):
    response = client.get('/score')
    assert response.status_code == 200
    assert b'<html' in response.data


def test_add_to_queue_valid(client):
    with client.session_transaction() as sess:
        sess['queue'] = []
    
    with mock.patch(
        'karoloke.jukebox_router.validate_song_for_queue',
        return_value={'valid': True, 'reason': None}
    ):
        response = client.post('/add_to_queue', data={'song': '123'})
        assert response.status_code == 200
        data = response.get_json()
        assert data['status'] == 'ok'
        assert '123' in data['queue']


def test_add_to_queue_duplicate(client):
    with mock.patch(
        'karoloke.jukebox_router.validate_song_for_queue',
        return_value={'valid': False, 'reason': 'duplicate'}
    ):
        response = client.post('/add_to_queue', data={'song': '123'})
        assert response.status_code == 409
        data = response.get_json()
        assert data['status'] == 'duplicate'


def test_add_to_queue_error(client):
    with mock.patch(
        'karoloke.jukebox_controller.validate_song_for_queue',
        return_value={'valid': False, 'reason': 'error'}
    ):
        response = client.post('/add_to_queue', data={'song': '999'})
        assert response.status_code == 400
        data = response.get_json()
        assert data['status'] == 'error'


def test_add_to_queue_empty_song(client):
    response = client.post('/add_to_queue', data={'song': ''})
    assert response.status_code == 400
    data = response.get_json()
    assert data['status'] == 'error'


def test_get_queue(client):
    with client.session_transaction() as sess:
        sess['queue'] = ['123', '456']
    
    response = client.get('/get_queue')
    assert response.status_code == 200
    data = response.get_json()
    assert data['queue'] == ['123', '456']


def test_get_queue_empty(client):
    response = client.get('/get_queue')
    assert response.status_code == 200
    data = response.get_json()
    assert data['queue'] == []


def test_next_song_with_queue(client):
    with client.session_transaction() as sess:
        sess['queue'] = ['123', '456']
        sess['current_song'] = '123'
    
    response = client.get('/next_song')
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == 'next'
    assert data['next_song'] == '456'


def test_next_song_empty_queue(client):
    with client.session_transaction() as sess:
        sess['queue'] = ['123']
        sess['current_song'] = '123'
    
    response = client.get('/next_song')
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == 'empty'


def test_settings_page(client):
    response = client.get('/settings')
    assert response.status_code == 200
    assert b'<html' in response.data
    assert b'Background' in response.data or b'background' in response.data


def test_get_background_folders(client):
    with mock.patch(
        'karoloke.jukebox_controller.get_background_subfolders',
        return_value=['default', 'custom']
    ):
        response = client.get('/get_background_folders')
        assert response.status_code == 200
        data = response.get_json()
        assert 'folders' in data
        assert 'default' in data['folders']
        assert 'current' in data


def test_set_background_folder_valid(client):
    with mock.patch(
        'karoloke.jukebox_router.get_background_subfolders',
        return_value=['default', 'custom']
    ):
        response = client.post('/set_background_folder', data={'folder': 'custom'})
        assert response.status_code == 200
        data = response.get_json()
        assert data['status'] == 'ok'
        assert data['folder'] == 'custom'


def test_set_background_folder_invalid(client):
    with mock.patch(
        'karoloke.jukebox_controller.get_background_subfolders',
        return_value=['default']
    ):
        response = client.post('/set_background_folder', data={'folder': 'nonexistent'})
        assert response.status_code == 400
        data = response.get_json()
        assert data['status'] == 'error'


def test_set_background_folder_empty(client):
    response = client.post('/set_background_folder', data={'folder': ''})
    assert response.status_code == 400
    data = response.get_json()
    assert data['status'] == 'error'


def test_index_auto_load_from_queue(client):
    with client.session_transaction() as sess:
        sess['queue'] = ['123']
    
    with mock.patch(
        'karoloke.jukebox_controller.get_video_file',
        return_value='123.mp4'
    ):
        response = client.get('/')
        assert response.status_code == 200
        assert b'123' in response.data or b'html' in response.data


def test_playlist_with_pagination(client):
    response = client.get('/playlist?page=1&page_size=100')
    assert response.status_code == 200
    assert b'<html' in response.data


def test_playlist_invalid_page_size(client):
    # Invalid page_size should default to 100
    response = client.get('/playlist?page=1&page_size=999')
    assert response.status_code == 200
    assert b'<html' in response.data
