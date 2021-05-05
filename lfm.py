# -*- coding: utf-8 -*- 
import hashlib
import urllib
from pprint import pprint
from urllib.request import urlopen
import simplejson as json
import webbrowser
from os import environ
from config import API_KEY, SECRET

ROOT_URL = 'http://ws.audioscrobbler.com/2.0/'

class LastFmAPI(object):
    def __init__(self, track, artist):
        self.username, self.session_key = self.create_session()
        self.track = track
        self.artist = artist

    
    def create_session(self):
        try:
            with open(environ['HOME'] + '/.lastfmsession', 'r') as session_file:

                # session is already opened
                username = session_file.readline()[:-1]
                key_str = session_file.readline()[:-1]
                if username and key_str:
                    return username, key_str
        except IOError: # file doesn't exist
            pass

        with open(environ['HOME'] + '/.lastfmsession', 'w', encoding='utf-8') as session_file:

            # session is not opened -> open
            token_url = self._make_request_url(method='auth.gettoken',
                                        api_key=API_KEY)
            token_response = urlopen(token_url)
            token = json.loads(token_response.read())['token']
            print(token)

            webbrowser.open('http://www.last.fm/api/auth/?api_key={}&token={}'
                            .format(API_KEY, token))
            print('Authorize request in your browser, then press Enter')
            input()
            
            session_req_url = self._make_signed_request_url(
                    method='auth.getsession',
                    token=token, api_key=API_KEY)
            print(session_req_url)
            session_response = urlopen(session_req_url)

            response_dict = json.loads(session_response.read())

            key = response_dict['session']['key']
            name = response_dict['session']['name']
            session_file.write(name + '\n')
            session_file.write(key + '\n')
            return name, key

    def get_top_artists_for_user(self):
        """Call *user.getTopArtists* method.
        Description: http://www.last.fm/api/show/user.getTopArtists
        """
        return self._call_lastfm_api('user.getTopArtists', user=self.username)

    def get_artist_playcount(self):
        r = self._call_lastfm_api('artist.getInfo', user=self.username, artist=self.artist)
        return r['artist']['stats']['userplaycount']


    def get_track(self):
        r = self._call_lastfm_api('track.getInfo', user=self.username, track=self.track , artist=self.artist)
        return r['track']['userplaycount']

    def get_artist_info(self, artist_name):
        """Call *artist.getInfo* method.
        
        Description: http://www.last.fm/api/show/artist.getInfo
        """
        return self._call_lastfm_api('artist.getInfo', artist=artist_name.encode('utf-8'))

    def _call_lastfm_api(self, method_name, **method_args):
        """Call lastfm method with given parameters, return result JSON"""
        method_args['api_key'] = API_KEY
        method_args['method'] = method_name
        url = self._make_request_url(**method_args)
        response_str = urlopen(url).read()
        return json.loads(response_str)


    def _make_request_url(self, **kwargs):
        """Create URL for regular GET request"""
        url = ROOT_URL + '?'
        kwargs['format'] = 'json'
        url += urllib.parse.urlencode(kwargs)
        return url

        
    def _make_signed_request_url(self, **kwargs):
        """Create URL for signed GET request
        
        More on this: http://www.last.fm/api/authspec
        (see `8. Signing Calls`)
        """
        md5 = hashlib.md5()
        for key in sorted(kwargs):
            md5.update(bytes('{}{}'.format(key, kwargs[key]), 'utf-8'))
        md5.update(bytes(SECRET, 'utf-8'))
        kwargs['api_sig'] = md5.hexdigest()
        return self._make_request_url(**kwargs)
        
#top_artists_dict = get_top_artists_for_user(username)
#pprint(top_artists_dict['topartists']['artist'][0:10])
#print(get_artist_info(u'Emilíana Torrini'))
