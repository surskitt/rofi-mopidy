#!/usr/bin/env python

import os
from tinytag import TinyTag
from itertools import groupby
from operator import itemgetter
import json
import urllib.parse


def listfiles(directory, exts):
    for root, dirs, files in os.walk(directory):
        for filename in dirs + files:
            path = os.path.join(root, filename)
            if os.path.isfile(path):
                if any(path.lower().endswith(f) for f in exts):
                    yield path


musicfiles = listfiles('/mnt/hd1/Music', ['flac', 'mp3'])
songs = [(TinyTag.get(f), f) for f in musicfiles]
so = [{'artist': s.artist,
       'albumartist': s.albumartist or s.artist,
       'album': s.album,
       'track': int(s.track) if (s.track and s.track.isdigit()) else 0,
       'title': s.title,
       'uri': 'file://{}'.format(urllib.parse.quote(f)),
       'mtime': os.path.getmtime(f),
       'type': 'file'} for s, f in songs]


grouper = itemgetter('albumartist', 'album')
gb = [(k, list(g)) for k, g in groupby(sorted(so, key=grouper), grouper)]
sa = [{'artist': k[0],
       'album': k[1],
       'mtime': max(i['mtime'] for i in g),
       'tracks': [i for i in g]} for k, g in gb]

with open('fs.json', 'w') as f:
    json.dump(sa, f)
