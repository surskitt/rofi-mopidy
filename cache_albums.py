#!/usr/bin/env python

# python stdlib
import os
# internal packages
import options
import utils
import collectors
import auth


if __name__ == '__main__':
    opts = options.get_options()

    if 'spotify' in opts.source:
        spotify_auth_args = {'username': opts.spotify_username,
                             'client_id': opts.spotify_client_id,
                             'client_secret': opts.spotify_client_secret}
        sp = auth.get_spotify_client(**spotify_auth_args)
        sc = collectors.spotify.SpotifyCollector(sp)
        spotify_albums = sc.collect()

        utils.write_albums(opts.cache_dir, 'spotify', spotify_albums)

    if 'files' in opts.source:
        files_dir = os.path.expanduser(opts.files_dir)
        file_albums = collectors.files.collect(files_dir)

        utils.write_albums(opts.cache_dir, 'files', file_albums)
