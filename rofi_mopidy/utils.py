import os
import json
import sys
import urllib.request
import io
from PIL import Image


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

    # if passed filename is the same as basename, then fn is a filename
    if os.path.basename(fn) == fn:
        return os.path.join(cache_dir, 'art', fn)
    else:
        return fn


def download_img(url, fn):
    """ Download given url as given filename """

    # make the destination dir if it doesn't exist
    dest_dir = os.path.dirname(fn)
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)

    #  with urllib.request.urlopen(url) as response, open(fn, 'wb') as f:
    with urllib.request.urlopen(url) as response:
        data = response.read()

    # convert image to png if needed and save to file
    img = Image.open(io.BytesIO(data))
    rgb_img = img.convert('RGB')
    rgb_img.save(fn, 'png')


def cache_art(cache_dir, albums):
    """ download any album art in list to cache dir """

    for a in albums:
        if 'art_url' in a:
            fn = get_cache_fn(cache_dir, a['art_fn'])
            download_img(a['art_url'], fn)
