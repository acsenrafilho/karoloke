import os
from unittest import mock

from karoloke import start_karaoke


def test_main_does_not_fail_if_directories_exist(monkeypatch, tmp_path):
    # Create directories beforehand
    backgrounds = tmp_path / 'backgrounds'
    videos = tmp_path / 'videos'
    backgrounds.mkdir()
    videos.mkdir()
    monkeypatch.setattr('karoloke.settings.BACKGROUND_DIR', backgrounds)
    monkeypatch.setattr('karoloke.settings.VIDEO_DIR', videos)

    with mock.patch.object(start_karaoke.app, 'run') as mock_run:
        start_karaoke.main()
        # Directories should still exist
        assert backgrounds.exists()
        assert videos.exists()
        mock_run.assert_called_once()
