import os
from tinytag import TinyTag
from itertools import groupby
from operator import itemgetter
import urllib.parse
import sys


def listfiles(directory, exts):
    for root, dirs, files in os.walk(directory):
        for filename in dirs + files:
            path = os.path.join(root, filename)
            if os.path.isfile(path):
                if any(path.lower().endswith(f) for f in exts):
                    yield path

def song_to_dict(s, f):
    return {'artist': s.artist,
            'albumartist': s.albumartist or s.artist,
            'album': s.album,
            'track': int(''.join(i for i in ((s.disc or '') + s.track)
                     if i.isdigit())[-3:]),
            'title': s.title,
            'uri': 'file://{}'.format(urllib.parse.quote(f)),
            'mtime': os.path.getmtime(f),
            'type': 'file'}

def album_to_dict(artist, album, tracks):
    return {'artist': artist,
            'title': album,
            'album': album,
            'type': 'file',
            'mtime': max(i['mtime'] for i in tracks),
            'tracks': tracks}

def group_songs(sl):
    grouper = itemgetter('albumartist', 'album')
    gb = [(k, list(g)) for k, g in groupby(sorted(sl, key=grouper), grouper)]
    albums = [album_to_dict(ar, al, ts) for (ar, al), ts in gb]

    return albums

def collect(local_dir):
    musicfiles = listfiles(local_dir, ['flac', 'mp3'])
    song_objects = [(TinyTag.get(f), f) for f in musicfiles]
    songs = [song_to_dict(s, f) for s, f in song_objects]
    albums = group_songs(songs)

    return albums
