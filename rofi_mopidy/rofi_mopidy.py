#!/usr/bin/env python

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

__version__ = '0.0.4'


def spotify_handler(opts):
    """ use client retrived using auth to collect albums using collector """

    # retrieve spotify authentication config args from options collector
    spotify_auth_args = {'username': opts.spotify_username,
                         'client_id': opts.spotify_client_id,
                         'client_secret': opts.spotify_client_secret}
    # use auth to create client object
    sp = auth.get_spotify_client(**spotify_auth_args)
    # create spotify collector with spotify client to collect albums
    sc = collectors.spotify.SpotifyCollector(sp)
    spotify_albums = sc.collect()

    return spotify_albums


def local_handler(opts):
    """ Collect albums from music dir in options using local collector """

    local_dir = os.path.expanduser(opts.local_dir)
    file_albums = collectors.local.collect(local_dir)

    return file_albums


def rofi_handler(music, sources, use_icons=False, row=0):
    """ Handle rofi using passed music list and display options """

    r = Rofi()
    # keys that can be used in rofi for different operations to be handled
    keys = {
        'key0': ('Return', 'Add'),
        'key1': ('Ctrl+i', 'Insert'),
        'key2': ('Alt+Return', 'Add...'),
        'key3': ('Alt+Ctrl+i', 'Insert...')
    }
    # If only one source is in use, set source name as prompt
    if len(sources) == 1:
        prompt = sources[0].capitalize()
    else:
        prompt = 'Music'

    # if the row arg is passed, set the initial current row
    args = '-i -selected-row {}'.format(row).split()

    # use nerdfont icons in rofi listings to show album/song source
    if use_icons:
        icons = {'file': '', 'spotify': ''}
        rows = ['{} {} - {}'.format(icons[i['type']], i['artist'], i['title'])
                for i in music]
    else:
        rows = ['{} - {}'.format(i['artist'], i['title']) for i in music]

    index, key = r.select(prompt, rows, rofi_args=args, **keys)

    return index, key


def mopidy_handler(selection, opts, cmd='add'):
    """ Parse uris from passed album/song and add to mopidy """

    # Create mpd client object and pass connection details from options
    client = MPDClient()
    client.connect(opts.mopidy_host, opts.mopidy_port)
    # if uri is in passed object, we have a spotify album or a single song
    if 'uri' in selection:
        client.add(selection['uri'])
    else:
        # if we don't have an album uri, add uris for all tracks separately
        for track in selection['tracks']:
            client.add(track['uri'])
    # if command was "insert", move all tracks from end to after current song
    if cmd == 'insert':
        # get either number of tracks if object has the key, or 1 if it doesn't
        count = len(selection.get('tracks') or 'a')
        # get position after current and length of playlist from status dict
        status = client.status()
        next_pos = int(status['song']) + 1
        pl_len = int(status['playlistlength'])
        # use mpd move {START:END} {TO} to move new tracks to after current
        client.move('{}:{}'.format(pl_len - count, pl_len), next_pos)


def main():
    """ Main execution method, called by all endpoints """

    # retrieve options set in either command line args or config file
    opts = options.get_options()

    # If the refresh option is set, refresh cache, otherwise read existing
    if opts.refresh:
        # dict containing results of all collectors passed in the source option
        handlers = {'spotify': spotify_handler, 'local': local_handler}
        albums_dict = {k: handlers[k](opts) for k in opts.source}

        # write each collected list to its cache file
        for k, v in albums_dict.items():
            utils.write_albums(opts.cache_dir, k, v)

        # exit once refresh complete if option passed
        if opts.no_rofi:
            sys.exit()
    else:
        # dictionary containing albums for each file defined in source option
        albums_dict = {k: utils.load_albums(opts.cache_dir, k)
                       for k in opts.source}

    # flatten dict into one list of albums from all sources
    music = [i for s in albums_dict.values() for i in s]
    # if songs mode is set, further flatten list of albums to list of songs
    if opts.mode == 'songs':
        music = [i for s in music for i in s['tracks']]
    # sort our list of albums/songs using key set in options
    music = sorted(music, key=lambda x: x[opts.sorting], reverse=opts.reverse)

    # index initially set to 0 so first row is shown
    index = 0
    # continue to show rofi window while continue shortcuts are used
    while True:
        index, key = rofi_handler(music, opts.source, opts.use_icons, index)

        # if index is -1, user either cancelled or picked an invalid entry
        if index > -1:
            selection = music[index]
            # 0 or 2 = mpd add command, 1 or 3 = mpd insert command
            if key in (0, 2):
                mopidy_handler(selection, opts, 'add')
            else:
                mopidy_handler(selection, opts, 'insert')

        # -1 = user escaped rofi, 0 or 1 = user picked add without continue
        if key in (-1, 0, 1):
            # break out of while loop
            break


if __name__ == '__main__':
    main()
