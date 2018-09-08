#!/usr/bin/env python

from os import environ
from os.path import expanduser
import configargparse


def get_options():
    conf_root = environ.get('XDG_CONFIG_HOME') or '~/.config'
    cache_root = environ.get('XDG_CACHE_HOME') or expanduser('~/.cache')
    conf_files = '{}/rofi-mopidy/*.yml'.format(conf_root)
    cache_dir = '{}/rofi-mopidy'.format(cache_root)

    p = configargparse.Parser(default_config_files=[conf_files])

    # general options
    p.add('--config', '-c', is_config_file=True, help='config file path')
    p.add('--cache_dir', '-C', default=cache_dir, help='app cache dir')
    p.add('--source', '-s', action='append', required=True,
          choices=['files', 'spotify'],
          help='different sources to scan/display')
    p.add('--mode', '-m', choices=['albums', 'songs'], default='albums',
          help='whether to show albums or songs in rofi')
    p.add('--refresh', '-r', action='store_true', default=False,
          help='refresh album cache')
    p.add('--sorting', required=True,
          choices=['mtime', 'artist', 'album'], default='mtime',
          help='key to sort rofi listing on')
    p.add('--use_icons', '-i', action='store_true',
          help='use nerdfont icons in rofi')

    # files source options
    p.add('--files_dir', help='music files directory')

    # spotify source options
    p.add('--spotify_username', help='spotify username')
    p.add('--spotify_client_id', help='spotify client id')
    p.add('--spotify_client_secret', help='spotify secret')

    options = p.parse()

    if 'files' in options.source and not options.files_dir:
        p.error('use of files source requires files_dir to be set')

    spotify_options = (options.spotify_username,
                       options.spotify_client_id,
                       options.spotify_client_secret)
    if 'spotify' in options.source and not all(spotify_options):
        p.error('use of spotify source requires api options to be set')

    return options
