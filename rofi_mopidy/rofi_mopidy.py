#!/usr/bin/env python

__version__ = '0.0.4'

# python stdlib
import os
import sys
# pip installed
from rofi import Rofi
from mpd import MPDClient
# internal packages
from . import options
from . import utils
from . import collectors
from . import auth


def spotify_handler(opts):
    spotify_auth_args = {'username': opts.spotify_username,
                         'client_id': opts.spotify_client_id,
                         'client_secret': opts.spotify_client_secret}
    sp = auth.get_spotify_client(**spotify_auth_args)
    sc = collectors.spotify.SpotifyCollector(sp)
    spotify_albums = sc.collect()

    return spotify_albums

def local_handler(opts):
    local_dir = os.path.expanduser(opts.local_dir)
    file_albums = collectors.local.collect(local_dir)

    return file_albums

def rofi_handler(music, sources, use_icons=False, row=0):
    r = Rofi()
    keys = {
        'key0': ('Return', 'Add'),
        'key1': ('Ctrl+i', 'Insert'),
        'key2': ('Alt+Return', 'Add...'),
        'key3': ('Alt+Ctrl+i', 'Insert...')
    }
    if len(sources) == 1:
        prompt = sources[0].capitalize()
    else:
        prompt = 'Music'
    args = '-i -selected-row {}'.format(row).split()

    if use_icons:
        icons = {'file': '', 'spotify': ''}
        rows = ['{} {} - {}'.format(icons[i['type']], i['artist'], i['title'])
                for i in music]
    else:
        rows = ['{} - {}'.format(i['artist'], i['title']) for i in music]

    index, key = r.select(prompt, rows, rofi_args=args, **keys)

    return index, key

def mopidy_handler(selection, opts, cmd='add'):
    client = MPDClient()
    client.connect(opts.mopidy_host, opts.mopidy_port)
    if 'uri' in selection:
        client.add(selection['uri'])
    else:
        for track in selection['tracks']:
            client.add(track['uri'])
    if cmd == 'insert':
        count = len(selection.get('tracks') or 'a')
        status = client.status()
        next_pos = int(status['song']) + 1
        pl_len = int(status['playlistlength'])
        client.move('{}:{}'.format(pl_len - count, pl_len), next_pos)

def main():
    opts = options.get_options()

    if opts.refresh:
        handlers = {'spotify': spotify_handler, 'local': local_handler}

        albums_dict = {k: handlers[k](opts) for k in opts.source}

        for k, v in albums_dict.items():
            utils.write_albums(opts.cache_dir, k, v)

        if opts.no_rofi:
            sys.exit()
    else:
        albums_dict = {k: utils.load_albums(opts.cache_dir, k)
                       for k in opts.source}

    music = [i for s in albums_dict.values() for i in s]
    if opts.mode == 'songs':
        music = [i for s in music for i in s['tracks']]
    music = sorted(music, key=lambda x: x[opts.sorting], reverse=opts.reverse)

    index = 0
    while True:
        index, key = rofi_handler(music, opts.source, opts.use_icons, index)

        if index > -1:
            selection = music[index]
            if key in (0, 2):
                mopidy_handler(selection, opts, 'add')
            else:
                mopidy_handler(selection, opts, 'insert')

        if key in (-1, 0, 1):
            break


if __name__ == '__main__':
    main()
