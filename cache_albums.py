#!/usr/bin/env python

# python stdlib
import sys
import json
import os
# internal packages
import collectors
import options
import auth

#  if not os.path.exists(args.cache_dir):
    #  os.makedirs(args.cache_dir)

if __name__ == '__main__':
    args = options.args
    config = options.config

    try:
        username = config.get('api', 'username')
        client_id = config.get('api', 'client_id')
        client_secret = config.get('api', 'client_secret')
    except NoOptionError as err:
        print('Error: Missing values in api.conf', file=sys.stderr)
        print(err, file=sys.stderr)
        sys.exit(1)

    sp = auth.get_spotify_client(username, client_id, client_secret)
    sc = collectors.SpotifyCollector(sp)
    spotify_albums = sc.collect()

    output = '{}/spotify_albums.json'.format(args.cache_dir)
    with open(output, 'w') as f:
        json.dump(spotify_albums, f)
