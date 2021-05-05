import spotipy
from spotipy.oauth2 import SpotifyOAuth
from config import client_id, secret
from pprint import pprint
import lfm

scope = "user-read-playback-state,user-modify-playback-state,user-library-read"
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope, client_id=client_id, client_secret=secret, redirect_uri='http://127.0.0.1:5000'))

def get_stuff():
    t = sp.currently_playing()['item']['name']
    track = sp.currently_playing()['item']['id']
    a = sp.currently_playing()['item']['artists'][0]['name']

    if a and t != None:
        results = sp.current_user_saved_tracks_contains(tracks=[track])
        pprint(results[0] == True)
        return_obj = {
            's': t,
            'a': a,
            'lb': results[0],
            'ac': lfm.LastFmAPI(track=t, artist=a).get_artist_playcount(),
            'tc': lfm.LastFmAPI(track=t, artist=a).get_track()
        }
    return return_obj