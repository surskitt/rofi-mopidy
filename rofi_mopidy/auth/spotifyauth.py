import spotipy
import spotipy.util


def get_api_dict(username, client_id, client_secret):
    """ Create the api dict for use by spotify auth """

    return {'username': username,
            'client_id': client_id,
            'client_secret': client_secret,
            'redirect_uri': 'http://localhost',
            'scope': 'user-library-read'}


def get_spotify_client(username, client_id, client_secret):
    """ Retrieve a token using api details and return client object """

    api = get_api_dict(username, client_id, client_secret)

    # retrieve token, asking user to auth in browser if necessary
    token = spotipy.util.prompt_for_user_token(**api)
    if not token:
        print('Error: token not received', file=sys.stderr)
        sys.exit(1)

    return spotipy.Spotify(auth=token)
