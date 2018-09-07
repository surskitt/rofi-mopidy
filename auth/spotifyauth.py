import spotipy
import spotipy.util


def get_api_dict(username, client_id, client_secret):
    return {'username': username,
            'client_id': client_id,
            'client_secret': client_secret,
            'redirect_uri': 'http://localhost',
            'scope': 'user-library-read'}

def get_spotify_client(username, client_id, client_secret):
    api = get_api_dict(username, client_id, client_secret)

    token = spotipy.util.prompt_for_user_token(**api)
    if not token:
        print('Error: token not received', file=sys.stderr)
        sys.exit(1)

    return spotipy.Spotify(auth=token)
