import time

class SpotifyCollector():
    def __init__(self, sp):
        self.sp = sp


    def __results_gen(self, r):
        while r:
            for i in r['items']:
                yield i
            r = self.sp.next(r)

    def __dt_to_mtime(self, dt):
        pattern = '%Y-%m-%dT%H:%M:%SZ'

        return int(time.mktime(time.strptime(dt, pattern)))

    def album_to_dict(self, a):
        aa = a['album']
        artist = ', '.join(i['name'] for i in aa['artists'])
        title = aa['name']
        mtime = self.__dt_to_mtime(a['added_at'])
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
        artist = ', '.join(i['name'] for i in t['artists'])
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
        results = self.sp.current_user_saved_albums(limit=50)
        albums = [self.album_to_dict(i) for i in self.__results_gen(results)]

        return albums
