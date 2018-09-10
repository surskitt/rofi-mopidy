import time


class SpotifyCollector():
    """ Spotify collector class, using spotipy client to collect albums """

    def __init__(self, sp):
        """ class init method, passing spotipy client to do work """

        self.sp = sp

    def __results_gen(self, r):
        """ yield all items continuing through each page of results """

        while r:
            for i in r['items']:
                yield i
            # sp.next(r) will return None if there are no more pages
            r = self.sp.next(r)

    def __dt_to_mtime(self, dt):
        """ convert spotify time format to unix epoch time format """

        pattern = '%Y-%m-%dT%H:%M:%SZ'
        return int(time.mktime(time.strptime(dt, pattern)))

    def album_to_dict(self, a):
        """ use spotify album results to return agnostic album dict """

        aa = a['album']
        artist = ', '.join(i['name'] for i in aa['artists'])
        title = aa['name']
        mtime = self.__dt_to_mtime(a['added_at'])
        # use results_gen to page through track pages (for more than 50 tracks)
        tracks = [self.track_to_dict(i, artist, title, mtime)
                  for i in self.__results_gen(aa['tracks'])]
        uri = aa['uri']

        return {'artist': artist,
                'title': title,
                'album': title,
                'mtime': mtime,
                'tracks': tracks,
                'type': 'spotify',
                'uri': uri}

    def track_to_dict(self, t, albumartist, album, mtime):
        """ use spotify track results to return agnostic track dict
            uses details from parent album """

        # spotify api returns artists as a list even if there is only one
        artist = ', '.join(i['name'] for i in t['artists'])
        # spotify api always returns disc no, we format all tracks like 1.01
        track = float('{}.{}'.format(t['disc_number'], t['track_number']))
        title = t['name']
        uri = t['uri']
        mtime = mtime

        return {'artist': artist,
                'albumartist': albumartist,
                'album': album,
                'track': track,
                'title': title,
                'uri': uri,
                'mtime': mtime,
                'type': 'spotify'}

    def collect(self):
        """ return list of agnostic album dicts """

        results = self.sp.current_user_saved_albums(limit=50)
        albums = [self.album_to_dict(i) for i in self.__results_gen(results)]

        return albums
