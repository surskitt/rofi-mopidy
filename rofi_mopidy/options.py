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
    p.add('--cache-dir', '-C', default=cache_dir, help='app cache dir')
    p.add('--source', '-s', action='append', required=True,
          choices=['local', 'spotify'],
          help='different sources to scan/display')
    p.add('--mode', '-m', choices=['albums', 'songs'], default='albums',
          help='whether to show albums or songs in rofi')
    p.add('--refresh', '-r', action='store_true', default=False,
          help='refresh album cache')
    p.add('--sorting', 
          choices=['mtime', 'artist', 'album', 'title'], default='title',
          help='key to sort rofi listing on')
    p.add('--reverse', action='store_true', default=False,
          help='sort rofi entries in reverse')

    # local source options
    p.add('--local-dir', help='local music directory')

    # spotify source options
    p.add('--spotify-username', help='spotify username')
    p.add('--spotify-client-id', help='spotify client id')
    p.add('--spotify-client-secret', help='spotify secret')

    # rofi options
    p.add('--no-rofi', action='store_true', default=False,
          help='don\'t show rofi (only works with -r)')
    p.add('--use-icons', '-i', action='store_true', default=False,
          help='use nerdfont icons in rofi')

    # mopidy options
    p.add('--mopidy-host', default='localhost',
          help='host that the mopidy server is running at')
    p.add('--mopidy-port', default=6600, type=int,
          help='port that the mopidy server is running on')

    options = p.parse()

    if 'local' in options.source and not options.local_dir:
        p.error('use of local source requires local-dir to be set')

    spotify_options = (options.spotify_username,
                       options.spotify_client_id,
                       options.spotify_client_secret)
    if 'spotify' in options.source and not all(spotify_options):
        p.error('use of spotify source requires api options to be set')

    return options
