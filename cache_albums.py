#!/usr/bin/env python

# python stdlib
import sys
import json
import os
# packages
import collectors
import options
import auth

args = options.args
config = options.config

for i in (args.conf_dir, args.cache_dir):
    if not os.path.exists(i):
        os.makedirs(i)

output = '{}/spotify_albums.json'.format(args.cache_dir)

# If the output file already exists, delete it
if os.path.exists(output):
    os.remove(output)

sp = auth.sp
sc = collectors.SpotifyCollector(sp)
spotify_albums = sc.collect()

with open(output, 'w') as f:
    json.dump(spotify_albums, f)
