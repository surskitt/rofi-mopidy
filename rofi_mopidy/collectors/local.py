import os
from tinytag import TinyTag
from itertools import groupby
from operator import itemgetter
import urllib.parse
import sys


def listfiles(directory, exts):
    """ unix find-a-like, recursive list of all files with given extensions """

    for root, dirs, files in os.walk(directory):
        for filename in dirs + files:
            path = os.path.join(root, filename)
            if os.path.isfile(path):
                if any(path.lower().endswith(f) for f in exts):
                    yield path


def song_to_dict(s, f):
    """ create agnostic song dict using tinytag output """

    return {'artist': s.artist,
            'albumartist': s.albumartist or s.artist,
            'album': s.album,
            # track in format like 101 if disc tag is set (handling "3 of 3")
            'track': int(''.join(i for i in ((s.disc or '') + s.track)
                         if i.isdigit())[-3:]),
            'title': s.title,
            # create file uri, converting unicode and spaces to punycode
            'uri': 'file://{}'.format(urllib.parse.quote(f)),
            'mtime': os.path.getmtime(f),
            'type': 'file'}


def album_to_dict(artist, album, tracks):
    """ create agnostic album dict """

    return {'artist': artist,
            'title': album,
            'album': album,
            'type': 'file',
            'mtime': max(i['mtime'] for i in tracks),
            'tracks': tracks}


def group_songs(sl):
    """ use grouper to group songs with same albumartist and album """

    # group on albumartist then album
    grouper = itemgetter('albumartist', 'album')
    # create list of ((albumartist, album), song_dict) tuples
    gb = [(k, list(g)) for k, g in groupby(sorted(sl, key=grouper), grouper)]
    # create list of agnost album dicts using album_to_dict on grouper results
    albums = [album_to_dict(ar, al, ts) for (ar, al), ts in gb]

    return albums


def collect(local_dir):
    """ read file tags from music dir into songs and group into albums  """

    musicfiles = listfiles(local_dir, ['flac', 'mp3'])
    song_objects = [(TinyTag.get(f), f) for f in musicfiles]
    songs = [song_to_dict(s, f) for s, f in song_objects]
    albums = group_songs(songs)

    return albums
