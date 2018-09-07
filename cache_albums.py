#!/usr/bin/env python

import sys
import json
import os
from configparser import ConfigParser, NoOptionError
import spotipy
import spotipy.util
import collectors
import options

args = options.args

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

sp = spotipy.Spotify(auth=token)
sc = collectors.SpotifyCollector(sp)
spotify_albums = sc.collect()

with open(output, 'w') as f:
    json.dump(spotify_albums, f)
