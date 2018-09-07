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
    p.add('-c', '--config', is_config_file=True, help='config file path')
    p.add('--cache_dir', '-C', default=cache_dir, help='app cache dir')
    p.add('--source', '-s', action='append', required=True,
          help='different sources to scan/display')
    p.add('--mode', '-m', default='albums')
    p.add('--refresh', '-r', action='store_true',
          help='refresh album cache')
    p.add('--use_icons', '-i', action='store_true',
          help='use nerdfont icons in rofi')

    # spotify source options
    p.add('--spotify_username', help='spotify username')
    p.add('--spotify_client_id', help='spotify client id')
    p.add('--spotify_client_secret', help='spotify secret')

    # files source options
    p.add('--files-dir', help='music files directory')

    options = p.parse()
    return options
