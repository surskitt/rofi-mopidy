import re
from setuptools import setup

version = re.search(
    '^__version__\s*=\s*\'(.*)\'',
    open('rofi_mopidy/rofi_mopidy.py').read(),
    re.M
    ).group(1)

with open("README.md", "rb") as f:
    long_descr = f.read().decode("utf-8")

setup(
    name = "rofi-mopidy",
    packages = ["rofi_mopidy", "rofi_mopidy.collectors", "rofi_mopidy.auth"],
    install_requires=[
        'ConfigArgParse',
        'python-mpd2',
        'spotipy',
        'tinytag',
        'python-rofi'
    ],
    dependency_links=['https://github.com/bcbnz/python-rofi.git@d20b3a2ba4ba1b294b002f25a8fb526c5115d0d4#egg=python_rofi'],
    entry_points = {
        "console_scripts": ['rofi-mopidy = rofi_mopidy.rofi_mopidy:main']
        },
    version = version,
    description = "Add spotify and local albums to current mopidy playlist using rofi",
    long_description = long_descr,
    author = "Shane Donohoe",
    author_email = "donohoe.shane@gmail.com",
    url = "https://github.com/sharktamer/rofi-mopidy",
    )
