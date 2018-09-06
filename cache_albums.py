#!/usr/bin/env python

import sys
import json
import os
import argparse
from configparser import ConfigParser, NoOptionError
import spotipy
import spotipy.util
import time

# Set defaults for config and output
cfgfile = os.path.expanduser('~/.config/rofi-mopidy-spotify/api.conf')
api_cache = os.path.expanduser('~/.cache/rofi-mopidy-spotify/spotify_api.json')
output = os.path.expanduser('~/.cache/rofi-mopidy-spotify/spotify_albums.json')

# Parse command line overrides if given
parser = argparse.ArgumentParser(description='Spotify album cache store')
parser.add_argument('-c', dest='cfgfile', default=cfgfile,
                    help='config file')
parser.add_argument('-C', dest='api_cache', default=api_cache,
                    help='api cache file')
parser.add_argument('-o', dest='output', default=output,
                    help='album output file')
args = parser.parse_args()
cfgfile = args.cfgfile
api_cache = args.api_cache
output = args.output

# Just in case cache dir does not exist, create it
if not os.path.exists(os.path.dirname(api_cache)):
    os.makedirs(os.path.dirname(api_cache))

# Just in case output dir does not exist, create it
if not os.path.exists(os.path.dirname(output)):
    os.makedirs(os.path.dirname(output))

# Open config file
config = ConfigParser()
try:
    config.readfp(open(cfgfile))
except FileNotFoundError:
    print('Error: {} not found'.format(cfgfile), file=sys.stderr)
    sys.exit(1)

# Parse config file, reading values into dict
try:
    api = {
        'username': config.get('api', 'username'),
        'client_id': config.get('api', 'client_id'),
        'client_secret': config.get('api', 'client_secret'),
        'redirect_uri': config.get('api', 'redirect_uri'),
        'scope': 'user-library-read',
        #'cache_path': api_cache
    }
except NoOptionError as err:
    print('Error: Missing values in api.conf', file=sys.stderr)
    print(err, file=sys.stderr)
    sys.exit(1)

# Receive a token using spotipy library, prompting user for login if needed
token = spotipy.util.prompt_for_user_token(**api)
if not token:
    print('Error: token not received', file=sys.stderr)
    sys.exit(1)

# If the output file already exists, delete it
if os.path.exists(output):
    os.remove(output)

def results_gen(r):
    while r:
        for i in r['items']:
            yield i
        r = sp.next(r)

def dt_to_mtime(dt):
    pattern = '%Y-%m-%dT%H:%M:%SZ'

    return int(time.mktime(time.strptime(dt, pattern)))

def track_to_dict(t, albumartist, album, mtime):
    artist = ', '.join(i['name'] for i in t['artists'])
    track = float('{}.{}'.format(t['disc_number'], t['track_number']))
    title =  t['name']
    uri = t['uri']
    mtime = mtime

    return {'artist': artist,
            'albumartist': albumartist,
            'album': album,
            'track': track,
            'title': title,
            'uri': uri,
            'mtime': mtime,
            'type': 'spotify'}

def album_to_dict(a):
    aa = a['album']
    artist = ', '.join(i['name'] for i in aa['artists'])
    album = aa['name']
    mtime = dt_to_mtime(a['added_at'])
    tracks = [track_to_dict(i, artist, album, mtime)
              for i in results_gen(aa['tracks'])]
    uri = aa['uri']

    return {'artist': artist,
            'album': album,
            'mtime': mtime,
            'tracks': tracks,
            'type': 'spotify',
            'uri': uri}

sp = spotipy.Spotify(auth=token)
results = sp.current_user_saved_albums(limit=50)

albums = [album_to_dict(i) for i in results_gen(results)]

with open(output, 'w') as f:
    json.dump(albums, f)
