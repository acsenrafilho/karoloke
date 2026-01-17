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
