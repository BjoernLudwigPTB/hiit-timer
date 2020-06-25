import os
from os.path import exists
from pathlib import PurePath

import pytest

from intervaltimer.initialize import (
    download_audio_files,
    download_file,
    _get_filename,
    _get_urls,
)


@pytest.fixture
def url():
    return _get_urls()["end"]


@pytest.fixture(autouse=True, scope="module")
def module_setup_teardown(tmpdir_factory):
    """Delete the temporary folder created for the audio file downloads."""
    yield
    try:
        print(f"Attempt to delete temporary folder '{tmpdir_factory.getbasetemp()}'...")
        tmpdir_factory.getbasetemp().remove()
        print(f"Deleted temporary folder '{tmpdir_factory.getbasetemp()}'.")
    except FileNotFoundError:
        print(f"Could not delete folder '{tmpdir_factory.getbasetemp()}'.")


def test_download_file_without_provided_filename(url, tmpdir):
    """Check download of a file given any one of the provided URLs."""
    assert download_file(url, save_to_folder=PurePath(tmpdir))


def test_download_file_with_provided_filename(url, tmpdir):
    """Check download of a named file given any one of the provided URLs and the
    existence afterwards."""
    filename = "my_test"
    assert download_file(url, save_to_folder=PurePath(tmpdir), filename=filename)
    assert exists(PurePath(tmpdir).joinpath(filename))


def test_download_file_with_positional_path_overwrite(url, tmpdir):
    """Check download of a named file given any one of the provided URLs and
    positional arguments' call."""
    filename = "my_test"
    assert download_file(url, PurePath(tmpdir), False, filename=filename)
    assert exists(PurePath(tmpdir).joinpath(filename))


def test_get_urls_type():
    """Check for return type."""
    urls = _get_urls()
    assert isinstance(urls, dict)
    for key, value in urls.items():
        assert isinstance(key, str)
        assert isinstance(value, str)


def test_get_filename_type(url):
    """Check for return type."""
    assert isinstance(_get_filename(url), str)


def test_get_filename():
    """Check for return type."""
    path = "test/"
    filename = "something.audio"
    assert _get_filename(f"{path}{filename}") == filename
