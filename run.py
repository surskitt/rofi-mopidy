#!/usr/bin/env python

# python stdlib
import os
import sys
# pip installed
from rofi import Rofi
from mpd import MPDClient
# internal packages
import options
import utils
import collectors
import auth


def spotify_handler(opts):
    spotify_auth_args = {'username': opts.spotify_username,
                         'client_id': opts.spotify_client_id,
                         'client_secret': opts.spotify_client_secret}
    sp = auth.get_spotify_client(**spotify_auth_args)
    sc = collectors.spotify.SpotifyCollector(sp)
    spotify_albums = sc.collect()

    return spotify_albums

def files_handler(opts):
    files_dir = os.path.expanduser(opts.files_dir)
    file_albums = collectors.files.collect(files_dir)

    return file_albums

def rofi_handler(music, sources, row=0):
    r = Rofi()
    if len(sources) == 1:
        prompt = sources[0].capitalize()
    else:
        prompt = 'Music'

    rows = ['{} - {}'.format(i['artist'], i['title']) for i in music]
    args = '-i -selected-row {}'.format(row).split()

    index, key = r.select(prompt.capitalize(), rows, rofi_args=args)

    return index, key

def mpd_handler(selection, opts, cmd='add'):
    client = MPDClient()
    client.connect(opts.mopidy_host, opts.mopidy_port)
    if 'uri' in selection:
        client.add(entry['uri'])
    else:
        for track in selection['tracks']:
            client.add(track['uri'])

def main():
    opts = options.get_options()

    if opts.refresh:
        handlers = {'spotify': spotify_handler, 'files': files_handler}

        albums_dict = {k: handlers[k](opts) for k in opts.source}

        for k, v in albums_dict.items():
            utils.write_albums(opts.cache_dir, k, v)
    else:
        albums_dict = {k: utils.load_albums(opts.cache_dir, k)
                       for k in opts.source}

    music = [i for s in albums_dict.values() for i in s]
    if opts.mode == 'songs':
        music = [i for s in music for i in s['tracks']]
    music = sorted(music, key=lambda x: x[opts.sorting])

    index, key = rofi_handler(music, opts.source)

    selection = music[index]

    mpd_handler(selection, opts)


if __name__ == '__main__':
    main()
