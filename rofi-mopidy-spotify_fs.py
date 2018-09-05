#!/usr/bin/env python

import json
from subprocess import Popen, PIPE

with open('fs.json') as f:
    fsj = json.load(f)

albums = '\n'.join('{} - {}'.format(i['artist'], i['album']) for i in fsj)

rofi_cmd = 'rofi -dmenu -p Music -i -no-custom -format i'.split()
caller = Popen(args=rofi_cmd, stdin=PIPE, stdout=PIPE)
stdout, stderr = caller.communicate(input=albums.encode())
print(stdout, stderr, caller.returncode)

# Add given uri to mpd playlist using mpc (TODO: use mopidy through python)
def add_uri(uri):
    print('mpc add {}'.format(uri).split())
    Popen(args='mpc add {}'.format(uri).split())


album = fsj[int(stdout.strip())]
for i in sorted(album['tracks'], key=lambda x: x['uri']):
    print(i['uri'])
    add_uri(i['uri'])
