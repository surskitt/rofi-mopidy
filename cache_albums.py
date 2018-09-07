#!/usr/bin/env python

# python stdlib
import json
import os
# internal packages
import collectors
import options
import auth


def write_albums(cache_dir, *albums):
    if not os.path.exists(cache_dir):
        os.makedirs(cache_dir)

    # flatten all albums lists into one list for writing
    aalbums = [i for s in albums for i in s]

    output = '{}/albums.json'.format(cache_dir)
    with open(output, 'w') as f:
        json.dump(aalbums, f)


if __name__ == '__main__':
    options = options.get_options()

    spotify_auth_args = {'username': options.spotify_username,
                         'client_id': options.spotify_client_id,
                         'client_secret': options.spotify_client_secret}
    sp = auth.get_spotify_client(**spotify_auth_args)
    sc = collectors.SpotifyCollector(sp)
    spotify_albums = sc.collect()

    write_albums(spotify_albums)
