#!/usr/bin/env python

import os
import mutagen

music_dir = '/mnt/hd1/Music/'
exts_list = ['.mp3', '.flac', '.m4a']


def get_album(f):
    try:
        mf = mutagen.File(f)
        if 'TPE1' in mf.tags:
            artist = mf['TPE1']
            album = mf['TALB']
        elif 'artist' in mf.tags:
            artist = ', '.join(mf['artist'])
            album = ', '.join(mf['album'])
        elif '©ART' in mf.tags:
            artist = ', '.join(mf['©ART'])
            album = ', '.join(mf['©alb'])
        return '{} - {}'.format(artist, album)
    except:
        return f


flist = [os.path.join(r, f) for r, _, fl in os.walk(music_dir) for f in fl
         if any(f.endswith(i) for i in exts_list)]

for i in flist[:100]:
    print(get_album(i))
