import os
import pathlib
import random

import pytest

from karoloke.jukebox_controller import (
    calculate_average_score,
    get_background_img,
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


def test_calculate_average_score_initial_zero():
    # When current_average is zero, should return new_score
    assert calculate_average_score(0, 80) == 80


def test_calculate_average_score_regular_case():
    # Should return the integer average of current_average and new_score
    assert calculate_average_score(70, 90) == 80


def test_calculate_average_score_negative_scores():
    # Should handle negative scores correctly
    assert calculate_average_score(-10, 10) == 0


def test_calculate_average_score_float_scores():
    # Should work with float inputs and return int
    assert calculate_average_score(75.5, 84.5) == int((75.5 + 84.5) / 2)


def test_calculate_average_score_large_numbers():
    # Should handle large numbers
    assert calculate_average_score(1000000, 2000000) == 1500000
