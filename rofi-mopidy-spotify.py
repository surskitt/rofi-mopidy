#!/usr/bin/env python

import argparse
from os.path import expanduser
import json
import sys
from subprocess import Popen, PIPE

# Parse command line arguments to get user options
def get_args():
    parser = argparse.ArgumentParser(description='Spotify album cache store')

    # Optionally override default spotify album cache location
    albums_file = expanduser('~/.cache/rofi-mopidy-spotify/spotify_albums.json')
    parser.add_argument('-f', dest='albums_file', default=albums_file,
                        help='Albums json file')

    # Sort rofi output by artist, album or date
    sort_fields = ['artist', 'album', 'date']
    parser.add_argument('-s', dest='sorting', choices=sort_fields,
                        default='album', help='Sort rofi output')

    # Return parsed arguments
    return parser.parse_args()

# Open given json file, sorted by given field
def get_json(albums_file, sorting):
    with open(albums_file) as f:
        return sorted(json.load(f), key=lambda x: x[sorting],
                      reverse=(sorting == 'date'))

# Get album names from json file
def get_albums(j):
    return '\n'.join('{} - {}'.format(i['artist'], i['album']) for i in j)

# Get uri of album at given index
def get_uri(j, index):
    return j[index]['uri']

# Call rofi, returning output and return code
def call_rofi(albums):
    rofi_cmd = 'rofi -dmenu -p Spotify -i -no-custom -format i'.split()
    caller = Popen(args=rofi_cmd, stdin=PIPE, stdout=PIPE)

    stdout, stderr = caller.communicate(input=albums.encode())
    return (stdout, stderr, caller.returncode)

# Add given uri to mpd playlist using mpc (TODO: use mopidy through python)
def add_uri(uri):
    Popen(args='mpc add {}'.format(uri).split())

def main():
    args = get_args()

    j = get_json(args.albums_file, args.sorting)
    albums = get_albums(j)

    stdout, stderr, code = call_rofi(albums)

    if code == 1:
        sys.exit()
    else:
        uri = get_uri(j, int(stdout))
        add_uri(uri)

if __name__ == '__main__':
    main()
