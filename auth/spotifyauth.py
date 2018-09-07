import options
import spotipy
import spotipy.util

config = options.config

# Parse config file, reading values into dict
try:
    api = {
        'username': config.get('api', 'username'),
        'client_id': config.get('api', 'client_id'),
        'client_secret': config.get('api', 'client_secret'),
        'redirect_uri': config.get('api', 'redirect_uri'),
        'scope': 'user-library-read',
    }
except NoOptionError as err:
    print('Error: Missing values in api.conf', file=sys.stderr)
    print(err, file=sys.stderr)
    sys.exit(1)

# Receive a token using spotipy library, prompting user for login if needed
token = spotipy.util.prompt_for_user_token(**api)
if not token:
    print('Error: token not received', file=sys.stderr)
    sys.exit(1)
sp = spotipy.Spotify(auth=token)
