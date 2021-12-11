# -*- coding: utf-8 -*-

import os
from io import BytesIO

import pytest
from PIL import Image

from PyPDFForm.core.image import Image as ImageCore


@pytest.fixture
def pdf_samples():
    return os.path.join(os.path.dirname(__file__), "..", "..", "pdf_samples")


@pytest.fixture
def image_samples():
    return os.path.join(os.path.dirname(__file__), "..", "..", "image_samples")


@pytest.fixture
def image_stream(image_samples):
    with open(os.path.join(image_samples, "sample_image.jpg"), "rb+") as f:
        return f.read()


@pytest.fixture
def before_converted(image_samples):
    with open(os.path.join(image_samples, "before_converted.png"), "rb+") as f:
        return f.read()


@pytest.fixture
def after_converted(image_samples):
    with open(os.path.join(image_samples, "after_converted.jpg"), "rb+") as f:
        return f.read()


@pytest.fixture
def after_converted_linux(image_samples):
    with open(os.path.join(image_samples, "after_converted_linux.jpg"), "rb+") as f:
        return f.read()


def test_is_image(image_stream):
    assert not ImageCore().is_image(b"bad_stream")
    assert ImageCore().is_image(image_stream)


def test_rotate_image(image_stream):
    rotated = ImageCore().rotate_image(image_stream, 180)

    assert rotated != image_stream

    buff = BytesIO()
    buff.write(image_stream)
    buff.seek(0)

    rotated_buff = BytesIO()
    rotated_buff.write(rotated)
    rotated_buff.seek(0)

    assert Image.open(buff).format == Image.open(rotated_buff).format

    buff.close()
    rotated_buff.close()


def test_any_image_to_jpg(before_converted, after_converted, after_converted_linux):
    _converted = ImageCore().any_image_to_jpg(before_converted)
    assert len(_converted) == (
        len(after_converted) if os.name == "nt" else len(after_converted_linux)
    )
    assert _converted == (after_converted if os.name == "nt" else after_converted_linux)
