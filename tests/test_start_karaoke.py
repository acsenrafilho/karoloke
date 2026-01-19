import os
from unittest import mock

import pytest

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


def test_main_creates_missing_directories(monkeypatch, tmp_path):
    """Test that main() creates BACKGROUND_DIR and VIDEO_DIR if they don't exist."""
    backgrounds = tmp_path / 'backgrounds'
    videos = tmp_path / 'videos'

    # Directories don't exist yet
    assert not backgrounds.exists()
    assert not videos.exists()

    monkeypatch.setattr('karoloke.start_karaoke.BACKGROUND_DIR', backgrounds)
    monkeypatch.setattr('karoloke.start_karaoke.VIDEO_DIR', videos)

    with mock.patch('threading.Timer') as mock_timer:
        with mock.patch.object(start_karaoke.app, 'run') as mock_run:
            start_karaoke.main()

            # Directories should be created
            assert backgrounds.exists()
            assert videos.exists()

            # Timer should be started for opening browser
            mock_timer.assert_called_once_with(1.0, start_karaoke.open_browser)
            mock_timer.return_value.start.assert_called_once()

            # App should run with correct parameters
            mock_run.assert_called_once_with(
                host='0.0.0.0', port=5000, debug=True, use_reloader=False
            )


def test_open_browser_opens_url(monkeypatch):
    """Test that open_browser calls webbrowser.open_new with the correct URL."""
    with mock.patch('webbrowser.open_new') as mock_open:
        start_karaoke.open_browser()
        mock_open.assert_called_once_with('http://localhost:5000/')


def test_open_browser_fallback_on_exception(capsys):
    """Test that open_browser falls back to specific browsers when default fails."""
    with mock.patch(
        'webbrowser.open_new', side_effect=Exception('Browser not found')
    ):
        with mock.patch('webbrowser.get') as mock_get:
            # Mock successful chrome browser
            mock_browser = mock.MagicMock()
            mock_get.return_value = mock_browser

            start_karaoke.open_browser()

            # Should try to get chrome first
            mock_get.assert_called_with('chrome')
            mock_browser.open_new.assert_called_once_with(
                'http://localhost:5000/'
            )

            # Check console output
            captured = capsys.readouterr()
            assert 'Could not open default browser' in captured.out
            assert 'Successfully opened in chrome' in captured.out


def test_open_browser_tries_multiple_browsers(capsys):
    """Test that open_browser tries multiple browsers in order."""
    with mock.patch(
        'webbrowser.open_new', side_effect=Exception('Default failed')
    ):
        with mock.patch('webbrowser.get') as mock_get:
            # First two browsers fail, third succeeds
            def get_browser(name):
                if name in ['chrome', 'chromium']:
                    raise Exception(f'{name} not found')
                mock_browser = mock.MagicMock()
                return mock_browser

            mock_get.side_effect = get_browser

            start_karaoke.open_browser()

            # Should have tried chrome, chromium, and firefox
            assert mock_get.call_count >= 3
            captured = capsys.readouterr()
            assert 'Successfully opened in firefox' in captured.out


def test_open_browser_all_browsers_fail(capsys):
    """Test that open_browser prints helpful message when all browsers fail."""
    with mock.patch(
        'webbrowser.open_new', side_effect=Exception('Default failed')
    ):
        with mock.patch(
            'webbrowser.get', side_effect=Exception('No browser found')
        ):
            start_karaoke.open_browser()

            captured = capsys.readouterr()
            assert (
                'ERROR: Could not open browser automatically' in captured.out
            )
            assert 'http://localhost:5000/' in captured.out
            assert 'Google Chrome' in captured.out
            assert 'Mozilla Firefox' in captured.out
            assert 'Microsoft Edge' in captured.out


def test_open_browser_specific_browser_succeeds_after_some_fail():
    """Test that open_browser succeeds when a specific browser is found after others fail."""
    with mock.patch(
        'webbrowser.open_new', side_effect=Exception('Default failed')
    ):
        with mock.patch('webbrowser.get') as mock_get:

            def get_browser(name):
                if name in ['chrome', 'chromium', 'firefox']:
                    raise Exception(f'{name} not available')
                # mozilla succeeds
                if name == 'mozilla':
                    mock_browser = mock.MagicMock()
                    return mock_browser
                raise Exception(f'{name} not found')

            mock_get.side_effect = get_browser

            start_karaoke.open_browser()

            # mozilla should be tried and succeed
            calls = [call[0][0] for call in mock_get.call_args_list]
            assert 'mozilla' in calls


def test_main_script_entry_point():
    """Test that the module can be run as a script."""
    import importlib
    import sys

    # Create a proper mock that will be used when the module is reloaded
    with mock.patch('karoloke.start_karaoke.app.run'):
        with mock.patch('threading.Timer'):
            with mock.patch('os.makedirs'):
                # Remove the module from sys.modules to force a fresh import
                if 'karoloke.start_karaoke' in sys.modules:
                    del sys.modules['karoloke.start_karaoke']

                # Import and run as __main__
                try:
                    import runpy

                    with mock.patch('sys.argv', ['start_karaoke.py']):
                        runpy.run_module(
                            'karoloke.start_karaoke', run_name='__main__'
                        )
                except SystemExit:
                    pass

                # Re-import the module for future tests
                import karoloke.start_karaoke


def test_main_calls_app_run_with_correct_parameters():
    """Test that main() calls app.run() with the correct host, port, and debug settings."""
    with mock.patch('threading.Timer'):
        with mock.patch.object(start_karaoke.app, 'run') as mock_run:
            with mock.patch('os.makedirs'):
                start_karaoke.main()

                mock_run.assert_called_once_with(
                    host='0.0.0.0', port=5000, debug=True, use_reloader=False
                )


def test_main_starts_browser_timer():
    """Test that main() starts a timer to open the browser after 1 second."""
    with mock.patch('threading.Timer') as mock_timer:
        with mock.patch.object(start_karaoke.app, 'run'):
            with mock.patch('os.makedirs'):
                start_karaoke.main()

                mock_timer.assert_called_once_with(
                    1.0, start_karaoke.open_browser
                )
                mock_timer.return_value.start.assert_called_once()


def test_main_creates_directories_with_makedirs():
    """Test that main() uses os.makedirs with exist_ok=True."""
    with mock.patch('os.makedirs') as mock_makedirs:
        with mock.patch('threading.Timer'):
            with mock.patch.object(start_karaoke.app, 'run'):
                start_karaoke.main()

                # Should call makedirs for both directories
                assert mock_makedirs.call_count == 2
                calls = mock_makedirs.call_args_list
                # Check that exist_ok=True is used
                for call in calls:
                    assert call[1]['exist_ok'] is True
