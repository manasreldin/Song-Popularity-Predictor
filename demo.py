import requests, json, logging
import pandas as pd

def get_info(song_name = 'africa', artist_name = 'toto', req_type = 'track'):
    r = requests.post('https://accounts.spotify.com/api/token', headers = {'Authorization': 'Basic NDM0YmFiM2VhNmM2NDg2MmI3NmJkYWUwOTA0NmU2Njg6ZjFlZmFhZmM5MjA1NDFiYzkyZGNlMTk2MzBhZjk1NzE='}, data= {'grant_type': 'client_credentials'})
    token = 'Bearer {}'.format(r.json()['access_token'])
    headers = {'Authorization': token, "Accept": 'application/json', 'Content-Type': "application/json"}
    
    payload = {"q" : "artist:{} track:{}".format(artist_name, song_name), "type": req_type, "limit": "1"}
    
    res = requests.get('https://api.spotify.com/v1/search', params = payload, headers = headers)
    res = res.json()['tracks']['items'][0]
    year = res['album']['release_date'][:4]
    artist_id = res['artists'][0]['id']
    track_id = res['id']
    track_pop = res['popularity']

    res = requests.get('https://api.spotify.com/v1/audio-analysis/{}'.format(track_id), headers = headers)
    res = res.json()['track']
    duration = res['duration']
    end_fade = res['end_of_fade_in']
    key = res['key']
    key_con = res['key_confidence']
    loud = res['loudness']
    mode = res['mode']
    mode_con = res['mode_confidence']
    start_fade = res['start_of_fade_out']
    temp = res['tempo']
    time_sig = res['time_signature']
    time_sig_con = res['time_signature_confidence']
    
    res = requests.get('https://api.spotify.com/v1/artists/{}'.format(artist_id), headers = headers)
    artist_hot = res.json()['popularity']/100
    
    return pd.to_numeric(pd.Series({'duration': duration, 
                      'key': key,
                    'loudness': loud,
                     'mode': mode,
                     'tempo': temp,
                     'artist_hotttnesss': artist_hot,
                     'end_of_fade_in': end_fade,
                     'start_of_fade_out': start_fade,
                     'mode_confidence': mode_con,
                     'key_confidence': key_con,
                     'time_signature': time_sig,
                     'time_signature_confidence': time_sig_con,
                     'year': year})), track_pop