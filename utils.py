import os
import json
import sys

def write_albums(cache_dir, filename, *albums):
    if not os.path.exists(cache_dir):
        os.makedirs(cache_dir)

    # flatten all albums lists into one list for writing
    aalbums = [i for s in albums for i in s]

    output = '{}/{}.json'.format(cache_dir, filename)
    with open(output, 'w') as f:
        json.dump(aalbums, f, indent=4)


def load_albums(cache_dir, filename):
    iput = '{}/{}.json'.format(cache_dir, filename)
    try:
        with open(iput) as f:
            albums = json.load(f)
    except FileNotFoundError:
        print('ERROR: {} cache not found, use -r to create'.format(filename),
              file=sys.stderr)
        sys.exit(1)
    return albums
