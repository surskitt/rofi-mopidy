import os
import json
import sys
import urllib.request
import shutil


def write_albums(cache_dir, filename, *albums):
    """ write given albums list using given cache_dir and filename """

    if not os.path.exists(cache_dir):
        os.makedirs(cache_dir)

    # flatten all albums lists into one list for writing
    aalbums = [i for s in albums for i in s]

    output = '{}/{}.json'.format(cache_dir, filename)
    with open(output, 'w') as f:
        json.dump(aalbums, f, indent=4)


def load_albums(cache_dir, filename):
    """ load albums from cache, raising exception if file does not exist  """

    iput = '{}/{}.json'.format(cache_dir, filename)
    try:
        with open(iput) as f:
            albums = json.load(f)
    except FileNotFoundError:
        print('ERROR: {} cache not found, use -r to create'.format(filename),
              file=sys.stderr)
        sys.exit(1)

    return albums


def get_cache_fn(cache_dir, fn):
    """ If fn is a url then return, if filename then prepend dir """

    if os.path.basename(fn) == fn:
        return os.path.join(cache_dir, fn)
    else:
        return fn


def download_url(url, fn):
    """ Download given url as given filename """

    dest_dir = os.path.dirname(fn)
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)

    with urllib.request.urlopen(url) as response, open(fn, 'wb') as f:
        data = response.read()
        f.write(data)


def cache_art(cache_dir, albums):
    """ download any album art in list to cache dir """

    art_dir = os.path.join(cache_dir, 'art')
    for a in albums:
        if 'art_url' in a:
            fn = get_cache_fn(art_dir, a['art_fn'])
            download_url(a['art_url'], fn)
