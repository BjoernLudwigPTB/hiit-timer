from setuptools import find_packages, setup
from intervaltimer import __version__ as version


with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="intervaltimer",
    version=version,
    author="Björn Ludwig",
    author_email="bjoern.ludwig@ptb.de",
    description="A timer for interval training",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/BjoernLudwigPTB/intervaltimer",
    packages=find_packages(),
    install_requires=["simpleaudio", "download"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
