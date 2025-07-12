import pytest
import os
import random

from karoloke.jukebox_controller import get_background_img
import pathlib

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
