#!/usr/bin/env python

# python stdlib
import json
import os
# internal packages
import options
import collectors
import auth


def write_albums(cache_dir, filename, *albums):
    if not os.path.exists(cache_dir):
        os.makedirs(cache_dir)

    # flatten all albums lists into one list for writing
    aalbums = [i for s in albums for i in s]

    output = '{}/{}.json'.format(cache_dir, filename)
    with open(output, 'w') as f:
        json.dump(aalbums, f, indent=4)


if __name__ == '__main__':
    opts = options.get_options()

    if 'spotify' in opts.source:
        spotify_auth_args = {'username': opts.spotify_username,
                             'client_id': opts.spotify_client_id,
                             'client_secret': opts.spotify_client_secret}
        sp = auth.get_spotify_client(**spotify_auth_args)
        sc = collectors.SpotifyCollector(sp)
        spotify_albums = sc.collect()

        write_albums(opts.cache_dir, 'spotify', spotify_albums)

    if 'files' in opts.source:
        files_dir = os.path.expanduser(opts.files_dir)
        file_albums = collectors.files_collect(files_dir)

        write_albums(opts.cache_dir, 'files', file_albums)
