from pathlib import PurePath
from typing import Dict, Tuple

from download import download


def _get_filename(url):
    """Extract the filename from a URL by looking for the string after the last slash

    Parameters
    ----------
    url : str
        the url to extract the filename from
    Returns
    -------
    str
        the filename in the download URL provided
    """
    return url.split("/")[-1]


def _get_urls() -> Dict[str, str]:
    """The URLs of the files we use for our audio feedback and their purpose

    Returns
    -------
    Dict[str, str]
        the URLs for all those wavs with their purpose as key as one of:

        - beep: the countdown for each exercise to start on point
        - start: begin of an exercise
        - end: end of an exercise
        - finish: final ending signal
    """
    return {
        "beep": "http://tastyspleen.net/~quake2/baseq2/sound/world/clock.wav",
        "ignition": "http://billor.chsh.chc.edu.tw/sound/rocket.wav",
        "running": "https://www.soundjay.com/human/heartbeat-04.wav",
        "end": "https://www.wavsource.com/snds_2020-06-10_7014036401687385/sfx"
        "/boxing_bell.wav",
        "finish": "https://www.wavsource.com/snds_2020-06-10_7014036401687385/sfx"
        "/applause2_x.wav",
    }


def download_file(
    url: str,
    save_to_folder: PurePath = PurePath(".//audio//"),
    overwrite: bool = False,
    filename: str = None,
) -> None:
    """Download a file from a given URL to a given location

    Parameters
    ----------
    save_to_folder : PurePath
        local filesystem path to a folder in which the files will be stored (defaults
        to ./audio) from the working directory
    url : str
        URL of the file to download
    overwrite : bool, optional
        if False (default) and the file is already present it does not get downloaded
        again, if True the download overwrites the possibly present file
    filename : str, optional
        the local name of the downloaded file (default is the download's filename)
    """
    if filename is None:
        filename = _get_filename(url)
    save_to_folder = save_to_folder.joinpath(filename)
    return download(url, save_to_folder, replace=overwrite)


def download_audio_files(
    urls: Dict[str, str],
    save_to_folder: PurePath = PurePath(".//audio//"),
    overwrite: bool = False,
) -> PurePath:
    """Download files from a given list of URLs to a given location

    Parameters
    ----------
    urls : str
        URL of the file to download
    save_to_folder : str
        local filesystem path to a folder in which the files will be stored (defaults
        to ./audio) from the working directory
    overwrite : bool, optional
        if False (default) and the file is already present it does not get downloaded
        again, if True the download overwrites the possibly present file"""
    for url in urls.values():
        download_file(url=url, save_to_folder=save_to_folder, overwrite=overwrite)
    return save_to_folder


if __name__ == "__main__":
    download_audio_files(_get_urls())
