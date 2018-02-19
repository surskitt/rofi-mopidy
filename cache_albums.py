#!/usr/bin/env python

import sys
import json
import os
import argparse
from configparser import ConfigParser, NoOptionError
import spotipy
import spotipy.util

# Set defaults for config and output
user_home = os.environ.get('HOME')
default_cfg = '{}/.config/rofi-mopidy-spotify/api.conf'.format(user_home)
default_cache_dir = '{}/.cache/rofi-mopidy-spotify'.format(user_home)
default_api_cache = '{}/spotify_api.json'.format(default_cache_dir)
default_output = '{}/spotify_albums.json'.format(default_cache_dir)

# Parse command line overrides if given
parser = argparse.ArgumentParser(description='Spotify album cache store')
parser.add_argument('-c', dest='config', default=default_cfg,
                    help='config file')
parser.add_argument('-C', dest='cache', default=default_api_cache,
                    help='api cache file')
parser.add_argument('-o', dest='output', default=default_output,
                    help='album output file')
args = parser.parse_args()
config_file = args.config
default_api_cache = args.cache
output_file = args.output

# Just in case cache dir does not exist, create it
if not os.path.exists(os.path.dirname(default_api_cache)):
    os.makedirs(os.path.dirname(default_api_cache))

# Just in case output dir does not exist, create it
if not os.path.exists(os.path.dirname(output_file)):
    os.makedirs(os.path.dirname(output_file))

# Open config file
config = ConfigParser()
try:
    config.readfp(open(config_file))
except FileNotFoundError:
    print('Error: {} not found'.format(config_file), file=sys.stderr)
    sys.exit(1)

# Parse config file, reading values into dict
try:
    api = {
        'username': config.get('api', 'username'),
        'client_id': config.get('api', 'client_id'),
        'client_secret': config.get('api', 'client_secret'),
        'redirect_uri': config.get('api', 'redirect_uri'),
        'scope': 'user-library-read',
        'cache_path': default_api_cache
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
if os.path.exists(output_file):
    os.remove(output_file)

# Function for writing albums from api to file
def get_albums(results):
    offset = results['offset']
    count = len(results['items'])
    print('Collecting albums {}-{}'.format(offset, offset + count))

    for item in results['items']:
        yield {'artist': ', '.join(i['name'] for i in item['album']['artists']),
               'name': item['album']['name'],
               'uri': item['album']['uri'],
               'date_added': item['added_at']}

sp = spotipy.Spotify(auth=token)
results = sp.current_user_saved_albums(limit=50)
with open(output_file, 'w') as f:
    #  writer = csv.writer(f)
    albums = [i for i in get_albums(results)]
    while results['next']:
        results = sp.next(results)
        albums += [i for i in get_albums(results)]
    print('Writing albums to {}'.format(output_file))
    json.dump(albums, f)
