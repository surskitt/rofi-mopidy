#!/usr/bin/env python

# python stdlib
import os
# internal packages
import options
import utils
import collectors
import auth


def spotify_handler(opts):
    spotify_auth_args = {'username': opts.spotify_username,
                         'client_id': opts.spotify_client_id,
                         'client_secret': opts.spotify_client_secret}
    sp = auth.get_spotify_client(**spotify_auth_args)
    sc = collectors.spotify.SpotifyCollector(sp)
    spotify_albums = sc.collect()

    return spotify_albums

def files_handler(opts):
    files_dir = os.path.expanduser(opts.files_dir)
    file_albums = collectors.files.collect(files_dir)

    return file_albums

def main():
    opts = options.get_options()

    if opts.refresh:
        handlers = {'spotify': spotify_handler, 'files': files_handler}

        albums_dict = {k: handlers[k](opts) for k in opts.source}

        for k, v in albums_dict.items():
            utils.write_albums(opts.cache_dir, k, v)
    else:
        albums_dict = {k: utils.load_albums(opts.cache_dir, k)
                       for k in opts.source}

    albums = [i for s in albums_dict.values() for i in s]

if __name__ == '__main__':
    main()
