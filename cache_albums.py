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
conf_dir = os.path.expanduser('~/.config/rofi-mopidy-spotify')
cache_dir = os.path.expanduser('~/.cache/rofi-mopidy-spotify')

# Parse command line overrides if given
parser = argparse.ArgumentParser(description='Spotify album cache store')
parser.add_argument('-c', dest='conf_dir', default=conf_dir,
                    help='config dir')
parser.add_argument('-C', dest='cache_dir', default=cache_dir,
                    help='cache dir')
args = parser.parse_args()

for i in (args.conf_dir, args.cache_dir):
    if not os.path.exists(i):
        os.makedirs(i)

cfgfile = '{}/api.conf'.format(args.conf_dir)
output = '{}/spotify_albums.json'.format(args.cache_dir)
api_cache = '{}/spotify_api.json'.format(args.cache_dir)

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


class SpotifyCollector():
    def __init__(self, sp):
        self.sp = sp


    def __results_gen(self, r):
        while r:
            for i in r['items']:
                yield i
            r = sp.next(r)

    def __dt_to_mtime(self, dt):
        pattern = '%Y-%m-%dT%H:%M:%SZ'

        return int(time.mktime(time.strptime(dt, pattern)))

    def album_to_dict(self, a):
        aa = a['album']
        artist = ', '.join(i['name'] for i in aa['artists'])
        album = aa['name']
        mtime = self.__dt_to_mtime(a['added_at'])
        tracks = [self.track_to_dict(i, artist, album, mtime)
                  for i in self.__results_gen(aa['tracks'])]
        uri = aa['uri']

        return {'artist': artist,
                'album': album,
                'mtime': mtime,
                'tracks': tracks,
                'type': 'spotify',
                'uri': uri}

    def track_to_dict(self, t, albumartist, album, mtime):
        artist = ', '.join(i['name'] for i in t['artists'])
        track = float('{}.{}'.format(t['disc_number'], t['track_number']))
        title = t['name']
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

    def collect(self):
        results = sp.current_user_saved_albums(limit=50)
        albums = [self.album_to_dict(i) for i in self.__results_gen(results)]

        return albums

sp = spotipy.Spotify(auth=token)
sc = SpotifyCollector(sp)
spotify_albums = sc.collect()

with open(output, 'w') as f:
    json.dump(spotify_albums, f)
